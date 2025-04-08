<script lang="ts">
  import { goto } from "$app/navigation";
  import MenuItem from "$lib/components/General/MenuItem.svelte";
  import Icon from "$lib/components/Icon/Icon.svelte";
  import Spinner from "$lib/components/Spinner/Spinner.svelte";
  import { architectureStore } from "$lib/stores/ArchitectureStore";
  import type { AvailableArchitecture } from "$lib/stores/types/architecture-store.interface";
  import { StylingUtility } from "$lib/utilities/styling.utility";
  import { Button, TextInput, Toast } from "kiwi-nl";
  import { onMount, setContext } from "svelte";
  import { writable, type Writable } from "svelte/store";
  import { modelStore } from "$lib/stores/ModelStore";
  import type { ArchitectureId } from "$lib/types/architecture";

  let selectedArchitecture: Writable<AvailableArchitecture | undefined> =
    writable(undefined);
  type Meta = { name: string; description?: string }; // Define the type for meta
  let creatingNewArchitecture: Writable<boolean> = writable(false);
  let validatingDelete: Writable<boolean> = writable(false);
  let newArchitectureName: string = "";
  let newArchitectureDescription: string = "";
  let newModelName: string = "";

  let modelSuccessToast: any;
  let architectureCreatedToast: any;
  let architectureDeletedToast: any;
  let modelFailureToast: any;
  let architectureCreateFailureToast: any;
  let architectureDeleteFailureToast: any;

  let newArchitectureId: Writable<ArchitectureId> = writable("");

  let validatingConvertToModel: Writable<boolean> = writable(false);

  setContext("selected-item", selectedArchitecture);

  $: if ($selectedArchitecture?.meta?.name) {
    newModelName = $selectedArchitecture.meta.name + " Model";
  }

  async function handleCreateNewArchitecture(): Promise<void> {
    let architectureCreationSuccess: { id?: ArchitectureId; success: boolean } =
      await architectureStore.createNewArchitecture(
        newArchitectureName,
        newArchitectureDescription
      );
    $creatingNewArchitecture = false;
    if (architectureCreationSuccess.success) {
      architectureCreatedToast.addToast();
      $newArchitectureId = architectureCreationSuccess.id ?? "";
    } else {
      architectureCreateFailureToast.addToast();
    }
  }

  async function handleDeleteArchitecture(id: string): Promise<void> {
    let deleteSuccess: boolean = false;
    if ($validatingDelete) {
      deleteSuccess = await architectureStore.deleteArchitecture(id);
      $selectedArchitecture = undefined;
      if (deleteSuccess) {
        architectureDeletedToast.addToast();
      } else {
        architectureDeleteFailureToast.addToast();
      }
    } else {
      $validatingDelete = true;
    }
  }

  async function handleConvertToModel(): Promise<void> {
    let modelCreationSuccess: boolean;
    if ($validatingConvertToModel) {
      if ($selectedArchitecture?.id) {
        modelCreationSuccess = await modelStore.createModel(
          $selectedArchitecture.id,
          { ...$selectedArchitecture.meta, name: newModelName }
        );
        if (modelCreationSuccess) {
          modelSuccessToast.addToast();
        } else {
          modelFailureToast.addToast();
        }
      } else {
        console.error("Selected architecture ID is undefined.");
      }
      $validatingConvertToModel = false;
    } else {
      $validatingConvertToModel = true;
    }
  }
  function handleCreateNewArchitectureInitialisation(): void {
    $selectedArchitecture = undefined;
    newArchitectureName = "";
    newArchitectureDescription = "";
    creatingNewArchitecture.set(true);
  }

  onMount(() => {
    architectureStore.getAvailableArchitectures();

    window.addEventListener("click", (event) => {
      if (!event.target) {
        return;
      }
      if (
        $validatingDelete &&
        !(event.target as Element)?.closest(
          ".select-architecture-page__bottom-right"
        )
      ) {
        validatingDelete.set(false);
      }
      if (
        $validatingConvertToModel &&
        !(event.target as Element)?.closest(
          ".select-architecture-page__bottom-right-wrapper"
        )
      ) {
        validatingConvertToModel.set(false);
      }
    });
  });
</script>

<div class="select-architecture-page">
  <div class="select-architecture-page__header">
    <h1>Select Architecture</h1>
  </div>
  <div class="select-architecture-page__top">
    <div class="select-architecture-page__top-left">
      <p>
        Select the architecture you would like to edit, delete, or convert to a
        model or start from scratch with a new architecture
      </p>
      <Button
        type="primary"
        style={StylingUtility.whiteBorderButton}
        on:click={handleCreateNewArchitectureInitialisation}
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
          <div class="select-architecture-page__items-header">
            <p>Name</p>
            <p>Last Modified</p>
          </div>
          {#each $architectureStore.availableArchitectures as a, i}
            <MenuItem item={a}></MenuItem>
          {/each}
        {/if}
      </div>
    </div>
  </div>
  <div class="select-architecture-page__bottom-wrapper">
    <div class="select-architecture-page__bottom">
      <div class="select-architecture-page__bottom-left">
        {#if $selectedArchitecture}
          <div class="select-architecture-page__bottom-left-architecture-info">
            <div class="name">
              <h2>{$selectedArchitecture.meta.name}</h2>
            </div>
            <div class="description">
              <p>{$selectedArchitecture.meta.description}</p>
            </div>
          </div>
        {:else if $creatingNewArchitecture}
          <div
            class="select-architecture-page__create-new-architecture-actions"
          >
            <div class="name-input">
              <TextInput
                label="Name"
                style={StylingUtility.textInput}
                bind:value={newArchitectureName}
              ></TextInput>
            </div>
            <div class="description-input">
              <TextInput
                label="Description"
                style={StylingUtility.textInput}
                bind:value={newArchitectureDescription}
              ></TextInput>
            </div>
          </div>
          <div
            class="select-architecture-page__create-new-architecture-actions-buttons"
          >
            <Button
              type="primary"
              style={StylingUtility.whiteBorderButton}
              on:click={async () => await handleCreateNewArchitecture()}
              >Create</Button
            >
            <Button
              type="primary"
              style={StylingUtility.redButton}
              on:click={() => creatingNewArchitecture.set(false)}>Cancel</Button
            >
          </div>
        {:else}
          <div class="select-architecture-page__bottom-left-empty">
            <p>No architecture selected</p>
          </div>
        {/if}
      </div>
      {#if $selectedArchitecture}
        <div class="select-architecture-page__bottom-right-wrapper">
          <div class="select-architecture-page__bottom-right">
            {#if $selectedArchitecture}
              {#if !$validatingDelete && !$validatingConvertToModel}
                <Button
                  type="primary"
                  style={StylingUtility.whiteBorderButton}
                  href="/architectures/edit/{$selectedArchitecture?.id}"
                  >Open Node Editor</Button
                >
              {/if}
              {#if $validatingConvertToModel}
                <TextInput
                  label="Model Name"
                  style={StylingUtility.textInput}
                  bind:value={newModelName}
                ></TextInput>
              {/if}
              {#if !$validatingDelete}
                <Button
                  type="primary"
                  style={StylingUtility.whiteBorderButton}
                  on:click={() => {
                    if ($selectedArchitecture) {
                      handleConvertToModel();
                    }
                  }}
                >
                  {#if $validatingConvertToModel}
                    Convert
                  {:else}
                    Convert to Model
                  {/if}
                </Button>
              {/if}
              {#if !$validatingConvertToModel}
                <Button
                  type="primary"
                  style={StylingUtility.redButton}
                  on:click={() => {
                    if ($selectedArchitecture) {
                      handleDeleteArchitecture($selectedArchitecture.id);
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
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>
<Toast
  title="Model Created Successfully"
  bind:this={modelSuccessToast}
  type="success"
  ><a class="toast-link" href="/models">Go to Models Page</a></Toast
>
<Toast
  title="Architecture Created Successfully"
  bind:this={architectureCreatedToast}
>
  <a class="toast-link" href={`/architectures/edit/${$newArchitectureId}`}
    >Start Creating Architecture</a
  >
</Toast>
<Toast
  title="Architecture Deleted Successfully"
  bind:this={architectureDeletedToast}
/>
<Toast
  title="Model Creation Failed"
  bind:this={modelFailureToast}
  type="error"
/>
<Toast
  title="Architecture Creation Failed"
  type="error"
  bind:this={architectureCreateFailureToast}
/>
<Toast
  title="Architecture Deletion Failed"
  type="error"
  bind:this={architectureDeleteFailureToast}
></Toast>

<style lang="scss">
  .select-architecture-page {
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
        margin: 0px auto;
        width: 100%;
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
      height: 160px;
      min-height: 160px;
      max-width: 1500px;
      margin: 0 auto;
    }

    &__bottom-wrapper {
      border-top: 1px solid #ffffff;
    }

    &__bottom-left {
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 100%;
    }

    &__bottom-right {
      display: flex;
      gap: 10px;
      height: 38px;
      align-items: end;
    }

    &__bottom-right-wrapper {
      display: flex;
      width: 100%;
      justify-content: flex-end;
      padding-left: 500px;
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
      .name {
        display: flex;
        gap: 10px;
      }
      .description {
        display: flex;
        flex-direction: column;
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

  .no-architectures-found {
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

  .toast-link {
    color: #ffffff;
    font-weight: 400;
    font-size: 10px;
  }
</style>
