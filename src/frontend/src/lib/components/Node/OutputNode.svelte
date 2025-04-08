<script lang="ts">
  import { type Writable } from "svelte/store";
  import { Handle, Position, type NodeProps } from "@xyflow/svelte";
  import { HandleStatusEnum, type HandleStatus } from "./handle-status.enum";

  type $$Props = NodeProps;

  export let data: $$Props["data"] = {};
  export let id: $$Props["id"] = "";
  export let selected: $$Props["selected"] = false;

  const color: Writable<string> = data?.color as Writable<string>;
  const leftConnected: Writable<boolean> =
    data?.leftConnected as Writable<boolean>;
  const leftStatus: Writable<HandleStatus> =
    data?.leftStatus as Writable<HandleStatus>;

  function toggleConnection(connected: boolean) {
    $leftConnected = connected;
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
  type="target"
  position={Position.Left}
  style="
    background-color: {getBackgroundColor($leftConnected, $leftStatus)};
    border-color: {$color + (selected ? 'ff' : '69')};
    border-radius: 0;
    height: 8px;
    width: 6px;
"
  onconnect={() => toggleConnection(true)}
  ondisconnect={() => toggleConnection(false)}
  isConnectable={!$leftConnected}
/>
<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="output-node"
  style="
        outline: {selected ? '1.5' : '1'}px solid {$color +
    (selected ? 'ff' : '69')};
        cursor: pointer;
        transition: outline 0.2s;
    "
>
  <div class="output-node__header node__header">Output</div>
</div>

<style lang="scss">
  .output-node {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 3px 7px #78787843;
    width: 150px;

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
      font-size: 12px;
      font-weight: 600;

      &:active {
        cursor: grabbing;
      }
    }
  }
</style>
