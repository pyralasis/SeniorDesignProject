<script>
	export let title = '';
	export let color = 'navy';
	export let href = '';
</script>

<a
	class="home-card"
	class:navy={color === 'navy'}
	class:red={color === 'red'}
	class:green={color === 'green'}
	{href}
>
	<span class="title">
		{title}
	</span>
	<slot></slot>
</a>

<style>
	@import '../../../variables.css';
	.home-card {
		width: 450px;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		border-radius: 16px;
		box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
		text-decoration: none;
		position: relative;
		padding: 16px;
		overflow: hidden;
		box-sizing: border-box;
		flex-grow: 1;
	}

	.title {
		font-size: 38px;
		color: var(--color-baige);
		font-weight: 700;
	}

	.navy {
		background-color: var(--color-navy);
	}

	.navy:hover {
		background-color: var(--color-navy-dark);
	}

	.red {
		background-color: var(--color-red);
	}

	.red:hover {
		background-color: var(--color-red-dark);
	}

	.green {
		background-color: var(--color-green);
	}

	.green:hover {
		background-color: var(--color-green-dark);
	}
</style>
