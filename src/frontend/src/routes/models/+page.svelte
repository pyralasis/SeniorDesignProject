<script>
// @ts-nocheck

    import { StylingUtility } from "$lib/utilities/styling.utility";

    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { Button } from "kiwi-nl";
    import { modelStore } from "$lib/stores/ModelStore";

    modelStore.getAvailableModels();

</script>

<div class="model-page">
    <div class="model-page__header">
        <h1>Select Model</h1>
    </div>
    <div class="model-page__top">
        <div class="model-page__top-left">
            <p>
                Select the model you would like to train...
            </p>
            <Button type="primary" style={StylingUtility.whiteBorderButton} on:click={() => {}}
                >Create New Model</Button
            >
        </div>
        <div class="model-page__top-right">
            <div class="model-model-items">
                <div class="spinner">
                    <Spinner></Spinner>
                </div>
                <!-- {#if $modelStore.availableModels === undefined}
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
                {/if} -->
            </div>
        </div>
    </div>

    <div class="model-page__bottom">
        <div class="model-page__bottom-left">
            <!-- {#if $selectedPipeline}
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
            {/if} -->
            <div class="select-pipeline-page__bottom-left-empty">
                <p>No model selected</p>
            </div>
        </div>
        <div class="model-page__bottom-right">
            <!-- {#if $selectedPipeline}
                <Button type="primary" style={StylingUtility.whiteBorderButton} href="/pipelines/edit/{$selectedPipeline?.id}"
                    >Open In Node Editor</Button
                >
                <Button type="primary" style={StylingUtility.whiteBorderButton}>Convert to Model</Button>
                <Button
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if ($selectedPipeline) {
                            handleDeletePipeline($selectedPipeline.id);
                        }
                    }}><Icon name="trash" /></Button
                >
            {/if} -->
        </div>
    </div>
</div>

<style lang="scss">

    .model-page {
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

        &__bottom-left-model-info {
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

        &__create-new-model-actions-buttons {
            display: flex;
            gap: 10px;
        }

        &__create-new-model-actions {
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
</style>