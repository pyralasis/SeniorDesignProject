<script lang="ts">
    import { SvelteFlowProvider } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';

    import NodeEditor from '$lib/components/NodeEditor/NodeEditor.svelte';
</script>

<div style="height:50vh;">
    <SvelteFlowProvider>
        <DnDProvider>
            <NodeEditor />
        </DnDProvider>
    </SvelteFlowProvider>
</div>
