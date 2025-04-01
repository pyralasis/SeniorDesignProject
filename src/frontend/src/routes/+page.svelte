<script lang="ts">
    import Logo from '$lib/assets/logo-5.svg';
</script>

<div class="home-page">
    <div class="content">
        <div class="left-container">
            <img src={Logo} alt="Home Page" />
        </div>
        <div class="right-container">
            <a href="/architectures">Architectures</a>
            <a href="/pipelines">Pipelines</a>
            <a href="/models">Models</a>
            <a href="/training">Training</a>
        </div>
    </div>
</div>

<style lang="scss">
    .home-page {
        height: 100%;
        box-sizing: border-box;
        width: 100%;
        overflow: hidden;
    }

    .content {
        display: flex;
        height: 100%;
        box-sizing: border-box;
    }

    .left-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50%;
        border-right: 1px solid #ffffff;
        background: url('$lib/assets/PatternAsset.png') repeat center center;
    }

    .right-container {
        display: flex;
        flex-direction: column;
        align-items: start;
        justify-content: end;
        width: 50%;
    }

    img {
        width: 321px;
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
        text-decoration: none;
        color: #ffffff;
        font-size: 32px;
        font-weight: 500;
        border-top: 1px solid #ffffff;
        height: 15%;
        transition:
            color 0.3s ease,
            height 0.5s ease-in-out;
        padding: 38px 0 0 16px;
        &:hover {
            color: #fe2e00;
            height: 40%;
        }
    }
</style>
