/**
 * Utility for playing sound effects from assets
 */
export class SoundUtility {
    private static audioContext: AudioContext | null = null;

    private static initAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new AudioContext();
        }
    }

    private static async playSound(soundPath: string) {
        this.initAudioContext();
        if (!this.audioContext) return;

        try {
            const response = await fetch(soundPath);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);

            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);
            source.start();
        } catch (error) {
            console.error('Error playing sound:', error);
        }
    }

    /**
     * Play click sound effect 1
     */
    public static playClick1() {
        this.playSound('/src/lib/assets/sounds/lighter-click.mp3');
    }

    /**
     * Play click sound effect 2
     */
    public static playClick2() {
        this.playSound('/src/lib/assets/sounds/lighter-click-2.mp3');
    }

    /**
     * Play success sound effect
     */
    public static playSuccess() {
        this.playSound('/src/lib/assets/sounds/success.mp3');
    }

    /**
     * Play error sound effect
     */
    public static playError() {
        this.playSound('/src/lib/assets/sounds/error.mp3');
    }
}

