import type { NextConfig } from "next";

// Adresse du backend Django vue depuis le serveur Next.js.
const BACKEND = process.env.BACKEND_INTERNAL_URL || "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  // Django attend des URL terminées par « / » : on ne les réécrit pas.
  skipTrailingSlashRedirect: true,
  // Les images sont déjà converties en WebP et redimensionnées par Django.
  images: { unoptimized: true },
  async rewrites() {
    // En production, le reverse proxy (Caddy) envoie ces chemins directement à
    // Django ; ces règles servent en développement et de filet de sécurité.
    return [
      { source: "/api/:path*", destination: `${BACKEND}/api/:path*/` },
      { source: "/media/:path*", destination: `${BACKEND}/media/:path*` },
      { source: "/admin", destination: `${BACKEND}/admin/` },
      { source: "/admin/:path*", destination: `${BACKEND}/admin/:path*/` },
      { source: "/static/:path*", destination: `${BACKEND}/static/:path*` },
    ];
  },
  async redirects() {
    // Anciennes adresses du premier site (fichiers .html).
    return [
      { source: "/index.html", destination: "/", permanent: true },
      { source: "/a-propos.html", destination: "/a-propos", permanent: true },
      { source: "/contact.html", destination: "/contact", permanent: true },
      { source: "/entreprises/:slug.html", destination: "/entreprises/:slug", permanent: true },
    ];
  },
};

export default nextConfig;
