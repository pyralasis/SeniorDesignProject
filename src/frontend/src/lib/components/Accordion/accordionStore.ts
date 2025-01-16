import { writable } from 'svelte/store';
import type { AccordionStoreProps, CustomAccordionStore } from './types';

export const createAccordionStore = (
    open: boolean = false,
): CustomAccordionStore => {
    const { subscribe, set, update } = writable<AccordionStoreProps>({
        open: open,
    });

    const expand = () => update(store => ({ ...store, open: true }));

    const close = () => update(store => ({ ...store, open: false }));

    const toggle = () => update(store => ({ ...store, open: !store.open }));


    return {
        subscribe,
        set,
        update,
        expand,
        close,
        toggle
    };
}

