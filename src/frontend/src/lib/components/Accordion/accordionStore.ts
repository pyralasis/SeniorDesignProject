import { writable } from 'svelte/store';
import type { AccordionStore } from './types';

export const createAccordionStore = (): AccordionStore => {
    const { subscribe, set, update } = writable({
        isOpen: false,
    });

    return {
        subscribe,
        open: () => update(store => ({ ...store, isOpen: true })),
        close: () => update(store => ({ ...store, isOpen: false })),
        toggle: () => update(store => ({ ...store, isOpen: !store.isOpen })),
        isOpen: false,
    };
}

