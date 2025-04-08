<script lang="ts">
  import { type Writable } from "svelte/store";
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import NodeField from "./NodeParameter.svelte";
  import type { Parameter, ParameterValue } from "$lib/types/parameter";

  type $$Props = NodeProps;

  export let data: $$Props["data"] = {};
  export let id: $$Props["id"] = "";
  export let selected: $$Props["selected"] = false;

  const color: Writable<string> = data?.color as Writable<string>;
  const name: Writable<string> = data?.name as Writable<string>;
  const parameters: Writable<
    { parameter: Parameter<any>; value: ParameterValue<any> }[]
  > = data?.parameters as Writable<
    { parameter: Parameter<any>; value: ParameterValue<any> }[]
  >;
  const rightConnected: Writable<boolean> =
    data?.rightConnected as Writable<boolean>;

  function toggleConnection(connected: boolean) {
    $rightConnected = connected;
  }

  function getBackgroundColor(connected: boolean) {
    if (!connected) {
      return "#333";
    } else {
      return "#FFF";
    }
  }
</script>

<Handle
  type="source"
  position={Position.Right}
  style="
        background-color: {getBackgroundColor($rightConnected)};
        border-color: {$color + (selected ? 'ff' : '69')};
        border-radius: 4px;
        height: 8px;
        width: 6px;
    "
  onconnect={() => toggleConnection(true)}
  ondisconnect={() => toggleConnection(false)}
  isConnectable={!$rightConnected}
/>
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="node"
  style="
        outline: {selected ? '1.5' : '1'}px solid {$color +
    (selected ? 'ff' : '69')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="node__header">
    <div class="node__title">Source</div>
    <div class="node__sub-title">{$name ? $name : "Untitled Layer"}</div>
  </div>
  <div class="node__content">
    {#each $parameters as parameter}
      <NodeField parameter={parameter.parameter} value={parameter.value} />
    {/each}
    {#if $parameters.length === 0}
      <div class="node__content-empty">No parameters for this source</div>
    {/if}
  </div>
</div>

<style lang="scss">
  .node {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    box-shadow: 0 3px 7px #78787843;
    width: 250px;
    background-color: #ffffff;
    transition: height 0.2s;

    &__header {
      display: flex;
      flex-direction: column;
      gap: 4px;
      align-items: center;
      justify-content: center;
      cursor: grab;
      color: #ffffff;
      background: #070707;
      height: 45px;

      &:active {
        cursor: grabbing;
      }
    }

    &__content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: default;
      border-top: 1px solid #ffffff;
      background-color: #070707;
      gap: 16px;
      padding: 16px;
    }

    &__title {
      font-size: 12px;
      font-weight: 600;
    }

    &__content-empty {
      font-size: 12px;
      color: #9f9f9f;
      width: 100%;
      text-align: center;
    }
  }
</style>
