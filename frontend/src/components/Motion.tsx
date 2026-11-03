"use client";

import { animate, motion, useInView, useMotionValue, useReducedMotion, useSpring, useTransform } from "motion/react";
import { type ReactNode, useEffect, useRef, useState } from "react";

const EASE = [0.22, 1, 0.36, 1] as const;

/** Fait apparaître son contenu (fondu + montée) quand il entre à l'écran. */
export function Reveal({ children, delay = 0, y = 40, className, as = "div" }: {
  children: ReactNode; delay?: number; y?: number; className?: string; as?: "div" | "li" | "article";
}) {
  const reduit = useReducedMotion();
  const Comp = motion[as];
  return (
    <Comp
      className={className}
      initial={reduit ? false : { opacity: 0, y, filter: "blur(6px)" }}
      whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{ duration: 0.8, delay, ease: EASE }}
    >
      {children}
    </Comp>
  );
}

/** Compteur animé : « 1.3K+ », « 100% », « 75 »… */
export function Counter({ value }: { value: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  const visible = useInView(ref, { once: true });
  const reduit = useReducedMotion();
  const m = value.match(/^([^\d]*)([\d.,]+)(.*)$/);
  const cible = m ? parseFloat(m[2].replace(",", ".")) : 0;
  const decimales = m && m[2].includes(".") ? m[2].split(".")[1].length : 0;
  const [texte, setTexte] = useState(reduit || !m ? value : `${m[1]}0${m[3]}`);

  useEffect(() => {
    if (!visible || !m || reduit) return;
    const c = animate(0, cible, {
      duration: 2,
      ease: EASE,
      onUpdate: (v) => setTexte(`${m[1]}${v.toFixed(decimales)}${m[3]}`),
    });
    return () => c.stop();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [visible]);

  return <span ref={ref}>{texte}</span>;
}

/** Carte qui s'incline en 3D en suivant la souris, avec halo lumineux. */
export function Tilt({ children, className, max = 8 }: { children: ReactNode; className?: string; max?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduit = useReducedMotion();
  const x = useMotionValue(0.5);
  const y = useMotionValue(0.5);
  const rx = useSpring(useTransform(y, [0, 1], [max, -max]), { stiffness: 200, damping: 20 });
  const ry = useSpring(useTransform(x, [0, 1], [-max, max]), { stiffness: 200, damping: 20 });

  function bouge(e: React.PointerEvent<HTMLDivElement>) {
    const r = ref.current!.getBoundingClientRect();
    x.set((e.clientX - r.left) / r.width);
    y.set((e.clientY - r.top) / r.height);
    ref.current!.style.setProperty("--mx", `${e.clientX - r.left}px`);
    ref.current!.style.setProperty("--my", `${e.clientY - r.top}px`);
  }

  return (
    <motion.div
      ref={ref}
      className={className}
      onPointerMove={reduit ? undefined : bouge}
      onPointerLeave={() => { x.set(0.5); y.set(0.5); }}
      style={reduit ? undefined : { rotateX: rx, rotateY: ry, transformPerspective: 900 }}
    >
      {children}
    </motion.div>
  );
}

/** Halo qui suit la souris (cartes classiques, sans inclinaison). */
export function Spotlight({ children, className }: { children: ReactNode; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  return (
    <div
      ref={ref}
      className={`${className ?? ""} spotlight`}
      onPointerMove={(e) => {
        const r = ref.current!.getBoundingClientRect();
        ref.current!.style.setProperty("--mx", `${e.clientX - r.left}px`);
        ref.current!.style.setProperty("--my", `${e.clientY - r.top}px`);
      }}
    >
      {children}
    </div>
  );
}

/** Titre qui apparaît mot par mot. */
export function SplitTitle({ text, className, delay = 0.2 }: { text: string; className?: string; delay?: number }) {
  const reduit = useReducedMotion();
  return (
    <h1 className={className} aria-label={text}>
      {text.split(" ").map((mot, i) => (
        <span className="word" key={`${mot}-${i}`} aria-hidden="true">
          <motion.span
            initial={reduit ? false : { y: "110%", rotate: 4 }}
            animate={{ y: 0, rotate: 0 }}
            transition={{ duration: 0.9, delay: delay + i * 0.08, ease: EASE }}
          >
            {mot}
          </motion.span>
          {" "}
        </span>
      ))}
    </h1>
  );
}

/** Fond parallaxe : se déplace plus lentement que la page. */
export function Parallax({ src, className }: { src: string; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState(0);
  const reduit = useReducedMotion();
  useEffect(() => {
    if (reduit) return;
    const onScroll = () => setOffset(window.scrollY * 0.3);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [reduit]);
  return (
    <div ref={ref} className={className}
         style={{ backgroundImage: `url(${src})`, transform: `translate3d(0, ${offset}px, 0) scale(1.1)` }} />
  );
}

export const ease = EASE;
