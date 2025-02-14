<script lang="ts">
    import type { AvailableArchitecture } from '$lib/stores/types/architecture-store.interface';
    import { FunUtilities } from '$lib/utilities/fun.utilities';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import { getContext, onMount } from 'svelte';
    import type { Writable } from 'svelte/store';

    export let item: AvailableArchitecture;

    const selectedItem = getContext<Writable<AvailableArchitecture | undefined>>('selected-item');

    let isSelected = false;
    let titleElement: HTMLElement;

    function handleClick() {
        if (isSelected) {
            selectedItem.set(undefined);
            SoundUtility.playClick1(0.1);
            return;
        }
        SoundUtility.playClick2(0.1);

        selectedItem.set(item);
    }

    $: isSelected = $selectedItem === item;
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<!-- svelte-ignore a11y_click_events_have_key_events -->

<div class="menu-item" on:click={handleClick} class:selected={isSelected}>
    <div class="menu-item__title" bind:this={titleElement}>
        {item.meta.name}
    </div>
    <div class="menu-item__separator"></div>
    <div class="menu-item__last-modified">
        {new Date(item.meta.lastModified ?? item.meta.createdAt ?? '').toLocaleDateString('en-US', {
            year: '2-digit',
            month: 'numeric',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        })}
    </div>
</div>

<style lang="scss">
    .menu-item {
        width: 100%;
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        white-space: nowrap;

        &__title {
            background-color: #111;
            padding: 4px 8px;
        }

        &__last-modified {
            background-color: #111;
            padding: 4px 8px;
        }

        &__separator {
            width: 100%;
            height: 1px;
            border-top: 2px dashed #fff;
        }

        &:hover:not(.selected) {
            font-weight: 600;
            transition: transform 0.1s ease-in-out;

            .menu-item__separator {
                border-top: 3px dashed #fff;
            }
        }

        &.selected {
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            z-index: 1;
            color: #fe2e00;

            .menu-item__separator {
                border-top: 2px dashed #fe2e00;
            }
        }
    }
</style>
