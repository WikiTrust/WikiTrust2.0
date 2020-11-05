import { getGroupingElems } from './findGroupingElems';
import { extractTextNodes } from './extractTextNodes';

/**
 * Combines the texts of an array of text nodes then splits the string node on whitespace, to get an array of words.
 * @param textNodeArr - An array of consecutive DOM text nodes (not the containing element) to find words in.
 */
const extractWords = (textNodeArr: Node[]) => {
  let textStr = '';
  for (let index = 0, len = textNodeArr.length; index < len; index++) {
    if (textNodeArr[index]) textStr += textNodeArr[index].nodeValue;
  }
  const words = textStr.split(/\s+/);
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
export const runPageSplitter = (articleContainer: HTMLElement) => {
  /** The elements we use to group words, such as paragraphs (this element should be nearly a direct decendant of the articleContainer). */
  const groupingElems = getGroupingElems(articleContainer);
  /** An array of arrays where the first index corresponds a grouping element's index and the second index is the text node within that group */
  const textNodesPerGroup: Node[][] = [];
  /** A string array of all words on the page (split on whitespace only). */
  let pageWordList: string[] = [];

  for (let groupIndex = 0; groupIndex < groupingElems.length; groupIndex++) {
    const groupingElem = groupingElems[groupIndex];
    const textNodes = extractTextNodes(groupingElem);
    pageWordList = pageWordList.concat(extractWords(textNodes));
    textNodesPerGroup.push(textNodes);
  }

  return {
    groupingElems,
    textNodesPerGroup,
    pageWordList,
  };
};
