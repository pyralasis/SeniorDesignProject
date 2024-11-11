import { writable } from 'svelte/store';
import type { CustomTabsStore } from './types';

export const createTabsStore = (
    activeTabIndex: number
): CustomTabsStore => {
    const { subscribe, set, update } = writable({
        activeTabIndex: activeTabIndex,
    });

    const updateActiveTabIndex = (newActiveTab: number) => update((store) => ({ ...store, activeTabIndex: newActiveTab }));

    return {
        subscribe,
        set,
        update,
        updateActiveTabIndex,
    };
}