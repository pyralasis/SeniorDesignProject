<script>
	import { getContext } from 'svelte';

	const popoverStore = getContext('popoverStore');

	function handleClick() {
		popoverStore.toggle();
	}
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div id="trigger" class="popover-trigger" on:click={handleClick}>
	<slot name="custom-trigger"></slot>
</div>

<style>
	.popover-trigger {
		cursor: pointer;
		width: fit-content;
	}
</style>
