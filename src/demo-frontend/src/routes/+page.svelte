<script lang="ts">
    import { onMount } from 'svelte';
    import { Button } from 'kiwi-nl';
    import { StylingUtility } from '$lib/utilities/styling.utility';
    import Logo from '$lib/assets/logo-5.svg';

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    let socket: WebSocket;
    let drawing = false;
    let predictedNumber = '';

    onMount(() => {
        ctx = canvas.getContext('2d')!;
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        socket = new WebSocket('ws://localhost:8080');
        socket.onopen = () => console.log('WebSocket connected');
        socket.onmessage = (event: MessageEvent) => {
            try {
                const data = JSON.parse(event.data);
                predictedNumber = data.prediction;
            } catch (error) {
                console.error('Error parsing message:', error);
            }
        };
        socket.onerror = (error) => console.error('WebSocket error:', error);
    });

    function startDrawing(event: PointerEvent) {
        drawing = true;
        draw(event);
    }

    function stopDrawing() {
        drawing = false;
        ctx.beginPath();
    }

    function draw(event: PointerEvent) {
        if (!drawing) return;

        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const pressure = event.pressure || 0.5;

        ctx.lineWidth = pressure * 20;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'white';

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }
    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        predictedNumber = '';
    }

    function submitDrawing() {
        const offCanvas = document.createElement('canvas');
        offCanvas.width = 28;
        offCanvas.height = 28;
        const offCtx = offCanvas.getContext('2d')!;
        offCtx.drawImage(canvas, 0, 0, offCanvas.width, offCanvas.height);

        const imageData = offCtx.getImageData(0, 0, offCanvas.width, offCanvas.height);
        const data = imageData.data;
        const matrix: number[][] = [];

        for (let i = 0; i < 28; i++) {
            let row: number[] = [];
            for (let j = 0; j < 28; j++) {
                const index = (i * 28 + j) * 4;
                const pixel = data[index];
                const normalized = pixel / 255;
                row.push(normalized);
            }
            matrix.push(row);
        }

        // Send the 28x28 matrix via WebSocket as JSON.
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ image: matrix }));
        } else {
            console.error('WebSocket is not open');
        }
    }
</script>

<main>
    <div class="logo"><img src={Logo} alt="Home Page" /></div>
    <div class="canvas">
        <canvas
            bind:this={canvas}
            width="360"
            height="360"
            on:pointerdown={startDrawing}
            on:pointermove={draw}
            on:pointerup={stopDrawing}
            on:pointerleave={stopDrawing}
        ></canvas>
        <!-- Control buttons -->
        <div class="buttons">
            <Button on:click={submitDrawing} style={StylingUtility.whiteBorderButton}>Submit</Button>
            <Button on:click={clearCanvas} style={StylingUtility.redButton}>Clear</Button>
        </div>
        <!-- Display the prediction from the WebSocket -->
        <div>
            <h2>Number: {predictedNumber}</h2>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: #111111;
        color: white;
        font-family: 'Inter', sans-serif;
        margin: 0;
        padding: 0;
    }

    .logo {
        width: 35px;
        height: 35px;
        position: fixed;
        top: 10px;
        left: 10px;

        img {
            width: 100%;
            height: 100%;
        }
    }

    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: url('$lib/assets/PatternAsset.png') repeat center center;
        height: 100vh;
        align-items: center;
        justify-content: center;
    }

    canvas {
        border: 1px solid white;
        touch-action: none;
        cursor: crosshair;
    }

    .buttons {
        display: flex;
        width: 100%;
        justify-content: space-between;
        padding-top: 10px;
    }
</style>
