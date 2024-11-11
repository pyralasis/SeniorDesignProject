import type { Writable } from 'svelte/store';

export interface TabsStoreProps {
    activeTabIndex?: number;
}

export interface CustomTabsStore extends Writable<TabsStoreProps> {
    updateActiveTabIndex: (index: number) => void;
}