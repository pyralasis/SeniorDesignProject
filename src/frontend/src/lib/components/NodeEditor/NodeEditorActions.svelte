<script lang="ts">
    import { Button, ButtonTypeEnum, TextInput } from 'kiwi-nl';
    import { getContext } from 'svelte';
    import { writable, type Writable } from 'svelte/store';
    import Icon from '../Icon/Icon.svelte';
    import { IconNameEnum } from '../Icon/types/icon-name.enum';

    export let selectedNodeTitle: Writable<string> | undefined;
    export let selectedNodeColor: Writable<string> | undefined;
    export let onDelete: () => void;
    export let onClearNodes: () => void;

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
    }

    function onColorChange(event: Event) {
        if (!selectedNodeColor) {
            xColor.update((color) => (color = `${(event.target as HTMLInputElement).value ?? '#fff'}`));
            return;
        }
        selectedNodeColor.update((color) => (color = `${(event.target as HTMLInputElement).value ?? '#fff'}`));
    }
</script>

<div class="node-editor-actions">
    <div class="node-editor-actions__left">
        <Button type={ButtonTypeEnum.secondary} on:click={handleSidebarToggle}>
            <div style="transform: rotate({$rotationDegrees}deg); transition: transform 0.2s;">
                <Icon name={IconNameEnum.chevron_right} />
            </div>
        </Button>
        <div class="node-editor-actions__color">
            <input class="color-input" type="color" value={$selectedNodeColor ?? $xColor} on:change={onColorChange} />
        </div>
        <div class="node-editor-actions__input" style="visibility: {$selectedNodeTitle ? 'visible' : 'hidden'};">
            <TextInput label="Node Title" on:change={onTitleChange} value={$selectedNodeTitle}></TextInput>
        </div>
    </div>
    <div class="node-editor-actions__delete">
        <Button type={ButtonTypeEnum.secondary} on:click={onDelete}>Delete</Button>
        <Button type={ButtonTypeEnum.primary} on:click={onClearNodes}>Clear</Button>
    </div>
</div>

<style lang="scss">
    .node-editor-actions {
        display: flex;
        width: auto;
        align-items: center;
        justify-content: space-between;
        padding: 16px;
        border-bottom: 2px solid #eaeaea;

        &__left {
            display: flex;
            gap: 10px;
            width: 60%;
            align-items: center;
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
        }
    }

    input[type='color'] {
        -webkit-appearance: none;
        border: none;
        cursor: pointer;
        width: 25px;
        height: 25px;
        padding: 0;
        background: none;
        box-shadow: inset 0 0 10px #ad3b3b;
    }

    input[type='color']::-webkit-color-swatch-wrapper {
        padding: 0;
        border-radius: 50%;
        overflow: hidden;
    }

    input[type='color']::-webkit-color-swatch {
        border-radius: 50%;
    }

    input[type='color'] {
        border-radius: 50%;
        border: 1px solid #f1f1f1;
    }
</style>
