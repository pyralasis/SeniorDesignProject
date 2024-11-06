export interface AccordionStore {
    isOpen: boolean;
    subscribe: (run: (value: { isOpen: boolean }) => void) => () => void;
    open: () => void;
    close: () => void;
    toggle: () => void;
}