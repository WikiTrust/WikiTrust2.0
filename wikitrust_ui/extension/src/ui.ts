import { getAsset } from './environment';
import { getColorForPercentage } from './applyScores';
import { showTooltipAtElement, hideTooltip } from './tooltip';

let activateWTButton: HTMLElement;

/**
 * Injects a style link tag into the head of the wikipedia page pointing to '/core/WikiTrustStyle.css'
 */
export const injectStylesheet = () => {
  // Inject a stylesheet into the current page.
  const style = (window.WikiTrustGlobalVars.styleElm = document.createElement(
    'link'
  ));
  style.rel = 'stylesheet';
  style.href = getAsset('core/WikiTrustStyle.css');
  document.getElementsByTagName('head')[0].appendChild(style);
};

/**
 * Returns an activate wikitrust button element.
 */
const buildButton = () => {
  activateWTButton = document.createElement('button');
  activateWTButton.id = 'WT_Activate_Button';
  activateWTButton.innerHTML = 'W<sub>T</sub>';
  return activateWTButton;
};

/**
 * Sets an on click listener on the activate WikiTrust Button with the passed function
 * @param clickEventFunction - the function to call when the activate button is clicked.
 */
export const addButtonClickCallback = (clickEventFunction: () => void) => {
  if (activateWTButton) activateWTButton.onclick = clickEventFunction;
};

/**
 * Returns an element to hold all the colored score markers/dots on the left of the article.
 */
let markContainer: HTMLElement;
const buildMarkContainer = () => {
  markContainer = document.createElement('div');
  markContainer.classList.add('wt-text-side-group-mark-container');
  markContainer.classList.add('mw-body'); // Uses wikipedia's mw-body class to adjust the left margin like the article.
  return markContainer;
};

/**
 * Adds a marker/dot element on the left side of the article which corresponds to a particular grouping.
 * @param groupingElement - The element that this marker is refering to (usually this is a paragraph or section element which contains many words and or child elements)
 * @param score - The score used to color this marker (usually the maximum score of the words within the groupingElement)
 */
export const addTextGroupMark = (
  groupingElement: HTMLElement,
  score: number
) => {
  if (!groupingElement || !markContainer || score === 0) return;
  groupingElement.classList.add('wt-grouping-container', 'trust-hidden');

  const rect = groupingElement.getBoundingClientRect();
  const yOffset = rect.top + window.pageYOffset + 5;
  const height = rect.bottom - rect.top - 10;

  const markElement = document.createElement('div');
  markElement.style.top = yOffset + 'px';
  markElement.style.height = height + 'px';
  markElement.classList.add('wt-text-side-group-mark');
  markElement.style.backgroundColor = getColorForPercentage(score, 1);
  markElement.onmouseenter = (e) => {
    groupingElement.classList.remove('trust-hidden');
    showTooltipAtElement(
      markElement,
      'Max Score: ' + Math.round(score * 1000) / 1000
    );
  };
  markElement.onmouseleave = (e) => {
    groupingElement.classList.add('trust-hidden');
    hideTooltip();
  };
  markContainer.appendChild(markElement);
};

let loadingAnimIntervalId = -1;
/** Shows an askii loading animation in the activate WikiTrust button */
export const showLoadingAnimation = () => {
  if (loadingAnimIntervalId !== -1) return;
  const frames = ['|...', '.|..', '..|.', '...|'];
  activateWTButton.innerText = frames[0];
  let counter = 0;
  loadingAnimIntervalId = window.setInterval(() => {
    counter = (counter + 1) % 4;
    activateWTButton.innerText = frames[counter];
  }, 600);
};

/** Stops the askii loading animation in the activate WikiTrust button */
export const hideLoadingAnimation = () => {
  if (loadingAnimIntervalId === -1) return;
  clearInterval(loadingAnimIntervalId);
};

/** Stops the askii loading animation in the activate WikiTrust button */
export const injectUi = () => {
  const uiFrameContainer = (window.WikiTrustGlobalVars.uiFrameContainer = document.createElement(
    'div'
  ));
  uiFrameContainer.id = 'Wikitrust_UI';
  uiFrameContainer.appendChild(buildButton());
  document.body.appendChild(buildMarkContainer());
  document.body.appendChild(uiFrameContainer);
};

export const removeUi = () => {
  document.body.removeChild(window.WikiTrustGlobalVars.uiFrameContainer!);
};

// unused: ----------.....!
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

// const buildCircleGradient = () => {
//   const gradient = document.createElement('img');
//   gradient.id = 'WikiTrustCircleGradient';
//   gradient.src = getAsset('core/Gradient_180.jpg');
//   return gradient;
// };
