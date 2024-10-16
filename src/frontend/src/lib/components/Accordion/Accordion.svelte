<script>
	import { setContext } from 'svelte';
	import { createAccordionStore } from './accordionStore.js';

	const accordionStore = createAccordionStore();
	setContext('accordionStore', accordionStore);
</script>

<div class="accordion">
	<div class="accordion-header">
		<slot name="header"></slot>
	</div>
	<div class="accordion-body">
		<slot name="body"></slot>
	</div>
</div>

<style>
	.accordion {
		overflow: hidden;
		border-radius: var(--size-sm);
		border: 1px solid var(--color-edge);
	}
</style>
