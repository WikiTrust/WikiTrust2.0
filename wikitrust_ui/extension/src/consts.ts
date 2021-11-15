// dictionary of html element types to apply the word spliting / wrapping functions to and then add the newly created word elements to the wordNodes array.
export const REPLACE_WORDS_IN: { [key: string]: boolean } = {
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
  caption: true,
};

// array of html element class names exclude from the word spliting / wrapping functions.
export const ELEMENT_CLASSES_TO_EXCLUDE = [
  'reference',
  'wikitable',
  'toc',
  'infobox',
  'thumb',
  'mw-editsection',
  'navbox',
  'metadata',
  'tmbox',
  'sistersitebox',
  'portal',
  'hatnote',
  'noprint',
  'mw-headline',
  'gallery',
  'mw-empty-elt',
  'noprint',
]; // "reference" "sistersitebox" "navbox"

export enum ENVIRONMENTS {
  bookmarklet,
  firefox_extension,
  chrome_extension,
}

export enum COMPLETION_STAGES {
  just_loaded,
  base_ui_injected,
  ui_injected,
  api_sent,
  api_recived,
  page_processed,
}

// word element attribute names (for debugging)
export const SCORE_ATTRIBUTE_NAME = 'data-trust-score';
export const WORD_INDEX_ATTRIBUTE_NAME = 'data-word-index';
