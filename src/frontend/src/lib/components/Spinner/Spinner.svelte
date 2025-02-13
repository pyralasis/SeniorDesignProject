<script lang="ts">
</script>

<div class="loading-animation">
    <div class="top-left">
        <svg class="square"></svg>
        <svg class="square white"></svg>
        <svg class="square"></svg>
        <svg class="square white"></svg>
        <svg class="square"></svg>
        <svg class="square white"></svg>
        <svg class="square"></svg>
        <svg class="square white"></svg>
        <svg class="square"></svg>
    </div>
    <svg class="square white right-top" />
    <svg class="square white right-bottom" />
    <svg class="square white bottom-right" />
    <svg class="square white bottom-left" />
</div>

<style>
    .loading-animation {
        width: 36px;
        height: 36px;
        position: relative;
        animation: rotateEntire 4s infinite;
    }

    .top-left {
        display: flex;
        flex-wrap: wrap;
        width: 36px;
        height: 36px;
        animation: rotateSpringPauseTopLeft 4s infinite;
    }

    .square {
        background-color: transparent;
        width: 12px;
        height: 12px;
    }

    .white {
        background-color: #ffffff;
        /* outline: 1px solid #ffffff; */
    }

    .right-top {
        position: absolute;
        right: -12px;
        top: 0;
        animation:
            slideLeft 4s infinite,
            topRight 4s infinite;
    }

    .right-bottom {
        position: absolute;
        right: -12px;
        top: 24px;
        animation:
            slideLeft 4s infinite,
            bottomRight 4s infinite;
    }

    .bottom-left {
        position: absolute;
        left: 0;
        top: 36px;
        animation:
            slideUp 4s infinite,
            bottomLeft 4s infinite;
    }

    .bottom-right {
        position: absolute;
        left: 24px;
        top: 36px;
        animation:
            slideUp 4s infinite,
            bottomRight 4s infinite;
    }

    @keyframes rotateSpringPauseTopLeft {
        0% {
            transform: rotate(0deg);
        }
        20% {
            transform: rotate(390deg);
        }
        25% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    @keyframes slideLeft {
        0%,
        31.25% {
            transform: translateX(0);
        }
        43.75% {
            transform: translateX(-12px);
        }
        93.75% {
            transform: translateX(-12px);
        }
        100% {
            transform: translateX(0);
        }
    }

    @keyframes slideUp {
        0%,
        31.25% {
            transform: translateY(0);
        }
        43.75% {
            transform: translateY(-12px);
        }
        93.75% {
            transform: translateY(-12px);
        }
        100% {
            transform: translateY(0);
        }
    }

    @keyframes rotateEntire {
        0%,
        50% {
            transform: rotate(0deg);
        }
        70% {
            transform: rotate(390deg);
        }
        75% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    @keyframes topRight {
        0%,
        31.25% {
            border-radius: 0 0 0 0;
        }
        43.75% {
            border-radius: 0 16px 0 0;
        }
        93.75% {
            border-radius: 0 16px 0 0;
        }
        100% {
            border-radius: 0 0 0 0;
        }
    }

    @keyframes bottomRight {
        0%,
        31.25% {
            border-radius: 0 0 0 0;
        }
        43.75% {
            border-radius: 0 0 16px 0;
        }
        93.75% {
            border-radius: 0 0 16px 0;
        }
        100% {
            border-radius: 0 0 0 0;
        }
    }
    @keyframes bottomLeft {
        0%,
        31.25% {
            border-radius: 0 0 0 0;
        }
        43.75% {
            border-radius: 0 0 0 16px;
        }
        93.75% {
            border-radius: 0 0 0 16px;
        }
        100% {
            border-radius: 0 0 0 0;
        }
    }
</style>
