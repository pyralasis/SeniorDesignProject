<script lang="ts">
    import { SvelteFlowProvider } from '@xyflow/svelte';
    import DnDProvider from '$lib/components/DnDProvider.svelte';

    import Flow from '$lib/components/Flow/Flow.svelte';
</script>

<div style="height:50vh;">
    <SvelteFlowProvider>
        <DnDProvider>
            <Flow />
        </DnDProvider>
    </SvelteFlowProvider>
</div>
