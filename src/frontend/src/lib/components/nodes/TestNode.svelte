<script lang="ts">
    import type { Writable } from 'svelte/store';
    import { Handle, Position, type NodeProps } from '@xyflow/svelte';
    import { Accordion, AccordionBody, AccordionHeader, Text, TextInput } from 'kiwi-nl';

    type $$Props = NodeProps;
</script>

<Accordion>
    <AccordionHeader class="drag-handle" slot="header"><Text>This is an Accordion</Text></AccordionHeader>
    <AccordionBody slot="body"
        ><Handle type="target" position={Position.Left} />
        <div class="test-node">
            <TextInput label="Input" />
        </div>
        <Handle type="source" position={Position.Right} /></AccordionBody
    >
</Accordion>

<style lang="scss">
    .test-node {
        height: 100px;
        width: 500px;
        background-color: white;
        overflow: hidden;
        padding: 8px;
        cursor: default;
    }
</style>
