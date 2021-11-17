import * as interfaces from './interfaces';
import * as consts from './consts';
import * as UI from './ui';
// import { injectTooltip } from './tooltip'; // Not needed anymore
import { runPageSplitter } from './splitingAlg';
import { getWordMatchMapping } from './runningMatch';
import { applyWordScores, calculateScaledScore } from './applyScores';
import { envIsBookmarklet, runFunctionInPageContext } from './environment';
import { fetchScores } from './serverAPI';

/* index.ts
This script is the entry point for everything, it calls each of the steps (found in the imports above) to inject the UI and process the page.
Once bundled into a single JS script, this will be injected into all pages on the wikipedia domain by the browser extension or injected by the bookmarklet.
This doesn't depend on any libraries or files outside of this folder & the assets found in the core folder (where the built js file ends up), so it should function on its own (inside or outside of an extension).

Note: All of this will get put into an annonoumous function by Parcel which means our
variables (except those explicitly defined on window) don't go in the Wikipedia page's js scope - so they dont
interfere with Wikipedia's own javascript, browsers also isolate extensions from page js so we have to do hacks to get to wikipedia-page own javascript.
*/

/** @returns The max number in an array of numbers */
const findMax = (arr: number[]) => {
  let max = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] > max) max = arr[i];
  }
  return max;
};

/** @returns The min number in an array of numbers */
const findMin = (arr: number[]) => {
  let min = 0;
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] < min) min = arr[i];
  }
  return min;
};

/**
 * @param word_list - An array of strings of every word in the current article in order.
 * @returns an object with a scores array and words array where the Nth score corresponds to the Nth word
 * The words & scores array has some words missing and some goblygook inserted to simulate an in-exact match
 * beteween the server's trust algorithim output and page content */
const generateFakeScores = (word_list: string[]) => {
  return new Promise<interfaces.serverScoresResponse>((resolve) => {
    const output: interfaces.serverScoresResponse = {
      words: [],
      scores: [],
      revisionIndex: 0,
    };
    for (let i = 0; i < word_list.length; i++) {
      const randomNumber = Math.round(Math.random() * 10);
      if (randomNumber === 2) continue;
      // skip this word
      else if (randomNumber === 3) {
        output.words.push('goblygook'); // insert junk word
      } else {
        output.words.push(word_list[i]); // otherwise use the actual word
      }
      output.scores.push(Math.sin(i * 0.04));
    }
    resolve(output);
  });
};

/* gets the revisionId and pageId that the wikipedia page javascript defines globally
NOTE: this must be run using the page's scope Not an extensions! */
const getWikipediaPageMetaData = () => {
  let revId = window.RLCONF.wgCurRevisionId;
  if (!revId) revId = window.RLCONF.wgRevisionId;

  const output: interfaces.PageMetaData = {
    revId: revId,
    pageId: window.RLCONF.wgArticleId,
  };
  return output;
};

const processScores = (
  serverResponse: interfaces.serverScoresResponse,
  splitData: any // TODO: ------------------- ACTUAL TYPE
) => {
  console.log('Server Response: ', serverResponse);

  // mark that the server has responded
  completionStage = consts.COMPLETION_STAGES.api_recived;
  const mapping = getWordMatchMapping(
    serverResponse.words,
    splitData.pageWordList
  );
  console.groupCollapsed('==== Wiki Page to Server Word Mappings ====');
  console.log(
    'Format: "Word on page" "mapped word from server word list" | index of page word->index of mapped server word '
  );
  const mappedScores = new Array(mapping.length);
  for (let index = 0; index < mapping.length; index++) {
    const mappedWord = serverResponse.words[mapping[index]] || '';
    const mappedScore = serverResponse.scores[mapping[index]] || -1;
    mappedScores[index] = mappedScore;
    console.log(
      '%c"' +
        splitData.pageWordList[index] +
        '" "' +
        mappedWord +
        '" | ' +
        index +
        '->' +
        mapping[index],
      //apply color / style based on mapping alignment
      'color: #0000' +
        (splitData.pageWordList[index] == mappedWord ? '00' : 'ff') +
        '; font-weight: ' +
        (index != mapping[index] ? 'bold' : 'normal') +
        ';'
    );
  }
  console.groupEnd();

  // The revsiionIndex and maxWordScore must be set before displaying the scores, as it is used to normalize them to a 0-1 scale
  window.WikiTrustGlobalVars.revisionIndex = serverResponse.revisionIndex;
  window.WikiTrustGlobalVars.maxWordScore = findMax(mappedScores);

  const minTrustPerGroup = applyWordScores(
    splitData.textNodesPerGroup,
    mappedScores
  );
  for (let i = 0, len = splitData.groupingElems.length; i < len; i++) {
    const groupingElem = splitData.groupingElems[i];
    const minTrustInGroup = calculateScaledScore(minTrustPerGroup[i]);
    UI.addTextGroupMark(groupingElem, minTrustInGroup);
  }
  UI.hideLoadingAnimation();
  completionStage = consts.COMPLETION_STAGES.page_processed; // Mark that WikiTrust has finished setup.
  // UI.removeUi();
};

const setupWikiTrust = () => {
  // injectTooltip();
  // completionStage = consts.COMPLETION_STAGES.ui_injected; // Mark that WikiTrust has injected the uiFrame.
  UI.showLoadingAnimation();
  const splitData = runPageSplitter(WIKI_CONTENT_TEXT_ELEMENT);
  console.log('splitData: ', splitData);
  console.log('Fetching page data');
  runFunctionInPageContext(getWikipediaPageMetaData).then(
    (pageMetaData: interfaces.PageMetaData) => {
      // generateFakeScores(splitData.pageWordList) //  uncoment this and comment out below line to always use fake scores
      fetchScores(pageMetaData.revId, pageMetaData.pageId)
        .then((serverResponse) => {
          if (serverResponse.error) {
            // If there was an error, show the error message and then show FAKE scores:
            alert(
              'server error! (PAGE WILL NOW SHOW FAKE SCORES) error:' +
                JSON.stringify(serverResponse)
            );
            generateFakeScores(splitData.pageWordList).then(
              (serverResponse) => {
                processScores(serverResponse, splitData);
              }
            );
            // Otherwise actually process the scores from the server:
          } else processScores(serverResponse, splitData);
        })
        .catch(console.warn);
      completionStage = consts.COMPLETION_STAGES.api_sent;
    }
  );
};

const handleActivateButtonClick = () => {
  if (completionStage === consts.COMPLETION_STAGES.base_ui_injected) {
    setupWikiTrust();
  } else if (completionStage !== consts.COMPLETION_STAGES.page_processed) {
    alert('TODO: Write Cancel Loading / displaying WikiTrust data function');
  }
  document.getElementById('WT_Activate_Button').blur();
};

// ------ Initilization Code (Runs on script injection) -------

if (window.WikiTrustGlobalVars === undefined) {
  window.WikiTrustGlobalVars = {
    completionStage: 0,
    revisionIndex: 1, // TODO: Hopefully there's some error if this is not updated from the server, if it itsn't "1" will create unexpected display scores.
    maxWordScore: 1, // TODO: Hopefully there's some error if this is not updated from the server, if it itsn't "1" will create unexpected displayed scores.
    trustVisible: false, // not used
  };
}

// Set the completionStage from any previous runs of WikiTrust on this current page or session
// This handles the case where the user tries to run WikiTrust twice on the same page
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
  } else
    alert(
      "WikiTrust can't parse this page yet - No wikipedia text container found."
    );
}

// sources:
// http://kathack.com/js/kh.js
// https://stackoverflow.com/questions/10730309/find-all-text-nodes-in-html-page
// https://stackoverflow.com/questions/31275446/how-to-wrap-part-of-a-text-in-a-node-with-javascript
// https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=revisions&continue=&titles=List_of_common_misconceptions&redirects=1&rvprop=ids
