import { writable } from 'svelte/store';

export const createPopoverStore = () => {
    const { subscribe, set, update } = writable({
        isOpen: false,
        // items: [{value, label}]
        selectedItems: []
    });


    return {
        subscribe,
        open: () => update(store => ({ ...store, isOpen: true })),
        close: () => update(store => ({ ...store, isOpen: false })),
        toggle: () => update(store => ({ ...store, isOpen: !store.isOpen })),
        updateItems: (items) => update(store => ({ ...store, selectedItems: items })),
    };
}