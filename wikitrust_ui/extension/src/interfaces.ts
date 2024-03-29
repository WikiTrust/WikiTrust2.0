interface WikiTrustGlobalVars {
  completionStage: number;
  trustVisible: boolean;
  revisionIndex: number;
  maxWordScore: number;
  styleElm?: HTMLElement;
  uiFrameContainer?: HTMLElement; // yes used?
}

declare global {
  interface Window {
    WikiTrustGlobalVars: WikiTrustGlobalVars;
    RLCONF: {
      // some metadata object wikipedia's js puts in the global scope
      wgCurRevisionId: number; // the latest? rev id
      wgRevisionId: number; // the rev id of the page we're looking at
      wgArticleId: number; // the page id
    };
  }
}

export interface PageMetaData {
  revId: number;
  pageId: number;
}

export interface serverScoresResponse {
  words: string[];
  scores: number[];
  revisionIndex: number;
  error?: string;
}

interface ColorObject {
  r: number;
  g: number;
  b: number;
}

export interface GradientStop {
  percent: number;
  color: ColorObject;
}
