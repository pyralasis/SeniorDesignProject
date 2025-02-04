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

`
} as const;
