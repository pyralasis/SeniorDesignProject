import { writable } from 'svelte/store';

export const createTabsStore = (activeTab) => {
    const { subscribe, set, update } = writable({
        activeTab: activeTab,
    });

    return {
        subscribe,
        set,
        update,
        setActiveTab: (activeTab) => update((store) => ({ ...store, activeTab })),
    };
}