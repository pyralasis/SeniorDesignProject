<script>
	import { createEventDispatcher } from 'svelte';
	export let label;
	export let required = false;
	export let checked = false;

	let checkbox;

	const dispatch = createEventDispatcher();
	function handleChange(event) {
		dispatch('change', { value: event.target.checked });

		const ripple = document.createElement('div');
		ripple.classList.add('checkbox-ripple');
		if (event.target.checked) {
			ripple.style.backgroundColor = 'var(--color-green)';
		} else {
			ripple.style.backgroundColor = 'var(--color-edge-darker)';
		}
		checkbox.appendChild(ripple);

		setTimeout(() => {
			ripple.remove();
		}, 1000);
	}
</script>

<div class="checkbox">
	<div class="checkbox-inner" bind:this={checkbox}>
		<input type="checkbox" {required} bind:checked on:change={handleChange} />
	</div>
	{#if label}
		<div class="checkbox-label">
			{label}
		</div>
	{/if}
</div>

<style>
	.checkbox {
		display: flex;
		align-items: center;
		gap: 8px;
		width: fit-content;
	}

	.checkbox-inner {
		width: var(--size-lg);
		height: var(--size-lg);
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
	}

	.checkbox-inner input {
		width: var(--size-md);
		height: var(--size-md);
		z-index: 2;
		accent-color: var(--color-green);
	}

	.checkbox-label {
		font-weight: 500;
		color: var(--color-text);
	}

	:global(.checkbox-ripple) {
		position: absolute;
		border-radius: 50%;
		width: 40%;
		height: 40%;
		animation: ripple 0.75s forwards;
		pointer-events: none;
		z-index: 1;
		top: 50%;
		left: 50%;
	}

	@keyframes ripple {
		from {
			opacity: 1;
			transform: translate(-50%, -50%) scale(0);
		}
		to {
			opacity: 0;
			transform: translate(-50%, -50%) scale(4);
		}
	}
</style>
