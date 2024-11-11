import { type Writable } from "svelte/store";

export interface FlyoutStoreProps {
    open?: boolean;
    hideBackground?: boolean;
}

export interface CustomFlyoutStore extends Writable<FlyoutStoreProps> {
    toggle: () => void;
    expand: () => void;
    close: () => void;
    updateHideBackground: (hideBackground: boolean) => void;
}