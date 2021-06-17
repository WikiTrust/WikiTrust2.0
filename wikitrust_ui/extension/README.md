# WikiTrust 2.0 Browser Extension

### Extension Folder Layout:

- [src/](src/) contains the source Typescript files
  - This typescript gets compiled into [core/WikiTrust.js](core/WikiTrust.js) by parcel.js on build.

- [core/](core/) is like the prod or build folder.
  - everthing compiles/outputs to `/core`, and everthing else put in that folder stays there.

- [core/WikiTrust.js](core/WikiTrust.js) is the content script that get injected on wikipedia domains.

### What this extension (or core/WikiTrust.js) does:
1. Check which kind of context it's runing in - Chrome extension, Firefox extension, or Bookmarklet

2. Injects some stying and a button into the body of the Wikipedia page.

3. On pressing the injected button (for extensions) or on loading the script (for bookmarklet):
    - Injects more UI elements,
    - runs the page processing steps to splits up the page words, fetches & matches the article text it to the server's text, then applies the text trust colors as span elements in the article.

### How to Install & Run:

1. Install NPM packages

   - Go into the wikitrust_ui folder: `cd ./wikitrust_ui/extension`
   - Run: `npm install`

2. Bundle the typescript into js:

   - Run: `npm run auto_build` (in the extension folder) which will automatically recompile your ts as it changes (you'll still need to reload the browser extensions manually)
   - Or run: `npm run prod_build` to make a one-time minified version that we'll actually publish.

3. Install the extension...

- As a Chrome extension (Best for debugging):

  1.  Visit [chrome://extensions](chrome://extensions) in the address bar.
  2.  Enable Developer Options in the top right.
  3.  Cick Load Unpacked Extension.
  4.  Select the wikitrust_ui/extension folder.
  5.  You should see the WikiTrust extension installed.
  6.  Go to a wiki page to test.

- As a Firefox extension:

  1.  Visit [about:debugging](about:debugging) in the address bar and then click on This Firefox -> Load Temporary Add-On.
  2.  Select the manifest.json in the wikitrust_ui/extension folder.
  3.  You should see the WikiTrust extension installed.
  4.  Go to a wiki page to test.

- As a Bookmarklet:

  -  **To test what the up-to-date Bookmarklet would do: (JS Part Only)** </br>
  copy-and-paste the contents of [core/WikiTrust.js](/wikitrust_ui/extension/core/WikiTrust.js) into your browser's web debug console.

  _Note: The following method relies on the WikiTrust.JS being hosted online, so this will load the last pushed version as a demo:_

  1. Drag and drop this link > <a href="javascript:(function(){var%20script=document.createElement('script');script.src='https://combinatronics.com/WikiTrust/WikiTrust2.0/Develop/wikitrust_ui/core/WikiTrust.js';document.getElementsByTagName('head')[0].appendChild(script);script.remove()})()">WikiTrust</a> < into your browser's bookmarks bar, or long press -> save as bookmark on mobile.
      - Note this won't work from the Github preview.
  2. To use, visit a wiki page and click the bookmark, as if it was an extension. On mobile, visit a wiki and enter "WikiTrust" in the address bar, then tap the bookmark.

  Bookmarklet JS:

```javascript
(function() {
  var script = document.createElement('script');
  script.src =
    'https://combinatronics.com/WikiTrust/WikiTrust2.0/Develop/wikitrust_ui/core/WikiTrust.js';
  document.getElementsByTagName('head')[0].appendChild(script);
  script.remove();
})();
```
