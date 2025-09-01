// Performance Optimization Scripts
// Handles image loading, lazy loading, and performance enhancements

document.addEventListener('DOMContentLoaded', function() {
    
    // Intersection Observer for lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.01
        });

        // Observe all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Preload critical resources
    function preloadCriticalResources() {
        const criticalResources = [
            'assets/fonts/equity/Equity Text A Regular.ttf',
            'assets/fonts/equity/Equity Caps A Regular.ttf'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = resource;
            link.as = 'font';
            link.type = 'font/ttf';
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }

    // Optimize images for different screen sizes
    function optimizeImages() {
        const images = document.querySelectorAll('img[src*="attorneys"]');
        const pixelRatio = window.devicePixelRatio || 1;
        
        images.forEach(img => {
            // Add responsive image attributes if not already present
            if (!img.sizes) {
                img.sizes = '(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw';
            }
        });
    }

    // Debounce function for performance
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Optimize scroll performance
    const optimizedScrollHandler = debounce(() => {
        // Handle scroll-based animations and updates
        const scrolled = window.scrollY > 16;
        const header = document.querySelector('header');
        
        if (header) {
            if (scrolled) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
    }, 16); // ~60fps

    window.addEventListener('scroll', optimizedScrollHandler, { passive: true });

    // Initialize performance optimizations
    preloadCriticalResources();
    optimizeImages();

    // Service Worker registration for caching (if supported)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page Load Time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                console.log('DOM Content Loaded:', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart, 'ms');
            }, 0);
        });
    }
});
