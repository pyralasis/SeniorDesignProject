<script lang="ts">
    import MenuItem from '$lib/components/General/MenuItem.svelte';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { pipelineStore } from '$lib/stores/PipelineStore';
    import type { AvailablePipeline } from '$lib/stores/types/pipeline-store.interface';
    import type { PipelineId } from '$lib/types/pipeline';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import { Button, TextInput } from 'kiwi-nl';
    import { onMount, setContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';

    let selectedPipeline: Writable<AvailablePipeline | undefined> = writable(undefined);
    let creatingNewPipeline: Writable<boolean> = writable(false);
    let validatingDelete: Writable<boolean> = writable(false);
    let newPipelineName: string = '';
    let newPipelineDescription: string = '';

    setContext('selected-item', selectedPipeline);

    async function handleCreateNewPipeline(): Promise<void> {
        await pipelineStore.createNewPipeline(newPipelineName, newPipelineDescription);
        creatingNewPipeline.set(false);
    }

    function handleDeletePipeline(id: PipelineId): void {
        if ($validatingDelete) {
            pipelineStore.deletePipeline(id);
            selectedPipeline.set(undefined);
        } else {
            validatingDelete.set(true);
        }
    }

    function handleCreateNewPipelineInitialisation(): void {
        selectedPipeline.set(undefined);
        newPipelineName = '';
        newPipelineDescription = '';
        creatingNewPipeline.set(true);
    }

    onMount(() => {
        pipelineStore.getAvailablePipelines();

        window.addEventListener('click', (event) => {
            if (!event.target) {
                return;
            }
            if ($validatingDelete && !(event.target as Element)?.closest('.select-pipeline-page__bottom-right')) {
                validatingDelete.set(false);
            }
        });
    });
</script>

<div class="select-pipeline-page">
    <div class="select-pipeline-page__header">
        <h1>Select Pipeline</h1>
    </div>
    <div class="select-pipeline-page__top">
        <div class="select-pipeline-page__top-left">
            <p>Select the pipeline you would like to edit, delete or start from scratch with a new pipeline</p>
            <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={handleCreateNewPipelineInitialisation}
                >Create New Pipeline</Button
            >
        </div>
        <div class="select-pipeline-page__top-right">
            <div class="select-pipeline-pipeline-items">
                {#if $pipelineStore.availablePipelines === undefined}
                    <div class="spinner">
                        <Spinner></Spinner>
                    </div>
                {:else if $pipelineStore.availablePipelines.length === 0}
                    <p class="no-pipelines-found">No pipelines found</p>
                {:else}
                    <div class="select-pipeline-page__items-header">
                        <p>Name</p>
                        <p>Last Modified</p>
                    </div>
                    {#each $pipelineStore.availablePipelines as p, i}
                        <MenuItem item={p}></MenuItem>
                    {/each}
                {/if}
            </div>
        </div>
    </div>
    <div class="select-pipeline-page__bottom">
        <div class="select-pipeline-page__bottom-left">
            {#if $selectedPipeline}
                <div class="select-pipeline-page__bottom-left-pipeline-info">
                    <h2>{$selectedPipeline.meta.name}</h2>
                    <p>{$selectedPipeline.meta.description}</p>
                </div>
            {:else if $creatingNewPipeline}
                <div class="select-pipeline-page__create-new-pipeline-actions">
                    <div class="name-input">
                        <TextInput label="Name" style={StylingUtility.textInput} bind:value={newPipelineName}></TextInput>
                    </div>
                    <div class="description-input">
                        <TextInput label="Description" style={StylingUtility.textInput} bind:value={newPipelineDescription}></TextInput>
                    </div>
                </div>
                <div class="select-pipeline-page__create-new-pipeline-actions-buttons">
                    <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={async () => await handleCreateNewPipeline()}
                        >Create</Button
                    >
                    <Button type="primary" style={StylingUtility.redButton} on:click={() => creatingNewPipeline.set(false)}>Cancel</Button>
                </div>
            {:else}
                <div class="select-pipeline-page__bottom-left-empty">
                    <p>No pipeline selected</p>
                </div>
            {/if}
        </div>
        <div class="select-pipeline-page__bottom-right">
            {#if $selectedPipeline}
                <Button type="primary" style={StylingUtility.whiteBorderButton} href="/pipelines/edit/{$selectedPipeline?.id}"
                    >Open Node Editor</Button
                >
                <Button
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if ($selectedPipeline) {
                            handleDeletePipeline($selectedPipeline.id);
                        }
                    }}
                >
                    {#if $validatingDelete}
                        Click Again To Confirm
                    {:else}
                        <Icon name="trash" />
                    {/if}
                </Button>
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    .select-pipeline-page {
        display: flex;
        flex-direction: column;
        justify-content: start;
        overflow: hidden;
        height: calc(100% - 55px);
        box-sizing: border-box;
        color: #ffffff;

        &__header {
            color: #ffffff;
            border-bottom: 1px solid #ffffff;
            padding: 20px;
            padding-left: 64px;
            h1 {
                font-size: 42px;
                font-weight: 500;
                margin: 0;
            }
        }

        &__top {
            display: flex;
            justify-content: space-between;
            flex-grow: 1;
            max-width: 1500px;
            margin: 64px auto;
        }

        &__bottom {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #ffffff;
            padding: 32px 64px;
            height: 160px;
            min-height: 160px;
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

        &__bottom-left-pipeline-info {
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

        &__create-new-pipeline-actions-buttons {
            display: flex;
            gap: 10px;
        }

        &__create-new-pipeline-actions {
            display: flex;
            gap: 10px;
        }

        &__items-header {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid #ffffff;
            margin: 0 8px 10px 8px;

            p {
                font-weight: 600;
                margin: 2px 0px;
            }
        }
    }

    .name-input {
        width: 20%;
    }

    .description-input {
        width: 80%;
    }

    .spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        box-sizing: border-box;
    }
</style>
