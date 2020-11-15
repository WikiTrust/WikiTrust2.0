import * as consts from './consts';

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
      'https://combinatronics.com/WikiTrust/WikiTrust2.0/Typescript-Extension/extension/' +
      relativePath
    );
  } else return extensionSpecificAPIs.getURL(relativePath);
};
