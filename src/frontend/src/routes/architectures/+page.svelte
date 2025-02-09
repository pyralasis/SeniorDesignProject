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
    <div class="select-architecture-page__header">
        <h1>Select Architecture</h1>
        <p>Select the architecture you would like to edit, delete, or convert to a model or start from scratch with a new architecture</p>
        <p></p>
        {#if $selectedItemId !== ''}
            <div class="select-architecture-page__architecture-actions">
                <div class="left-actions">
                    <Button type="primary" style={StylingUtility.whiteBorderButton} href="/architectures/edit/{$selectedItemId}"
                        >Edit Architecture</Button
                    >
                    <Button type="primary" style={StylingUtility.whiteBorderButton}>Convert to Model</Button>
                    <Button type="primary" style={StylingUtility.redButton} on:click={() => handleDeleteArchitecture($selectedItemId)}
                        ><Icon name="trash" /></Button
                    >
                </div>
            </div>
        {/if}

        {#if $selectedItemId === '' && !$creatingNewArchitecture}
            <div class="select-architecture-page__architecture-actions">
                <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={() => creatingNewArchitecture.set(true)}
                    >Create New Architecture</Button
                >
            </div>
        {:else if $selectedItemId === '' && $creatingNewArchitecture}
            <div class="select-architecture-page__create-new-architecture-actions">
                <TextInput label="Architecture Name" style={StylingUtility.textInput} bind:value={newArchitectureName}></TextInput>
            </div>
            <div class="select-architecture-page__create-new-architecture-actions-buttons">
                <Button type="primary" style={StylingUtility.redButton} on:click={() => creatingNewArchitecture.set(false)}>Cancel</Button>
                <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={() => handleCreateNewArchitecture()}
                    >Create</Button
                >
            </div>
        {/if}
    </div>

    <div class="select-architecture-page__panels">
        <div class="select-architecture-page__architecture-items">
            {#if $architectureStore.availableArchitectures === undefined}
                <div class="spinner">
                    <Spinner></Spinner>
                </div>
            {:else if $architectureStore.availableArchitectures.length === 0}
                <p class="no-architectures-found">No architectures found</p>
            {:else}
                {#each $architectureStore.availableArchitectures as a, i}
                    <ArchitectureMenuItem title={a.meta.name} id={a.id}></ArchitectureMenuItem>
                {/each}
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    .select-architecture-page {
        display: flex;
        justify-content: start;
        overflow: hidden;
        height: 100%;

        &__header {
            display: flex;
            flex-direction: column;
            color: #ffffff;
            padding: 64px;
            width: 40%;
            gap: 16px;
        }

        &__panels {
            width: 50%;
            border-left: 1px solid #ffffff;
        }

        &__architecture-items {
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 64px 32px;
        }

        &__architecture-actions {
            display: flex;
            gap: 16px;
            justify-content: space-between;
        }

        &__create-new-architecture-actions {
            justify-content: space-between;
            width: 100%;
            box-sizing: border-box;
        }

        &__create-new-architecture-actions-buttons {
            display: flex;
            gap: 16px;
        }
    }

    .left-actions {
        display: flex;
        gap: 16px;
    }

    .delete-action {
        display: flex;
        gap: 16px;
    }

    .no-architectures-found {
        color: #d1d1d1ae;
        font-size: 16px;
        font-weight: 400;
        width: 100%;
        text-align: center;
    }

    .spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }

    h1 {
        font-size: 64px;
        font-weight: 500;
    }

    p {
        font-size: 18px;
        font-weight: 400;
    }

    h1,
    p {
        margin: 0;
    }
</style>
