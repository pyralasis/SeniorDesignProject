<script lang="ts">
    import { FunUtilities } from '$lib/utilities/fun.utilities';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import { getContext, onMount } from 'svelte';
    import type { Writable } from 'svelte/store';

    export let title;
    export let id: string;

    const selectedItemId = getContext<Writable<string>>('selected-item-id');

    let isSelected = false;
    let titleElement: HTMLElement;

    function handleClick() {
        if (isSelected) {
            selectedItemId.set('');
            SoundUtility.playClick1(0.1);
            return;
        }
        SoundUtility.playClick2(0.1);

        selectedItemId.set(id);
    }

    $: isSelected = $selectedItemId === id;
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->

<div class="architecture-menu-item" on:click={handleClick} class:selected={isSelected}>
    <div class="architecture-menu-item-title" bind:this={titleElement}>
        {title}
    </div>
</div>

<style>
    .architecture-menu-item {
        width: 100%;
        min-height: 50px;
        background-color: #000;
        border: 1px solid #fff;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;

        &:hover:not(.selected) {
            transform: scale(1.03);
            transition: transform 0.1s ease-in-out;
        }

        &.selected {
            border: 1px solid #fe2e00;
            color: #fe2e00;
            transform: scale(1.03);
            transition: all 0.2s ease-in-out;
            z-index: 1;
        }
    }
</style>
