import { writable } from 'svelte/store';
import { type PopoverStoreProps, type CustomPopoverStore, type PopoverItem } from './types';

export const createPopoverStore = (
    items: PopoverItem[] = [],
    selectedItems: PopoverItem[] = []
): CustomPopoverStore => {
    const { subscribe, set, update } = writable<PopoverStoreProps>({
        items: items,
        selectedItems: selectedItems,
    });

    const expand = () => update(store => ({ ...store, open: true }));
    const close = () => update(store => ({ ...store, open: false }));
    const toggle = () => update(store => ({ ...store, open: !store.open }));

    const updatePopoverElement = (element: HTMLElement) => update(store => ({ ...store, popoverElement: element }));
    const updateItems = (items: PopoverItem[]) => update(store => ({ ...store, items: items }));
    const updateSelectedItems = (items: PopoverItem[]) => update(store => ({ ...store, selectedItems: items }));


    return {
        subscribe,
        set,
        update,
        expand,
        close,
        toggle,
        updatePopoverElement,
        updateItems,
        updateSelectedItems
    };
}