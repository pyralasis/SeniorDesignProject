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

    private static async playSound(soundPath: string, volume: number = 1) {
        this.initAudioContext();
        if (!this.audioContext) return;

        try {
            const response = await fetch(soundPath);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
            const gainNode = this.audioContext.createGain();
            gainNode.gain.value = volume;

            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            source.start();
        } catch (error) {
            console.error('Error playing sound:', error);
        }
    }


    public static playClick1(volume: number = 1) {
        this.playSound('/src/lib/assets/sounds/lighter-click.mp3', volume);
    }

    public static playClick2(volume: number = 1) {
        this.playSound('/src/lib/assets/sounds/lighter-click-2.mp3', volume);
    }

    public static playSwoosh(volume: number = 1) {
        this.playSound('/src/lib/assets/sounds/swoosh.mp3', volume);
    }

    public static playGrab(volume: number = 1) {
        this.playSound('/src/lib/assets/sounds/grab1.mp3', volume);
    }

    public static playDrop(volume: number = 1) {
        this.playSound('/src/lib/assets/sounds/drop1.mp3', volume);
    }
}
