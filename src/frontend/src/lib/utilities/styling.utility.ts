export class StylingUtility {
    // Button styles
    static readonly redButton = {
        backgroundColor: '#dc2626',
        border: '1px solid #dc2626',
        hover: {
            backgroundColor: '#b91c1c',
        },
    } as const;

    // Text Input styles
    static readonly textInput = {
        backgroundColor: '#000000',
        color: '#ffffff',
        border: '1px solid #ffffff',
        label: {
            color: '#ffffff',
        },
        hover: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
        focus: {
            backgroundColor: '#000000',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
    } as const;

} 