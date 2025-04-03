<script lang="ts">
    // @ts-nocheck
    import { StylingUtility } from '$lib/utilities/styling.utility';

    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { type ButtonCustomStyling, Button, Popover, PopoverChipTrigger, PopoverSingleSelectContent, TextInput, type PopoverItem, Flyout, ButtonTypeEnum, FlyoutSideEnum } from 'kiwi-nl';
    import { modelStore } from '$lib/stores/ModelStore';
    import { onMount, setContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import type { AvailableModel } from '$lib/stores/types/models-store.interface';
    import MenuItem from '$lib/components/General/MenuItem.svelte';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { pipelineStore } from '$lib/stores/PipelineStore';
    import type { Parameter, ParameterValue } from '$lib/types/parameter';
    import NodeField from '$lib/components/Node/NodeParameter.svelte';

    let selectedModel: Writable<AvailableModel | undefined> = writable(undefined);
        
    let parameters: { parameter: Parameter<any>; value: ParameterValue<any> }[] = $state([]);

    setContext('selected-item', selectedModel);

    let optimizerItems: PopoverItem[] = $derived($modelStore.availableOptimizers?.map((x) => ({ label: x.name, value: x })));
    let lossItems: PopoverItem[] = $derived($modelStore.availableLosses?.map((x) => ({ label: x.name, value: x })));
    let sources: PopoverItem[] = $derived($pipelineStore.availablePipelines?.map((x) => ({ label: x.meta.name, value: x.id })));

    let selectedOptimizerItem: PopoverItem[] = [];

    let validatingDelete: Writable<boolean> = writable(false);

        function handleDeleteModel(){
        console.log('Delete model', $selectedModel);
        if ($validatingDelete) {
            modelStore.deleteModel($selectedModel.id);
            selectedModel.set(undefined);
            validatingDelete.set(false);
            // Refresh the models list
            modelStore.getAvailableModels();
        } else {
            validatingDelete.set(true);
        }
    }


    let selectedOptimizerItem: PopoverItem | undefined = $state(undefined);
    function handleOptimizerPopoverItemChanged(event: CustomEvent): void {
        console.log(event)
        selectedOptimizerItem = event.detail.selectedItems[0];
        if (selectedOptimizerItem) {
            parameters.length = 0;
            selectedOptimizerItem.value.parameters.forEach((x) => parameters?.push({parameter: x, value: {type: x.type, val: x.default}}))
        }
    }

    let selectedLossItem: PopoverItem | undefined = $state(undefined);
    function handleLossPopoverItemChanged(event: CustomEvent): void {
        selectedLossItem = event.detail.selectedItems[0];
        
    }

    let selectedSourceItem: PopoverItem | undefined =  $state(undefined);
    function handleSourcePopoverItemChanged(event: CustomEvent): void {
        selectedSourceItem = event.detail.selectedItems[0];
    }

    let epochs_value = $state(10);
    let batch_value = $state(16);
    let learning_value = $state(0.001);

    let flyoutElement;

    let validatingDelete: Writable<boolean> = writable(false);
    function handleDeleteArchitecture(id: string): void {
        if ($validatingDelete) {
            modelStore.deleteModel(id);
            selectedModel.set(undefined);
        } else {
            validatingDelete.set(true);
        }
    }

    let can_train = $derived(selectedOptimizerItem !== undefined && selectedLossItem !== undefined && selectedSourceItem !== undefined);
    const DISABLED_BUTTON_STYLE: ButtonCustomStyling = {
        backgroundColor: "#444",
        hover: "#444",
        cursor: "not-allowed"
    }

    onMount(() => {
        modelStore.getAvailableModels();
        pipelineStore.getAvailablePipelines();
        modelStore.getAvailableOptimizers();
        modelStore.getAvailableLosses();
        window.addEventListener('click', (event) => {
            if (!event.target) {
                return;
            }
            if ($validatingDelete && !(event.target as Element)?.closest('.model-page__bottom-right')) {
                validatingDelete.set(false);
        }
        });
    });

</script>

<div class="model-page">
    <div class="model-page__header">
        <h1>Select Model</h1>
    </div>
    <div class="model-page__top">
        <div class="model-page__top-left">
            <p>Create a model from an existing architecture on the Architectures Page!</p>
            <p>Select the model you would like to Train!</p>
        </div>
        <div class="model-page__top-right">
            <div class="model-model-items">
                {#if $modelStore.availableModels === undefined}
                    <div class="spinner">
                        <Spinner></Spinner>
                    </div>
                {:else if $modelStore.availableModels.length === 0}
                    <p class="no-models-found">No models found. Create a model from an existing architecture on the Architectures Page!</p>
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
                <div class="two-rows">
                    <div class="inputs">
                        <TextInput label="Training Epochs" bind:value={epochs_value} style={StylingUtility.textInput} />
                        <TextInput label="Batch Size" bind:value={batch_value} style={StylingUtility.textInput} />
                        <TextInput label="Learning Rate" bind:value={learning_value} style={StylingUtility.textInput} />
                    </div>
                    
                    <div class="popovers">
                        <Popover on:popoverItemsChanged={handleOptimizerPopoverItemChanged} items={optimizerItems}>
                            <PopoverChipTrigger slot="trigger" label="Optimizers" style={StylingUtility.popoverChipTrigger} />
                            <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                        </Popover>
                        <Button style={selectedOptimizerItem || DISABLED_BUTTON_STYLE} on:click={selectedOptimizerItem && (() => flyoutElement.toggle())}><Icon name="pencil" /></Button>

                        <Popover on:popoverItemsChanged={handleLossPopoverItemChanged} items={lossItems}>
                            <PopoverChipTrigger slot="trigger" label="Loss Functions" style={StylingUtility.popoverChipTrigger} />
                            <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                        </Popover>
                        <Popover on:popoverItemsChanged={handleSourcePopoverItemChanged} items={sources}>
                            <PopoverChipTrigger slot="trigger" label="Data Sources" style={StylingUtility.popoverChipTrigger} />
                            <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                        </Popover>
                    </div>
                </div>
                <Button
                    type="primary"
                    style={can_train ? undefined : DISABLED_BUTTON_STYLE}
                    on:click={can_train && (() => {
                        // console.log(parameters)
                        modelStore.trainModel(
                            $selectedModel.id,
                            selectedSourceItem.value,
                            learning_value,
                            { id: selectedLossItem.value.id, param_values: selectedLossItem.value.parameters },
                            { id: selectedOptimizerItem.value.id, param_values: $state.snapshot(parameters) },
                            batch_value,
                            true,
                            epochs_value,
                        );
                    })}>
                    Train
                </Button>
                <Button
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if($selectedModel){
                            handleDeleteModel();
                        }
                    }}> 
                    {#if $validatingDelete}
                        Click To Confirm
                    {:else}
                        <Icon name="trash" />
                    {/if}
                    </Button
                >
            {/if}
        </div>
    </div>
    <Flyout bind:this={flyoutElement} style={StylingUtility.flyout} header="Optimizer Parameters" subheader="">
        <div slot="flyout-body" class="flyout-body" style="gap: 20px; display: flex; flex-direction: column;">
            {#each parameters as parameter}
                <NodeField parameter={parameter.parameter} value={parameter.value}/>
            {/each}
            {#if parameters.length === 0}
                <div class="node__content-empty">Optimizer has no parameters.</div>
            {/if}
        </div>
    </Flyout>
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
        flex-direction: row;
    }

    .inputs {
        display: flex;
        gap: 10px;
        flex-direction: row;
    }

    .two-rows {
        display: flex;
        gap: 10px;
        flex-direction: column;
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
