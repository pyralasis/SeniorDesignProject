export class StylingUtility {
    // Button styles
    static readonly redButton = {
        backgroundColor: '#dc2626',
        border: '1px solid #dc2626',
        hover: {
            backgroundColor: '#b91c1c',
        },
    } as const;

    static readonly whiteBorderButton = {
        backgroundColor: '#000000',
        border: '1px solid #ffffff',
        hover: {
            backgroundColor: '#090909',
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

    // Input Series
    static readonly inputSeries = {
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

    // Checkbox
    static readonly checkbox = {
        border: '2px solid #FFFFFF',
        borderRadius: '0px',
        hover: {
            backgroundColor: '#000000',
            border: '2px solid #CCCCCC',
        },
        checked: {
            backgroundColor: '#000000',
            border: '2px solid #FFFFFF',
            hover: {
                backgroundColor: '#111111',
                border: '2px solid #CCCCCC',
            },
        },
    } as const;

} 