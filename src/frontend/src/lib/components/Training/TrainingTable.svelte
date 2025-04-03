<script lang="ts">
    import type { AvailableModel } from '$lib/stores/types/models-store.interface';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import { getContext, onMount } from 'svelte';
    import type { Writable } from 'svelte/store';
    import { modelStore } from '$lib/stores/ModelStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { Tag, TagColorEnum } from 'kiwi-nl'
    import { BackendApi, BackendApiRequestsEnum } from '$lib/utilities/api.utilities';


    const selectedModel = getContext<Writable<AvailableModel | undefined>>('selected-item');

    function handleClick(model: AvailableModel) {
        const isSelected = $selectedModel === model;
        
        if (isSelected) {
            selectedModel.set(undefined);
            SoundUtility.playClick1(0.1);
            return;
        }
        
        SoundUtility.playClick2(0.1);
        selectedModel.set(model);
    }
   
    
    let availableTrainModels: any[];
    onMount (async() => {

        availableTrainModels = await BackendApi.getAvailableTrainingModels();
        availableTrainModels.map((model) => {
            BackendApi.getTrainedModelByID(model.id)
        });
        console.log(availableTrainModels);
    });
    
    

</script>


<div class="training-table">
    <div class="training-table__header">
        <p>Name</p>
        <p>Training Start Time</p>
        <p>Status</p>
    </div>
    {#if $modelStore.availableModels === undefined}
        <div class="spinner">
            <Spinner></Spinner>
        </div>
    {:else if $modelStore.availableModels.length === 0}
        <p class="no-models-found">No models found</p>
    {:else}
        {#each availableTrainModels as model}
            <button 
                class="training-table__row" 
                class:selected={$selectedModel === model}
                on:click={() => handleClick(model)}
                type="button"
            >
                <div class="training-table__col">{model.meta.name}</div>
                <div class="training-table__col time"> 

                </div>
                <div class="training-table__col status">
                    <span class="status-badge" >
                        
                    </span>
                </div>
            </button>
        {/each}
    {/if}
</div>

<style lang="scss">
    .training-table {
        width: 100%;
        max-width: 1200px; 
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin: 0 auto; 

        &__header {
            display: grid;
            grid-template-columns: minmax(200px, 2fr) minmax(200px, 2fr) minmax(150px, 1fr);
            gap: 24px;
            padding: 16px 24px;
            border-bottom: 2px solid #ffffff;
            font-weight: 600;

            p {
                margin: 0;
                font-size: 16px;
            }
        }

        &__row {
            display: grid;
            grid-template-columns: minmax(200px, 2fr) minmax(200px, 2fr) minmax(150px, 1fr);
            gap: 24px;
            padding: 16px 24px;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            align-items: center;
            cursor: pointer;
            color: inherit;
            font-family: inherit;
            font-size: inherit;

            &:hover {
                font-weight: 600;
                transition: transform 0.1s ease-in-out;
            }

            &.selected {
                font-weight: 600;
                color: #fe2e00;
            }
        }

        &__col {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            
            &.time {
                opacity: 0.8;
                font-size: 14px;
                font-family: monospace;
            }

            &.status {
                display: flex;
                justify-content: center;
            }
        }

        .status-badge {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            color: #000000;
            min-width: 100px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .loss-value {
            margin-left: 8px;
            font-family: monospace;
            opacity: 0.8;
        }

        .no-models-found {
            text-align: center;
            padding: 48px;
            color: rgba(255, 255, 255, 0.6);
            font-style: italic;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 8px;
            margin: 24px 0;
        }
        .spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 48px;
        }
    }
</style>