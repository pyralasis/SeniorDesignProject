<script lang="ts">
    import { Button, ButtonTypeEnum, TextInput } from 'kiwi-nl';
    import { getContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import { architectureStore } from '$lib/stores/ArchitectureStore';
    
    export let selectedNodeTitle: Writable<string> | undefined;
    export let selectedNodeColor: Writable<string> | undefined;
    export let nodeNameEditor: boolean = true;
    export let onDelete: () => void;
    export let onClearNodes: () => void;
    export let onChange: () => void;

    let xColor: Writable<string> = getContext('xColor');
    let sidebarExpanded: Writable<boolean> = getContext('sidebarExpanded');
    let rotationDegrees: Writable<number> = writable(180);

    function handleSidebarToggle() {
        sidebarExpanded.update((expanded) => (expanded = !expanded));
        rotationDegrees.update((degrees) => (degrees = degrees === 0 ? 180 : 0));
    }

    function onTitleChange(event: CustomEvent) {
        if (!selectedNodeTitle) {
            return;
        }
        selectedNodeTitle.update((title) => (title = event.detail.value));
        onChange();
    }

    function onColorChange(event: Event) {
        if (!selectedNodeColor) {
            xColor.update((color) => (color = `${(event.target as HTMLInputElement).value ?? '#fff'}`));
            return;
        }
        selectedNodeColor.update((color) => (color = `${(event.target as HTMLInputElement).value ?? '#fff'}`));
        onChange();
    }
</script>

<div class="node-editor-actions">
    <div class="node-editor-actions__left">
        <Button type={ButtonTypeEnum.primary} on:click={handleSidebarToggle} style={StylingUtility.defaultButton}>
            <div style="transform: rotate({$rotationDegrees}deg); transition: transform 0.2s;">
                <Icon name={IconNameEnum.chevron_right} />
            </div>
        </Button>
        {#if $selectedNodeTitle !== undefined && nodeNameEditor}
            <div class="node-editor-actions__input">
                <TextInput style={StylingUtility.textInput} label="Node Title" on:change={onTitleChange} value={$selectedNodeTitle}
                ></TextInput>
            </div>
        {/if}
        <div class="node-editor-actions__color">
            <input class="color-input" type="color" value={$selectedNodeColor ?? $xColor} on:change={onColorChange} />
        </div>
    </div>

    <div class="node-editor-actions__delete">
        <Button type="primary" style={StylingUtility.defaultButton} on:click={() => architectureStore.updateArchitectureSaveStatus()}> <Icon name={IconNameEnum.save} /></Button>
        <div class="vertical-line"> </div>
        <Button type={ButtonTypeEnum.primary} on:click={onDelete} style={StylingUtility.redButton}>Delete</Button>
        <Button type={ButtonTypeEnum.primary} on:click={onClearNodes} style={StylingUtility.whiteBorderButton}>Clear</Button>
    </div>
</div>

<style lang="scss">
    .node-editor-actions {
        display: flex;
        width: auto;
        align-items: flex-end;
        justify-content: space-between;
        padding: 16px;
        border-bottom: 1px solid #ffffff;

        &__left {
            display: flex;
            gap: 10px;
            width: 60%;
            height: 54px;
            align-items: flex-end;
        }

        &__input {
            width: 100%;
        }

        &__color {
            display: flex;
            flex-direction: column;
            gap: 2px;
            width: fit-content;
            align-items: center;
            white-space: nowrap;
            font-size: 12px;
        }

        &__delete {
            padding-right: 10px;
            display: flex;
            gap: 10px;
            .vertical-line {
                width: 2px;          
                height: max;            
                background-color: #ffffff;   
                margin: 0 10px;         
                display: flex;    

            }
        }
        
    }

    input[type='color'] {
        -webkit-appearance: none;
        border: none;
        cursor: pointer;
        width: 16px;
        height: 34px;
        padding: 0;
        background: none;
        border-radius: 10%;
    }

    input[type='color']::-webkit-color-swatch-wrapper {
        padding: 0;
        overflow: hidden;
    }

    input[type='color']::-webkit-color-swatch {
        border: 0px solid #ffffff;
    }
  

</style>
