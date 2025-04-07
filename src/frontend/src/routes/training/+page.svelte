<script lang="ts">
    import { onMount, setContext } from "svelte";
    import { modelStore } from "$lib/stores/ModelStore";
    import type { AvailableModel } from "$lib/stores/types/models-store.interface";
    import { writable, type Writable } from "svelte/store";
    import TrainingTable, {
        type ColumnDef,
        type CompleteTrainingStatus,
        type FailedTrainingStatus,
        type InProgressTrainingStatus,
        type LoadedTrainingObj,
        type QueuedTrainingStatus,
        type TrainingTaskContent,
        type TrainingTaskInfo,
    } from "$lib/components/Training/TrainingTable.svelte";
    import { pipelineStore } from "$lib/stores/PipelineStore";
    import { BackendApi } from "$lib/utilities/api.utilities";
    import { StylingUtility } from "$lib/utilities/styling.utility";
    import { Button } from "kiwi-nl";

    let selectedTask: TrainingTaskContent | undefined = $state(undefined);

    let availableTrainingTasks: TrainingTaskInfo[] = $state([]);
    let availableTasks: LoadedTrainingObj[] = $state([]);

    $effect(() => {
        const interval = setInterval(async () => {
            availableTrainingTasks = await BackendApi.getAvailableTrainingTasks();
            availableTasks = await Promise.all(
                availableTrainingTasks.map(async (info) => await BackendApi.getTrainingTaskByID(info.id))
            );
        }, 1000);
        modelStore.getAvailableModels();
        return () => clearInterval(interval);
    });

    const ms_to_time = (ms: number) => {
        return new Date(ms).toLocaleString();
    };

    const queued_columns: ColumnDef[] = [
        {
            name: "Model Name",
            get_val: async (task) => {
                return await modelStore.getModelNameById(task.config.model_id);
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Queue Time",
            get_val: async (task) => {
                let status = task.data as QueuedTrainingStatus;
                return ms_to_time(status.queue_time);
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Dataset",
            get_val: async (task) => {
                return await pipelineStore.getPipelineNameById(task.config.source_id);
            },
            min_width: "200px",
            proportion: 2,
        },
    ];

    const in_progress_columns: ColumnDef[] = [
        {
            name: "Model Name",
            get_val: async (task) => {
                return await modelStore.getModelNameById(task.config.model_id);
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Average Loss",
            get_val: async (task) => {
                let status = task.data as CompleteTrainingStatus;
                return status.avg_loss.toFixed(4)
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Current Epoch",
            get_val: async (task) => {
                let status = task.data as InProgressTrainingStatus;
                return status.epoch.toString() + " / " + task.config.epochs.toString();
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Time/Epoch",
            get_val: async (task) => {
                let status = task.data as InProgressTrainingStatus;
                let avg = status.avg_time_per_epoch;
                // console.log(avg);
                if (avg < 1000) {
                    return avg.toString() + " ms";
                } else if (avg < 60000) {
                    return (avg / 1000).toFixed(2) + " secs";
                }
                return (avg / 1000 / 60).toFixed(2) + " mins";
            },
            min_width: "100px",
            proportion: 1,
        },
    ];

    const completed_columns: ColumnDef[] = [
        {
            name: "Model Name",
            get_val: async (task) => {
                return await modelStore.getModelNameById(task.config.model_id);
            },
            min_width: "200px",
            proportion: 2,
        },
        // {
        //     name: "Dataset",
        //     get_val: async (task) => {
        //         return await pipelineStore.getPipelineNameById(task.config.source_id);
        //     },
        //     min_width: "200px",
        //     proportion: 2,
        // },
        // {
        //     name: "Start Time",
        //     get_val: async (task) => {
        //         let status = task.data as CompleteTrainingStatus;
        //         return ms_to_time(status.start_time);
        //     },
        //     min_width: "200px",
        //     proportion: 2,
        // },
        // {
        //     name: "Completed Time",
        //     get_val: async (task) => {
        //         let status = task.data as CompleteTrainingStatus;
        //         return ms_to_time(status.end_time);
        //     },
        //     min_width: "200px",
        //     proportion: 2,
        // },
        {
            name: "Average Loss",
            get_val: async (task) => {
                let status = task.data as CompleteTrainingStatus;
                return status.avg_loss.toFixed(4)
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Training Duration",
            get_val: async (task) => {
                let status = task.data as CompleteTrainingStatus;
                let elapsed = status.end_time - status.start_time;
                if (elapsed < 1000) {
                    return elapsed.toString() + " ms";
                } else if (elapsed < 60000) {
                    return (elapsed / 1000).toFixed(2) + " secs";
                }
                return (elapsed / 1000 / 60).toFixed(2) + " mins";
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Time/Epoch",
            get_val: async (task) => {
                let status = task.data as CompleteTrainingStatus;
                let avg = status.avg_time_per_epoch;
                if (avg < 1000) {
                    return avg.toString() + " ms";
                } else if (avg < 60000) {
                    return (avg / 1000).toFixed(2) + " secs";
                }
                return (avg / 1000 / 60).toFixed(2) + " mins";
            },
            min_width: "100px",
            proportion: 1,
        },
    ];

    const failed_columns: ColumnDef[] = [
        {
            name: "Model Name",
            get_val: async (task) => {
                return await modelStore.getModelNameById(task.config.model_id);
            },
            min_width: "200px",
            proportion: 2,
        },
        {
            name: "Failure Reason",
            get_val: async (task) => {
                let status = task.data as FailedTrainingStatus;
                return status.description;
            },
            min_width: "416px",
            proportion: 4,
        },
        // {
        //     name: "Dataset",
        //     get_val: async (task) => {
        //         return await pipelineStore.getPipelineNameById(task.config.source_id);
        //     },
        //     min_width: "200px",
        //     proportion: 1,
        // }
    ];

    const delete_train_task = (id: number) => {
        availableTasks = availableTasks.filter((tsk) => tsk.id !== id);
        selectedTask = undefined;
        BackendApi.deleteTrainingTaskByID(id);
    };

    let onSelectTask = (value: number) => {
        selectedTask = availableTasks.filter((task) => task.id == value)[0]?.content;
    };
</script>

<div class="training-page">
    <div class="training-page__header">
        <h1>Training List</h1>

        <div style="height: 38px; display: flex; margin: auto 0;">
            <Button
                type="primary"
                style={StylingUtility.redButton}
                on:click={() => {
                    availableTasks.forEach((tsk) => {
                        if (tsk.content.data.status === "complete" || tsk.content.data.status === "failed") {
                            delete_train_task(tsk.id);
                        }
                    });
                    availableTasks = availableTasks.filter(
                        (tsk) => tsk.content.data.status !== "complete" && tsk.content.data.status !== "failed"
                    );
                }}>Delete All</Button
            >
        </div>
    </div>

    <div class="training-page__top">
        <TrainingTable
            name="In Progress"
            status="in_progress"
            columns={in_progress_columns}
            available_tasks={availableTasks}
            on_select={onSelectTask}
        ></TrainingTable>
        <TrainingTable
            name="Queued"
            status="queued"
            columns={queued_columns}
            available_tasks={availableTasks}
            on_select={onSelectTask}
        ></TrainingTable>
        <TrainingTable
            name="Complete"
            status="complete"
            columns={completed_columns}
            available_tasks={availableTasks}
            on_select={onSelectTask}
            can_delete
            on_delete={delete_train_task}
        ></TrainingTable>
        <TrainingTable
            name="Failed"
            status="failed"
            columns={failed_columns}
            available_tasks={availableTasks}
            on_select={onSelectTask}
            can_delete
            on_delete={delete_train_task}
        ></TrainingTable>
    </div>

    <div class="training-page__bottom">
        <div class="training-page__bottom-left">
            {#if selectedTask}
                <div class="model-table-header">
                    <p>Model ID</p>
                    <p>Source ID</p>
                    <p>Loss Function</p>
                    <p>Optimizer</p>
                    <p>Shuffle Data</p>
                    <p>Batch Size</p>
                    <p>Epochs</p>
                    <p>Device</p>
                    <p>Loader Workers</p>
                    <p>Pin Memory</p>
                    <p>Prefetch Factor</p>
                    <p>Persistent Workers</p>
                </div>
                <div class="model-table">
                    <div class="col">{selectedTask.config.model_id}</div>
                    <div class="col">{selectedTask.config.source_id}</div>
                    <div class="col">{selectedTask.config.loss_fn.id}</div>
                    <div class="col">{selectedTask.config.optimizer.id}</div>
                    <div class="col">{selectedTask.config.shuffle_data}</div>
                    <div class="col">{selectedTask.config.batch_size}</div>
                    <div class="col">{selectedTask.config.epochs}</div>
                    <div class="col">{selectedTask.config.device}</div>
                    <div class="col">{selectedTask.config.loader_workers}</div>
                    <div class="col">{selectedTask.config.pin_memory}</div>
                    <div class="col">{selectedTask.config.prefetch_factor}</div>
                    <div class="col">{selectedTask.config.persistent_workers}</div>
                </div>
            {:else}
                <div class="training-page__bottom-left-empty">
                    <p>No training task selected</p>
                </div>
            {/if}
        </div>
        <div class="model-page__bottom-right">
            {#if selectedTask}
                <Button
                    type="primary"
                    style={StylingUtility.whiteBorderButton}
                    on:click={() => {
                        if (selectedTask !== undefined) {
                            modelStore.trainModel(selectedTask.config);
                        }
                    }}
                >
                    Re-train
                </Button>
            {/if}
        </div>
    </div>
</div>

<style lang="scss">
    .training-page {
        display: flex;
        flex-direction: column;
        height: calc(100% - 55px);
        color: #ffffff;
        background-color: #111111;

        &__header {
            display: flex;
            justify-content: space-between;

            border-bottom: 1px solid #ffffff;
            padding: 20px 64px;
            h1 {
                font-size: 44px;
                font-weight: 500;
                margin: 0;
            }
        }

        &__top {
            display: flex;
            justify-content: center;
            flex-grow: 1;
            margin: 0px auto;
            padding: 0 2%;
            width: 96%;
            flex-grow: 1;
            overflow-y: scroll;
            flex-direction: row;
            flex-wrap: wrap;
        }

        &__bottom {
            display: flex;
            border-top: 1px solid #ffffff;
            justify-content: space-between;
            padding: 32px 64px;
            height: 160px;
            min-height: 160px;
        }

        &__bottom-left-empty {
            color: #c2c2c2;
        }
        &__bottom-right {
            display: flex;
            gap: 10px;
            height: 38px;
        }
    }

    .model-table-header {
        display: grid;
        grid-template-columns: 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px;
        gap: 24px;
        padding: 16px 24px;
        border-bottom: 2px solid #ffffff;
        font-weight: 600;
        // background-color: #161616;
        // color: #ccc;

        p {
            margin: 0;
            font-size: 16px;
        }
    }

    .model-table {
        display: grid;
        grid-template-columns: 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px 90px;

        gap: 24px;
        padding: 16px 24px;
        border: none;
        background: none;
        // width: 100%;
        text-align: left;
        // border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        align-items: center;
        color: inherit;
        font-family: inherit;
        font-size: inherit;
        background-color: #222222;
    }
</style>
