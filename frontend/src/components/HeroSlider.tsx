"use client";

import { ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";

import AgenceWordmark from "./AgenceWordmark";

const DUREE = 6000;
const MOTS = ["Événementielle", "&", "Marketing"];

export default function HeroSlider({ slides, titre }: {
  slides: { id: number; image: string | null }[]; titre: string;
}) {
  const images = slides.map((s) => s.image).filter(Boolean) as string[];
  const [index, setIndex] = useState(0);
  const [pause, setPause] = useState(false);
  const reduit = useReducedMotion();
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const yContenu = useTransform(scrollYProgress, [0, 1], [0, 140]);
  const opacite = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  const aller = useCallback((i: number) => setIndex((i + images.length) % Math.max(images.length, 1)), [images.length]);

  useEffect(() => {
    if (pause || images.length < 2) return;
    const t = setTimeout(() => aller(index + 1), DUREE);
    return () => clearTimeout(t);
  }, [index, pause, images.length, aller]);

  return (
    <section className="hero grain" ref={ref} onMouseEnter={() => setPause(true)} onMouseLeave={() => setPause(false)}
             aria-roledescription="carrousel" aria-label={titre}>
      <AnimatePresence initial={false}>
        {images[index] && (
          <motion.div
            key={index}
            className="hero-slide"
            style={{ backgroundImage: `url(${images[index]})` }}
            initial={{ opacity: 0, scale: 1.14 }}
            animate={{ opacity: 1, scale: reduit ? 1 : 1.03 }}
            exit={{ opacity: 0 }}
            transition={{ opacity: { duration: 1.4 }, scale: { duration: DUREE / 1000 + 1.5, ease: "linear" } }}
          />
        )}
      </AnimatePresence>

      <motion.div className="container hero-content" style={reduit ? undefined : { y: yContenu, opacity: opacite }}>
        <motion.span className="eyebrow hero-eyebrow" initial={{ opacity: 0, y: -10 }}
                     animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1, duration: 0.7 }}>
          {titre}
        </motion.span>
        <h1 className="hero-title" aria-label="Agence événementielle & marketing">
          {/* « Agence » apparaît comme écrit à la main, de gauche à droite. */}
          <motion.span className="hero-script" aria-hidden="true"
                       initial={reduit ? false : { clipPath: "inset(0 100% 0 0)" }}
                       animate={{ clipPath: "inset(0 0% 0 0)" }}
                       transition={{ duration: 1.6, delay: 0.25, ease: [0.65, 0, 0.35, 1] }}>
            <AgenceWordmark />
          </motion.span>
          <span className="hero-display" aria-hidden="true">
            {MOTS.map((mot, i) => (
              <span className="word" key={mot}>
                <motion.span className="gradient-text" initial={reduit ? false : { y: "110%" }} animate={{ y: 0 }}
                             transition={{ duration: 0.8, delay: 1.1 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}>
                  {mot}
                </motion.span>
                {i < MOTS.length - 1 && " "}
              </span>
            ))}
          </span>
        </h1>
        <motion.div className="hero-actions" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.6, duration: 0.8 }}>
          <Link href="/#entreprises" className="btn btn-primary">Découvrir nos entreprises <ArrowRight size={18} /></Link>
          <Link href="/catalogue" className="btn btn-outline">Composer ma demande</Link>
        </motion.div>
      </motion.div>

      {images.length > 1 && (
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
