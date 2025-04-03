export class StylingUtility {
    // Button styles
    static defaultButton = {
        color: '#ffffff',
        backgroundColor: 'transparent',
        border: '1px solid transparent',
        hover: {
            backgroundColor: '#252525',
        },
    } as const;

    static readonly redButton = {
        color: '#FE2E00',
        backgroundColor: '#FE2E0030',
        border: '0px solid #transparent',
        hover: {
            backgroundColor: '#FE2E0050',
        },
    } as const;

    static readonly whiteBorderButton = {
        backgroundColor: '#111111',
        border: '1px solid #ffffff',
        hover: {
            backgroundColor: '#252525',
        },
    } as const;


    // Text Input styles
    static readonly textInput = {
        backgroundColor: '#111111',
        color: '#ffffff',
        border: '1px solid #ffffff',
        label: {
            color: '#ffffff',
        },
        hover: {
            backgroundColor: '#111111',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
        focus: {
            backgroundColor: '#111111',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
    } as const;

    // Input Series
    static readonly inputSeries = {
        backgroundColor: '#111111',
        color: '#ffffff',
        border: '1px solid #ffffff',
        label: {
            color: '#ffffff',
        },
        hover: {
            backgroundColor: '#111111',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
        focus: {
            backgroundColor: '#111111',
            color: '#ffffff',
            border: '1px solid #ffffff',
        },
    } as const;

    // Checkbox
    static readonly checkbox = {
        border: '2px solid #FFFFFF',
        borderRadius: '0px',
        hover: {
            backgroundColor: '#111111',
            border: '2px solid #CCCCCC',
        },
        checked: {
            backgroundColor: '#111111',
            border: '2px solid #FFFFFF',
            hover: {
                backgroundColor: '#111111',
                border: '2px solid #CCCCCC',
            },
        },
    } as const;

    // Popover
    static readonly popoverChipTrigger = {
        borderRadius: 0,
        backgroundColor: '#111111',
        color: '#FFFFFF',
        hover: {
            backgroundColor: '#212121',
            color: '#FFFFFF',
            border: '1px solid #FFFFFF',
        },
        chevronColor: '#FFFFFF',
    }
    static readonly popoverSingleSelectContent = {
        borderRadius: 0,
        backgroundColor: '#222222',
        color: '#FFFFFF',
        itemColor: '#FFFFFF',
        hover: {
            backgroundColor: '#FE2E0030',
            color: '#FE2E00',
        },
        selected: {
            itemBackgroundColor: '#FE2E0030',
            itemColor: '#FE2E00',
        },
        chevronColor: '#FFFFFF',
    }

} 