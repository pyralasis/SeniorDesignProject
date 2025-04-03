<script lang="ts">
  import { onMount, setContext } from 'svelte';
  import { modelStore } from '$lib/stores/ModelStore';
  import type { AvailableModel } from '$lib/stores/types/models-store.interface';
  import { writable, type Writable } from 'svelte/store';
  import TrainingTable from '$lib/components/Training/TrainingTable.svelte';

  let selectedModel: Writable<AvailableModel | undefined> = writable(undefined);
  setContext('selected-item', selectedModel);
  
  onMount(() => {
      modelStore.getAvailableModels();
  });
</script>

<div class="training-page">
  <div class="training-page__header">
      <h1>Training List</h1>
  </div>
  
  <div class="training-page__top">
      <div class="training-page__models-list">
              <TrainingTable/>
      </div>
  </div>

  <div class="training-page__bottom">
      <div class="training-page__bottom-left">
          {#if $selectedModel}
              <div class="training-page__bottom-left-model-info">
                  <h2>{$selectedModel.meta.name}</h2>
                  <p>{$selectedModel.meta.description}</p>\
                  <p>{$selectedModel.id}</p>
              </div>
          {:else}
              <div class="training-page__bottom-left-empty">
                  <p>No model selected</p>
              </div>
          {/if}
      </div>
  </div>
</div>

<style lang="scss">
  .training-page {
      display: flex;
      flex-direction: column;
      height: 100%;
      color: #ffffff;
      background-color: #111111;

      &__header {
          border-bottom: 1px solid #ffffff;
          padding: 20px 64px;
          
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

      &__bottom-left-empty {
          color: #c2c2c2;
      }
  }
</style>