<script>
	import { createEventDispatcher, getContext } from 'svelte';
	import Text from '$lib/components/Text/Text.svelte';

	export let tabnum;

	let dispatch = createEventDispatcher();
	const tabsStore = getContext('tabsStore');
	let active;

	$: $tabsStore.activeTab, (active = $tabsStore.activeTab === tabnum);
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="tab-label" class:active on:click={tabsStore.setActiveTab(tabnum)}>
	<Text>
		<slot></slot>
	</Text>
</div>

<style>
	.tab-label {
		padding: 8px 16px;
		cursor: pointer;
		border-bottom: 2px solid transparent;
	}

	.tab-label:hover {
		background-color: var(--color-surface-dark);
		border-bottom: 2px solid var(--color-edge-dark);
	}

	.active {
		border-bottom: 2px solid var(--color-green);
		font-weight: 600;
	}

	.active:hover {
		border-bottom: 2px solid var(--color-green);
	}
</style>
