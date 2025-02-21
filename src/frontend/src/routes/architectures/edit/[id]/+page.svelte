<script lang="ts">
    import { SvelteFlowProvider, type Edge, type Node } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';
    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
    import { writable, type Writable } from 'svelte/store';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    import Spinner from '$lib/components/Spinner/Spinner.svelte';
    import { onDestroy, onMount } from 'svelte';
    import { page } from '$app/state';
    import { Button, TextInput } from 'kiwi-nl';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import Icon from '$lib/components/Icon/Icon.svelte';
    import { IconNameEnum } from '$lib/components/Icon/types/icon-name.enum';
    import { BackendApi } from '$lib/utilities/api.utilities';
    import type { DnDContext } from '$lib/utilities/DnDUtils';
    import type { Layer } from '$lib/types/layer';
    import { NodeTypeEnum } from '$lib/types/node-type.enum';

    let nodes: Writable<Node[]>;
    let edges: Writable<Edge[]>;
    let availableLayers: Writable<DnDContext[]> = writable([]);

    $: id = page.params.id;
    let isEditingTitle: Writable<boolean> = writable(false);

    architectureStore.subscribe((store) => {
        if (!store.activeArchitecture) {
            return;
        }
        nodes = store?.activeArchitecture?.nodes;
        edges = store?.activeArchitecture?.edges;
    });

    function onSave() {
        architectureStore.saveActiveArchitecture();
    }

    onDestroy(() => {
        architectureStore.clearActiveArchitecture();
    });

    onMount(async () => {
        availableLayers.set(
            (await BackendApi.getAvailableLayers()).map(
                (layer: Layer<any>) => ({ type: NodeTypeEnum.Layer, nodeBlueprint: layer }) as DnDContext,
            ),
        );
        await architectureStore.loadArchitectureById(id);
    });

    function onTitleChange(event: CustomEvent) {
        if (!$architectureStore.activeArchitecture) {
            return;
        }
        $architectureStore.activeArchitecture.meta.name = event.detail.value;
    }
</script>

<div class="edit-architectures-page">
    <div class="edit-architectures-page__header">
        <div class="edit-architectures-page__header-left">
            {#if $isEditingTitle}
                <TextInput
                    label="Architecture Name"
                    on:change={onTitleChange}
                    value={$architectureStore.activeArchitecture?.meta.name}
                    style={StylingUtility.textInput}
                ></TextInput>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(false)}
                    ><Icon name={IconNameEnum.checkmark} /></Button
                >
            {:else}
                <h1>{$architectureStore.activeArchitecture?.meta.name}</h1>
                <Button style={StylingUtility.defaultButton} on:click={() => isEditingTitle.set(true)}
                    ><Icon name={IconNameEnum.pencil} /></Button
                >
            {/if}
        </div>
        <Button type="primary" style={StylingUtility.defaultButton} on:click={onSave}><Icon name={IconNameEnum.save} /></Button>
    </div>
    <SvelteFlowProvider>
        <DnDProvider>
            {#if $architectureStore.activeArchitecture?.loading}
                <div class="spinner-container">
                    <Spinner />
                </div>
            {:else if !$architectureStore.activeArchitecture?.loading && nodes && edges}
                <NodeEditor
                    {onSave}
                    onCreateNode={architectureStore.addNodeToActiveArchitecture}
                    onDeleteNode={architectureStore.deleteNodeFromActiveArchitecture}
                    {nodes}
                    {edges}
                    nodeblueprints={$availableLayers}
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
