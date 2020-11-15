// inspired by: https://johnresig.com/projects/javascript-diff-algorithm/
// See comments on functions.

const CONSECUTIVE_MATCHES_REQUIRED = 3;
let currConsecutiveMatches = 0;

let sourceWords: string[] = new Array();
let targetWords: string[] = new Array();
const sourceToTargetMapping: number[] = new Array(sourceWords.length);

let sourceWordIndex = 0,
  targetWordIndex = 0;

/**
 * A dictionary where each key is a word and the indecies where that
 * word is found in the source and target are stored in the first and second
 * arrays for that key respectively. Dictionary format:
 * { word: [ [indecies where word is found in the source], [indecies where word is found in the target] ] }
 */
let wordMatchIndicieDictionary: {
  [wordKey: string]: [number[], number[]];
} = {};

enum wordOrigin {
  source = 0,
  target = 1,
}

/**
 * Adds a word to the word match index dictionary
 * @param word - The word to insert
 * @param wordOrigin - 0 if the word comes from the source array, 1 if it comes from the target array (see enum above).
 * @param index - The index of the word in the array it came from (source or target).
 */
const addWordIndexToIndicieDictionary = (
  word: string,
  index: number,
  wordOrigin: wordOrigin
) => {
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
const getWordIndeciesFromDictionary = (
  word: string,
  wordOrigin: wordOrigin
) => {
  return wordMatchIndicieDictionary[word][wordOrigin] || [];
};

/**
 * Given a starting index in the souceWordList and a starting index in the targetWordList,
 * compares the next n words in the two list to see if they also match (where n = CONSECUTIVE_MATCHES_REQUIRED)
 * @param startSourceIndex - The index to start comparing from in the sourceWordList
 * @param startTargetIndex - The index to start comparing from in the targetWordList
 * @returns true if the next n words in the sourceWordList also match the next n words in the targetWordList.
 */
const checkConsecutiveMatches = (
  startSourceIndex: number,
  startTargetIndex: number
) => {
  for (let i = 0; i < CONSECUTIVE_MATCHES_REQUIRED; i++) {
    // TODO: check if indexes are over size;
    if (
      targetWords[startTargetIndex + i] !== sourceWords[startSourceIndex + i]
    ) {
      return false;
    }
  }
  console.log(
    'found ' +
      CONSECUTIVE_MATCHES_REQUIRED +
      ' consecutive matches starting at source index: ' +
      startSourceIndex +
      ' and target index: ' +
      startTargetIndex
  );
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
const checkCrossMatch = (currSourceWord: string, currTargetWord: string) => {
  // Try to find indecies where the current target word shows up in the sourceWordList:
  const matchingSourceIndecies = getWordIndeciesFromDictionary(
    currTargetWord,
    wordOrigin.source
  );
  console.log('Source Match:' + currTargetWord, matchingSourceIndecies);
  for (let u = 0; u < matchingSourceIndecies.length; u++) {
    const foundSourceWordIndex = matchingSourceIndecies[u];
    if (checkConsecutiveMatches(foundSourceWordIndex, targetWordIndex)) {
      sourceWordIndex = foundSourceWordIndex;
      return true;
    }
  }

  // Try to find indecies where the current source word shows up in the targetWordList:
  const matchingTargetIndecies = getWordIndeciesFromDictionary(
    currSourceWord,
    wordOrigin.target
  );
  console.log('Target Match:' + currSourceWord, matchingTargetIndecies);
  for (let u = 0; u < matchingTargetIndecies.length; u++) {
    const foundPageWordIndex = matchingTargetIndecies[u];
    if (checkConsecutiveMatches(sourceWordIndex, foundPageWordIndex)) {
      targetWordIndex = foundPageWordIndex;
      return true;
    }
  }

  // no matches found ):
  return false;
};

/**
 * Compares two lists of words where words in the targetWordList are close to the words in the sourceWordList, but they may have words added and/or deleted.
 * @param sourceWordList - An array of words as strings
 * @param targetWordList - An array of words as strings, potentially with edits from the sourceWordList
 * @returns an array mapping from the words in the source to the words in the target where the nth mapping array index, corresponds to the nth word in the source array and the value at mapping[n] is the index of where the same word goes in the target array.
 */
export const getWordMatchMapping = (
  sourceWordList: string[],
  targetWordList: string[]
) => {
  sourceWords = sourceWordList;
  targetWords = targetWordList;
  while (true) {
    const currSourceWord: string = sourceWords[sourceWordIndex],
      currTargetWord: string = targetWords[targetWordIndex];

    if (currSourceWord === currTargetWord) {
      sourceToTargetMapping[sourceWordIndex] = targetWordIndex;
      currConsecutiveMatches++;
    } else {
      currConsecutiveMatches = 0;
      // add the current words to the dictionary.
      addWordIndexToIndicieDictionary(
        currSourceWord,
        sourceWordIndex,
        wordOrigin.source
      );
      addWordIndexToIndicieDictionary(
        currTargetWord,
        targetWordIndex,
        wordOrigin.target
      );
      if (checkCrossMatch(currSourceWord, currTargetWord)) continue;
    }

    if (targetWordIndex < targetWords.length - 1) targetWordIndex++;
    if (sourceWordIndex < sourceWords.length - 1) sourceWordIndex++;
    if (
      sourceWordIndex === sourceWords.length - 1 &&
      targetWordIndex === targetWords.length - 1
    ) {
      break;
    }

    if (currConsecutiveMatches === CONSECUTIVE_MATCHES_REQUIRED) {
      // free up memory by clearing dictionaries. (We assume that we've found the next set of matches):
      wordMatchIndicieDictionary = {};
    }
  }
  return sourceToTargetMapping;
};
