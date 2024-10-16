<script>
	import { getContext } from 'svelte';
	import Checkbox from '$lib/components/Checkbox/Checkbox.svelte';
	import PopoverContent from '../PopoverContent.svelte';
	const popoverStore = getContext('popoverStore');

	export let items = [];

	function setSelectedItem(selected, value) {
		if ($popoverStore.selectedItems) {
			const label = items.find((item) => item.value === value).label;

			if (selected) {
				popoverStore.updateItems([...$popoverStore.selectedItems, { value, label }]);
			} else {
				popoverStore.updateItems(
					$popoverStore.selectedItems.filter((item) => item.value !== value)
				);
			}
		}
	}
</script>

<PopoverContent>
	<div slot="custom-content" class="popover-multi-select-content">
		{#each items as item}
			<Checkbox
				on:change={(event) => setSelectedItem(event.detail.value, item.value)}
				label={item.label}
			/>
		{/each}
	</div>
</PopoverContent>

<style>
	.popover-multi-select-content {
		display: flex;
		flex-direction: column;
	}
</style>
