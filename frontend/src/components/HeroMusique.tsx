"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { type CSSProperties, useCallback, useEffect, useState } from "react";

import { BadgeRotatif } from "./BlocOuverture";

const DUREE = 6500;
// Hauteurs de départ des barres de l'égaliseur (effet « son qui joue »).
const BARRES = [0.35, 0.7, 0.5, 0.9, 0.6, 0.4, 0.8, 1, 0.55, 0.75, 0.45, 0.95, 0.65, 0.5, 0.85, 0.4, 0.7, 0.6, 0.9, 0.5];

/**
 * Ouverture « musique » (inspirée de derin15.com) : photos plein écran avec lignes de balayage,
 * grand titre qui vibre au rythme (décalage rouge / bleu façon glitch + battement), sous-titre
 * espacé et égaliseur animé. Bas de section en biais.
 */
export default function HeroMusique({ slides, titre, sousTitre }: {
  slides: { id: number; image: string | null; legende: string }[]; titre: string; sousTitre?: string;
}) {
  const images = slides.filter((s) => s.image);
  const n = images.length;
  const [index, setIndex] = useState(0);
  const reduit = useReducedMotion();
  const aller = useCallback((i: number) => setIndex(((i % n) + n) % n), [n]);

  useEffect(() => {
    if (n < 2) return;
    const t = setTimeout(() => aller(index + 1), DUREE);
    return () => clearTimeout(t);
  }, [index, n, aller]);

  return (
    <section className="hero hero-musique grain" aria-label={`${titre}${sousTitre ? ` — ${sousTitre}` : ""}`}>
      <AnimatePresence initial={false}>
        {images[index] && (
          <motion.div key={index} className="hero-slide" style={{ backgroundImage: `url(${images[index].image})` }}
                      initial={{ opacity: 0, scale: 1.12 }} animate={{ opacity: 1, scale: reduit ? 1 : 1.02 }}
                      exit={{ opacity: 0 }}
                      transition={{ opacity: { duration: 1.4 }, scale: { duration: DUREE / 1000 + 1.5, ease: "linear" } }} />
        )}
      </AnimatePresence>

      <div className="hero-musique-contenu">
        <motion.h1 className="glitch" data-text={titre}
                   initial={reduit ? false : { opacity: 0, scale: 1.3, filter: "blur(12px)" }}
                   animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
                   transition={{ duration: 0.9, ease: [0.22, 1, 0.36, 1] }}>
          <span>{titre}</span>
        </motion.h1>
        {sousTitre && (
          <motion.p className="hero-musique-sous" initial={{ opacity: 0, letterSpacing: "0.9em" }}
                    animate={{ opacity: 1, letterSpacing: "0.45em" }} transition={{ delay: 0.5, duration: 1.2 }}>
            {sousTitre}
          </motion.p>
        )}
        <div className="egaliseur" aria-hidden="true">
          {BARRES.map((h, i) => (
            <span key={i} style={{ "--h": h, "--d": `${0.55 + (i % 5) * 0.12}s`, "--r": `${(i * 0.07) % 0.5}s` } as CSSProperties} />
          ))}
        </div>
      </div>

      {n > 1 && (
        <>
          <button className="hero-arrow prev" onClick={() => aller(index - 1)} aria-label="Image précédente">
            <ChevronLeft size={54} strokeWidth={1} />
          </button>
          <button className="hero-arrow next" onClick={() => aller(index + 1)} aria-label="Image suivante">
            <ChevronRight size={54} strokeWidth={1} />
          </button>
        </>
      )}
      <a href="#contenu" className="souris" aria-label="Voir la suite"><span /></a>
      <BadgeRotatif texte={`${titre} • ${sousTitre || "Musique"} • Yaoundé • `} />
    </section>
  );
}
