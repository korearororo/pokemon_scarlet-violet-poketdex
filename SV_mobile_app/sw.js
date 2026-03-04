const CACHE_NAME = "sv-guide-pwa-v1";
const CORE_ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./SV_files/SV_%EA%B3%B5%EB%9E%B5%EC%A7%91.html",
  "./SV_files/sv_paldea_data.js",
  "./SV_files/sv_national_data.js",
  "./SV_files/sv_move_data.js",
  "./SV_files/sv_ability_data.js",
  "./SV_files/sv_tool_data.js",
  "./SV_files/sv_nature_data.js",
  "./SV_files/sv_type_chart_data.js",
  "./SV_files/sv_evolution_data.js",
  "./SV_files/frlg_type_icons.js",
  "./SV_files/assets/maps/PaldeaMap.jpg",
  "./SV_files/assets/icons/pokeball.svg",
  "./SV_files/assets/icons/items/tm-ingame.png",
  "./SV_files/assets/icons/items/key-item-ingame.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request)
        .then((res) => {
          if (!res || res.status !== 200 || res.type !== "basic") return res;
          const cloned = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, cloned));
          return res;
        })
        .catch(() => caches.match("./index.html"));
    })
  );
});
