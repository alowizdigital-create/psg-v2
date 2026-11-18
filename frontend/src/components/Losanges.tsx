"use client";

import { motion, useReducedMotion } from "motion/react";
import {
  siBehance, siBluesky, siDiscord, siFacebook, siGoogle, siInstagram, siMessenger, siPinterest, siReddit,
  siSnapchat, siSpotify, siTelegram, siThreads, siTiktok, siTwitch, siWhatsapp, siX, siYoutube,
} from "simple-icons";
import { type CSSProperties, useEffect, useState } from "react";

import { BadgeRotatif } from "./BlocOuverture";

type Icone = { title: string; path: string; hex: string };

// Logos des réseaux sociaux reconnus par leur nom (en minuscules, sans espace).
const RESEAUX: Record<string, Icone> = Object.fromEntries(
  [siFacebook, siInstagram, siTiktok, siYoutube, siWhatsapp, siSnapchat, siX, siTelegram, siPinterest, siThreads,
   siMessenger, siTwitch, siDiscord, siSpotify, siGoogle, siReddit, siBehance, siBluesky]
    .map((i) => [i.title.toLowerCase().replace(/\s/g, ""), i]),
);
RESEAUX.twitter = siX;

export type Logo = { id: number; titre: string; image: string | null; lien: string; en_avant?: boolean };

/** Place le logo « mis en avant » au centre de la grille (rangée du milieu ayant une tuile centrale). */
function auCentre<T extends { en_avant?: boolean }>(liste: T[], large: number): T[] {
  const i = liste.findIndex((l) => l.en_avant);
  if (i < 0) return liste;
  const reste = [...liste.slice(0, i), ...liste.slice(i + 1)];
  const tailles: number[] = [];
  for (let n = 0, k = 0; n < liste.length; k++) { const t = k % 2 ? large - 1 : large; tailles.push(Math.min(t, liste.length - n)); n += t; }
  const milieu = (tailles.length - 1) / 2;
  let meilleure = -1;
  tailles.forEach((t, r) => {
    if (t % 2 === 1 && (meilleure < 0 || Math.abs(r - milieu) < Math.abs(meilleure - milieu))) meilleure = r;
  });
  if (meilleure < 0) return liste;
  const position = tailles.slice(0, meilleure).reduce((a, b) => a + b, 0) + (tailles[meilleure] - 1) / 2;
  reste.splice(position, 0, liste[i]);
  return reste;
}

/** Découpe en rangées alternées (ex. 5, 4, 5, 4…) pour l'effet « nid d'abeille » en losanges. */
function rangees<T>(liste: T[], large: number): T[][] {
  const r: T[][] = [];
  for (let i = 0, k = 0; i < liste.length; k++) {
    const n = k % 2 ? large - 1 : large;
    r.push(liste.slice(i, i + n));
    i += n;
  }
  return r;
}

/**
 * Grille de logos en losanges (inspirée de derin15.com) : tuiles blanches inclinées à 45°, logos en
 * gris qui prennent leur couleur au survol, apparition en cascade et formes floues qui flottent.
 */
export default function Losanges({ logos }: { logos: Logo[] }) {
  const reduit = useReducedMotion();
  const [large, setLarge] = useState(5);

  useEffect(() => {
    const mesure = () => setLarge(window.innerWidth < 640 ? 3 : window.innerWidth < 1000 ? 4 : 5);
    mesure();
    window.addEventListener("resize", mesure);
    return () => window.removeEventListener("resize", mesure);
  }, []);

  const lignes = rangees(auCentre(logos, large), large);
  let rang = 0;

  return (
    <div className="losanges" style={{ "--large": large } as CSSProperties}>
      <span className="losanges-forme f1" aria-hidden="true" />
      <span className="losanges-forme f2" aria-hidden="true" />
      <span className="losanges-forme f3" aria-hidden="true" />
      <span className="losanges-forme f4" aria-hidden="true" />
      <div className="losanges-grille">
        {lignes.map((ligne, l) => (
          <div key={l} className={`losanges-rangee ${l % 2 ? "decalee" : ""}`}>
            {ligne.map((logo) => {
              const icone = RESEAUX[logo.titre.toLowerCase().replace(/\s/g, "")];
              const contenu = (
                <>
                  {logo.image ? (
                    <img src={logo.image} alt={logo.titre} loading="lazy" />
                  ) : icone ? (
                    <svg viewBox="0 0 24 24" role="img" aria-label={logo.titre}><path d={icone.path} /></svg>
                  ) : (
                    <strong>{logo.titre}</strong>
                  )}
                  <small>{logo.titre}</small>
                </>
              );
              const i = rang++;
              return (
                <div key={logo.id} className="losange-place">
                  <motion.div
                    className="losange"
                    style={{ "--couleur": icone ? `#${icone.hex === "000000" || icone.hex === "FFFC00" ? "111111" : icone.hex}` : "var(--primary)" } as CSSProperties}
                    initial={reduit ? false : { opacity: 0, scale: 0.4, rotate: 0 }}
                    whileInView={{ opacity: 1, scale: 1, rotate: 45 }}
                    viewport={{ once: true, margin: "-40px" }}
                    transition={{ duration: 0.6, delay: (i % 9) * 0.06 + Math.floor(i / 9) * 0.12, ease: [0.22, 1, 0.36, 1] }}
                  >
                    {logo.lien ? (
                      <a href={logo.lien} target="_blank" rel="noopener noreferrer" className="losange-contenu">{contenu}</a>
                    ) : (
                      <div className="losange-contenu">{contenu}</div>
                    )}
                  </motion.div>
                </div>
              );
            })}
          </div>
        ))}
      </div>
      <BadgeRotatif texte="PS DIGITAL • Réseaux sociaux • Yaoundé • " />
    </div>
  );
}
