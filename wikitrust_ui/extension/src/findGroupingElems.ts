import * as consts from './consts';

const allowedGroupingTags: { [tagName: string]: boolean } = {
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
  section: true,
};

// -- check if an html element has the passed name in its class parameter (used to check whether an Element has an Class Name that we want to exclude):
const hasClass = (element: HTMLElement, className: string) => {
  // looks for the className in the element's classes string (the spaces ensure only full class names, not just a part of the class name is matched).
  return ` ${element.className} `.indexOf(` ${className} `) !== -1;
}

/**
 * Returns all the child elements of the parent that pass filters.
 * Includes the children of 'section' elements rather than the section elements themselves.
 * This is because mobile wikipedia burries all the paragraphs in collapsable sections.
 * @param parent - The parent element to get the children in
 */
const elementPassesFilters = (domNode: Node) => {
  if (domNode.nodeType !== Node.ELEMENT_NODE || !domNode.childNodes) {
    return false;
  }
  if (!allowedGroupingTags[(domNode as HTMLElement).tagName.toLowerCase()]) {
    return false;
  }
  // loops through the EXCLUDE_ELEMENT_CLASSES object and checks the element for each class name.
  for (const className of consts.ELEMENT_CLASSES_TO_EXCLUDE) {
    if (hasClass(domNode as HTMLElement, className)) return false;
  } // excluded class, element should be excluded;
  return true;
};

/**
 * @Returns all the child elements of the parent that pass filters.
 * Includes the children of 'section' elements rather than the section elements themselves.
 * This is because mobile wikipedia burries all the paragraphs in collapsable sections.
 * @param parent - The parent element to get the children in
 */
export const getGroupingElems = (parent: HTMLElement) => {
  let outputElements: HTMLElement[] = [];
  for (let i = 0, len = parent.childNodes.length; i < len; i++) {
    const childNode = parent.childNodes[i];
    if (elementPassesFilters(childNode)) {
      if ((childNode as HTMLElement).tagName.toLowerCase() === 'section') {
        outputElements = outputElements.concat(
          getGroupingElems(childNode as HTMLElement)
        );
      } else outputElements.push(childNode as HTMLElement);
    }
  }
  return outputElements;
};
