import * as consts from './consts';

/**
 * Given an html element checks if it is of an included type and
 * does not have any of the excluded classes specified in the ./consts module.
 * @param element - The HTML element to check.
 * @returns {boolean} True if the element passes the filters, false otherwise.
 */
const elementPassesFilters = (element: HTMLElement) => {
  // -- check element for included Tag name:
  if (
    !element.tagName ||
    !consts.REPLACE_WORDS_IN[element.tagName.toLowerCase()]
  ) {
    return false; // incorrect tag, element should be excluded;
  }

  // -- check element For excluded class:
  const hasClass = (className: string) => {
    // looks for the className in the element's classes string (the spaces ensure only full class names not just a part of the class name is matched).
    return ` ${element.className} `.indexOf(` ${className} `) > -1;
  };

  // loops through the EXCLUDE_ELEMENT_CLASSES object and checks the element for each class name.
  for (const className of consts.ELEMENT_CLASSES_TO_EXCLUDE) {
    if (hasClass(className)) return false; // has excluded class, element should be excluded;
  }

  return true; // all filters pass (element not excluded);
};

/**
 * Recursively extracts all text nodes that are decendants of the passed element.
 * @param parentElement - Returns all the text nodes within this element.
 * @returns An array of text nodes.
 */
export const extractTextNodes = (parentElement: HTMLElement) => {
  let outputNodes: Node[] = [];
  if (parentElement && elementPassesFilters(parentElement)) {
    for (let i = 0, len = parentElement.childNodes.length; i < len; i++) {
      const childNode = parentElement.childNodes[i];
      if (childNode.nodeType === Node.TEXT_NODE && childNode.nodeValue) {
        outputNodes.push(childNode);
      } else if (childNode.nodeType === Node.ELEMENT_NODE) {
        // Recursively call this function on the childNode:
        outputNodes = outputNodes.concat(
          extractTextNodes(childNode as HTMLElement)
        );
      }
    }
  }
  return outputNodes;
};
