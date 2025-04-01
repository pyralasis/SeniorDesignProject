<script lang="ts">
    // @ts-nocheck

    import { StylingUtility } from '$lib/utilities/styling.utility';

    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { Button, Popover, PopoverChipTrigger, PopoverSingleSelectContent, TextInput, type PopoverItem } from 'kiwi-nl';
    import { modelStore } from '$lib/stores/ModelStore';
    import { onMount, setContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import type { AvailableModel } from '$lib/stores/types/models-store.interface';
    import MenuItem from '$lib/components/General/MenuItem.svelte';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { pipelineStore } from '$lib/stores/PipelineStore';

    let selectedModel: Writable<AvailableModel | undefined> = writable(undefined);

    setContext('selected-item', selectedModel);

    let optimizerItems: PopoverItem[] = $derived($modelStore.availableOptimizers?.map((x) => ({ label: x.name, value: x })));

    let lossItems: PopoverItem[] = $derived($modelStore.availableLosses?.map((x) => ({ label: x.name, value: x })));

    let sources: PopoverItem[] = $derived($pipelineStore.availablePipelines?.map((x) => ({ label: x.meta.name, value: x.id })));

    let selectedOptimizerItem: PopoverItem[] = [];

    function handleOptimizerPopoverItemChanged(event: CustomEvent): void {
        selectedOptimizerItem = event.detail.selectedItems;
    }

    let selectedLossItem: PopoverItem[] = [];

    function handleLossPopoverItemChanged(event: CustomEvent): void {
        selectedLossItem = event.detail.selectedItems;
    }

    let selectedSourceItem: PopoverItem[] = [];

    function handleSourcePopoverItemChanged(event: CustomEvent): void {
        selectedSourceItem = event.detail.selectedItems;
    }

    let epochs_value = $state(10);
    let batch_value = $state(16);
    let learning_value = $state(0.001);

    onMount(() => {
        modelStore.getAvailableModels();
        pipelineStore.getAvailablePipelines();
        modelStore.getAvailableOptimizers();
        modelStore.getAvailableLosses();
    });
</script>

<div class="model-page">
    <div class="model-page__header">
        <h1>Select Model</h1>
    </div>
    <div class="model-page__top">
        <div class="model-page__top-left">
            <p>Create a model from an existing architecture on the Architectures Page! (FIND A BETTER SPOT FOR THIS MESSAGE)</p>
            <p>Select the model you would like to...</p>
        </div>
        <div class="model-page__top-right">
            <div class="model-model-items">
                {#if $modelStore.availableModels === undefined}
                    <div class="spinner">
                        <Spinner></Spinner>
                    </div>
                {:else if $modelStore.availableModels.length === 0}
                    <p class="no-models-found">No models found</p>
                {:else}
                    <div class="model-page__items-header">
                        <p>Name</p>
                        <p>Last Modified</p>
                    </div>
                    {#each $modelStore.availableModels as p, i}
                        <MenuItem item={p}></MenuItem>
                    {/each}
                {/if}
            </div>
        </div>
    </div>

    <div class="model-page__bottom">
        <div class="model-page__bottom-left">
            {#if $selectedModel}
                <div class="model-page__bottom-left-model-info">
                    <h2>{$selectedModel.meta.name}</h2>
                    <p>{$selectedModel.meta.description}</p>
                </div>
            {:else}
                <div class="model-page__bottom-left-empty">
                    <p>No model selected</p>
                </div>
            {/if}
        </div>
        <div class="model-page__bottom-right">
            {#if $selectedModel}
                <TextInput label="Training Epochs" bind:value={epochs_value} />
                <TextInput label="Batch Size" bind:value={batch_value} />
                <TextInput label="Learning Rate" bind:value={learning_value} />
                <div class="popovers">
                    <Popover on:popoverItemsChanged={handleOptimizerPopoverItemChanged} items={optimizerItems}>
                        <PopoverChipTrigger slot="trigger" label="Optimizers" style={StylingUtility.popoverChipTrigger} />
                        <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                    </Popover>

                    <Popover on:popoverItemsChanged={handleLossPopoverItemChanged} items={lossItems}>
                        <PopoverChipTrigger slot="trigger" label="Loss Functions" style={StylingUtility.popoverChipTrigger} />
                        <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                    </Popover>
                    <Popover on:popoverItemsChanged={handleSourcePopoverItemChanged} items={sources}>
                        <PopoverChipTrigger slot="trigger" label="Data Sources" style={StylingUtility.popoverChipTrigger} />
                        <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                    </Popover>
                </div>
                <Button
                    type="primary"
                    on:click={() => {
                        modelStore.trainModel(
                            $selectedModel.id,
                            selectedSourceItem[0].value,
                            learning_value,
                            { id: selectedLossItem[0].value.id, param_values: selectedLossItem[0].value.parameters },
                            { id: selectedOptimizerItem[0].value.id, param_values: selectedOptimizerItem[0].value.parameters },
                            batch_value,
                            true,
                            epochs_value,
                        );
                    }}>Train</Button
                >
                <Button
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if ($selectedModel) {
                            console.log('hello');
                        }
                    }}><Icon name="trash" /></Button
                >
            {/if}
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
        box-sizing: border-box;
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

    .popovers {
        display: flex;
        gap: 10px;
    }
    .no-pipeline-found {
        color: #c2c2c2;
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
