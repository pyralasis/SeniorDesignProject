<script lang="ts">
    import { getParentStore } from '$lib/utilities';
    import type { CustomTabsStore } from './types';

    // -----------------------
    // External Properties
    // -----------------------
    export let tabnum: number;

    // -----------------------
    // Internal Properties
    // -----------------------
    const tabsStore: CustomTabsStore = getParentStore() as CustomTabsStore;
    let active: boolean;
    tabsStore.subscribe((value) => {
        active = value.activeTabIndex === tabnum;
    });
</script>

<div class="tab-content" class:tab-content--active={active}>
    <slot></slot>
</div>

<style lang="scss">
    .tab-content {
        width: auto;
        height: auto;
        display: none;

        &--active {
            display: block;
        }
    }
</style>
