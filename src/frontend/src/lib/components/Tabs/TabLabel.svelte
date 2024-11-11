<script lang="ts">
    import Text from '$lib/components/Text/Text.svelte';
    import type { CustomTabsStore } from './types';
    import { getParentStore } from '$lib/utilities/store-utilities';
    import { TextColorEnum } from '../Text';

    // -----------------------
    // External Properties
    // -----------------------
    export let tabnum: number;

    // -----------------------
    // Internal Properties
    // -----------------------
    const tabsStore: CustomTabsStore = getParentStore() as CustomTabsStore;
    let active: boolean;
    let activeTabIndex: number;

    tabsStore.subscribe((value) => {
        active = value.activeTabIndex === tabnum;
        activeTabIndex = value.activeTabIndex ?? -1;
    });

    // -----------------------
    // Internal Methods
    // -----------------------
    function handleTabClick(tabnum: number): void {
        tabsStore.updateActiveTabIndex(tabnum);
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="tab-label" class:tab-label--active={active} on:click={() => handleTabClick(tabnum)}>
    <Text color={TextColorEnum.primary}>
        <slot></slot>
    </Text>
    <div class="tab-label__indicator" class:tab-label__indicator--active={active}></div>
</div>

<style lang="scss">
    .tab-label {
        padding: 12px 16px;
        cursor: pointer;
        user-select: none;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;

        .tab-label__indicator {
            height: 4px;
            width: 24px;
            border-radius: 8px;
            transition: all 0.3s ease;
            position: absolute;
            bottom: 2px;
            &--active {
                background-color: var(--color-primary);
            }
        }

        &:hover {
            background-color: var(--color-interactable-secondary-hover);
        }

        &--active {
            background-color: var(--color-surface);
            font-weight: 600;

            &:hover {
                background-color: var(--color-surface);
            }
        }
    }
</style>
