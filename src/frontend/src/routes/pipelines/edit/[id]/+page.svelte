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

    let nodes: Writable<Node[]>;
    let edges: Writable<Edge[]>;
    let availableSources: Writable<DnDContext[]> = writable([]);
    let availableTransforms: Writable<DnDContext[]> = writable([]);

    $: id = parseInt(page.params.id);
    let isEditingTitle: Writable<boolean> = writable(false);

    pipelineStore.subscribe((store) => {
        if (!store.activePipeline) {
            return;
        }
        nodes = store?.activePipeline?.nodes;
        edges = store?.activePipeline?.edges;
    });

    function onSave() {
        pipelineStore.saveActivePipeline();
    }

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

<div class="edit-architectures-page">
    <div class="edit-architectures-page__header">
        <div class="edit-architectures-page__header-left">
            {#if $isEditingTitle}
                <TextInput
                    label="Architecture Name"
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
        <Button type="primary" style={StylingUtility.defaultButton} on:click={onSave}><Icon name={IconNameEnum.save} /></Button>
    </div>
    <SvelteFlowProvider>
        <DnDProvider>
            {#if $pipelineStore.activePipeline?.loading}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {:else if !$pipelineStore.activePipeline?.loading && nodes && edges}
                <NodeEditor
                    {onSave}
                    onCreateNode={pipelineStore.addNodeToActivePipeline}
                    onDeleteNode={pipelineStore.deleteNodeFromActivePipeline}
                    {nodes}
                    {edges}
                    nodeblueprints={[...$availableSources, ...$availableTransforms]}
                />
            {:else}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {/if}
        </DnDProvider>
    </SvelteFlowProvider>
</div>

<style lang="scss">
    .edit-architectures-page {
        width: 100%;
        height: 100%;

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
    }
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
</style>
