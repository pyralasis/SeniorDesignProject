<script>
	export let type = 'default';
	export let size = 'default';
</script>

<span
	class="text"
	class:default={type === 'default'}
	class:light={type === 'light'}
	class:small={size === 'small'}
>
	<slot></slot>
</span>

<style>
	.text {
		color: var(--color-text);
		font-size: 16px;
	}

	.light {
		color: #787878;
	}

	.small {
		font-size: 13px;
	}
</style>
