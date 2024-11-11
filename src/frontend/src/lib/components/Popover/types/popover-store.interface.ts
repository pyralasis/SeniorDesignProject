import { type Writable } from 'svelte/store';
import { type PopoverItem } from './popover-item.interface';

export interface PopoverStoreProps {
    popoverElement?: HTMLElement;
    open?: boolean;
    items?: PopoverItem[];
    selectedItems?: PopoverItem[];
}

export interface CustomPopoverStore extends Writable<PopoverStoreProps> {
    toggle: () => void;
    close: () => void;
    expand: () => void;
    updatePopoverElement: (element: HTMLElement) => void;
    updateItems: (items: PopoverItem[]) => void;
    updateSelectedItems: (items: PopoverItem[]) => void;
}