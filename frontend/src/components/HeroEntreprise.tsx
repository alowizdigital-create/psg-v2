"use client";

import { ArrowRight, ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const DUREE = 6500;

/**
 * Ouverture plein écran d'une page d'entreprise : même diaporama que l'accueil (fondu + zoom lent,
 * flèches, points), mais le texte est posé en bas pour laisser les visages bien visibles.
 */
export default function HeroEntreprise({ slides, surTitre, nom, accroche, cta }: {
  slides: { id: number; image: string | null; legende: string }[];
  surTitre: string; nom: string; accroche: string;
  cta?: { href: string; label: string };
}) {
  const images = slides.filter((s) => s.image);
  const n = images.length;
  const [index, setIndex] = useState(0);
  const [pause, setPause] = useState(false);
  const reduit = useReducedMotion();
  const aller = useCallback((i: number) => setIndex(((i % n) + n) % n), [n]);

  useEffect(() => {
    if (pause || n < 2) return;
    const t = setTimeout(() => aller(index + 1), DUREE);
    return () => clearTimeout(t);
  }, [index, pause, n, aller]);

  // « Concours Miss Afrijeune » → « MISS AFRIJEUNE » en grand.
  const principal = nom.replace(/^Concours\s+/i, "").toUpperCase();

  return (
    <section className="hero hero-entreprise grain" onMouseEnter={() => setPause(true)}
             onMouseLeave={() => setPause(false)} aria-roledescription="carrousel" aria-label={nom}>
      <AnimatePresence initial={false}>
        {images[index] && (
          <motion.div
            key={index}
            className="hero-slide"
            style={{ backgroundImage: `url(${images[index].image})` }}
            role="img"
            aria-label={images[index].legende || nom}
            initial={{ opacity: 0, scale: 1.14 }}
            animate={{ opacity: 1, scale: reduit ? 1 : 1.03 }}
            exit={{ opacity: 0 }}
            transition={{ opacity: { duration: 1.4 }, scale: { duration: DUREE / 1000 + 1.5, ease: "linear" } }}
          />
        )}
      </AnimatePresence>

      <div className="container hero-entreprise-contenu">
        <motion.span className="eyebrow hero-eyebrow" initial={{ opacity: 0, y: -10 }}
                     animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1, duration: 0.7 }}>
          {surTitre}
        </motion.span>
        <h1 className="hero-title" aria-label={nom}>
          <span className="hero-display hero-entreprise-nom" aria-hidden="true">
            <span className="word">
              <motion.span className="gradient-text" initial={reduit ? false : { y: "110%" }} animate={{ y: 0 }}
                           transition={{ duration: 0.9, delay: 0.9, ease: [0.22, 1, 0.36, 1] }}>
                {principal}
              </motion.span>
            </span>
          </span>
        </h1>
        {accroche && (
          <motion.p className="hero-entreprise-accroche" initial={{ opacity: 0, y: 14 }}
                    animate={{ opacity: 1, y: 0 }} transition={{ delay: 1.3, duration: 0.8 }}>
            {accroche}
          </motion.p>
        )}
        <motion.div className="hero-actions" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.5, duration: 0.8 }}>
          {cta && <Link href={cta.href} className="btn btn-primary">{cta.label} <ArrowRight size={18} /></Link>}
          <a href="#contenu" className="btn btn-outline">Découvrir <ChevronDown size={18} /></a>
        </motion.div>
      </div>

      {n > 1 && (
        <>
          <button className="hero-arrow prev" onClick={() => aller(index - 1)} aria-label="Image précédente">
            <ChevronLeft size={54} strokeWidth={1} />
          </button>
          <button className="hero-arrow next" onClick={() => aller(index + 1)} aria-label="Image suivante">
            <ChevronRight size={54} strokeWidth={1} />
          </button>
          <div className="hero-dots" role="tablist" aria-label="Choisir une image">
            {images.map((_, i) => (
              <button key={i} className={`hero-dot ${i === index ? "is-active" : ""}`} onClick={() => aller(i)}
                      role="tab" aria-selected={i === index} aria-label={`Image ${i + 1}`} />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
