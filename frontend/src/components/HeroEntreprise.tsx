"use client";

import { ArrowRight, ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const DUREE = 6500;

/** Ouverture plein écran d'une page d'entreprise : photos seules (fondu + zoom lent), logo en haut à droite. */
export default function HeroEntreprise({ slides, nom, logo, slogan, cta }: {
  slides: { id: number; image: string | null; legende: string }[];
  nom: string; logo?: string | null; slogan?: string; cta?: { href: string; label: string };
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

      {logo && (
        <motion.img src={logo} alt={`Logo ${nom}`} className="hero-entreprise-logo"
                    initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, duration: 0.9 }} />
      )}
      {(cta || slogan) && (
        <motion.div className="hero-entreprise-cta" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9, duration: 0.8 }}>
          {cta && <Link href={cta.href} className="btn btn-primary">{cta.label} <ArrowRight size={18} /></Link>}
          {slogan && <p>{slogan}</p>}
        </motion.div>
      )}
      <a href="#contenu" className="hero-entreprise-bas" aria-label="Voir la suite">
        <ChevronDown size={30} strokeWidth={1.5} />
      </a>

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
