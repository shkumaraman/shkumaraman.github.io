const CACHE_NAME = "app-cache";
const OFFLINE_URL = "/offline.html";

const BYPASS_HOSTS = [
  "googlesyndication.com",
  "doubleclick.net",
  "googleadservices.com",
  "google-analytics.com",
  "googletagmanager.com",
  "adtrafficquality.google"
];

self.addEventListener("install", event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.add(OFFLINE_URL))
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys =>
        Promise.all(
          keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== "GET") return;
  if (BYPASS_HOSTS.some(host => url.hostname.endsWith(host))) return;
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(request)
      .then(response => {
        if (response && response.status === 200 && response.type === "basic") {
          const clone = response.clone();
          event.waitUntil(
            caches.open(CACHE_NAME).then(cache => cache.put(request, clone))
          );
        }
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(request);
        if (cached) return cached;
        if (request.mode === "navigate") {
          return caches.match(OFFLINE_URL);
        }
        return Response.error();
      })
  );
});
