<script lang="ts">
  import { type Writable, writable } from "svelte/store";
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import { Button, InputSeries } from "kiwi-nl";
  import { StylingUtility } from "$lib/utilities/styling.utility";
  import { HandleStatusEnum, type HandleStatus } from "./handle-status.enum";

  type $$Props = NodeProps;

  export let data: $$Props["data"] = {};
  export let id: $$Props["id"] = "";
  export let selected: $$Props["selected"] = false;

  const color: Writable<string> = data?.color as Writable<string>;
  const outputSize: Writable<string[]> = data?.outputSize as Writable<string[]>;
  const rightConnected: Writable<boolean> =
    data?.rightConnected as Writable<boolean>;
  const rightStatus: Writable<HandleStatus> =
    data?.rightStatus as Writable<HandleStatus>;
  let sizeDimensions = writable<number>($outputSize.length);
  function toggleConnection(connected: boolean) {
    $rightConnected = connected;
  }

  function getBackgroundColor(connected: boolean, status: HandleStatus) {
    if (!connected) {
      return "#333";
    } else {
      switch (status) {
        case HandleStatusEnum.default:
          return "#FFF";
        case HandleStatusEnum.error:
          return "red";
        case HandleStatusEnum.success:
          return "green";
      }
    }
  }
</script>

<Handle
  type="source"
  position={Position.Right}
  style="
    background-color: {getBackgroundColor($rightConnected, $rightStatus)};
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
  class="input-node"
  style="
        outline: {selected ? '1.5' : '1'}px solid {$color +
    (selected ? 'ff' : '69')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div class="input-node__header node__header">
    <Button
      style={StylingUtility.defaultButton}
      on:click={() => {
        sizeDimensions.update((value) => value - 1);
        $outputSize.pop();
      }}>-</Button
    >Input <Button
      style={StylingUtility.defaultButton}
      on:click={() => {
        sizeDimensions.update((value) => value + 1);
      }}>+</Button
    >
  </div>
  <div class="input-node__content">
    <InputSeries
      style={StylingUtility.inputSeries}
      label={"Input Size"}
      maxlength={2}
      inputamount={$sizeDimensions}
      value={$outputSize}
      type="digit"
    />
  </div>
</div>

<style lang="scss">
  .input-node {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 3px 7px #78787843;
    width: fit-content;

    &__header {
      display: flex;
      flex-direction: row;
      gap: 16px;
      align-items: center;
      justify-content: center;
      cursor: grab;
      color: #ffffff;
      background: #070707;
      height: 45px;
      padding: 0 8px;
      font-size: 12px;
      font-weight: 600;

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
  }
</style>
