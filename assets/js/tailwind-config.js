// Centralized Tailwind Configuration
// Used across all HTML files to eliminate duplication
window.tailwindConfig = {
    theme: {
        extend: {
            colors: {
                'navy': {
                    50: '#f8fafc',
                    100: '#f1f5f9',
                    200: '#e2e8f0',
                    300: '#cbd5e1',
                    400: '#94a3b8',
                    500: '#64748b',
                    600: '#475569',
                    700: '#334155',
                    800: '#1e293b',
                    900: '#0f172a',
                    950: '#020617'
                },
                'gray': {
                    50: '#f9fafb',
                    100: '#f3f4f6',
                    200: '#e5e7eb',
                    300: '#d1d5db',
                    400: '#9ca3af',
                    500: '#6b7280',
                    600: '#4b5563',
                    700: '#374151',
                    800: '#1f2937',
                    900: '#111827',
                    950: '#030712'
                },
                'white': '#ffffff',
                'black': '#000000'
            },
            fontFamily: {
                'serif': ['Equity Text', 'Georgia', 'serif'],
                'sans': ['Equity Text', 'Georgia', 'serif'],
                'caps': ['Equity Caps', 'Equity Text', 'Georgia', 'serif']
            },
            spacing: {
                '1': '0.125rem',
                '2': '0.25rem',
                '3': '0.375rem',
                '4': '0.5rem',
                '6': '0.75rem',
                '8': '1rem',
                '10': '1.25rem',
                '12': '1.5rem',
                '16': '2rem',
                '20': '2.5rem',
                '24': '3rem',
                '32': '4rem',
                '40': '5rem',
                '48': '6rem',
                '56': '7rem',
                '64': '8rem'
            },
            borderRadius: {
                'xl': '0.75rem',
                '2xl': '1rem',
                '3xl': '1.5rem'
            }
        }
    }
};