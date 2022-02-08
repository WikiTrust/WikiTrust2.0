import * as consts from './consts';
import * as interfaces from './interfaces';

// Checks where this code is running (firefox_extension, chrome_extension, or bookmarklet).
// Provides methods that abstract away environment-dependant things (such as fetching other parts of the app).

let extensionSpecificAPIs: typeof chrome.extension | typeof browser.extension;
let ENVIRONMENT: consts.ENVIRONMENTS;
if (
  typeof browser! !== 'undefined' &&
  typeof browser.extension !== 'undefined'
) {
  // check if the firefox extension "browser" namespace is avalable
  ENVIRONMENT = consts.ENVIRONMENTS.firefox_extension;
  extensionSpecificAPIs = browser.extension;
} else if (
  typeof chrome !== 'undefined' &&
  typeof chrome.extension !== 'undefined'
) {
  // check if the chrome extension "chrome" namespace is avalable
  ENVIRONMENT = consts.ENVIRONMENTS.chrome_extension;
  extensionSpecificAPIs = chrome.extension;
} else {
  // otherwise we must not be in an extension:
  ENVIRONMENT = consts.ENVIRONMENTS.bookmarklet;
}

/**
 * Returns true if this code is being run outside of an extension (presumably injected by a bookmarklet).
 */
export const envIsBookmarklet = () => {
  return ENVIRONMENT === consts.ENVIRONMENTS.bookmarklet;
};

/**
 * Returns the url to a file in the '/extension/...' folder either from the installed extension (extension context) or from a web-hosted version (bookmarklet context).
 * @param relativePath - The path to the asset in the extension folder (without leading '/' or 'extension/')
 */
export const getAsset = (relativePath: string) => {
  // For the extension ENVIRONMENT use the path from the extension, otherwise use the same asset hosted on the web:
  if (envIsBookmarklet()) {
    return (
      'https://combinatronics.com/WikiTrust/WikiTrust2.0/develop/wikitrust_ui/extension/' +
      relativePath
    );
  } else return extensionSpecificAPIs.getURL(relativePath);
};

let runFunctionInPageContext_lock: boolean = false;
/* returns a promise that resolves with the return value of the function
// Idea from: https://stackoverflow.com/questions/3955803/chrome-extension-get-page-variables-in-content-script
*/

export const runFunctionInPageContext = (fn: Function) => {
  // Note: this promise is of type interfaces.PageMetaData purely because that's the only type we use it with, you'll need to refactor this to use multiple types.
  return new Promise<interfaces.PageMetaData>((resolve, reject) => {
    if (envIsBookmarklet()) resolve(fn());
    else if (
      ENVIRONMENT === consts.ENVIRONMENTS.chrome_extension ||
      ENVIRONMENT === consts.ENVIRONMENTS.firefox_extension
    ) {
      if (runFunctionInPageContext_lock == true) {
        alert(
          'Uh Oh runFunctionInPageContext() called again before the last execution of it could finish!'
        );
        reject();
      }

      runFunctionInPageContext_lock = true;

      window.addEventListener(
        'message',
        ({ data }) => {
          // We only accept messages from ourselves
          let result: interfaces.PageMetaData = data.wikiTrustPageContextRun;
          if (data.wikiTrustPageContextRun) resolve(result);
        },
        false
      );

      // Inject script into page scope
      const script = document.createElement('script');
      script.text = `window.postMessage({wikiTrustPageContextRun:(${fn.toString()})()}, '*');`;
      document.documentElement.appendChild(script);

      // restore lock so this function can be called again
      runFunctionInPageContext_lock = false;
    }
  });
};

