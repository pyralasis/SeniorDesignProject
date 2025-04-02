<script lang="ts">
    import Logo from '$lib/assets/logo-5.svg';
</script>

<div class="home-page">
    <div class="content">
        <div class="left-container">
            <img src={Logo} alt="Home Page" />
        </div>
        <div class="right-container">
            <a href="/architectures">
                <h1>Architectures</h1>
                <p>
                  An Architecture is the blueprint of your neural network, composed of layers with specific parameters and connections that determine how data flows through the system. In our Architecture Editor, you can easily create or select an Architecture by dragging, dropping, and connecting available layer types to build your desired model.
                </p>
                <strong>Supported layer types:</strong>
                <ul class="supported-layers">
                    <li>ReLU</li>
                    <li>2D Convolution</li>
                    <li>Linear</li>
                    <li>2D Max Pooling</li>
                </ul>
              </a>
            <a href="/pipelines"> <h1>Pipelines </h1> <p>A Pipeline defines how data flows and is transformed before it reaches your model, letting you chain together sources and operations in a logical sequence. From the 'Pipeline' page, you can create a new pipeline or pick an existing one, then use the Pipeline Editor to drag and configure data steps. This approach ensures you can easily prepare and pass data to your model for training, all within an intuitive, visual environment</p></a>
            <a href="/models"><h1> Models</h1> <p>A Model is a fully realized version of your neural network architecture, capturing all the parameters needed for training and inference. Once you convert an architecture into a model, you can train it on your chosen data using various optimizers, loss functions, and hyperparameters. This page provides a streamlined interface for configuring and running those training experiments</p></a>
            <a href="/training"><h1> Training </h1> <p> The Training Page will show you the list of models and the progress you've made on certain models during and post testing. While the model is testing, you will see the status it's made with the number of epochs completed</p></a>
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


    a {
        width: 100%;
        text-decoration: none;
 
        border-top: 1px solid #ffffff;
        height: 15%;
        transition:
            color 0.3s ease,
            height 0.5s ease-in-out;
        padding: 38px 0 0 16px;
        &:hover {
            
            height: 40%;
            h1 {
                color: #fe2e00;
            }
            p, strong {
                opacity: 1;     
                visibility: visible;
                font-size: 20px;
            }
            .supported-layers {   
                opacity: 1;               /* Fade in */
                visibility: visible;
            }
        }
        h1 {
            font-size: 24px;
            color: #ffffff;
            margin: 0;
        }
        p, strong {
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.5s ease;
            color: #ffffff;
            padding-right: 300px;
        }
        .supported-layers {
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.5s ease;
            color: #ffffff;
            font-size: 16px;
        }
        .supported-layers li {
            margin-bottom: 4px;
        }
    }
</style>
