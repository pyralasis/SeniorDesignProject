<script lang="ts">
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import { getContext } from 'svelte';
    import type { Writable } from 'svelte/store';

    export let title;
    export let id: number;

    const selectedItemId = getContext<Writable<number>>('selected-item-id');

    let isSelected;

    function handleClick() {
        selectedItemId.set(id);
    }

    $: isSelected = $selectedItemId === id;
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->
<div class="architecture-menu-item" on:click={handleClick} on:mouseenter={() => SoundUtility.playClick2()} class:selected={isSelected}>
    <div class="architecture-menu-item-title">{title}</div>
</div>

<style>
    .architecture-menu-item {
        width: 100%;
        height: 50px;
        background-color: #000;
        border: 1px solid #fff;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;

        &:hover {
            transform: scale(1.05);
            transition: transform 0.1s ease-in-out;
        }

        &.selected {
            background-color: #fff;
            color: #000;
            scale: 1.05;
        }
    }
</style>
