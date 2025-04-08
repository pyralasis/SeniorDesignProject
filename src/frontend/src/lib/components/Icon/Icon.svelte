<script lang="ts">
  import { iconNameSvgMapping } from "./types/icon-name-svg-mapping";
  import { IconNameEnum, type IconName } from "./types/icon-name.enum";

  export let name: IconName;
</script>

<div class="icon">
  {@html iconNameSvgMapping[name]}
</div>

<style>
  .icon {
    width: 16px;
    height: 18px;
  }
</style>
