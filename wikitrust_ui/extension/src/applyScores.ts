import * as interfaces from './interfaces';
import { showTooltipAtElement } from './tooltip';

/**
 * Returns true if the character code is a whitespace character.
 * @param {Node} code - The char code you want to test
 */
const charCodeIsWhitespace = (code: number) => {
  return (code <= 32 && code >= 0) || code === 127;
};

/**
 * @return an 'rgba(255,255,255,1)' formated color string based on a percent through a hard-coded gradient and an opacity.
 * @param {string} percent - The percentage (0-1) representing how far along the gradient you want to sample the color.
 * @param {string} opacity - The opacity in the output color string.
 */
export const getColorForPercentage = (percent: number, opacity: number) => {
  // Source: https://stackoverflow.com/questions/7128675/from-green-to-red-color-depend-on-percentage
  const percentColorsGradient: interfaces.GradientStop[] = [
    // Define a gradient (0 = least trustworthy color, 1 = most trustworthy color)
    { percent: 0.0, color: { r: 0xff, g: 0xff, b: 0xff } }, // white
    { percent: 0.5, color: { r: 0xf7, g: 0xb7, b: 0x33 } }, // #f7b733
    { percent: 1.0, color: { r: 0xfc, g: 0x4a, b: 0x1a } }, // #fc4a1a
  ];
  let i = 1;
  for (i = 1; i < percentColorsGradient.length - 1; i++) {
    if (percent < percentColorsGradient[i].percent) {
      break;
    }
  }
  const lower = percentColorsGradient[i - 1];
  const upper = percentColorsGradient[i];
  const range = upper.percent - lower.percent;
  const rangepercent = (percent - lower.percent) / range;
  const percentLower = 1 - rangepercent;
  const percentUpper = rangepercent;
  const color = {
    r: Math.floor(lower.color.r * percentLower + upper.color.r * percentUpper),
    g: Math.floor(lower.color.g * percentLower + upper.color.g * percentUpper),
    b: Math.floor(lower.color.b * percentLower + upper.color.b * percentUpper),
  };
  return `rgba(${[color.r, color.g, color.b, opacity].join(',')})`;
  // or output as hex if preferred
};

/**
 * Inserts a section of text (wrapped in a span highlighted based on the passed score), right before the given text node.
 * This function is inteneded to be called for every word chunk in a text node before deleting the text node.
 * @param {Node} textNode - The text node where this word chunk was found
 * @param {string} wordChunk - A contiguous string found within the text node where all the words have the same score
 * @param {string} score - The trust score given to all the words in the wordChunk.
 */
const insertWordChunk = (textNode: Node, wordChunk: string, score: number) => {
  const parentElement = textNode.parentElement;
  if (!parentElement) return;
  const wordChunkElement = document.createElement('span');
  wordChunkElement.textContent = wordChunk;
  wordChunkElement.className = 'wt-word-chunk';
  wordChunkElement.setAttribute('trust', score.toString()); // for debug
  wordChunkElement.onmouseover = (e) => {
    showTooltipAtElement(
      wordChunkElement,
      'Scaled Score:</br>' + Math.round(score * 1000) / 1000
    );
  };
  if (score >= 0) {
    // if the word has a score applied
    wordChunkElement.style.borderBottom = `1px solid ${getColorForPercentage(
      score,
      1
    )}`;
    wordChunkElement.style.backgroundColor = getColorForPercentage(score, 0.1);
  } else wordChunkElement.style.borderBottom = `2px solid lightgrey`; // if the wordChunk was not matched to the algorithim's output, highlight blue
  parentElement.insertBefore(wordChunkElement, textNode);
};

/**
 * Takes all the text nodes and the word scores and groups sections of contiguous scores and calls insert word chunk on them.
 * @param textNodesPerGroup - An array of arrays of text DOM Nodes where the Nth array corresponds to the Nth grouping element and each node within that array is a text node in that grouping element.
 * @param wordScores - An array of trust scores where the Nth score corresponds to the Nth word on the page
 * @param maxWordScore - The maximum trust score in this article
 * @returns - An array containing the maximum trust score for each grouping element.
 */
export const applyWordScores = (
  textNodesPerGroup: Node[][],
  wordScores: number[],
  maxWordScore: number
) => {
  const maxTrustPerGroup: number[] = [];
  let currWordIndex = 0;
  let lastCharWasWhitespace = false;
  for (let gi = 0, len = textNodesPerGroup.length; gi < len; gi++) {
    let maxTrustInThisGroup = 0;
    for (let ti = 0, len = textNodesPerGroup[gi].length; ti < len; ti++) {
      const textNode = textNodesPerGroup[gi][ti];
      const nodeText = textNode.nodeValue || '';
      let wordChunkStartIndex = 0;
      let scaledScore = wordScores[currWordIndex] / maxWordScore;
      const len = nodeText.length;
      let allCharsAreWhitespace = true;
      // loop through every character in this text node finding words.
      for (let charindex = 0; charindex < len; charindex++) {
        const currCharIsWhitespace = charCodeIsWhitespace(
          nodeText.charCodeAt(charindex)
        );
        if (!currCharIsWhitespace && lastCharWasWhitespace) {
          allCharsAreWhitespace = false;
          if (wordScores[currWordIndex] !== wordScores[currWordIndex + 1]) {
            if (scaledScore > maxTrustInThisGroup)
              maxTrustInThisGroup = scaledScore;
            insertWordChunk(
              textNode,
              nodeText.substring(wordChunkStartIndex, charindex),
              scaledScore
            );
            wordChunkStartIndex = charindex;
          }
          currWordIndex++;
        }
        lastCharWasWhitespace = currCharIsWhitespace;
      }
      if (wordChunkStartIndex !== 0) {
        if (wordChunkStartIndex !== len - 1) {
          insertWordChunk(
            textNode,
            nodeText.substring(wordChunkStartIndex, len),
            scaledScore
          );
          if (scaledScore > maxTrustInThisGroup)
            maxTrustInThisGroup = scaledScore;
        }
      } else if (!charCodeIsWhitespace(nodeText.charCodeAt(0))) {
        insertWordChunk(textNode, nodeText.substring(0, len), scaledScore);
        if (scaledScore > maxTrustInThisGroup)
          maxTrustInThisGroup = scaledScore;
      } else if (allCharsAreWhitespace) {
        insertWordChunk(textNode, nodeText.substring(0, len), 0);
      }
      textNode.parentNode?.removeChild(textNode);
    }
    maxTrustPerGroup.push(maxTrustInThisGroup);
  }
  return maxTrustPerGroup;
};
