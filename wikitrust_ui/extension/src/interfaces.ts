interface WikiTrustGlobalVars {
  completionStage: number;
  trustVisible: boolean;
  styleElm?: HTMLElement;
  uiFrameContainer?: HTMLElement;
}

declare global {
  interface Window {
    WikiTrustGlobalVars: WikiTrustGlobalVars;
  }
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
