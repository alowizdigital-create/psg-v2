import { Mail, MapPin, Phone } from "lucide-react";
import Link from "next/link";

import { telLien } from "@/lib/format";
import type { Site } from "@/lib/types";

import { Logo } from "./Logo";
import { FacebookIcon, InstagramIcon, TiktokIcon, YoutubeIcon } from "./Social";

export function Socials({ reglages }: { reglages: Site["reglages"] }) {
  const reseaux = [
    { url: reglages.facebook, label: "Facebook", Icone: FacebookIcon },
    { url: reglages.instagram, label: "Instagram", Icone: InstagramIcon },
    { url: reglages.tiktok, label: "TikTok", Icone: TiktokIcon },
    { url: reglages.youtube, label: "YouTube", Icone: YoutubeIcon },
  ].filter((r) => r.url);
  if (!reseaux.length) return null;
  return (
    <div className="socials">
      {reseaux.map(({ url, label, Icone }) => (
        <a key={label} href={url} target="_blank" rel="noopener noreferrer" aria-label={label}><Icone /></a>
      ))}
    </div>
  );
}

export default function Footer({ site }: { site: Site }) {
  const { reglages, entreprises } = site;
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-grid">
          <div>
            <Link href="/"><Logo /></Link>
            <p style={{ marginTop: 16 }}>{reglages.devise_pied}</p>
            <Socials reglages={reglages} />
          </div>
          <div>
            <h4>Nos entreprises</h4>
            <ul>
              {entreprises.map((e) => (
                <li key={e.slug}><Link href={`/entreprises/${e.slug}`}>{e.nom}</Link></li>
              ))}
            </ul>
          </div>
          <div>
            <h4>Navigation</h4>
            <ul>
              <li><Link href="/">Accueil</Link></li>
              <li><Link href="/a-propos">À propos</Link></li>
              <li><Link href="/catalogue">Catalogue</Link></li>
              <li><Link href="/contact">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h4>Contact</h4>
            <ul>
              {reglages.adresse && <li style={{ display: "flex", gap: 10 }}><MapPin size={18} />{reglages.adresse}</li>}
              {reglages.telephones.map((t) => (
                <li key={t} style={{ display: "flex", gap: 10 }}><Phone size={18} /><a href={telLien(t)}>{t}</a></li>
              ))}
              {reglages.email && (
                <li style={{ display: "flex", gap: 10, wordBreak: "break-all" }}>
                  <Mail size={18} style={{ flex: "none" }} /><a href={`mailto:${reglages.email}`}>{reglages.email}</a>
                </li>
              )}
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <span>&copy; {new Date().getFullYear()} {reglages.nom}. Tous droits réservés.</span>
          <span>{reglages.slogan}</span>
        </div>
      </div>
      <div className="footer-big" aria-hidden="true">PS GROUP</div>
    </footer>
  );
}
