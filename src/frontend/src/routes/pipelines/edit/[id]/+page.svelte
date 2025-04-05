<script lang="ts">
    import { SvelteFlowProvider, type Edge, type Node } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';
    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable } from 'svelte/store';
    import { pipelineStore } from '$lib/stores/PipelineStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { onDestroy, onMount } from 'svelte';
    import { page } from '$app/state';
    import { Button, TextInput } from 'kiwi-nl';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { IconNameEnum } from '$lib/components/Icon/types/icon-name.enum';
    import type { DnDContext } from '$lib/utilities/DnDUtils';
    import { BackendApi } from '$lib/utilities/api.utilities';
    import type { SourceBlueprint } from '$lib/types/source';
    import { NodeTypeEnum } from '$lib/types/node-type.enum';
    import { PipelineStatusEnum } from '$lib/stores/types/pipeline-store.interface';
    import type { NodeBlueprint } from '$lib/utilities/DnDUtils';

    let nodes: Writable<Node[]>;
    let edges: Writable<Edge[]>;
    let availableSources: Writable<DnDContext[]> = writable([]);
    let availableTransforms: Writable<DnDContext[]> = writable([]);
    let valueOutput: DnDContext = {
        type: NodeTypeEnum.ValuesOutput,
        nodeBlueprint: { id: 'value-output', name: 'Value Output', parameters: [] },
    };
    let labelOutput: DnDContext = {
        type: NodeTypeEnum.LabelsOutput,
        nodeBlueprint: { id: 'label-output', name: 'Label Output', parameters: [] },
    };

    $: id = parseInt(page.params.id);

    let isEditingTitle: Writable<boolean> = writable(false);

    pipelineStore.subscribe((store) => {
        if (!store.activePipeline) {
            return;
        }
        nodes = store?.activePipeline?.nodes;
        edges = store?.activePipeline?.edges;
    });
    function handleKeydown(event: KeyboardEvent) {
        if ((event.ctrlKey || event.metaKey) && (event.key === 's' || event.key === 'S')) {
            event.preventDefault();
            pipelineStore.updatePipelineSaveStatus();
        }
    }
    function onChange() {
        if ($pipelineStore.saveStatus === PipelineStatusEnum.NotSaved) {
            return;
        }
        pipelineStore.updateSaveStatus(false, PipelineStatusEnum.NotSaved);
    }
    onMount(() => {
        window.addEventListener('keydown', handleKeydown);

        return () => {
            window.removeEventListener('keydown', handleKeydown);
        };
    });
    onDestroy(() => {
        pipelineStore.clearActivePipeline();
    });

    onMount(async () => {
        availableSources.set(
            (await BackendApi.getAvailableSources()).map(
                (source: SourceBlueprint<any>) => ({ type: NodeTypeEnum.Source, nodeBlueprint: source }) as DnDContext,
            ),
        );
        availableTransforms.set(
            (await BackendApi.getAvailableTransforms()).map(
                (transform: SourceBlueprint<any>) => ({ type: NodeTypeEnum.Transform, nodeBlueprint: transform }) as DnDContext,
            ),
        );
        await pipelineStore.loadPipelineById(id);
    });

    function onTitleChange(event: CustomEvent) {
        if (!$pipelineStore.activePipeline) {
            return;
        }
        $pipelineStore.activePipeline.meta.name = event.detail.value;
    }
</script>

<div class="edit-pipelines-page">
    <a
        href="/pipelines"
        on:click={() => {
            pipelineStore.saveActivePipeline();
        }}
    >
        Back to Pipelines
    </a>
    <div class="edit-pipelines-page__header">
        <div class="edit-pipelines-page__header-left">
            {#if $isEditingTitle}
                <TextInput
                    label="Pipeline Name"
                    on:change={onTitleChange}
                    value={$pipelineStore.activePipeline?.meta.name}
                    style={StylingUtility.textInput}
                ></TextInput>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(false)}
                    ><Icon name={IconNameEnum.checkmark} /></Button
                >
            {:else}
                <h1>{$pipelineStore.activePipeline?.meta.name}</h1>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(true)}
                    ><Icon name={IconNameEnum.pencil} /></Button
                >
            {/if}
        </div>
        <div class="save-status">
            <span>{$pipelineStore.saveStatus}</span>
        </div>
    </div>
    <SvelteFlowProvider>
        <DnDProvider>
            {#if $pipelineStore.activePipeline?.loading}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {:else if !$pipelineStore.activePipeline?.loading && nodes && edges}
                {#key $nodes.length !== 0}
                    <NodeEditor
                        onSave={() => pipelineStore.updatePipelineSaveStatus()}
                        {onChange}
                        onCreateNode={pipelineStore.addNodeToActivePipeline}
                        onDeleteNode={pipelineStore.deleteNodeFromActivePipeline}
                        {nodes}
                        {edges}
                        nodeblueprints={[valueOutput, labelOutput, ...$availableSources, ...$availableTransforms]}
                        nodeNameEditor={false}
                    />
                {/key}
            {:else}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {/if}
        </DnDProvider>
    </SvelteFlowProvider>
</div>

<style lang="scss">
    .edit-pipelines-page {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        overflow: hidden;
        &__header {
            padding: 16px;
            display: flex;
            align-items: end;
            justify-content: space-between;
            height: 54px;
        }

        &__header-left {
            display: flex;
            align-items: end;
            gap: 8px;
        }

        h1 {
            margin: 0;
            color: #ffffff;
        }
        a {
            display: inline-block;
            gap: 8px;
            text-decoration: none;
            cursor: pointer;
            padding: 8px 16px;
            border-radius: 4px;
            white-space: nowrap;
            color: #ffffff;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        a:hover {
            color: #fe2e00;
            text-decoration: underline;
            transition: all 0.3s ease;
        }
    }
    .save-status {
        display: flex;
        align-items: center;
        color: white;
        font-size: 14px;
        font-weight: bold;
        margin-left: auto;
        margin-right: 0;
    }
    .save-status span {
        margin-right: 10px;
    }
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        box-sizing: border-box;
    }
</style>
