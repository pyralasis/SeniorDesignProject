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

{#if active}
    <div class="tab-content">
        <slot></slot>
    </div>
{/if}

<style lang="scss">
    .tab-content {
        width: auto;
        height: auto;
    }
</style>
