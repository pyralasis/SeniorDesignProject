<script lang="ts">
    import { createTabsStore } from './TabsStore.js';
    import { setParentStoreContext } from '$lib/utilities/store-utilities.js';

    // -----------------------
    // External Properties
    // -----------------------
    export let activeTab: number;

    // -----------------------
    // Internal Properties
    // -----------------------
    const private_store = createTabsStore(activeTab);
    setParentStoreContext(private_store);
</script>

<div class="tabs">
    <div class="tabs__labels">
        <slot name="labels"></slot>
    </div>
    <div class="tabs__content">
        <slot name="contents"></slot>
    </div>
</div>

<style lang="scss">
    @import '../../../variables.css';

    .tabs {
        display: flex;
        flex-direction: column;

        &__labels {
            display: flex;

            & > * {
                flex: 1;
                text-align: center;
                padding: 8px 16px;
                cursor: pointer;
            }

            & > *:hover {
                background-color: var(--color-surface);
            }

            & > *:not(:last-child) {
                border-right: 1px solid var(--color-surface);
            }
        }

        &__content {
            padding: 16px;
        }
    }
</style>
