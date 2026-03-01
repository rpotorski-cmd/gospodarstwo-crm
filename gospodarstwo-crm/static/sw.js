const CACHE_NAME = 'kabanek-crm-v2';
const STATIC_ASSETS = [
  '/',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Network-first for API calls
  if (e.request.url.includes('/api/')) {
    e.respondWith(
      fetch(e.request)
        .catch(() => caches.match(e.request))
    );
    return;
  }
  // Cache-first for static assets
  e.respondWith(
    caches.match(e.request)
      .then(cached => cached || fetch(e.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        }
        return response;
      }))
  );
});
