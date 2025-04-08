<script lang="ts">
  // @ts-nocheck
  import { StylingUtility } from "$lib/utilities/styling.utility";

  import Spinner from "$lib/components/Spinner/Spinner.svelte";
  import {
    type ButtonCustomStyling,
    Button,
    Popover,
    PopoverChipTrigger,
    PopoverSingleSelectContent,
    TextInput,
    type PopoverItem,
    Flyout,
    ButtonTypeEnum,
    FlyoutSideEnum,
    Checkbox,
    InputSeries,
    Toast,
  } from "kiwi-nl";
  import { modelStore } from "$lib/stores/ModelStore";
  import { onMount, setContext } from "svelte";
  import { writable, type Writable } from "svelte/store";
  import type { AvailableModel } from "$lib/stores/types/models-store.interface";
  import MenuItem from "$lib/components/General/MenuItem.svelte";
  import Icon from "$lib/components/Icon/Icon.svelte";
  import { pipelineStore } from "$lib/stores/PipelineStore";
  import type { Parameter, ParameterValue } from "$lib/types/parameter";
  import NodeField from "$lib/components/Node/NodeParameter.svelte";
  import { BackendApi } from "$lib/utilities/api.utilities";
  import { type TrainingConfig } from "$lib/stores/types/models-store.interface";
  import { IconNameEnum } from "$lib/components/Icon/types/icon-name.enum";

  let selectedModel: Writable<AvailableModel | undefined> = writable(undefined);
  let trainingStartedToast: any;

  let parameters: { parameter: Parameter<any>; value: ParameterValue<any> }[] =
    $state([]);

  setContext("selected-item", selectedModel);

  let optimizerItems: PopoverItem[] = $derived(
    $modelStore.availableOptimizers?.map((x) => ({ label: x.name, value: x }))
  );
  let lossItems: PopoverItem[] = $derived(
    $modelStore.availableLosses?.map((x) => ({ label: x.name, value: x }))
  );
  let sources: PopoverItem[] = $derived(
    $pipelineStore.availablePipelines?.map((x) => ({
      label: x.meta.name,
      value: x.id,
    }))
  );

  let devices: PopoverItem[] = $state([]);

  let validatingDelete: Writable<boolean> = writable(false);

  function handleDeleteModel() {
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
    selectedOptimizerItem = event.detail.selectedItems[0];
    if (selectedOptimizerItem) {
      parameters.length = 0;
      selectedOptimizerItem.value.parameters.forEach((x) =>
        parameters?.push({
          parameter: x,
          value: { type: x.type, val: x.default },
        })
      );
    }
  }

  let selectedLossItem: PopoverItem | undefined = $state(undefined);
  function handleLossPopoverItemChanged(event: CustomEvent): void {
    selectedLossItem = event.detail.selectedItems[0];
  }

  let selectedSourceItem: PopoverItem | undefined = $state(undefined);
  function handleSourcePopoverItemChanged(event: CustomEvent): void {
    selectedSourceItem = event.detail.selectedItems[0];
  }

  let selectedDeviceItem: PopoverItem | undefined = $state(undefined);
  function handleDevicePopoverItemChanged(event: CustomEvent): void {
    selectedDeviceItem = event.detail.selectedItems[0];
  }

  let epochs_value = $state(10);
  let batch_value = $state(16);

  let flyoutElement;
  let settingsFlyout;
  let loader_workers: int[] = $state([0]);
  let prefetch_factor: int[] = $state([2]);
  let pin_memory: bool = $state(false);
  let persistent_workers: bool = $state(false);

  let can_train = $derived(
    selectedOptimizerItem !== undefined &&
      selectedLossItem !== undefined &&
      selectedSourceItem !== undefined
  );
  const DISABLED_BUTTON_STYLE: ButtonCustomStyling = {
    backgroundColor: "#111",
    hover: {
      backgroundColor: "#111",
      color: "#999",
    },
    border: "1px solid transparent",
    color: "#999",
    cursor: "not-allowed",
  };

  const ADVANCED_SETTINGS_BUTTON_STYLE: ButtonCustomStyling = {
    padding: "20px",
  };

  onMount(async () => {
    modelStore.getAvailableModels();
    pipelineStore.getAvailablePipelines();
    modelStore.getAvailableOptimizers();
    modelStore.getAvailableLosses();
    let deviceResponse = await BackendApi.getAvailableDevices();
    devices = deviceResponse.map((x) => ({ label: x, value: x }));
    selectedDeviceItem = devices[0];
    window.addEventListener("click", (event) => {
      if (!event.target) {
        return;
      }
      if (
        $validatingDelete &&
        !(event.target as Element)?.closest(".model-page__bottom-right")
      ) {
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
      <p>
        Create a model from an existing architecture on the Architectures Page!
      </p>
      <p>Select the model you would like to Train!</p>
    </div>
    <div class="model-page__top-right">
      <div class="model-model-items">
        {#if $modelStore.availableModels === undefined}
          <div class="spinner">
            <Spinner></Spinner>
          </div>
        {:else if $modelStore.availableModels.length === 0}
          <p class="no-models-found">
            No models found. Create a model from an existing architecture on the
            Architectures Page!
          </p>
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

  <div class="model-page__bottom-wrapper">
    <div class="model-page__bottom">
      <div class="model-page__bottom-left">
        <div class="model-page__bottom-header">
          {#if $selectedModel}
            <div class="model-page__bottom-header-model-info">
              <h2>{$selectedModel.meta.name}</h2>
              <p>{$selectedModel.meta.description}</p>
            </div>
          {:else}
            <div class="model-page__bottom-header-empty">
              <p>No model selected</p>
            </div>
          {/if}
        </div>
        <div class="model-page__parameters">
          {#if $selectedModel}
            <div class="top-param-row">
              <div class="inputs param_row">
                <TextInput
                  label="Training Epochs"
                  bind:value={epochs_value}
                  style={StylingUtility.textInput}
                />
                <TextInput
                  label="Batch Size"
                  bind:value={batch_value}
                  style={StylingUtility.textInput}
                />
              </div>
              <Button
                style={StylingUtility.defaultButton}
                type="primary"
                on:click={() => settingsFlyout.toggle()}
                ><Icon name={IconNameEnum.gear}></Icon></Button
              >
            </div>
            <div class="popovers param_row">
              <Popover
                on:popoverItemsChanged={handleLossPopoverItemChanged}
                items={lossItems}
              >
                <PopoverChipTrigger
                  slot="trigger"
                  label="Loss Function"
                  style={StylingUtility.popoverChipTrigger}
                />
                <PopoverSingleSelectContent
                  slot="content"
                  style={StylingUtility.popoverSingleSelectContent}
                />
              </Popover>
              <Popover
                on:popoverItemsChanged={handleSourcePopoverItemChanged}
                items={sources}
              >
                <PopoverChipTrigger
                  slot="trigger"
                  label="Data Source"
                  style={StylingUtility.popoverChipTrigger}
                />
                <PopoverSingleSelectContent
                  slot="content"
                  style={StylingUtility.popoverSingleSelectContent}
                />
              </Popover>
            </div>
            <div class="popovers param_row">
              <Popover
                on:popoverItemsChanged={handleOptimizerPopoverItemChanged}
                items={optimizerItems}
              >
                <PopoverChipTrigger
                  slot="trigger"
                  label="Optimizer"
                  style={StylingUtility.popoverChipTrigger}
                />
                <PopoverSingleSelectContent
                  slot="content"
                  style={StylingUtility.popoverSingleSelectContent}
                />
              </Popover>
              <Button
                style={selectedOptimizerItem
                  ? StylingUtility.defaultButton
                  : DISABLED_BUTTON_STYLE}
                on:click={selectedOptimizerItem &&
                  (() => flyoutElement.toggle())}><Icon name="pencil" /></Button
              >
            </div>
          {/if}
        </div>
      </div>
      <div class="model-page__bottom-right">
        {#if $selectedModel}
          <Button
            type="primary"
            style={can_train
              ? StylingUtility.whiteBorderButton
              : DISABLED_BUTTON_STYLE}
            on:click={can_train &&
              (() => {
                let optim_param_values = $state
                  .snapshot(parameters)
                  .map((x) => [x.parameter.id, x.value]);
                let cfg: TrainingConfig = {
                  model_id: $selectedModel.id,
                  source_id: selectedSourceItem.value,
                  loss_fn: { id: selectedLossItem.value.id, param_values: [] },
                  optimizer: {
                    id: selectedOptimizerItem.value.id,
                    param_values: optim_param_values,
                  },
                  shuffle_data: true,
                  batch_size: batch_value,
                  epochs: epochs_value,
                  device: selectedDeviceItem?.value,
                  loader_workers: loader_workers[0],
                  pin_memory: pin_memory,
                  prefetch_factor: prefetch_factor[0],
                  persistent_workers: persistent_workers,
                };
                modelStore.trainModel(cfg);
                trainingStartedToast.addToast();
              })}
          >
            Train
          </Button>
          <Button
            type="primary"
            style={StylingUtility.redButton}
            on:click={() => {
              if ($selectedModel) {
                handleDeleteModel();
              }
            }}
          >
            {#if $validatingDelete}
              Click To Confirm
            {:else}
              <Icon name="trash" />
            {/if}
          </Button>
        {/if}
      </div>
    </div>
  </div>
  <Flyout
    bind:this={flyoutElement}
    style={StylingUtility.flyout}
    header="Optimizer Parameters"
    subheader=""
  >
    <div
      slot="flyout-body"
      class="flyout-body"
      style="gap: 20px; display: flex; flex-direction: column;"
    >
      {#each parameters as parameter}
        <NodeField parameter={parameter.parameter} value={parameter.value} />
      {/each}
      {#if parameters.length === 0}
        <div class="node__content-empty">Optimizer has no parameters.</div>
      {/if}
    </div>
  </Flyout>

  <Flyout
    bind:this={settingsFlyout}
    style={StylingUtility.flyout}
    header="Advanced Settings"
    subheader=""
  >
    <div
      slot="flyout-body"
      class="flyout-body"
      style="gap: 20px; display: flex; flex-direction: column;"
    >
      {#if $selectedModel}
        <Popover
          on:popoverItemsChanged={handleDevicePopoverItemChanged}
          items={$state.snapshot(devices)}
          selectedItems={[selectedDeviceItem]}
        >
          <PopoverChipTrigger
            slot="trigger"
            label="Devices"
            style={StylingUtility.popoverChipTrigger}
          />
          <PopoverSingleSelectContent
            slot="content"
            style={StylingUtility.popoverSingleSelectContent}
          />
        </Popover>
        <Checkbox
          style={StylingUtility.checkbox}
          label="Pin Memory"
          bind:checked={pin_memory}
        ></Checkbox>
        <Checkbox
          style={StylingUtility.checkbox}
          label="Persistent Workers"
          bind:checked={persistent_workers}
        ></Checkbox>
        <InputSeries
          style={StylingUtility.inputSeries}
          label="Loader Workers"
          inputamount="1"
          bind:value={loader_workers}
        ></InputSeries>
        <InputSeries
          style={StylingUtility.inputSeries}
          label="Prefetch Factor"
          inputamount="1"
          bind:value={prefetch_factor}
        ></InputSeries>
      {/if}
    </div>
  </Flyout>
</div>
<Toast
  type="info"
  title={"Started Training " + $selectedModel?.meta?.name}
  bind:this={trainingStartedToast}
>
  <a href="/training" class="toast-link">Go to Training Page</a>
</Toast>

<style lang="scss">
  .model-page {
    display: flex;
    flex-direction: column;
    justify-content: start;
    overflow: hidden;
    height: calc(100% - 55px);
    box-sizing: border-box;
    color: #ffffff;

    &__header {
      color: #ffffff;
      padding-top: 80px;
      h1 {
        font-size: 44px;
        font-weight: 500;
        margin: 0;
        max-width: 1500px;
        margin: 0 auto;
      }
    }

    &__top {
      display: flex;
      justify-content: space-between;
      flex-grow: 1;
      max-width: 1500px;
      margin: 64px auto;
      width: 100%;
    }

    &__bottom {
      display: flex;
      justify-content: space-between;
      padding: 32px 64px;
      height: 250px;
      min-height: 160px;
      max-width: 1500px;
      margin: 0 auto;
    }

    &__bottom-wrapper {
      border-top: 1px solid #ffffff;
    }

    &__bottom-header {
      display: flex;
      gap: 10px;
    }

    &__bottom-left {
      display: flex;
      flex-direction: column;
      width: 100%;
    }

    &__parameters {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    &__bottom-right {
      display: flex;
      gap: 10px;
      height: 38px;
      width: 100%;
      justify-content: flex-end;
    }

    &__bottom-header-model-info {
      display: flex;
      gap: 24px;
      align-items: center;

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

    &__bottom-header-empty {
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

  .param_row {
    display: flex;
    gap: 10px;
    flex-direction: row;
  }

  .top-param-row {
    display: flex;
    align-items: end;
  }

  .adv_settings {
    height: 34px;
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

  .toast-link {
    color: #ffffff;
    font-weight: 400;
    font-size: 10px;
  }
</style>
