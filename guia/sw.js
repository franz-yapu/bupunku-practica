// Este subdominio antes servía otra app que instaló un service worker en /sw.js.
// Este archivo lo reemplaza: se activa, se da de baja y recarga las pestañas abiertas.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const claves = await caches.keys();
      await Promise.all(claves.map((c) => caches.delete(c)));
      await self.registration.unregister();
      const pestanas = await self.clients.matchAll({ type: 'window' });
      pestanas.forEach((p) => p.navigate(p.url));
    })(),
  );
});
