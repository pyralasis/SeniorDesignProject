<script lang="ts">
    import { createEventDispatcher, onMount, onDestroy } from 'svelte';
    import { type Instance } from '@popperjs/core';
    import { createPopoverStore } from './PopoverStore.js';
    import { PopoverPositionEnum, type PopoverItem, type PopoverPosition } from './types';
    import { PopoverUtilities } from './utils';
    import { setParentStoreContext } from '$lib/utilities/store-utilities.js';

    // -----------------------
    // External Properties
    // -----------------------
    export let id: string = '';
    export let items: PopoverItem[] = [];
    export let selectedItems: PopoverItem[] = [];
    export let position: PopoverPosition = PopoverPositionEnum.bottom;

    // -----------------------
    // Internal Properties
    // -----------------------
    let popoverElement: HTMLElement;
    let private_store = createPopoverStore(items, selectedItems);
    let popperInstance: Instance;

    // -----------------------
    // External Events
    // -----------------------
    setParentStoreContext(private_store);

    const dispatch = createEventDispatcher();

    const popoverOverOpenedDispatch = () => {
        dispatch('popoverOverOpened', id);
    };

    const popoverOverClosedDispatch = () => {
        dispatch('popoverOverClosed', id);
    };

    const popoverItemsChangedDispatch = () => {
        dispatch('popoverItemsChanged', { id: id, selectedItems: $private_store.selectedItems });
    };

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleClickOutside(event: MouseEvent) {
        if ($private_store.open && popoverElement && !popoverElement.contains(event.target as Node)) {
            private_store.close();
        }
    }

    // -----------------------
    // Reactive Lifecycle
    // -----------------------
    $: $private_store.selectedItems, popoverItemsChangedDispatch();
    $: {
        if ($private_store.open) {
            popoverOverOpenedDispatch();
            popperInstance?.update();
        } else {
            popoverOverClosedDispatch();
        }
    }

    // -----------------------
    // Lifecycle Hooks
    // -----------------------
    onMount(async () => {
        private_store.updatePopoverElement(popoverElement);
        if ($private_store?.popoverElement) {
            popperInstance = PopoverUtilities.createPopperInstance($private_store?.popoverElement, position);
        }
        popperInstance.update();

        window.addEventListener('click', handleClickOutside);
    });
</script>

<div class="popover" aria-haspopup="true" aria-expanded="true" bind:this={popoverElement}>
    <slot name="trigger" />
    <slot name="content" />
</div>

<style lang="scss">
    .popover {
        width: fit-content;
        position: relative;
    }
</style>
