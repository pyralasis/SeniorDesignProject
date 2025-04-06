<script lang="ts">
    import type { AvailableModel, TrainingConfig } from '$lib/stores/types/models-store.interface';
    import { SoundUtility } from '$lib/utilities/sound.utility';
    import { getContext, onMount } from 'svelte';
    import type { Writable } from 'svelte/store';
    import { modelStore } from '$lib/stores/ModelStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { Button, Tag, TagColorEnum } from 'kiwi-nl'
    import { BackendApi, BackendApiRequestsEnum } from '$lib/utilities/api.utilities';
    import { pipelineStore } from '$lib/stores/PipelineStore';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import Icon from '../Icon/Icon.svelte';

    type Props = {
        name: string
        status: "queued" | "complete" | "in_progress" | "failed",
        columns: ColumnDef[], 
        available_tasks: LoadedTrainingObj[],
        on_select: (id: number) => void,
        can_delete?: boolean,
        on_delete?: (id: number) => void,
    }

    export type ColumnDef = { name: string, min_width: string, proportion: number, get_val: (content: TrainingTaskContent) => Promise<string> };

    let { name, status, columns, available_tasks, on_select, can_delete = false, on_delete= () => {} }: Props  = $props();

    export type LoadedTrainingObj = {
        id: number,
        info: any,
        content: TrainingTaskContent,
    }
    
    export type TrainingTaskContent = {
        config: TrainingConfig,
        data: TrainingTaskStatus,
        meta: {[key: string]: any}
    }

    export type TrainingTaskStatus = CompleteTrainingStatus | QueuedTrainingStatus | InProgressTrainingStatus | FailedTrainingStatus;
    
    export type CompleteTrainingStatus = {
        status: "complete",
        avg_loss: number,
        avg_time_per_epoch: number,
        end_time: number,
        start_time: number,
    };

    export type QueuedTrainingStatus = {
        status: "queued",
        queue_time: number,
    };

    export type InProgressTrainingStatus = {
        status: "in_progress"
        start_time: number
        avg_time_per_epoch: number
        epoch: number
        avg_loss: number
    };

    export type FailedTrainingStatus = {
        status: "failed"
        start_time: number
        end_time: number
        reason: string
        description: string
    };


    export type TrainingTaskInfo = {
        id: number,
        info: {version: number},
        meta: {[key: string]: any}
    }

    type TableRow = {
        id: number,
        value: string[]
    }
  
    let availableTrainingTaskIds: number[] = $state([]);
    let trainingTasks: TrainingTaskContent[] = $state([]);
    let table_values: TableRow[] = $state([]);

    let grid_template_css: string = $derived(columns.reduce((prev, cur) => prev + `minmax(${cur.min_width},${cur.proportion}fr) `,"grid-template-columns: ") + " 30px");

    $effect(() => {
        (async () => {
            table_values = await Promise.all(
                available_tasks
                    .filter(task => task.content.data.status == status)
                    .map(async (task) => ({
                        id: task.id,
                        value: await Promise.all(columns.map(async col => await col.get_val(task.content)))
                    })
                        
                )
            );
        })();
	});
</script>


<div class="training-table">
    
    <h2 class="training-table__title">{name}</h2>
    <div class="training-table__header" style={grid_template_css}>
        {#each columns as column}
            <p>{column.name}</p>
        {/each}
    </div>
    {#if table_values.length == 0}
        <div class="training-table__row">No training tasks found.</div>
    {/if}
    {#each table_values as row}
        <!-- class:selected={$selectedModel === model}
        on:click={() => handleClick(model)} -->

        <button 
            class="training-table__row button" 
            style={grid_template_css}
            type="button"
            onclick={() => {on_select(row.id)}}
        >
            {#each row.value as value}
                <div class="training-table__col">{value}</div>
            {/each}
            {#if can_delete}
                <div class="training-table__col"><Button
                    size="small"
                    type="primary"
                    style={StylingUtility.redButton}
                    on:click={() => {
                        if (can_delete) {
                            on_delete(row.id);
                        }
                    }}>
                        <Icon name="trash" />
                    </Button>
                </div>
            {/if}
            
        </button>

        <!-- <button 
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
        </button> -->
    {/each}
</div>

<style lang="scss">
    .training-table {
        // width: 100%;
        // max-width: 1400px; 
        display: flex;
        flex-direction: column;
        gap: 4px;
        margin: 0 auto; 

        &__title {
            margin: 24px 16px 8px;
            color: #c9c9c9;
        }

        &__header {
            display: grid;
            gap: 24px;
            padding: 16px 16px 16px 24px;
            border-bottom: 2px solid #ffffff;
            font-weight: 600;
            // background-color: #161616;
            // color: #ccc;

            p {
                margin: 0;
                font-size: 16px;
            }
        }

        &__row {
            display: grid;
            gap: 24px;
            padding: 16px 16px 16px 24px;
            border: none;
            background: none;
            // width: 100%;
            text-align: left;
            // border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            align-items: center;
            color: inherit;
            font-family: inherit;
            font-size: inherit;

            &.button {
                cursor: pointer;

                &:hover {
                    font-weight: 600;
                    transition: transform 0.1s ease-in-out;
                }
            }

            &.selected {
                font-weight: 600;
                color: #fe2e00;
            }
        }
        &__row:nth-child(odd){
            background-color: #222222;
        }       
        // &__col:nth-child(even){
        //     background-color: #ffffff;
        // }       
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