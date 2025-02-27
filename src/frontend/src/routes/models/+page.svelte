<script>
    import { StylingUtility } from "$lib/utilities/styling.utility";


    import { Button } from "kiwi-nl";

</script>

<div class="model-page">
    <div class="model-page__top">
        <div class="model-page__top-left">
            <p>
                Select the model you would like to train...
            </p>
            
        </div>
    </div>
</div>

<style lang="scss">

    .model-page {
        display: flex;
        flex-direction: column;
        justify-content: start;
        overflow: hidden;
        height: 100%;
        color: #ffffff;

        &__header {
            color: #ffffff;
            border-bottom: 1px solid #ffffff;
            padding: 20px;
            padding-left: 64px;
            h1 {
                font-size: 50px;
                font-weight: 500;
                margin: 0;
            }
        }

        &__top {
            display: flex;
            justify-content: space-between;
            height: 75%;
            max-width: 1500px;
            margin: 64px auto;
        }

        &__bottom {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #ffffff;
            padding: 32px 64px;
            height: 35%;
        }

        &__bottom-left {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 65%;
        }

        &__bottom-right {
            display: flex;
            gap: 10px;
            max-width: 60%;
            height: 38px;
        }
        &__top-left {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 30%;

            p {
                color: #ffffff;
            }
        }
    }
</style>