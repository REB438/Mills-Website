// Service Worker for Mills Shirley LLP Website
// Provides caching and offline functionality

// Bump CACHE_NAME whenever the precached list below changes. Static assets are
// versioned with ?v=N, so they no longer depend on this alone.
const CACHE_NAME = 'mills-shirley-v1.5.0';
const urlsToCache = [
    '/',
    '/index.html',
    '/assets/css/styles.css',
    '/assets/js/scripts.js',
    '/assets/js/performance.js',
    '/assets/js/tailwind-config.js',
    '/assets/favicon/favicon.png'
];

// Install event - cache resources
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
            // Without this the new worker sits in "waiting" until every tab
            // controlled by the old one closes, and a reload does not release
            // control, so a deploy would never reach returning visitors.
            .then(() => self.skipWaiting())
    );
});

// Fetch event
self.addEventListener('fetch', event => {
    const request = event.request;
    if (request.method !== 'GET') {
        return;
    }

    // Pages carry no cache-busting query, so serving them cache-first pins
    // visitors to stale markup. Go to the network first and keep the cached
    // copy purely as an offline fallback.
    if (request.mode === 'navigate') {
        event.respondWith(
            // 'no-cache' revalidates with the server instead of letting the HTTP
            // disk cache answer, while still allowing a 304 to reuse the body. A
            // plain fetch() here can be answered from that cache, which would put
            // stale markup back in front of visitors.
            fetch(request.url, { cache: 'no-cache', credentials: 'same-origin' })
                .then(response => {
                    if (response.ok) {
                        const copy = response.clone();
                        caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
                    }
                    return response;
                })
                .catch(() => caches.match(request))
        );
        return;
    }

    // Static assets are versioned, so cache-first is safe and fast.
    event.respondWith(
        caches.match(request).then(response => response || fetch(request))
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys()
            .then(cacheNames => Promise.all(
                cacheNames
                    .filter(cacheName => cacheName !== CACHE_NAME)
                    .map(cacheName => caches.delete(cacheName))
            ))
            // Take over pages that were loaded by the previous worker.
            .then(() => self.clients.claim())
    );
});
