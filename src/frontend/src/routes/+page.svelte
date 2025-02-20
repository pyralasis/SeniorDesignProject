<script lang="ts">
    import Logo from '$lib/assets/logo-5.svg';
    import Design from '$lib/assets/Cool Neural network design.png';
</script>

<div class="home-page">
    <div class="logo-container">
        <img src={Logo} alt="Home Page" />
    </div>
    <div class="link-container">
        <a href="/select-architecture">Architectures</a>
        <a href="/general-layout">Models</a>
        <a href="/general-layout">Pipelines</a>
        <a href="/general-layout">Training</a>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <a href="https://github.com/pyralasis/SeniorDesignProject" target="_blank" class="footer-link">GitHub</a>
        </div>
    </footer>
</div>



<style lang="scss">

    .home-page {
        height: 100%;
        width: 100%;
        overflow: hidden;
    }

    .content {
        display: flex;
        flex-direction: column;
        height: 100%; 
        background: url('$lib/assets/CheckeredBackground.png') no-repeat center center fixed;
        background-size: cover; 
        min-height: 100vh;
    }

    .container {
        max-width: 1200px;
        width: 100%;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        flex-grow: 1; 
    }
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: relative; /* Needed for absolute positioning of border */
    }

    .nav-bar__left {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    img {
        width: 250px;
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
        border: 1px solid transparent;
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
