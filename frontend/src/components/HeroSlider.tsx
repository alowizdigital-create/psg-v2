"use client";

import { ArrowRight, ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";

import { SplitTitle } from "./Motion";

const DUREE = 6000;

export default function HeroSlider({ slides, titre, slogan }: {
  slides: { id: number; image: string | null }[]; titre: string; slogan: string;
}) {
  const images = slides.map((s) => s.image).filter(Boolean) as string[];
  const [index, setIndex] = useState(0);
  const [pause, setPause] = useState(false);
  const reduit = useReducedMotion();
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const yContenu = useTransform(scrollYProgress, [0, 1], [0, 160]);
  const opacite = useTransform(scrollYProgress, [0, 0.8], [1, 0]);

  const aller = useCallback((i: number) => setIndex((i + images.length) % Math.max(images.length, 1)), [images.length]);

  useEffect(() => {
    if (pause || images.length < 2) return;
    const t = setTimeout(() => aller(index + 1), DUREE);
    return () => clearTimeout(t);
  }, [index, pause, images.length, aller]);

  return (
    <section className="hero grain" ref={ref} onMouseEnter={() => setPause(true)} onMouseLeave={() => setPause(false)}
             aria-roledescription="carrousel">
      <AnimatePresence initial={false}>
        {images[index] && (
          <motion.div
            key={index}
            className="hero-slide"
            style={{ backgroundImage: `url(${images[index]})` }}
            initial={{ opacity: 0, scale: 1.18 }}
            animate={{ opacity: 1, scale: reduit ? 1 : 1.04 }}
            exit={{ opacity: 0 }}
            transition={{ opacity: { duration: 1.4 }, scale: { duration: DUREE / 1000 + 1.5, ease: "linear" } }}
          />
        )}
      </AnimatePresence>
      <div className="orb" style={{ width: 420, height: 420, background: "rgba(245,184,0,.18)", top: "10%", right: "-8%" }} />

      <motion.div className="container hero-content" style={reduit ? undefined : { y: yContenu, opacity: opacite }}>
        <motion.span className="eyebrow" style={{ color: "var(--accent)" }} initial={{ opacity: 0, x: -20 }}
                     animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1, duration: 0.7 }}>
          Groupe camerounais · Yaoundé
        </motion.span>
        <SplitTitle text={titre} />
        <motion.p className="hero-subtitle" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7, duration: 0.8 }}>
          <span className="gradient-text" style={{ fontWeight: 700 }}>{slogan}</span>
          <br />
          Audiovisuel, digital, formation, musique, concours et média : six expertises réunies pour donner vie à vos projets.
        </motion.p>
        <motion.div className="hero-actions" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9, duration: 0.8 }}>
          <Link href="/#entreprises" className="btn btn-primary">Découvrir nos entreprises <ArrowRight size={18} /></Link>
          <Link href="/catalogue" className="btn btn-outline">Composer ma demande</Link>
        </motion.div>
      </motion.div>

      <div className="hero-controls">
        <div className="container">
          <div className="scroll-hint"><i /> Défiler</div>
          {images.length > 1 && (
            <>
              <div className="hero-dots" role="tablist">
                {images.map((_, i) => (
                  <button key={i} className="hero-dot" onClick={() => aller(i)} role="tab" aria-selected={i === index}
                          aria-label={`Image ${i + 1}`}>
                    {i === index && (
                      <motion.span key={`${index}-${pause}`} initial={{ scaleX: 0 }} animate={{ scaleX: pause ? 0.15 : 1 }}
                                   transition={{ duration: pause ? 0.2 : DUREE / 1000, ease: "linear" }} />
                    )}
                    {i < index && <span />}
                  </button>
                ))}
              </div>
              <div className="hero-arrows">
                <button className="round-btn" onClick={() => aller(index - 1)} aria-label="Image précédente"><ChevronLeft /></button>
                <button className="round-btn" onClick={() => aller(index + 1)} aria-label="Image suivante"><ChevronRight /></button>
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  );
}
