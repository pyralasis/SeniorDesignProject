<script lang="ts">
    import { onMount } from "svelte";
    import { Button, Popover, PopoverChipTrigger, PopoverSingleSelectContent, type PopoverItem } from "kiwi-nl";
    import { StylingUtility } from "$lib/utilities/styling.utility";
    import Logo from "$lib/assets/logo-5.svg";
    import { ApiUtility, type ModelObjectDesc } from "$lib/utilities/api-utility";
    import { writable, type Writable } from "svelte/store";

    let canvas: HTMLCanvasElement;
    let ctx: CanvasRenderingContext2D;
    let socket: WebSocket;
    let drawing = $state(false);
    let predictedNumber = $state("");

    let models: Writable<ModelObjectDesc[]> = writable([]);
    let selected_model: undefined | PopoverItem = $state();

    const refreshModels = async () => {
        models.set(await ApiUtility.get_models());
    };

    onMount(async () => {
        await refreshModels();

        ctx = canvas.getContext("2d")!;
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    });

    $effect(() => {
        if (drawing) {
            let handle = setInterval(submitDrawing, 200);
            return () => clearInterval(handle);
        } else {
            submitDrawing();
        }
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
        const pressure = event.pressure || 0.65;

        ctx.lineWidth = pressure * 30;
        ctx.lineCap = "round";
        ctx.strokeStyle = "white";
        // Make line fade on edges

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        predictedNumber = "";
    }

    async function submitDrawing() {
        const offCanvas = document.createElement("canvas");
        offCanvas.width = 28;
        offCanvas.height = 28;
        const offCtx = offCanvas.getContext("2d")!;
        offCtx.drawImage(canvas, 0, 0, offCanvas.width, offCanvas.height);

        const imageData = offCtx.getImageData(0, 0, offCanvas.width, offCanvas.height);
        const data = imageData.data;
        const matrix: number[][] = [];

        for (let i = 0; i < 28; i++) {
            let row: number[] = [];
            for (let j = 0; j < 28; j++) {
                const index = (i * 28 + j) * 4;
                const pixel = data[index];
                const normalized = pixel;
                row.push(normalized);
            }
            matrix.push(row);
        }

        predictedNumber = (await ApiUtility.inferNumber(matrix))?.toString() ?? "0";
    }
</script>

<main>
    <div class="logo"><img src={Logo} alt="Home Page" /></div>
    <div class="canvas">
        <div class="model-select">
            {#key $models}
                <Popover
                    selectedItems={selected_model ? [selected_model] : []}
                    items={$models.map((m) => ({ label: m.meta.name, value: m.id }))}
                    on:popoverItemsChanged={(evt) => {
                        selected_model = evt.detail.selectedItems[0];
                        if (selected_model !== undefined) {
                                ApiUtility.load_model(Number(selected_model.value));

                        }
                    }}
                >
                    <PopoverChipTrigger slot="trigger" label="Models" style={StylingUtility.popoverChipTrigger as any} />
                    <PopoverSingleSelectContent slot="content" style={StylingUtility.popoverSingleSelectContent} />
                </Popover>
            {/key}
            <Button on:click={refreshModels} style={StylingUtility.whiteBorderButton}>Refresh</Button>
        </div>
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
        font-family: "Inter", sans-serif;
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

    .model-select {
        display: flex;
        width: 100%;
        justify-content: space-between;
        padding-bottom: 10px;
    }

    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: url("$lib/assets/PatternAsset.png") repeat center center;
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
