import { IconNameEnum, type IconName } from './icon-name.enum';

export const iconNameSvgMapping: Record<IconName, string> = {
    [IconNameEnum.chevron_right]: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M7.33045 3.61282C7.66485 3.93922 10.9321 7.36882 10.9321 7.36882C11.0167 7.45053 11.0841 7.54846 11.1301 7.65677C11.1761 7.76508 11.1998 7.88154 11.1998 7.99922C11.1998 8.11689 11.1761 8.23336 11.1301 8.34167C11.0841 8.44998 11.0167 8.54791 10.9321 8.62962C10.9321 8.62962 7.66485 12.0608 7.33045 12.3856C6.99605 12.712 6.39445 12.7344 6.03845 12.3856C5.68165 12.0384 5.65365 11.5528 6.03845 11.1264L9.03605 8.00002L6.03845 4.87362C5.65365 4.44722 5.68165 3.96082 6.03845 3.61282C6.39445 3.26402 6.99605 3.28562 7.33045 3.61282Z" fill="currentColor"/>
</svg>
`,
    [IconNameEnum.plus]: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M8 3.5V12.5M3.5 8H12.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
`,
    [IconNameEnum.collapse]: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4 0V16H6V0H4ZM7 3V8V13L12 7.5L7 3Z" fill="currentColor"/>
</svg>
`,
    [IconNameEnum.sideways_hamburger]: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#clip0_130_22)">
<path d="M12.3472 0L12.3472 16L9.69454 16L9.69454 -1.17949e-07L12.3472 0ZM5.69454 -2.95809e-07L5.69454 16L2.9998 16L2.9998 -4.15631e-07L5.69454 -2.95809e-07Z" fill="currentColor"/>
</g>
<defs>
<clipPath id="clip0_130_22">
<rect width="16" height="16" fill="white"/>
</clipPath>
</defs>
</svg>
`,
    [IconNameEnum.trash]: `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M14.0279 5.16923L13.4512 15.3319C13.4326 15.7011 13.0977 16 12.707 16H3.29302C2.90233 16 2.56744 15.7011 2.54884 15.3319L1.97209 5.16923C1.95349 4.78242 2.26977 4.44835 2.67907 4.43077C3.08837 4.41319 3.44186 4.71209 3.46047 5.0989L4 14.5934H12.0186L12.5581 5.0989C12.5767 4.71209 12.9302 4.41319 13.3395 4.43077C13.7302 4.44835 14.0465 4.78242 14.0279 5.16923ZM16 2.81319C16 3.2 15.6651 3.51648 15.2558 3.51648H0.744186C0.334884 3.51648 0 3.2 0 2.81319C0 2.42637 0.334884 2.10989 0.744186 2.10989H4.83721V0.527473C4.83721 0.193407 5.07907 0 5.43256 0H10.5674C10.9209 0 11.1628 0.193407 11.1628 0.527473V2.10989H15.2558C15.6651 2.10989 16 2.42637 16 2.81319ZM6.13953 2.10989H9.86047V1.23077H6.13953V2.10989ZM6.45581 13.5385C6.82791 13.5385 7.10698 13.2044 7.10698 12.8703L6.92093 5.27473C6.92093 4.94066 6.62326 4.65934 6.25116 4.65934C5.89767 4.65934 5.6 4.94066 5.6186 5.29231L5.80465 12.9055C5.80465 13.2396 6.10233 13.5385 6.45581 13.5385ZM9.52558 13.5385C9.87907 13.5385 10.1767 13.2571 10.1767 12.9231L10.3628 5.32747C10.3628 4.99341 10.0837 4.69451 9.73023 4.69451C9.35814 4.69451 9.07907 4.95824 9.06047 5.29231L8.87442 12.8879C8.85581 13.2396 9.15349 13.5385 9.52558 13.5385C9.50698 13.5385 9.50698 13.5385 9.52558 13.5385Z" fill="currentColor"/>
</svg>

`,
} as const;

