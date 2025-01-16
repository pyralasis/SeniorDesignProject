import type { Writable } from 'svelte/store';

export interface AccordionStoreProps {
    open?: boolean;
}

export interface CustomAccordionStore extends Writable<AccordionStoreProps> {
    expand: () => void;
    close: () => void;
    toggle: () => void;
}