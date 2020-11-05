import * as consts from './consts';
import * as UI from './ui';
import { injectTooltip } from './tooltip';
import { runPageSplitter } from './splitingAlg';
import { getWordMatchMapping } from './runningMatch';
import { applyWordScores } from './applyScores';
import { envIsBookmarklet, getAsset } from './environment';
import { fetchScores } from './fetchScores';

/* index.ts
This script is the entry point for everything, it calls each of the steps (found in the imports above) to inject the UI and process the page.
Once bundled into a single JS script, this will be injected into all pages on the wikipedia domain by the browser extension or injected by the bookmarklet.
This doesn't depend on any libraries or files outside of the bundle & core folder, so it should function on its own (outside of an extension).

Note: All of this will get put into an annonoumous function by Parcel which will avoid putting our
variables (except those explicitly defined on window) in the Wikipedia page's scope - so they dont
interfere with Wikipedia's own javascript.
*/

/** @returns The max number in an array of numbers */
const findMax = (arr: number[]) => {
  let max = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] > max) max = arr[i];
  }
  return max;
};

/**
 * @param word_list - An array of strings of every word in the current article in order.
 * @returns an object with a scores array and words array where the Nth score corresponds to the Nth word
 * The words & scores array has some words missing and some goblygook inserted to simulate an in-exact match
 * beteween the algorithim output and page content */
const generateFakeScores = (word_list: string[]) => {
  return new Promise<{ words: string[]; scores: number[] }>(resolve => {
    const output: { words: string[]; scores: number[] } = {
      words: [],
      scores: [],
    };
    for (let i = 0; i < word_list.length; i++) {
      const randomNumber = Math.round(Math.random() * 10);
      if (randomNumber === 2) continue;
      else if (randomNumber === 3) {
        output.words.push('goblygook');
      } else {
        output.words.push(word_list[i]);
      }
      output.scores.push(Math.sin(i * 0.04));
    }
    resolve(output);
  });
};

const setupWikiTrust = () => {
  injectTooltip();
  completionStage = consts.COMPLETION_STAGES.ui_injected; // Mark that WikiTrust has injected the uiFrame.
  UI.showLoadingAnimation();
  const splitData = runPageSplitter(WIKI_CONTENT_TEXT_ELEMENT);
  console.log('splitData: ', splitData);
  // fetchScores() // comment out generateFakeScores and uncoment this to use the real python algorithms
  generateFakeScores(splitData.pageWordList)
    .then(serverScores => {
      console.log('server response: ', serverScores);
      completionStage = consts.COMPLETION_STAGES.api_recived;
      const mapping = getWordMatchMapping(
        serverScores.words,
        splitData.pageWordList
      );
      const mappedScores = new Array(mapping.length);
      for (let index = 0; index < mapping.length; index++) {
        const mappedWord = serverScores.words[mapping[index]] || '';
        const mappedScore = serverScores.scores[mapping[index]] || -1;
        mappedScores[index] = mappedScore;
        console.log(
          splitData.pageWordList[index],
          mappedWord + ' | ' + index + '->' + mapping[index]
        );
      }

      const maxTrustPerGroup = applyWordScores(
        splitData.textNodesPerGroup,
        mappedScores,
        findMax(mappedScores)
      );
      for (let i = 0, len = splitData.groupingElems.length; i < len; i++) {
        const groupingElem = splitData.groupingElems[i];
        const maxTrustInGroup = maxTrustPerGroup[i];
        UI.addTextGroupMark(groupingElem, maxTrustInGroup);
      }
      UI.hideLoadingAnimation();
      completionStage = consts.COMPLETION_STAGES.page_processed; // Mark that WikiTrust has finished setup.
      UI.removeUi();
    })
    .catch(console.warn);
  completionStage = consts.COMPLETION_STAGES.api_sent;
};

const handleActivateButtonClick = () => {
  if (completionStage === consts.COMPLETION_STAGES.base_ui_injected) {
    setupWikiTrust();
  } else alert('TODO: Write Cancel Loading WikiTrust function');
};

// ------ Initilization Code (Runs on script injection) -------

if (window.WikiTrustGlobalVars === undefined) {
  window.WikiTrustGlobalVars = {
    completionStage: 0,
    trustVisible: false, // not used
  };
}

let completionStage: consts.COMPLETION_STAGES =
  window.WikiTrustGlobalVars.completionStage;

// Find the element containing the wikipedia article text:
const WIKI_CONTENT_TEXT_ELEMENT = document.querySelector(
  '.mw-parser-output'
) as HTMLElement;

if (completionStage === consts.COMPLETION_STAGES.just_loaded) {
  // ^ Here we know that this script just loaded & hasn't been run on the page before...
  if (WIKI_CONTENT_TEXT_ELEMENT) {
    UI.injectStylesheet();
    UI.injectUi();
    UI.addButtonClickCallback(handleActivateButtonClick);

    completionStage = consts.COMPLETION_STAGES.base_ui_injected; // Mark that WikiTrust has injected the base UI (button & style).

    if (envIsBookmarklet() === true) setupWikiTrust();
  } else console.warn("WikiTrust doesn't work on this page yet.");
}

// sources:
// http://kathack.com/js/kh.js
// https://stackoverflow.com/questions/10730309/find-all-text-nodes-in-html-page
// https://stackoverflow.com/questions/31275446/how-to-wrap-part-of-a-text-in-a-node-with-javascript
