<script>
	import { createPopper } from '@popperjs/core';
	import { createEventDispatcher, onMount, setContext } from 'svelte';
	import { createPopoverStore } from './PopoverStore.js';

	export let id = '';
	export let selectedItems = [];
	export let position = 'bottom';

	let popoverElement;
	let popperInstance;

	let popoverStore = createPopoverStore(id, selectedItems);
	setContext('popoverStore', popoverStore);

	const dispatch = createEventDispatcher();

	const popoverOverOpenedDispatch = () => {
		dispatch('popoverOverOpened', id);
	};

	const popoverOverClosedDispatch = () => {
		dispatch('popoverOverClosed', id);
	};

	const popoverItemsChangedDispatch = () => {
		dispatch('popoverItemsChanged', { id: id, selectedItems: $popoverStore.selectedItems });
	};

	function getTriggerElement() {
		return popoverElement.querySelector('#trigger');
	}

	function getContentElement() {
		return popoverElement.querySelector('#content');
	}

	function createPopperInstance() {
		const triggerElement = getTriggerElement();
		const contentElement = getContentElement();

		if (triggerElement && contentElement) {
			popperInstance = createPopper(triggerElement, contentElement, {
				placement: position,
				modifiers: [
					{
						name: 'offset',
						options: {
							offset: [0, 4] // Adjust this value to bring the popover closer to the trigger
						}
					},
					{
						name: 'preventOverflow',
						options: {
							padding: 8
						}
					}
				]
			});
		}
	}

	$: $popoverStore.selectedItems, popoverItemsChangedDispatch();
	$: {
		if ($popoverStore.isOpen) {
			popoverOverOpenedDispatch();
			popperInstance?.update();
		} else {
			popoverOverClosedDispatch();
		}
	}

	onMount(async () => {
		createPopperInstance();
		popperInstance.update();
	});
</script>

<div class="popover" aria-haspopup="true" aria-expanded="true" bind:this={popoverElement}>
	<slot name="trigger" />
	<slot name="content" />
</div>

<style>
	.popover {
		width: fit-content;
	}
</style>
