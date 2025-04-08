<script lang="ts">
  import { type Writable } from "svelte/store";
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import NodeField from "./NodeParameter.svelte";
  import type { Parameter, ParameterValue } from "$lib/types/parameter";
  import { HandleStatusEnum, type HandleStatus } from "./handle-status.enum";

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
  const leftConnected: Writable<boolean> =
    data?.leftConnected as Writable<boolean>;
  const rightConnected: Writable<boolean> =
    data?.rightConnected as Writable<boolean>;

  function toggleConnection(side: "left" | "right", connected: boolean) {
    if (side === "left") {
      $leftConnected = connected;
    } else {
      $rightConnected = connected;
    }
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
  type="target"
  position={Position.Left}
  style="
        background-color: {getBackgroundColor($leftConnected)};
        border-color: {$color + (selected ? 'ff' : '69')};
        border-radius: 0;
        height: 8px;
        width: 6px;
    "
  onconnect={() => toggleConnection("left", true)}
  ondisconnect={() => toggleConnection("left", false)}
  isConnectable={!$leftConnected}
/>
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
  onconnect={() => toggleConnection("right", true)}
  ondisconnect={() => toggleConnection("right", false)}
  isConnectable={!$rightConnected}
/>
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="transform-node"
  style="
        outline: {selected ? '1.5' : '1'}px solid {$color +
    (selected ? 'ff' : '69')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="transform-node__header node__header">
    <div class="transform-node__title">Transform</div>
    <div class="transform-node__sub-title">{$name}</div>
  </div>
  {#if $parameters.length !== 0}
    <div class="transform-node__content">
      {#each $parameters as parameter}
        <NodeField parameter={parameter.parameter} value={parameter.value} />
      {/each}
    </div>
  {/if}
</div>

<style lang="scss">
  .transform-node {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 3px 7px #78787843;
    width: 250px;
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
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      cursor: default;
      background-color: #070707;
    }

    &__content-empty {
      font-size: 12px;
      color: #9f9f9f;
      width: 100%;
      text-align: center;
    }

    &__title {
      font-size: 12px;
      font-weight: 600;
    }
  }
</style>
