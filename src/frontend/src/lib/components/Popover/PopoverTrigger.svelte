<script lang="ts">
    import { getContext } from 'svelte';
    import type { CustomPopoverStore } from './types';
    import { getParentStore } from '$lib/utilities';

    const popoverStore: CustomPopoverStore = getParentStore() as CustomPopoverStore;

    function handleClick(): void {
        popoverStore.toggle();
    }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div id="trigger" class="popover__trigger" on:click={handleClick}>
    <slot name="custom-trigger"></slot>
</div>

<style lang="scss">
    .popover__trigger {
        cursor: pointer;
        width: fit-content;
    }
</style>
