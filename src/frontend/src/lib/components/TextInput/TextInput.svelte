<script>
	import { createEventDispatcher } from 'svelte';
	export let label = '';
	export let placeholder = '';
	export let required = false;
	export let value = '';

	const dispatch = createEventDispatcher();

	function handleChange(event) {
		dispatch('change', { value: event.target.value });
	}
</script>

<div class="container">
	<div class="entryarea">
		<input type="text" {required} {placeholder} bind:value on:change={handleChange} />
		<div class="labelline">
			{label}
		</div>
	</div>
</div>

<style>
	@import '../../../variables.css';
	.container {
		width: auto;
	}

	.entryarea {
		position: relative;
		height: 40px;
		line-height: 40px;
	}

	input {
		position: absolute;
		width: 100%;
		box-sizing: border-box;
		border: none;
		font-size: 16px;
		color: var(--color-text);
		padding: 0 30px;
		height: 40px;
		border-radius: var(--size-xs);
		outline: 1px solid var(--color-edge-darker);
		background: transparent;
		transition: 0.1s ease-in-out;
		z-index: 1111;
	}

	input:hover {
		outline: 2px solid var(--color-edge-darker);
	}

	.labelline {
		position: absolute;
		font-size: 16px;
		color: var(--color-text-lighter);
		padding: 0 8px;
		background-color: var(--color-surface);
		transition: 0.1s ease-in-out;
		width: fit-content;
		margin-left: 20px;
	}

	input:focus + .labelline,
	input:valid + .labelline {
		height: 25px;
		line-height: 25px;
		transform: translate(0, -15px) scale(0.8);
		padding: 0 8px;
		z-index: 1111;
	}

	input:focus + .labelline {
		color: var(--color-green);
	}

	input:focus {
		outline: 2px solid var(--color-green);
	}
</style>
