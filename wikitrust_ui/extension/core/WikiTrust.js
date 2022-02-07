// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  var error;
  for (var i = 0; i < entry.length; i++) {
    try {
      newRequire(entry[i]);
    } catch (e) {
      // Save first error but execute all entries
      if (!error) {
        error = e;
      }
    }
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  parcelRequire = newRequire;

  if (error) {
    // throw error from earlier, _after updating parcelRequire_
    throw error;
  }

  return newRequire;
})({"consts.ts":[function(require,module,exports) {
"use strict";

exports.__esModule = true; // dictionary of html element types to apply the word spliting / wrapping functions to and then add the newly created word elements to the wordNodes array.

exports.REPLACE_WORDS_IN = {
  p: true,
  a: true,
  span: true,
  b: true,
  big: true,
  cite: true,
  code: true,
  dd: true,
  dt: true,
  em: true,
  font: true,
  h1: true,
  h2: true,
  h3: true,
  h4: true,
  h5: true,
  h6: true,
  i: true,
  label: true,
  legend: true,
  ul: true,
  li: true,
  pre: true,
  small: true,
  strong: true,
  section: true,
  td: true,
  th: true,
  tt: true,
  div: true,
  caption: true
}; // array of html element class names exclude from the word spliting / wrapping functions.

exports.ELEMENT_CLASSES_TO_EXCLUDE = ['reference', 'wikitable', 'toc', 'infobox', 'thumb', 'mw-editsection', 'navbox', 'metadata', 'tmbox', 'sistersitebox', 'portal', 'hatnote', 'noprint', 'mw-headline', 'gallery', 'mw-empty-elt', 'noprint']; // "reference" "sistersitebox" "navbox"

var ENVIRONMENTS;

(function (ENVIRONMENTS) {
  ENVIRONMENTS[ENVIRONMENTS["bookmarklet"] = 0] = "bookmarklet";
  ENVIRONMENTS[ENVIRONMENTS["firefox_extension"] = 1] = "firefox_extension";
  ENVIRONMENTS[ENVIRONMENTS["chrome_extension"] = 2] = "chrome_extension";
})(ENVIRONMENTS = exports.ENVIRONMENTS || (exports.ENVIRONMENTS = {}));

var COMPLETION_STAGES;

(function (COMPLETION_STAGES) {
  COMPLETION_STAGES[COMPLETION_STAGES["just_loaded"] = 0] = "just_loaded";
  COMPLETION_STAGES[COMPLETION_STAGES["base_ui_injected"] = 1] = "base_ui_injected";
  COMPLETION_STAGES[COMPLETION_STAGES["ui_injected"] = 2] = "ui_injected";
  COMPLETION_STAGES[COMPLETION_STAGES["api_sent"] = 3] = "api_sent";
  COMPLETION_STAGES[COMPLETION_STAGES["api_recived"] = 4] = "api_recived";
  COMPLETION_STAGES[COMPLETION_STAGES["page_processed"] = 5] = "page_processed";
})(COMPLETION_STAGES = exports.COMPLETION_STAGES || (exports.COMPLETION_STAGES = {})); // word element attribute names (for debugging)


exports.SCORE_ATTRIBUTE_NAME = 'data-trust-score';
exports.WORD_INDEX_ATTRIBUTE_NAME = 'data-word-index';
},{}],"environment.ts":[function(require,module,exports) {
"use strict";

var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
  }
  result["default"] = mod;
  return result;
};

exports.__esModule = true;

var consts = __importStar(require("./consts")); // Checks where this code is running (firefox_extension, chrome_extension, or bookmarklet).
// Provides methods that abstract away environment-dependant things (such as fetching other parts of the app).


var extensionSpecificAPIs;
var ENVIRONMENT;

if (typeof browser !== 'undefined' && typeof browser.extension !== 'undefined') {
  // check if the firefox extension "browser" namespace is avalable
  ENVIRONMENT = consts.ENVIRONMENTS.firefox_extension;
  extensionSpecificAPIs = browser.extension;
} else if (typeof chrome !== 'undefined' && typeof chrome.extension !== 'undefined') {
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


exports.envIsBookmarklet = function () {
  return ENVIRONMENT === consts.ENVIRONMENTS.bookmarklet;
};
/**
 * Returns the url to a file in the '/extension/...' folder either from the installed extension (extension context) or from a web-hosted version (bookmarklet context).
 * @param relativePath - The path to the asset in the extension folder (without leading '/' or 'extension/')
 */


exports.getAsset = function (relativePath) {
  // For the extension ENVIRONMENT use the path from the extension, otherwise use the same asset hosted on the web:
  if (exports.envIsBookmarklet()) {
    return 'https://combinatronics.com/WikiTrust/WikiTrust2.0/develop/wikitrust_ui/extension/' + relativePath;
  } else return extensionSpecificAPIs.getURL(relativePath);
};

var runFunctionInPageContext_lock = false;
/* returns a promise that resolves with the return value of the function
// Idea from: https://stackoverflow.com/questions/3955803/chrome-extension-get-page-variables-in-content-script
*/

exports.runFunctionInPageContext = function (fn) {
  // Note: this promise is of type interfaces.PageMetaData purely because that's the only type we use it with, you'll need to refactor this to use multiple types.
  return new Promise(function (resolve, reject) {
    if (exports.envIsBookmarklet()) resolve(fn());else if (ENVIRONMENT === consts.ENVIRONMENTS.chrome_extension || ENVIRONMENT === consts.ENVIRONMENTS.firefox_extension) {
      if (runFunctionInPageContext_lock == true) {
        alert('Uh Oh runFunctionInPageContext() called again before the last execution of it could finish!');
        reject();
      }

      runFunctionInPageContext_lock = true;
      window.addEventListener('message', function (_a) {
        var data = _a.data; // We only accept messages from ourselves

        var result = data.wikiTrustPageContextRun;
        if (data.wikiTrustPageContextRun) resolve(result);
      }, false); // Inject script into page scope

      var script = document.createElement('script');
      script.text = "window.postMessage({wikiTrustPageContextRun:(" + fn.toString() + ")()}, '*');";
      document.documentElement.appendChild(script); // restore lock so this function can be called again

      runFunctionInPageContext_lock = false;
    }
  });
};
},{"./consts":"consts.ts"}],"applyScores.ts":[function(require,module,exports) {
"use strict";

var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
  }
  result["default"] = mod;
  return result;
};

exports.__esModule = true;

var UI = __importStar(require("./ui")); // import { showTooltipAtElement } from './tooltip'; // not needed anymore, score is shown in corner

/**
 * normalizes the score to be between 0 and 1
 * @note This function REQUIRES that the maxWordScore and revisionIndex
 *       are set in window.WikiTrustGlobalVars before calling this function.
 * @param {number} score - The raw score (from the algorithim output) to be normalized
 * @returns {number} The normalized score
 */


exports.calculateScaledScore = function (score) {
  // var max = window.WikiTrustGlobalVars.maxWordScore;
  var x = window.WikiTrustGlobalVars.revisionIndex;
  var Y = 1 / (1 + Math.exp(4.5 - 9 * x)); // sigmoid function https://www.desmos.com/calculator/ksmz4tnvyc

  return score / window.WikiTrustGlobalVars.maxWordScore;
};
/**
 * Returns true if the character code is a whitespace character.
 * @param {number} code - The char code you want to test
 */


var charCodeIsWhitespace = function charCodeIsWhitespace(code) {
  return code <= 32 && code >= 0 || code === 127;
}; // Hard coded color gradient used in below getColorForPercentage() function


var percentColorsGradient = [// Define a gradient (percent = 0.0 - least trustworthy color, percent = 1.0 - most trustworthy color)
{
  percent: 0.0,
  color: {
    r: 0xfc,
    g: 0x4a,
    b: 0x1a
  }
}, {
  percent: 0.5,
  color: {
    r: 0xf7,
    g: 0xb7,
    b: 0x33
  }
}, {
  percent: 1.0,
  color: {
    r: 0xff,
    g: 0xff,
    b: 0xff
  }
}];
/**
 * @return an 'rgba(255,255,255,1)' formated color string based on a percent through a hard-coded gradient and an opacity.
 * @param {string} percent - The percentage (0-1) representing how far along the gradient you want to sample the color.
 * @param {string} opacity - The opacity in the output color string.
 */

exports.getColorForPercentage = function (percent, opacity) {
  // Source: https://stackoverflow.com/questions/7128675/from-green-to-red-color-depend-on-percentage
  var i = 1;

  for (i = 1; i < percentColorsGradient.length - 1; i++) {
    if (percent < percentColorsGradient[i].percent) {
      break;
    }
  }

  var lower = percentColorsGradient[i - 1];
  var upper = percentColorsGradient[i];
  var range = upper.percent - lower.percent;
  var rangepercent = (percent - lower.percent) / range;
  var percentLower = 1 - rangepercent;
  var percentUpper = rangepercent;
  var color = {
    r: Math.floor(lower.color.r * percentLower + upper.color.r * percentUpper),
    g: Math.floor(lower.color.g * percentLower + upper.color.g * percentUpper),
    b: Math.floor(lower.color.b * percentLower + upper.color.b * percentUpper)
  };
  return "rgba(" + [color.r, color.g, color.b, opacity].join(',') + ")"; // or output as hex if preferred
};
/**
 * Inserts a section of text (wrapped in a span highlighted based on the passed score), right before the given text node.
 * This function is inteneded to be called for every word chunk in a text node before deleting the text node.
 * @param {Node} textNode - The text node where this word chunk was found
 * @param {string} wordChunk - A contiguous string found within the text node where all the words have the same score
 * @param {string} score - The trust score given to all the words in the wordChunk.
 */


var insertWordChunk = function insertWordChunk(textNode, wordChunk, score) {
  var parentElement = textNode.parentElement;
  if (!parentElement) return;
  var wordChunkElement = document.createElement('span');
  wordChunkElement.textContent = wordChunk;
  wordChunkElement.className = 'wt-word-chunk';
  wordChunkElement.setAttribute('trust', score.toString()); // for debug
  // after showing the real score, we can calculate the scaled score

  score = exports.calculateScaledScore(score);

  wordChunkElement.onmouseenter = function (e) {
    UI.showTrustScore(score);
    wordChunkElement.classList.add('wt-word-hover');
  };

  wordChunkElement.onmouseleave = function (e) {
    UI.hideTrustScore();
    wordChunkElement.classList.remove('wt-word-hover');
  };

  if (score <= 1 && score !== 0) {
    // if the word has a score applied
    wordChunkElement.style.borderBottom = "1px solid " + exports.getColorForPercentage(score, 1); // wordChunkElement.style.color = `green`;

    wordChunkElement.style.backgroundColor = exports.getColorForPercentage(score, 0.1);
  } else wordChunkElement.style.borderBottom = "2px solid lightgrey"; // if the wordChunk was not matched to the algorithim's output, highlight with grey


  parentElement.insertBefore(wordChunkElement, textNode);
};
/**
 * Takes all the text nodes and the word scores and groups sections of contiguous scores and calls insert word chunk on them.
 * @param textNodesPerGroup - An array of arrays of text DOM Nodes where the Nth array corresponds to the Nth grouping element and each node within that array is a text node in that grouping element.
 * @param wordScores - An array of trust scores where the Nth score corresponds to the Nth word on the page
 * @param maxWordScore - The maximum trust score in this article
 * @returns - An array containing the minimum trust score for each grouping element.
 */


exports.applyWordScores = function (textNodesPerGroup, wordScores) {
  var _a;

  var minTrustPerGroup = [];
  var currWordIndex = 0;
  var lastCharWasWhitespace = false;

  for (var gi = 0, len = textNodesPerGroup.length; gi < len; gi++) {
    var minTrustInThisGroup = Infinity;

    for (var ti = 0, len_1 = textNodesPerGroup[gi].length; ti < len_1; ti++) {
      var textNode = textNodesPerGroup[gi][ti];
      var nodeText = textNode.nodeValue || '';
      var wordChunkStartIndex = 0;
      var wordScore = wordScores[currWordIndex];
      var len_2 = nodeText.length;
      var allCharsAreWhitespace = true; // loop through every character in this text node finding words.

      for (var charindex = 0; charindex < len_2; charindex++) {
        var currCharIsWhitespace = charCodeIsWhitespace(nodeText.charCodeAt(charindex));

        if (!currCharIsWhitespace && lastCharWasWhitespace) {
          allCharsAreWhitespace = false;

          if (wordScores[currWordIndex] !== wordScores[currWordIndex + 1]) {
            if (wordScore < minTrustInThisGroup) minTrustInThisGroup = wordScore;
            insertWordChunk(textNode, nodeText.substring(wordChunkStartIndex, charindex), wordScore);
            wordChunkStartIndex = charindex;
          }

          currWordIndex++;
        }

        lastCharWasWhitespace = currCharIsWhitespace;
      }

      if (wordChunkStartIndex !== 0) {
        if (wordChunkStartIndex !== len_2 - 1) {
          insertWordChunk(textNode, nodeText.substring(wordChunkStartIndex, len_2), wordScore);
          if (wordScore < minTrustInThisGroup) minTrustInThisGroup = wordScore;
        }
      } else if (!charCodeIsWhitespace(nodeText.charCodeAt(0))) {
        insertWordChunk(textNode, nodeText.substring(0, len_2), wordScore);
        if (wordScore < minTrustInThisGroup) minTrustInThisGroup = wordScore;
      } else if (allCharsAreWhitespace) {
        insertWordChunk(textNode, nodeText.substring(0, len_2), 0);
      }

      (_a = textNode.parentNode) === null || _a === void 0 ? void 0 : _a.removeChild(textNode);
    }

    minTrustPerGroup.push(minTrustInThisGroup);
  }

  return minTrustPerGroup;
};
},{"./ui":"ui.ts"}],"ui.ts":[function(require,module,exports) {
"use strict";

exports.__esModule = true;

var environment_1 = require("./environment");

var applyScores_1 = require("./applyScores");

var activateWTButton;
var WTDialPointer;
/**
 * Injects a style link tag into the head of the wikipedia page pointing to '/core/WikiTrustStyle.css'
 */

exports.injectStylesheet = function () {
  // Inject a stylesheet into the current page.
  var style = window.WikiTrustGlobalVars.styleElm = document.createElement('link');
  style.rel = 'stylesheet';
  style.href = environment_1.getAsset('core/WikiTrustStyle.css');
  document.getElementsByTagName('head')[0].appendChild(style);
};
/**
 * Returns the gradient dial that goes behind the activate wikitrust button.
 */


var buildCircularGradient = function buildCircularGradient() {
  var gradient = document.createElement('img');
  gradient.id = 'WT_Gradient_Dial';
  gradient.src = environment_1.getAsset('core/Gradient.png');
  return gradient;
};
/**
 * Returns the black pointer line element for the gradient dial visualization.
 */


var buildDialPointer = function buildDialPointer() {
  WTDialPointer = document.createElement('div');
  WTDialPointer.id = 'WT_Gradient_Dial_Pointer';
  return WTDialPointer;
};
/**
 * Returns the activate wikitrust button element.
 */


var buildWTButton = function buildWTButton() {
  activateWTButton = document.createElement('button');
  activateWTButton.id = 'WT_Activate_Button';
  activateWTButton.innerHTML = 'W<sub>T</sub>';
  return activateWTButton;
};
/**
 * Sets an on click listener on the activate WikiTrust Button with the passed function
 * @param clickEventFunction - the function to call when the activate button is clicked.
 */


exports.addButtonClickCallback = function (clickEventFunction) {
  if (activateWTButton) activateWTButton.onclick = clickEventFunction;
};
/**
 * Returns an element to hold all the colored score markers/dots on the left of the article.
 */


var markContainer;

var buildMarkContainer = function buildMarkContainer() {
  markContainer = document.createElement('div');
  markContainer.classList.add('wt-text-side-group-mark-container');
  markContainer.classList.add('mw-body'); // Uses wikipedia's mw-body class to adjust the left margin like the article.

  return markContainer;
};
/* shows the gradient dial, sets the position dial pointer to the correct position on the gradient dial and sets the color scheme to match. */


exports.showTrustScore = function (score) {
  window.WikiTrustGlobalVars.uiFrameContainer.classList.add('showing-score');
  activateWTButton.innerText = score.toFixed(1); // (score * 100).toFixed(1);

  activateWTButton.style.borderColor = applyScores_1.getColorForPercentage(score, 1);
  WTDialPointer.style.transform = "scale(1.5) rotate(" + (1 - score) * 90 + "deg)";
};

exports.hideTrustScore = function () {
  window.WikiTrustGlobalVars.uiFrameContainer.classList.remove('showing-score');
  WTDialPointer.style.transform = "scale(1)";
  activateWTButton.innerHTML = 'W<sub>T</sub>';
};
/**
 * Adds a marker/dot element on the left side of the article which corresponds to a particular grouping.
 * @param groupingElement - The element that this marker is refering to (usually this is a paragraph or section element which contains many words and or child elements)
 * @param score - The score used to color this marker (usually the maximum score of the words within the groupingElement)
 */


exports.addTextGroupMark = function (groupingElement, score) {
  if (!groupingElement || !markContainer || score === 0) return;
  groupingElement.classList.add('wt-grouping-container', 'trust-hidden');
  var rect = groupingElement.getBoundingClientRect();
  var yOffset = rect.top + window.pageYOffset + 5;
  var height = rect.bottom - rect.top - 10;
  var markElement = document.createElement('div');
  markElement.style.top = yOffset + 'px';
  markElement.style.height = height + 'px';
  markElement.classList.add('wt-text-side-group-mark');
  markElement.style.backgroundColor = applyScores_1.getColorForPercentage(score, 1);

  markElement.onmouseenter = function (e) {
    groupingElement.classList.remove('trust-hidden'); // showTooltipAtElement(
    //   markElement,
    //   'Max Score: ' + Math.round(score * 1000) / 1000
    // );

    exports.showTrustScore(score);
  };

  markElement.onmouseleave = function (e) {
    groupingElement.classList.add('trust-hidden'); // hideTooltip();

    exports.hideTrustScore();
  };

  markContainer.appendChild(markElement);
};

var loadingAnimIntervalId = -1;
/** Shows an askii loading animation in the activate WikiTrust button */

exports.showLoadingAnimation = function () {
  if (loadingAnimIntervalId !== -1) return;
  var frames = ['|...', '.|..', '..|.', '...|'];
  activateWTButton.innerText = frames[0];
  var counter = 0;
  loadingAnimIntervalId = window.setInterval(function () {
    counter = (counter + 1) % 4;
    activateWTButton.innerText = frames[counter];
  }, 600);
};
/** Stops the askii loading animation in the activate WikiTrust button */


exports.hideLoadingAnimation = function () {
  if (loadingAnimIntervalId === -1) return;
  clearInterval(loadingAnimIntervalId);
  activateWTButton.innerHTML = 'W<sub>T</sub>';
  activateWTButton.classList.add('wt-active');
};
/** Stops the askii loading animation in the activate WikiTrust button */


exports.injectUi = function () {
  var uiFrameContainer = window.WikiTrustGlobalVars.uiFrameContainer = document.createElement('div');
  uiFrameContainer.id = 'Wikitrust_UI_Container'; // uiFrameContainer.appendChild(buildWikiTrustButtonComponent());

  uiFrameContainer.appendChild(buildWTButton());
  uiFrameContainer.appendChild(buildCircularGradient());
  uiFrameContainer.appendChild(buildDialPointer());
  document.body.appendChild(buildMarkContainer());
  document.body.appendChild(uiFrameContainer);
};

exports.removeUi = function () {
  document.body.removeChild(window.WikiTrustGlobalVars.uiFrameContainer);
}; // unused: ----------.....!
// export const injectUiFrame = () => {
//   // Inject an iframe element that can serve as a container for UI & Controls:
//   const uiFrame = document.createElement('iframe');
//   const uiFrameContainer = (window.WikiTrustGlobalVars.uiFrameContainer = document.createElement(
//     'div'
//   ));
//   uiFrameContainer.id = 'Wikitrust_UI';
//   uiFrame.src = getAsset('core/UIFrame.html');
//   uiFrameContainer.appendChild(uiFrame);
//   document.body.appendChild(uiFrameContainer);
// };
},{"./environment":"environment.ts","./applyScores":"applyScores.ts"}],"findGroupingElems.ts":[function(require,module,exports) {
"use strict";

var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
  }
  result["default"] = mod;
  return result;
};

exports.__esModule = true;

var consts = __importStar(require("./consts"));

var allowedGroupingTags = {
  p: true,
  span: true,
  code: true,
  h1: true,
  h2: true,
  h3: true,
  h4: true,
  h5: true,
  h6: true,
  ul: true,
  ol: true,
  pre: true,
  section: true
}; // -- check if an html element has the passed name in its class parameter (used to check whether an Element has an Class Name that we want to exclude):

var hasClass = function hasClass(element, className) {
  // looks for the className in the element's classes string (the spaces ensure only full class names, not just a part of the class name is matched).
  return (" " + element.className + " ").indexOf(" " + className + " ") !== -1;
};
/**
 * Returns all the child elements of the parent that pass filters.
 * Includes the children of 'section' elements rather than the section elements themselves.
 * This is because mobile wikipedia burries all the paragraphs in collapsable sections.
 * @param parent - The parent element to get the children in
 */


var elementPassesFilters = function elementPassesFilters(domNode) {
  if (domNode.nodeType !== Node.ELEMENT_NODE || !domNode.childNodes) {
    return false;
  }

  if (!allowedGroupingTags[domNode.tagName.toLowerCase()]) {
    return false;
  } // loops through the EXCLUDE_ELEMENT_CLASSES object and checks the element for each class name.


  for (var _i = 0, _a = consts.ELEMENT_CLASSES_TO_EXCLUDE; _i < _a.length; _i++) {
    var className = _a[_i];
    if (hasClass(domNode, className)) return false;
  } // excluded class, element should be excluded;


  return true;
};
/**
 * @Returns all the child elements of the parent that pass filters.
 * Includes the children of 'section' elements rather than the section elements themselves.
 * This is because mobile wikipedia burries all the paragraphs in collapsable sections.
 * @param parent - The parent element to get the children in
 */


exports.getGroupingElems = function (parent) {
  var outputElements = [];

  for (var i = 0, len = parent.childNodes.length; i < len; i++) {
    var childNode = parent.childNodes[i];

    if (elementPassesFilters(childNode)) {
      if (childNode.tagName.toLowerCase() === 'section') {
        outputElements = outputElements.concat(exports.getGroupingElems(childNode));
      } else outputElements.push(childNode);
    }
  }

  return outputElements;
};
},{"./consts":"consts.ts"}],"extractTextNodes.ts":[function(require,module,exports) {
"use strict";

var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
  }
  result["default"] = mod;
  return result;
};

exports.__esModule = true;

var consts = __importStar(require("./consts"));
/**
 * Given an html element checks if it is of an included type and
 * does not have any of the excluded classes specified in the ./consts module.
 * @param element - The HTML element to check.
 * @returns {boolean} True if the element passes the filters, false otherwise.
 */


var elementPassesFilters = function elementPassesFilters(element) {
  // -- check element for included Tag name:
  if (!element.tagName || !consts.REPLACE_WORDS_IN[element.tagName.toLowerCase()]) {
    return false; // incorrect tag, element should be excluded;
  } // -- check element For excluded class:


  var hasClass = function hasClass(className) {
    // looks for the className in the element's classes string (the spaces ensure only full class names not just a part of the class name is matched).
    return (" " + element.className + " ").indexOf(" " + className + " ") > -1;
  }; // loops through the EXCLUDE_ELEMENT_CLASSES object and checks the element for each class name.


  for (var _i = 0, _a = consts.ELEMENT_CLASSES_TO_EXCLUDE; _i < _a.length; _i++) {
    var className = _a[_i];
    if (hasClass(className)) return false; // has excluded class, element should be excluded;
  }

  return true; // all filters pass (element not excluded);
};
/**
 * Recursively extracts all text nodes that are decendants of the passed element.
 * @param parentElement - Returns all the text nodes within this element.
 * @returns An array of text nodes.
 */


exports.extractTextNodes = function (parentElement) {
  var outputNodes = [];

  if (parentElement && elementPassesFilters(parentElement)) {
    for (var i = 0, len = parentElement.childNodes.length; i < len; i++) {
      var childNode = parentElement.childNodes[i];

      if (childNode.nodeType === Node.TEXT_NODE && childNode.nodeValue) {
        outputNodes.push(childNode);
      } else if (childNode.nodeType === Node.ELEMENT_NODE) {
        // Recursively call this function on the childNode:
        outputNodes = outputNodes.concat(exports.extractTextNodes(childNode));
      }
    }
  }

  return outputNodes;
};
},{"./consts":"consts.ts"}],"splitingAlg.ts":[function(require,module,exports) {
"use strict";

exports.__esModule = true;

var findGroupingElems_1 = require("./findGroupingElems");

var extractTextNodes_1 = require("./extractTextNodes");
/**
 * Combines the texts of an array of text nodes then splits the string node on whitespace, to get an array of words.
 * @param textNodeArr - An array of consecutive DOM text nodes (not the containing element) to find words in.
 */


var extractWords = function extractWords(textNodeArr) {
  var textStr = '';

  for (var index = 0, len = textNodeArr.length; index < len; index++) {
    if (textNodeArr[index]) textStr += textNodeArr[index].nodeValue;
  }

  var words = textStr.split(/\s+/);
  if (words[0] === '') words.shift();
  if (words[words.length - 1] === '') words.pop();
  return words;
};
/**
 * @param articleContainer - The element that contains all of the wikipedia article content to be proccessed.
 * @returns Three things -
 * groupingElems: The elements we use to group words, such as paragraphs (this element should be nearly a direct decendant of the articleContainer).
 * textNodesPerGroup: An array of arrays where the first index corresponds a grouping element's index and the second index is a text node within that group.
 * pageWordList: A string array of all words on the page (split on whitespace only).
 */


exports.runPageSplitter = function (articleContainer) {
  /** The elements we use to group words, such as paragraphs (this element should be nearly a direct decendant of the articleContainer). */
  var groupingElems = findGroupingElems_1.getGroupingElems(articleContainer);
  /** An array of arrays where the first index corresponds a grouping element's index and the second index is the text node within that group */

  var textNodesPerGroup = [];
  /** A string array of all words on the page (split on whitespace only). */

  var pageWordList = [];

  for (var groupIndex = 0; groupIndex < groupingElems.length; groupIndex++) {
    var groupingElem = groupingElems[groupIndex];
    var textNodes = extractTextNodes_1.extractTextNodes(groupingElem);
    pageWordList = pageWordList.concat(extractWords(textNodes));
    textNodesPerGroup.push(textNodes);
  }

  return {
    groupingElems: groupingElems,
    textNodesPerGroup: textNodesPerGroup,
    pageWordList: pageWordList
  };
};
},{"./findGroupingElems":"findGroupingElems.ts","./extractTextNodes":"extractTextNodes.ts"}],"runningMatch.ts":[function(require,module,exports) {
"use strict"; // inspired by: https://johnresig.com/projects/javascript-diff-algorithm/
// See comments on functions.

exports.__esModule = true;
var CONSECUTIVE_MATCHES_REQUIRED = 3;
var currConsecutiveMatches = 0;
var sourceWords = new Array();
var targetWords = new Array();
var sourceToTargetMapping = new Array(sourceWords.length);
var sourceWordIndex = 0,
    targetWordIndex = 0;
/**
 * A dictionary where each key is a word and the indecies where that
 * word is found in the source and target are stored in the first and second
 * arrays for that key respectively. Dictionary format:
 * { word: [ [indecies where word is found in the source], [indecies where word is found in the target] ] }
 */

var wordMatchIndicieDictionary = {};
var WordOrigin;

(function (WordOrigin) {
  WordOrigin[WordOrigin["source"] = 0] = "source";
  WordOrigin[WordOrigin["target"] = 1] = "target";
})(WordOrigin || (WordOrigin = {}));
/**
 * Adds a word to the word match index dictionary
 * @param word - The word to insert
 * @param wordOrigin - 0 if the word comes from the source array, 1 if it comes from the target array (see enum above).
 * @param index - The index of the word in the array it came from (source or target).
 */


var addWordIndexToIndicieDictionary = function addWordIndexToIndicieDictionary(word, index, wordOrigin) {
  if (wordMatchIndicieDictionary[word] === undefined) {
    wordMatchIndicieDictionary[word] = [[], []];
  }

  wordMatchIndicieDictionary[word][wordOrigin].push(index);
};
/**
 * Gets the indecies in the (sourceWordList or targetWordList depending on wordOrigin) where the given word is found.
 * @param word - The word to find
 * @param wordOrigin - Which array indecies to return.
 */


var getWordIndeciesFromDictionary = function getWordIndeciesFromDictionary(word, wordOrigin) {
  return wordMatchIndicieDictionary[word][wordOrigin] || [];
};
/**
 * Given a starting index in the souceWordList and a starting index in the targetWordList,
 * compares the next n words in the two list to see if they also match (where n = CONSECUTIVE_MATCHES_REQUIRED)
 * @param startSourceIndex - The index to start comparing from in the sourceWordList
 * @param startTargetIndex - The index to start comparing from in the targetWordList
 * @returns true if the next n words in the sourceWordList also match the next n words in the targetWordList.
 */


var checkConsecutiveMatches = function checkConsecutiveMatches(startSourceIndex, startTargetIndex) {
  for (var i = 0; i < CONSECUTIVE_MATCHES_REQUIRED; i++) {
    // TODO: check if indexes are over size;
    if (targetWords[startTargetIndex + i] !== sourceWords[startSourceIndex + i]) {
      return false;
    }
  }

  console.log('found ' + CONSECUTIVE_MATCHES_REQUIRED + ' consecutive matches starting at source index: ' + startSourceIndex + ' and target index: ' + startTargetIndex);
  return true;
};
/**
 * Tries to use the wordMatchIndicieDictionary to find indexes where the source word shows up in the target list or the target word shows up in the source list.
 * For each matching index in the target array it trys to test the next n consecutive words in both arrays to make sure they match, if they do it sets the current target word index to the index of the original/first matching word.
 * For each matching index in the source array it trys to test the next n consecutive words in both arrays to make sure they match, if they do it sets the current source word index to the index of the original/first matching word.
 * @param currSourceWord - The current word in the sourceWordList as a string
 * @param currTargetWord - The current word in the targetWordList as a string
 * @returns true if a valid match was found (has more than CONSECUTIVE_MATCHES_REQUIRED consecutive matches)
 */


var checkCrossMatch = function checkCrossMatch(currSourceWord, currTargetWord) {
  // Try to find indecies where the current target word shows up in the sourceWordList:
  var matchingSourceIndecies = getWordIndeciesFromDictionary(currTargetWord, WordOrigin.source);
  console.log('Source Match:' + currTargetWord, matchingSourceIndecies);

  for (var u = 0; u < matchingSourceIndecies.length; u++) {
    var foundSourceWordIndex = matchingSourceIndecies[u];

    if (checkConsecutiveMatches(foundSourceWordIndex, targetWordIndex)) {
      sourceWordIndex = foundSourceWordIndex;
      return true;
    }
  } // Try to find indecies where the current source word shows up in the targetWordList:


  var matchingTargetIndecies = getWordIndeciesFromDictionary(currSourceWord, WordOrigin.target);
  console.log('Target Match:' + currSourceWord, matchingTargetIndecies);

  for (var u = 0; u < matchingTargetIndecies.length; u++) {
    var foundPageWordIndex = matchingTargetIndecies[u];

    if (checkConsecutiveMatches(sourceWordIndex, foundPageWordIndex)) {
      targetWordIndex = foundPageWordIndex;
      return true;
    }
  } // no matches found ):


  return false;
};
/**
 * Compares two lists of words where words in the targetWordList are close to the words in the sourceWordList, but they may have words added and/or deleted.
 * @param sourceWordList - An array of words as strings
 * @param targetWordList - An array of words as strings, potentially with edits from the sourceWordList
 * @returns an array mapping from the words in the source to the words in the target where the nth mapping array index, corresponds to the nth word in the source array and the value at mapping[n] is the index of where the same word goes in the target array.
 */


exports.getWordMatchMapping = function (sourceWordList, targetWordList) {
  console.groupCollapsed('==== Finding Word Mappings ====');
  sourceWords = sourceWordList;
  targetWords = targetWordList;

  while (true) {
    var currSourceWord = sourceWords[sourceWordIndex],
        currTargetWord = targetWords[targetWordIndex];

    if (currSourceWord === currTargetWord) {
      sourceToTargetMapping[sourceWordIndex] = targetWordIndex;
      currConsecutiveMatches++;
    } else {
      currConsecutiveMatches = 0; // add the current words to the dictionary.

      addWordIndexToIndicieDictionary(currSourceWord, sourceWordIndex, WordOrigin.source);
      addWordIndexToIndicieDictionary(currTargetWord, targetWordIndex, WordOrigin.target);
      console.group('Checking for cross matches...');
      var crossMatchFound = checkCrossMatch(currSourceWord, currTargetWord);
      console.groupEnd();
      if (crossMatchFound) continue;
    }

    if (targetWordIndex < targetWords.length - 1) targetWordIndex++;
    if (sourceWordIndex < sourceWords.length - 1) sourceWordIndex++;

    if (sourceWordIndex === sourceWords.length - 1 && targetWordIndex === targetWords.length - 1) {
      break;
    }

    if (currConsecutiveMatches === CONSECUTIVE_MATCHES_REQUIRED) {
      // free up memory by clearing dictionaries. (We assume that we've found the next set of matches):
      wordMatchIndicieDictionary = {};
    }
  }

  console.groupEnd();
  return sourceToTargetMapping;
};
},{}],"serverAPI.ts":[function(require,module,exports) {
"use strict";

exports.__esModule = true;
/**
 * Super simple api call to get the text score data
 * Assumes the main.py is running from the wikitrust folder.
 * Expects the api to return json in the format: { words: ['the','brown','fox'], trust_values: [1.5,2,8] }
 * Where the nth word is the nth word in the wikipedia page & the nth trust_value corresponds to the nth word.
 *
 * @returns a promise which resolves with the parsed JSON returned by the API
 *  */

var url_base = 'http://b3c4-63-249-68-2.ngrok.io'; //'http://localhost:8000';

exports.fetchScores = function (revisionId, pageId) {
  // RIGHT NOW We're using revisionId assuming it's unique across all pages. if not, pageId will need to be sent too.
  return new Promise(function (resolve, reject) {
    fetch(url_base + '/api?action=get_revision_text_trust&revision_id=' + revisionId).then(function (response) {
      return response.json();
    }).then(function (data) {
      setTimeout(function () {
        console.log('Got revision (' + revisionId + ') text trust from server: ', data);

        if (data['error']) {
          console.warn('Server Error: ' + data['error']);
          reject('Server Error: ' + data['error']);
        }

        var output = {
          words: data.words,
          scores: data.trust_values,
          revisionIndex: data.revision_index
        };
        resolve(output);
      }, 1200); // for testing
    })["catch"](function (error) {
      alert('Error Fetching: ' + error);
      url_base = prompt('If you have the wt server running at a known IP address please enter that here eg: "http://192.168.0.10:8000"') || url_base;
      exports.fetchScores(revisionId, pageId).then(resolve, reject);
    });
  });
};
},{}],"main.ts":[function(require,module,exports) {
"use strict";

var __importStar = this && this.__importStar || function (mod) {
  if (mod && mod.__esModule) return mod;
  var result = {};
  if (mod != null) for (var k in mod) {
    if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
  }
  result["default"] = mod;
  return result;
};

exports.__esModule = true;

var consts = __importStar(require("./consts"));

var UI = __importStar(require("./ui")); // import { injectTooltip } from './tooltip'; // Not needed anymore


var splitingAlg_1 = require("./splitingAlg");

var runningMatch_1 = require("./runningMatch");

var applyScores_1 = require("./applyScores");

var environment_1 = require("./environment");

var serverAPI_1 = require("./serverAPI");
/* index.ts
This script is the entry point for everything, it calls each of the steps (found in the imports above) to inject the UI and process the page.
Once bundled into a single JS script, this will be injected into all pages on the wikipedia domain by the browser extension or injected by the bookmarklet.
This doesn't depend on any libraries or files outside of this folder & the assets found in the core folder (where the built js file ends up), so it should function on its own (inside or outside of an extension).

Note: All of this will get put into an annonoumous function by Parcel which means our
variables (except those explicitly defined on window) don't go in the Wikipedia page's js scope - so they dont
interfere with Wikipedia's own javascript, browsers also isolate extensions from page js so we have to do hacks to get to wikipedia-page own javascript.
*/

/** @returns The max number in an array of numbers */


var findMax = function findMax(arr) {
  var max = 0;

  for (var i = 0; i < arr.length; i++) {
    if (arr[i] > max) max = arr[i];
  }

  return max;
};
/** @returns The min number in an array of numbers */


var findMin = function findMin(arr) {
  var min = 0;

  for (var i = 0; i < arr.length; i++) {
    if (arr[i] < min) min = arr[i];
  }

  return min;
};
/**
 * @param word_list - An array of strings of every word in the current article in order.
 * @returns an object with a scores array and words array where the Nth score corresponds to the Nth word
 * The words & scores array has some words missing and some goblygook inserted to simulate an in-exact match
 * beteween the server's trust algorithim output and page content */


var generateFakeScores = function generateFakeScores(word_list) {
  return new Promise(function (resolve) {
    var output = {
      words: [],
      scores: [],
      revisionIndex: 0
    };

    for (var i = 0; i < word_list.length; i++) {
      var randomNumber = Math.round(Math.random() * 10);
      if (randomNumber === 2) continue; // skip this word
      else if (randomNumber === 3) {
          output.words.push('goblygook'); // insert junk word
        } else {
          output.words.push(word_list[i]); // otherwise use the actual word
        }
      output.scores.push(randomNumber * Math.sin(i * 0.0004) > 5 ? Math.sin(i * 0.0004) : 1);
    }

    resolve(output);
  });
};
/* gets the revisionId and pageId that the wikipedia page javascript defines globally
NOTE: this must be run using the page's scope Not an extensions! */


var getWikipediaPageMetaData = function getWikipediaPageMetaData() {
  var revId = window.RLCONF.wgCurRevisionId;
  if (!revId) revId = window.RLCONF.wgRevisionId;
  var output = {
    revId: revId,
    pageId: window.RLCONF.wgArticleId
  };
  return output;
};

var processScores = function processScores(serverResponse, splitData // TODO: ------------------- ACTUAL TYPE
) {
  console.log('Server Response: ', serverResponse); // mark that the server has responded

  completionStage = consts.COMPLETION_STAGES.api_recived;
  var mapping = runningMatch_1.getWordMatchMapping(serverResponse.words, splitData.pageWordList);
  console.groupCollapsed('==== Wiki Page to Server Word Mappings ====');
  console.log('Format: "Word on page" "mapped word from server word list" | index of page word->index of mapped server word ');
  var mappedScores = new Array(mapping.length);

  for (var index = 0; index < mapping.length; index++) {
    var mappedWord = serverResponse.words[mapping[index]] || '';
    var mappedScore = serverResponse.scores[mapping[index]] || -1;
    mappedScores[index] = mappedScore;
    console.log('%c"' + splitData.pageWordList[index] + '" "' + mappedWord + '" | ' + index + '->' + mapping[index], //apply color / style based on mapping alignment
    'color: #0000' + (splitData.pageWordList[index] == mappedWord ? '00' : 'ff') + '; font-weight: ' + (index != mapping[index] ? 'bold' : 'normal') + ';');
  }

  console.groupEnd(); // The revsiionIndex and maxWordScore must be set before displaying the scores, as it is used to normalize them to a 0-1 scale

  window.WikiTrustGlobalVars.revisionIndex = serverResponse.revisionIndex;
  window.WikiTrustGlobalVars.maxWordScore = findMax(mappedScores);
  var minTrustPerGroup = applyScores_1.applyWordScores(splitData.textNodesPerGroup, mappedScores);

  for (var i = 0, len = splitData.groupingElems.length; i < len; i++) {
    var groupingElem = splitData.groupingElems[i];
    var minTrustInGroup = applyScores_1.calculateScaledScore(minTrustPerGroup[i]);
    UI.addTextGroupMark(groupingElem, minTrustInGroup);
  }

  UI.hideLoadingAnimation();
  completionStage = consts.COMPLETION_STAGES.page_processed; // Mark that WikiTrust has finished setup.
  // UI.removeUi();
};

var setupWikiTrust = function setupWikiTrust() {
  // injectTooltip();
  // completionStage = consts.COMPLETION_STAGES.ui_injected; // Mark that WikiTrust has injected the uiFrame.
  UI.showLoadingAnimation();
  var splitData = splitingAlg_1.runPageSplitter(WIKI_CONTENT_TEXT_ELEMENT);
  console.log('splitData: ', splitData);
  console.log('Fetching page data');
  environment_1.runFunctionInPageContext(getWikipediaPageMetaData).then(function (pageMetaData) {
    console.log('Wikipedia Page Meta Data: ', pageMetaData); //generateFakeScores(splitData.pageWordList) //  uncoment this and comment out below line to always use fake scores

    serverAPI_1.fetchScores(pageMetaData.revId, pageMetaData.pageId).then(function (serverResponse) {
      if (serverResponse.error) {
        // If there was an error, show the error message and then show FAKE scores:
        alert('server error! (PAGE WILL NOW SHOW FAKE SCORES) error:' + JSON.stringify(serverResponse));
        generateFakeScores(splitData.pageWordList).then(function (serverResponse) {
          processScores(serverResponse, splitData);
        }); // Otherwise actually process the scores from the server:
      } else processScores(serverResponse, splitData);
    })["catch"](console.warn);
    completionStage = consts.COMPLETION_STAGES.api_sent;
  });
};

var handleActivateButtonClick = function handleActivateButtonClick() {
  if (completionStage === consts.COMPLETION_STAGES.base_ui_injected) {
    setupWikiTrust();
  } else if (completionStage !== consts.COMPLETION_STAGES.page_processed) {
    alert('TODO: Write Cancel Loading / displaying WikiTrust data function');
  }

  document.getElementById('WT_Activate_Button').blur();
}; // ------ Initilization Code (Runs on script injection) -------


if (window.WikiTrustGlobalVars === undefined) {
  window.WikiTrustGlobalVars = {
    completionStage: 0,
    revisionIndex: 1,
    maxWordScore: 1,
    trustVisible: false
  };
} // Set the completionStage from any previous runs of WikiTrust on this current page or session
// This handles the case where the user tries to run WikiTrust twice on the same page


var completionStage = window.WikiTrustGlobalVars.completionStage; // Find the element containing the wikipedia article text:

var WIKI_CONTENT_TEXT_ELEMENT = document.querySelector('.mw-parser-output');

if (completionStage === consts.COMPLETION_STAGES.just_loaded) {
  // ^ Here we know that this script just loaded & hasn't been run on the page before...
  if (WIKI_CONTENT_TEXT_ELEMENT) {
    UI.injectStylesheet();
    UI.injectUi();
    UI.addButtonClickCallback(handleActivateButtonClick);
    completionStage = consts.COMPLETION_STAGES.base_ui_injected; // Mark that WikiTrust has injected the base UI (button & style).

    if (environment_1.envIsBookmarklet() === true) setupWikiTrust();
  } else alert("WikiTrust can't parse this page yet - No wikipedia text container found.");
} // sources:
// http://kathack.com/js/kh.js
// https://stackoverflow.com/questions/10730309/find-all-text-nodes-in-html-page
// https://stackoverflow.com/questions/31275446/how-to-wrap-part-of-a-text-in-a-node-with-javascript
// https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=revisions&continue=&titles=List_of_common_misconceptions&redirects=1&rvprop=ids
},{"./consts":"consts.ts","./ui":"ui.ts","./splitingAlg":"splitingAlg.ts","./runningMatch":"runningMatch.ts","./applyScores":"applyScores.ts","./environment":"environment.ts","./serverAPI":"serverAPI.ts"}],"../node_modules/parcel-bundler/src/builtins/hmr-runtime.js":[function(require,module,exports) {
var global = arguments[3];
var OVERLAY_ID = '__parcel__error__overlay__';
var OldModule = module.bundle.Module;

function Module(moduleName) {
  OldModule.call(this, moduleName);
  this.hot = {
    data: module.bundle.hotData,
    _acceptCallbacks: [],
    _disposeCallbacks: [],
    accept: function (fn) {
      this._acceptCallbacks.push(fn || function () {});
    },
    dispose: function (fn) {
      this._disposeCallbacks.push(fn);
    }
  };
  module.bundle.hotData = null;
}

module.bundle.Module = Module;
var checkedAssets, assetsToAccept;
var parent = module.bundle.parent;

if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== 'undefined') {
  var hostname = "" || location.hostname;
  var protocol = location.protocol === 'https:' ? 'wss' : 'ws';
  var ws = new WebSocket(protocol + '://' + hostname + ':' + "52426" + '/');

  ws.onmessage = function (event) {
    checkedAssets = {};
    assetsToAccept = [];
    var data = JSON.parse(event.data);

    if (data.type === 'update') {
      var handled = false;
      data.assets.forEach(function (asset) {
        if (!asset.isNew) {
          var didAccept = hmrAcceptCheck(global.parcelRequire, asset.id);

          if (didAccept) {
            handled = true;
          }
        }
      }); // Enable HMR for CSS by default.

      handled = handled || data.assets.every(function (asset) {
        return asset.type === 'css' && asset.generated.js;
      });

      if (handled) {
        console.clear();
        data.assets.forEach(function (asset) {
          hmrApply(global.parcelRequire, asset);
        });
        assetsToAccept.forEach(function (v) {
          hmrAcceptRun(v[0], v[1]);
        });
      } else if (location.reload) {
        // `location` global exists in a web worker context but lacks `.reload()` function.
        location.reload();
      }
    }

    if (data.type === 'reload') {
      ws.close();

      ws.onclose = function () {
        location.reload();
      };
    }

    if (data.type === 'error-resolved') {
      console.log('[parcel] ✨ Error resolved');
      removeErrorOverlay();
    }

    if (data.type === 'error') {
      console.error('[parcel] 🚨  ' + data.error.message + '\n' + data.error.stack);
      removeErrorOverlay();
      var overlay = createErrorOverlay(data);
      document.body.appendChild(overlay);
    }
  };
}

function removeErrorOverlay() {
  var overlay = document.getElementById(OVERLAY_ID);

  if (overlay) {
    overlay.remove();
  }
}

function createErrorOverlay(data) {
  var overlay = document.createElement('div');
  overlay.id = OVERLAY_ID; // html encode message and stack trace

  var message = document.createElement('div');
  var stackTrace = document.createElement('pre');
  message.innerText = data.error.message;
  stackTrace.innerText = data.error.stack;
  overlay.innerHTML = '<div style="background: black; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; opacity: 0.85; font-family: Menlo, Consolas, monospace; z-index: 9999;">' + '<span style="background: red; padding: 2px 4px; border-radius: 2px;">ERROR</span>' + '<span style="top: 2px; margin-left: 5px; position: relative;">🚨</span>' + '<div style="font-size: 18px; font-weight: bold; margin-top: 20px;">' + message.innerHTML + '</div>' + '<pre>' + stackTrace.innerHTML + '</pre>' + '</div>';
  return overlay;
}

function getParents(bundle, id) {
  var modules = bundle.modules;

  if (!modules) {
    return [];
  }

  var parents = [];
  var k, d, dep;

  for (k in modules) {
    for (d in modules[k][1]) {
      dep = modules[k][1][d];

      if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) {
        parents.push(k);
      }
    }
  }

  if (bundle.parent) {
    parents = parents.concat(getParents(bundle.parent, id));
  }

  return parents;
}

function hmrApply(bundle, asset) {
  var modules = bundle.modules;

  if (!modules) {
    return;
  }

  if (modules[asset.id] || !bundle.parent) {
    var fn = new Function('require', 'module', 'exports', asset.generated.js);
    asset.isNew = !modules[asset.id];
    modules[asset.id] = [fn, asset.deps];
  } else if (bundle.parent) {
    hmrApply(bundle.parent, asset);
  }
}

function hmrAcceptCheck(bundle, id) {
  var modules = bundle.modules;

  if (!modules) {
    return;
  }

  if (!modules[id] && bundle.parent) {
    return hmrAcceptCheck(bundle.parent, id);
  }

  if (checkedAssets[id]) {
    return;
  }

  checkedAssets[id] = true;
  var cached = bundle.cache[id];
  assetsToAccept.push([bundle, id]);

  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    return true;
  }

  return getParents(global.parcelRequire, id).some(function (id) {
    return hmrAcceptCheck(global.parcelRequire, id);
  });
}

function hmrAcceptRun(bundle, id) {
  var cached = bundle.cache[id];
  bundle.hotData = {};

  if (cached) {
    cached.hot.data = bundle.hotData;
  }

  if (cached && cached.hot && cached.hot._disposeCallbacks.length) {
    cached.hot._disposeCallbacks.forEach(function (cb) {
      cb(bundle.hotData);
    });
  }

  delete bundle.cache[id];
  bundle(id);
  cached = bundle.cache[id];

  if (cached && cached.hot && cached.hot._acceptCallbacks.length) {
    cached.hot._acceptCallbacks.forEach(function (cb) {
      cb();
    });

    return true;
  }
}
},{}]},{},["../node_modules/parcel-bundler/src/builtins/hmr-runtime.js","main.ts"], null)
//# sourceMappingURL=/WikiTrust.js.map