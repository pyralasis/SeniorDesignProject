<script lang="ts">
    import { goto } from '$app/navigation';
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

    let selectedArchitecture: Writable<AvailableArchitecture | undefined> = writable(undefined);
    let creatingNewArchitecture: Writable<boolean> = writable(false);
    let newArchitectureName: string = '';
    let newArchitectureDescription: string = '';

    setContext('selected-item', selectedArchitecture);

    async function handleCreateNewArchitecture(): Promise<void> {
        await architectureStore.createNewArchitecture(newArchitectureName, newArchitectureDescription);
        creatingNewArchitecture.set(false);
    }

    function handleDeleteArchitecture(id: string): void {
        architectureStore.deleteArchitecture(id);
        selectedArchitecture.set(undefined);
    }

    function handleCreateNewArchitectureInitialisation(): void {
        console.log($creatingNewArchitecture);
        selectedArchitecture.set(undefined);
        newArchitectureName = '';
        newArchitectureDescription = '';
        creatingNewArchitecture.set(true);
    }
</script>

<div class="select-architecture-page">
    <div class="select-architecture-page__header">
        <h1>Select Architecture</h1>
    </div>
    <div class="select-architecture-page__top">
        <div class="select-architecture-page__top-left">
            <p>
                Select the architecture you would like to edit, delete, or convert to a model or start from scratch with a new architecture
            </p>
            <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={handleCreateNewArchitectureInitialisation}
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
                        <ArchitectureMenuItem item={a}></ArchitectureMenuItem>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
    <div class="select-architecture-page__bottom">
        <div class="select-architecture-page__bottom-left">
            {#if $selectedArchitecture}
                <div class="select-architecture-page__bottom-left-architecture-info">
                    <h2>{$selectedArchitecture.meta.name}</h2>
                    <p>{$selectedArchitecture.meta.description}</p>
                </div>
            {:else if $creatingNewArchitecture}
                <div class="select-architecture-page__create-new-architecture-actions">
                    <div class="name-input">
                        <TextInput label="Name" style={StylingUtility.textInput} bind:value={newArchitectureName}></TextInput>
                    </div>
                    <div class="description-input">
                        <TextInput label="Description" style={StylingUtility.textInput} bind:value={newArchitectureDescription}></TextInput>
                    </div>
                </div>
                <div class="select-architecture-page__create-new-architecture-actions-buttons">
                    <Button
                        type="primary"
                        style={StylingUtility.whiteBorderButton}
                        on:click={async () => await handleCreateNewArchitecture()}>Create</Button
                    >
                    <Button type="primary" style={StylingUtility.redButton} on:click={() => creatingNewArchitecture.set(false)}
                        >Cancel</Button
                    >
                </div>
            {:else}
                <div class="select-architecture-page__bottom-left-empty">
                    <p>No architecture selected</p>
                </div>
            {/if}
        </div>
        <div class="select-architecture-page__bottom-right">
            {#if $selectedArchitecture}
                <Button type="primary" style={StylingUtility.whiteBorderButton} href="/architectures/edit/{$selectedArchitecture?.id}"
                    >Open In Node Editor</Button
                >
                <Button type="primary" style={StylingUtility.whiteBorderButton}>Convert to Model</Button>
                <Button
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if ($selectedArchitecture) {
                            handleDeleteArchitecture($selectedArchitecture.id);
                        }
                    }}><Icon name="trash" /></Button
                >
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    .select-architecture-page {
        display: flex;
        flex-direction: column;
        justify-content: start;
        overflow: hidden;
        height: 100%;
        color: #ffffff;

        &__header {
            color: #ffffff;
            border-bottom: 1px solid #ffffff;
            padding: 20px;
            padding-left: 64px;
            h1 {
                font-size: 50px;
                font-weight: 500;
                margin: 0;
            }
        }

        &__top {
            display: flex;
            justify-content: space-between;
            height: 75%;
            max-width: 1500px;
            margin: 64px auto;
        }

        &__bottom {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #ffffff;
            padding: 32px 64px;
            height: 35%;
        }

        &__bottom-left {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 65%;
        }

        &__bottom-right {
            display: flex;
            gap: 10px;
            max-width: 60%;
            height: 38px;
        }

        &__bottom-left-architecture-info {
            display: flex;
            flex-direction: column;
            gap: 10px;

            h2 {
                font-size: 24px;
                font-weight: 600;
                margin: 0;
            }
        }

        &__top-left {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 30%;

            p {
                color: #ffffff;
            }
        }

        &__bottom-left-empty {
            color: #c2c2c2;
        }

        &__top-right {
            width: 700px;
        }

        &__create-new-architecture-actions-buttons {
            display: flex;
            gap: 10px;
        }

        &__create-new-architecture-actions {
            display: flex;
            gap: 10px;
        }
    }

    .no-architectures-found {
        color: #c2c2c2;
    }

    .name-input {
        width: 20%;
    }

    .description-input {
        width: 80%;
    }
</style>
