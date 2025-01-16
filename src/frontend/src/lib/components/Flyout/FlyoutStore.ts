import { writable } from 'svelte/store';
import type { CustomFlyoutStore } from './types';

export const createFlyoutStore = (
    open: boolean = false,
    hideBackground: boolean = false
): CustomFlyoutStore => {
    const { subscribe, set, update } = writable({ open: open, hideBackground: hideBackground });

    const toggle = () => {
        update((store) => ({ ...store, open: !store.open }));
    }

    const expand = () => {
        update((store) => ({ ...store, open: true }));
    }

    const close = () => {
        update((store) => ({ ...store, open: false }));
    }

    const updateHideBackground = (hideBackground: boolean) => {
        update((store) => ({ ...store, hideBackground }));
    }

    return {
        subscribe,
        set,
        update,
        toggle,
        expand,
        close,
        updateHideBackground,
    };
};