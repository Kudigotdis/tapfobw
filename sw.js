// TapFo.bw Service Worker — Offline First
const CACHE_NAME = 'tapfo-v1.01.267';
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/assets/icons/TapFo_Logo.png',
  '/assets/icons/TapFo_Logo_White.png',
  '/assets/icons/TapFo_Logo_Icon.png',
  '/fonts/PTSans-Regular.ttf',
  '/fonts/PTSans-Bold.ttf',
  '/data/businesses.json',
  '/data/updates_changelog.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  // Network first for API calls, cache first for assets
  if (event.request.url.includes('fonts.googleapis') || event.request.url.includes('fonts.gstatic')) {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(event.request).then(cached =>
          cached || fetch(event.request).then(resp => {
            cache.put(event.request, resp.clone());
            return resp;
          })
        )
      )
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached =>
      cached || fetch(event.request).catch(() => caches.match('/index.html'))
    )
  );
});
