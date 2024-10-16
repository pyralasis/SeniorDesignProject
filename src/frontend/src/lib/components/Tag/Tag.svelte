<script>
	export let color = 'green';
	export let size = 'md';
</script>

<div
	class="tag"
	class:green={color === 'green'}
	class:gray={color === 'gray'}
	class:orange={color === 'orange'}
	class:red={color === 'red'}
	class:navy={color === 'navy'}
	class:sm={size === 'sm'}
	class:md={size === 'md'}
	class:lg={size === 'lg'}
>
	<slot></slot>
</div>

<style>
	.tag {
		display: flex;
		align-items: center;
		justify-content: center;
		width: fit-content;
		height: fit-content;
		padding: var(--size-xs) var(--size-sm);
		border-radius: var(--border-radius-lg);
		font-size: 12px;
		font-weight: 600;
		border: 2px solid transparent;
	}

	.sm {
		font-size: 8px;
		border-width: 2px;
		padding: var(--size-xs) var(--size-sm);
	}

	.lg {
		font-size: 16px;
		padding: var(--size-xs) var(--size-md);
	}

	.green {
		color: var(--color-green);
		border-color: var(--color-green);
	}

	.red {
		color: var(--color-red);
		border-color: var(--color-red);
	}

	.orange {
		color: var(--color-orange);
		border-color: var(--color-orange);
	}

	.gray {
		color: var(--color-edge-darker);
		border-color: var(--color-edge-darker);
	}

	.navy {
		color: var(--color-navy);
		border-color: var(--color-navy);
	}
</style>
