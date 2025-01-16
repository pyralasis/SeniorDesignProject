import { createPopper, type Instance } from '@popperjs/core';
import type { PopoverPosition } from '../types';

export class PopoverUtilities {

    static getTriggerElement(popoverElement: HTMLElement): HTMLElement {
        return popoverElement.querySelector('#trigger') as HTMLElement;
    }

    static getContentElement(popoverElement: HTMLElement): HTMLElement{
        return popoverElement.querySelector('#content') as HTMLElement;
    }

    static createPopperInstance(popoverElement: HTMLElement, position: PopoverPosition): Instance {
        const triggerElement: HTMLElement = this.getTriggerElement(popoverElement);
        const contentElement: HTMLElement = this.getContentElement(popoverElement);
        return createPopper(triggerElement, contentElement, {
            placement: position,
            modifiers: [
                {
                    name: 'offset',
                    options: {
                        offset: [0, 4], // Adjust this value to bring the popover closer to the trigger
                    },
                },
                {
                    name: 'preventOverflow',
                    options: {
                        padding: 8,
                    },
                },
            ],
        }) as Instance;
    }
}