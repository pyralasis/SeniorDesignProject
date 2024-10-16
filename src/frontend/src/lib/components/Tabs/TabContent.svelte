<script>
	import { createEventDispatcher, getContext } from 'svelte';

	export let tabnum;
	const tabsStore = getContext('tabsStore');
	let active;

	$: active = $tabsStore.activeTab === tabnum;
</script>

{#if active}
	<div class="tab-content active">
		<slot></slot>
	</div>
{/if}

<style>
	.tab-content {
		width: auto;
		height: auto;
	}
</style>
