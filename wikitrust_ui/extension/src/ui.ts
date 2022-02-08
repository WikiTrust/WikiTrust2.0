import { getAsset } from './environment';
import { getColorForPercentage } from './applyScores';
import { showTooltipAtElement, hideTooltip } from './tooltip';

let activateWTButton: HTMLElement;
let WTDialPointer: HTMLElement;

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
 * Returns the gradient dial that goes behind the activate wikitrust button.
 */
const buildCircularGradient = () => {
  const gradient = document.createElement('img');
  gradient.id = 'WT_Gradient_Dial';
  gradient.src = getAsset('core/Gradient.png');
  return gradient;
};

/**
 * Returns the black pointer line element for the gradient dial visualization.
 */
const buildDialPointer = () => {
  WTDialPointer = document.createElement('div');
  WTDialPointer.id = 'WT_Gradient_Dial_Pointer';
  return WTDialPointer;
};

/**
 * Returns the activate wikitrust button element.
 */
 const buildWTButton = () => {
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

/* shows the gradient dial, sets the position dial pointer to the correct position on the gradient dial and sets the color scheme to match. */
export const showTrustScore = (score: number) => {
  window.WikiTrustGlobalVars.uiFrameContainer!.classList.add('showing-score');
  activateWTButton.innerText = score.toFixed(1); // (score * 100).toFixed(1);
  activateWTButton.style.borderColor = getColorForPercentage(score, 1);
  WTDialPointer.style.transform = `scale(1.5) rotate(${(1 - score) * 90}deg)`;
};
export const hideTrustScore = () => {
  window.WikiTrustGlobalVars.uiFrameContainer!.classList.remove(
    'showing-score'
  );
  WTDialPointer.style.transform = `scale(1)`;
  activateWTButton.innerHTML = 'W<sub>T</sub>';
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
    // showTooltipAtElement(
    //   markElement,
    //   'Max Score: ' + Math.round(score * 1000) / 1000
    // );
    showTrustScore(score);
  };
  markElement.onmouseleave = (e) => {
    groupingElement.classList.add('trust-hidden');
    // hideTooltip();
    hideTrustScore();
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
  activateWTButton.innerHTML = 'W<sub>T</sub>';
  activateWTButton.classList.add('wt-active');
};

/** Stops the askii loading animation in the activate WikiTrust button */
export const injectUi = () => {
  const uiFrameContainer = (window.WikiTrustGlobalVars.uiFrameContainer = document.createElement(
    'div'
  ));
  uiFrameContainer.id = 'Wikitrust_UI_Container';
  // uiFrameContainer.appendChild(buildWikiTrustButtonComponent());
  uiFrameContainer.appendChild(buildWTButton());
  uiFrameContainer.appendChild(buildCircularGradient());
  uiFrameContainer.appendChild(buildDialPointer());
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
