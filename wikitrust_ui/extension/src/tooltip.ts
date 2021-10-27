// I moved the styles that were here to the wikiTrustStyles.css styleSheet
let tooltip: HTMLElement;
let tooltip_base_content =
  '<div class="tooltip-gradient"><div id="Gradient_Indicator_Line"></div></div>';

/**
 * Injects the tooltip element (div) at the end of the body of the wikipedia page.
 */
const injectTooltip = () => {
  tooltip = document.createElement('div');
  tooltip.classList.add('wt-tooltip');
  window.document.body.appendChild(tooltip);
  console.log('Tooltip injected: ', tooltip);
};

/**
 * Show the info tooltip at a given position with some html content.
 * @param x - The x position of the tooltip element (page absolute position)
 * @param y - The y position of the tooltip element
 * @param content - The html content to put in the tooltip
 */
const showTooltip = (x: number, y: number, content: string) => {
  tooltip.innerHTML = tooltip_base_content + content;
  tooltip.style.left = x + 'px';
  tooltip.style.top = y + 'px';
  tooltip.style.visibility = 'visible';
};

/**
 * Show the info tooltip pointing at the target element with some html content.
 * @param targetElem - The element you want the tooltip to point at
 * @param content - The html content to put in the tooltip
 */
const showTooltipAtElement = (targetElem: HTMLElement, content: string) => {
  if (!tooltip || !targetElem) return;
  const rect = targetElem.getBoundingClientRect();
  const height = rect.bottom - rect.top;
  const left = rect.left + window.pageXOffset - tooltip.clientWidth - 8;
  const top =
    rect.top + window.pageYOffset + height / 2 - tooltip.clientHeight / 2;
  showTooltip(left, top, content);
};

/** Hide the info tooltip */
const hideTooltip = () => {
  tooltip.style.visibility = 'hidden';
};

export { injectTooltip, showTooltipAtElement, showTooltip, hideTooltip };
