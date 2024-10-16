<script>
	import { getContext } from 'svelte';
	const popoverStore = getContext('popoverStore');
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div id="content" class="popover-content" class:hidden={!$popoverStore.isOpen}>
	<slot name="custom-content"></slot>
</div>

<style>
	.popover-content {
		padding: 8px 16px;
		background-color: var(--color-surface);
		box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.2);
	}

	.hidden {
		display: none;
	}
</style>
