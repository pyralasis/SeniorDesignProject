<script lang="ts">
    import ArchitectureMenuItem from '$lib/components/General/ArchitectureMenuItem.svelte';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    import type { AvailableArchitecture } from '$lib/stores/types/architecture-store.interface';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import { Button, TextInput } from 'kiwi-nl';
    import { setContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';

    architectureStore.getAvailableArchitectures();

    let selectedItemId: Writable<string> = writable('');
    let creatingNewArchitecture: Writable<boolean> = writable(false);
    let newArchitectureName: string = '';

    setContext('selected-item-id', selectedItemId);

    function handleCreateNewArchitecture(): void {
        architectureStore.createNewArchitecture(newArchitectureName);
        creatingNewArchitecture.set(false);
    }

    function handleDeleteArchitecture(id: string): void {
        architectureStore.deleteArchitecture(id);
        selectedItemId.set('');
    }

    $: $selectedItemId === '' && creatingNewArchitecture.set(false);
</script>

<div class="select-architecture-page">
    <div class="select-architecture-page__top">
        <div class="select-architecture-page__top-left">
            <p>
                Select the architecture you would like to edit, delete, or convert to a model or start from scratch with a new architecture
            </p>
            <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={() => creatingNewArchitecture.set(true)}
                >Create New Architecture</Button
            >
        </div>
        <div class="select-architecture-page__top-right">
            <div class="select-architecture-page__architecture-items">
                {#if $architectureStore.availableArchitectures === undefined}
                    <div class="spinner">
                        <Spinner></Spinner>
                    </div>
                {:else if $architectureStore.availableArchitectures.length === 0}
                    <p class="no-architectures-found">No architectures found</p>
                {:else}
                    {#each $architectureStore.availableArchitectures as a, i}
                        <ArchitectureMenuItem title={a.meta.name} id={a.id} lastModified={a.meta?.lastModified ?? a.meta?.createdAt ?? ''}
                        ></ArchitectureMenuItem>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
    <div class="select-architecture-page__bottom">
        <div class="select-architecture-page__bottom-left"></div>
        <div class="select-architecture-page__bottom-right">
            <Button type="primary" style={StylingUtility.whiteBorderButton} href="/architectures/edit/{$selectedItemId}"
                >Edit Architecture</Button
            >
            <Button type="primary" style={StylingUtility.whiteBorderButton}>Convert to Model</Button>
            <Button type="primary" style={StylingUtility.redButton} on:click={() => handleDeleteArchitecture($selectedItemId)}
                ><Icon name="trash" /></Button
            >
        </div>
    </div>
    <div class="select-architecture-page__header">
        {#if $selectedItemId !== ''}
            <div class="select-architecture-page__architecture-actions">
                <div class="left-actions"></div>
            </div>
        {/if}

        {#if $selectedItemId === '' && !$creatingNewArchitecture}
            <div class="select-architecture-page__architecture-actions"></div>
        {:else if $selectedItemId === '' && $creatingNewArchitecture}
            <div class="select-architecture-page__create-new-architecture-actions">
                <TextInput label="Architecture Name" style={StylingUtility.textInput} bind:value={newArchitectureName}></TextInput>
            </div>
            <div class="select-architecture-page__create-new-architecture-actions-buttons">
                <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={() => handleCreateNewArchitecture()}
                    >Create</Button
                >
                <Button type="primary" style={StylingUtility.redButton} on:click={() => creatingNewArchitecture.set(false)}>Cancel</Button>
            </div>
        {/if}
    </div>

    <div class="select-architecture-page__panels"></div>
</div>

<style lang="scss">
    .select-architecture-page {
        display: flex;
        flex-direction: column;
        justify-content: start;
        overflow: hidden;
        height: 100%;

        &__top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 75%;
        }

        &__bottom {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #ffffff;
        }

        &__top-left {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 50%;
        }

        &__top-right {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 50%;
        }
    }
</style>
