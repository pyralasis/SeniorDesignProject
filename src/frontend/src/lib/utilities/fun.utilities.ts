import gsap from 'gsap';

export class FunUtilities {

    private static randChar() {
        let c = "abcdefghijklmnopqrstuvwxyz1234567890!@#$^&*()…æ_+-=;[]/~`"
        c = c[Math.floor(Math.random() * c.length)]
        return (Math.random() > 0.5) ? c : c.toUpperCase()
    }

    public static decodeAnimation(element: HTMLElement): void {
        const text = element.textContent || '';
        const chars = text.split('');

        const tl = gsap.timeline();
        tl.fromTo(element as HTMLElement, {
            textContent: chars.map(() => this.randChar()).join(''),
        }, {
            duration: chars.length / 20,
            ease: 'power4.in',
            delay: 0.1,
            onUpdate: () => {
                const progress = Math.floor(tl.progress() * chars.length);
                const remainingChars = chars.length - progress;

                const decoded = element.classList.contains('fromRight')
                    ? chars.slice(chars.length - progress).join('')
                    : chars.slice(0, progress).join('');

                const random = Array(remainingChars)
                    .fill(0)
                    .map(() => this.randChar())
                    .join('');

                element.textContent = element.classList.contains('fromRight')
                    ? random + decoded
                    : decoded + random;
            }
        });
    }

}
