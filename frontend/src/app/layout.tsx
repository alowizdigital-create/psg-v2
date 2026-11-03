import "./globals.css";

import type { Metadata, Viewport } from "next";
import type { ReactNode } from "react";

import Footer from "@/components/Footer";
import Header from "@/components/Header";
import WhatsappButton from "@/components/WhatsappButton";
import { api } from "@/lib/api";

// Les pages lisent le contenu de l'admin à chaque requête (données mises en cache 60 s).
export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const { reglages } = await api.site();
  return {
    title: { default: `${reglages.nom} — ${reglages.slogan}`, template: `%s — ${reglages.nom}` },
    description:
      "PS GROUP SARL réunit audiovisuel, digital, formation, musique, concours et média (AFRIJEUNE TV) à Yaoundé, Cameroun.",
    openGraph: { siteName: reglages.nom, locale: "fr_FR", type: "website" },
    icons: { icon: "/favicon.svg" },
  };
}

export const viewport: Viewport = { themeColor: "#120607", width: "device-width", initialScale: 1 };

export default async function RootLayout({ children }: { children: ReactNode }) {
  const site = await api.site();
  return (
    <html lang="fr">
      <body>
        <a href="#contenu" className="hp">Aller au contenu</a>
        <Header entreprises={site.entreprises} />
        <main id="contenu">{children}</main>
        <Footer site={site} />
        <WhatsappButton numero={site.reglages.whatsapp} />
      </body>
    </html>
  );
}
