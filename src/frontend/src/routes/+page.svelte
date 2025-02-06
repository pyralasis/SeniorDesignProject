<script lang="ts">
    import Logo from '$lib/assets/logo-3.svg';
</script>

<div class="home-page">
    <div class="content">
        <div class="logo-container">
            <img src={Logo} alt="Home Page" />
        </div>
        <div class="link-container">
            <a href="/architectures">Architectures</a>
            <a href="/general-layout">Models</a>
            <a href="/pipelines">Pipelines</a>
            <a href="/general-layout">Training</a>
        </div>
    </div>
</div>

<style lang="scss">
    .home-page {
        display: flex;
        height: 100vh;
        justify-content: center;
        align-items: center;
        gap: 70px;
        background: url('$lib/assets/background.png') no-repeat center center fixed;
        background-size: cover;
    }

    .content {
        display: flex;
        justify-content: center;
        gap: 120px;
        height: fit-content;
    }

    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    img {
        width: 350px;
    }

    .link-container {
        display: flex;
        flex-direction: column;
        height: auto;
        align-items: start;
        justify-content: space-between;
    }

    a {
        width: 100%;
        align-items: center;
        text-decoration: none;
        color: #ffffff;
        font-size: 32px;
        font-weight: 600;
        border: 1px solid transparent;

        &:hover {
            color: #b91c1c;
            transition: all 0.3s ease;
        }
    }
</style>
