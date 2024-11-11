<script lang="ts">
    import PopoverContent from '../PopoverContent.svelte';
    import type { CustomPopoverStore, PopoverItem } from '../types';
    import { getParentStore } from '$lib/utilities';
    import { Text, TextColorEnum } from '$lib/components';
    import { createEventDispatcher } from 'svelte';

    // -----------------------
    // Internal Properties
    // -----------------------
    const popoverStore: CustomPopoverStore = getParentStore() as CustomPopoverStore;
    let items: PopoverItem[];
    let selectedItems: PopoverItem[];

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleItemClicked(item: PopoverItem): void {
        if (selectedItems) {
            const label = item.label;
            const value = item.value;
            if (!selectedItems.includes(item)) {
                popoverStore.updateSelectedItems([{ value, label }]);
            } else {
                popoverStore.updateSelectedItems([]);
            }
        }
        popoverStore.close();
    }

    function isItemSelected(item: PopoverItem): boolean {
        return selectedItems.some((selectedItem) => selectedItem.value === item.value);
    }

    // -----------------------
    // Reactive Lifecycle
    // -----------------------
    $: items = $popoverStore.items ?? [];
    $: selectedItems = $popoverStore.selectedItems ?? [];
</script>

<PopoverContent>
    <div slot="custom-content" class="single-select-content">
        {#each items as item}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div
                class="single-select-content__item"
                class:single-select-content__item--selected={isItemSelected(item)}
                on:click={() => handleItemClicked(item)}
            >
                <Text color={isItemSelected(item) ? TextColorEnum.secondary : TextColorEnum.primary}>{item.label}</Text>
            </div>
        {/each}
    </div>
</PopoverContent>

<style lang="scss">
    .single-select-content {
        display: flex;
        flex-direction: column;
        width: 200px;
        gap: var(--size-xs);

        &__item {
            width: auto;
            padding: var(--size-xs) var(--size-md) var(--size-xs) var(--size-md);
            cursor: pointer;
            border-radius: var(--size-sm);
            transition: all 0.2s ease;

            &:hover {
                background-color: var(--color-primary-light);
            }

            &--selected {
                background-color: var(--color-primary-light);

                &:hover {
                    background-color: var(--color-primary);
                }
            }
        }

        &__selected-indicator {
            width: var(--size-sm);
            height: var(--size-sm);
            border-radius: 50%;
            background-color: transparent;
            margin-right: var(--size-xs);
            display: flex;
            align-items: center;
            justify-content: center;

            &--selected {
                background-color: #f5a623;
            }
        }
    }
</style>
