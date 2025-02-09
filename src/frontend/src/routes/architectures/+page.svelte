<script lang="ts">
    import ArchitectureMenuItem from '$lib/components/General/ArchitectureMenuItem.svelte';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import { Button } from 'kiwi-nl';
    import { setContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';

    architectureStore.getAvailableArchitectures();

    let selectedItemId: Writable<string> = writable('');
    $: availableArchitectures = $architectureStore.availableArchitectures;

    setContext('selected-item-id', selectedItemId);

    function handleCreateNewArchitecture(): void {
        architectureStore.createNewArchitecture('New Architecture');
    }
</script>

<div class="select-architecture-page">
    <div class="select-architecture-page__header">
        <h1>Select Architecture</h1>
        <p>Select the architecture you would like to edit, delete, or convert to a model</p>
        <p>Or start from scratch with a new architecture</p>
    </div>
    <div class="select-architecture-page__panels">
        <div class="select-architecture-page__architecture-items">
            {#each availableArchitectures as a}
                <ArchitectureMenuItem title={a.meta.name} id={a.id}></ArchitectureMenuItem>
            {/each}
        </div>

        {#if $selectedItemId !== ''}
            <div class="select-architecture-page__architecture-actions">
                <div class="left-actions">
                    <Button type="primary" style={StylingUtility.whiteBorderButton} href="/architectures/edit/{$selectedItemId}"
                        >Edit Architecture</Button
                    >
                    <Button type="primary" style={StylingUtility.whiteBorderButton}>Convert to Model</Button>
                </div>
                <div class="delete-action"><Button type="primary" style={StylingUtility.redButton}>Delete Architecture</Button></div>
            </div>
        {/if}
        {#if $selectedItemId === ''}
            <div class="select-architecture-page__architecture-actions">
                <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={handleCreateNewArchitecture}
                    >Create New Architecture</Button
                >
            </div>
        {/if}
    </div>
</div>

<style lang="scss">
    .select-architecture-page {
        display: flex;
        flex-direction: column;
        height: 100vh;
        align-items: center;
        overflow: hidden;

        &__header {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #ffffff;
            padding: 24px 0;
        }

        &__panels {
            max-width: 1000px;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        &__architecture-items {
            display: flex;
            flex-direction: column;
            max-height: calc(50px * 10);
            overflow-y: auto;
            overflow-x: hidden;
            padding: 32px 32px;
            box-shadow:
                inset 0px -100px 20px rgba(0, 0, 0, 0.4),
                inset 0px 100px 20px rgba(0, 0, 0, 0.4);
        }

        &__architecture-actions {
            display: flex;
            gap: 16px;
            justify-content: space-between;
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

    p,
    h1 {
        margin: 4px;
    }
</style>
