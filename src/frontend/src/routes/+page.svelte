<script lang="ts">
    import Logo from '$lib/assets/logo-2.svg';
</script>

<div class="home-page">
    <div class="logo-container">
        <img src={Logo} alt="Home Page" />
    </div>
    <div class="link-container">
        <a href="/general-layout">Architectures</a>
        <a href="/general-layout">Models</a>
        <a href="/general-layout">Pipelines</a>
        <a href="/general-layout">Training</a>
    </div>
</div>

<style lang="scss">
    .home-page {
        display: flex;
        flex-direction: column;
        height: 100vh;
        justify-content: center;
        align-items: center;
        gap: 70px;
    }

    .logo-container {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    img {
        width: 200px;
    }

    .link-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        justify-content: center;
        gap: 16px;
    }

    a {
        text-decoration: none;
        color: #ffffff;
        font-size: 28px;
        font-weight: 600;
        height: 80px;
        width: 200px;
        border: 1px solid #000000;
        display: flex;
        align-items: center;
        justify-content: center;

        &:hover {
            border: 1px solid #b91c1c;
            color: #b91c1c;
            transition: all 0.3s ease;
        }
    }
</style>
