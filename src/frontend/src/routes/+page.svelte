<script lang="ts">
    import Logo from '$lib/assets/logo-3.svg';
    import Design from '$lib/assets/Cool Neural network design.png';
</script>

<div class="home-page">
    <div class="container">
        <nav class="nav-bar">
            <div class="nav-bar__left">
                <img src={Logo} alt="Home Page" />
                <div class="website-title">
                    <span class="white">Ch</span>
                    <span class="white red">e</span>
                    <span class="white">ck</span>
                </div>
            </div>
            <div class="nav-bar__right">
                <a href="/select-architecture">Architectures</a>
                <a href="/general-layout">Models</a>
                <a href="/general-layout">Pipelines</a>
            </div>
        </nav>
    </div>
        <!-- Divider for the line -->
        <div class="divider"></div>
    <div class="container">
        <!-- Content Section -->
        <div class="content">
            <div class="cta">
                <h2>Get Started with Creating or Loading a Model</h2>
                <div class="action-buttons">
                    <a href="/select-architecture" class="primary-button">Load Model Architecture</a>
                    <a href="/create-architecture" class="primary-button">Create Model Architecture</a>
                </div>
            </div>
            <!-- Neural Network Design Section -->
            <div class="neural-network-container">
                <img src={Design} alt="Neural Network Design" class="neural-network-img" />
            </div>
        </div>
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
    }

    .nav-bar__right {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    .divider {
        width: 100%;
        height: 1px;
        background-color: white;
        margin-bottom: 30px;
    }
    .website-title {
        margin-left: 20px;
        display: flex;
        align-items: center;
        font-size: 2rem;
        font-weight: bold;
    }

    .white {
        color: #ffffff;
        &.red {
            color: #dc2626;
        }
    }

    a {
        position: relative;
        text-decoration: none;
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
        transition: color 0.2s ease;

        &:hover {
            color: #dc2626;
            text-decoration: underline;
        }

        /* Cool Ripple Effect */
        &:hover::after {
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            width: 0;
            height: 100%;
            background-color: rgba(220, 38, 38, 0.5);
            transform: translateX(-50%);
            animation: ripple 0.6s ease-out;
        }
    }

    .cta {
        text-align: center;
        margin-top: 100px; /* Pushes the buttons down a bit */
    }

    .cta h2 {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 30px;
    }

    .action-buttons {
        display: flex;
        justify-content: center;
        gap: 40px;
    }

    .primary-button {
        padding: 20px 50px;
        font-size: 1.5rem;
        background-color: rgba(220, 38, 38, 0.8);
        color: white;
        border: 2px solid white;
        border-radius: 5px;
        transition: background-color 0.3s ease, transform 0.3s ease;
        text-decoration: none;
    }

    .primary-button:hover {
        background-color: #dc2626;
        transform: scale(1.05);
    }

    @keyframes ripple {
        to {
            width: 100%;
            opacity: 0;
        }
    }

    .content {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    img {
        width: 100%;
        height: auto;
    }


    .neural-network-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }

    .neural-network-img {
        max-width: 80%;  
        height: auto;
    }

    .footer {
        padding: 20px 0;
        text-align: center;
        border-top: 1px solid white; 
        width: 100%;
    }

    .footer-content {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
        margin-top: 10px;
    }

    .footer-link {
        color: white;
        text-decoration: none;
        font-size: 1.1rem;
        transition: color 0.3s ease;
    }

    .footer-link:hover {
        color: #dc2626;
    }
</style>
