interface WikiTrustGlobalVars {
  completionStage: number;
  trustVisible: boolean;
  styleElm?: HTMLElement;
  uiFrameContainer?: HTMLElement;
}

declare global {
  interface Window {
    WikiTrustGlobalVars: WikiTrustGlobalVars;
    RLCONF: { // some metadata object wikipedia's js puts in the global scope
      wgCurRevisionId: Number, // the latest? rev id
      wgRevisionId: Number, // the rev id of the page we're looking at
      wgArticleId: Number, // the page id
    }
  }
}

export interface PageMetaData {
  revId: Number,
  pageId: Number
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
