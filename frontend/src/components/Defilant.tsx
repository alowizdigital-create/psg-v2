"use client";

import {
  motion, useAnimationFrame, useMotionValue, useReducedMotion, useScroll, useSpring, useTransform, useVelocity,
} from "motion/react";
import { useRef } from "react";

const boucle = (min: number, max: number, v: number) => {
  const r = max - min;
  return ((((v - min) % r) + r) % r) + min;
};

/**
 * Une rangée de mots qui défile en continu. Elle accélère quand on fait défiler la page,
 * change de sens quand on remonte et s'incline selon la vitesse.
 */
function Rangee({ mots, vitesse, contour }: { mots: string[]; vitesse: number; contour?: boolean }) {
  const base = useMotionValue(0);
  const { scrollY } = useScroll();
  const lisse = useSpring(useVelocity(scrollY), { damping: 50, stiffness: 400 });
  const facteur = useTransform(lisse, [0, 1000], [0, 5], { clamp: false });
  const inclinaison = useTransform(lisse, [-2500, 0, 2500], [14, 0, -14]);
  const x = useTransform(base, (v) => `${boucle(-25, 0, v)}%`);
  const sens = useRef(1);
  const reduit = useReducedMotion();

  useAnimationFrame((_, delta) => {
    if (reduit) return;
    let pas = sens.current * vitesse * (delta / 1000);
    const f = facteur.get();
    if (f < 0) sens.current = -1;
    else if (f > 0) sens.current = 1;
    pas += sens.current * pas * f;
    base.set(base.get() + pas);
  });

  return (
    <div className="defilant-rangee">
      <motion.div className={`defilant-piste ${contour ? "contour" : ""}`}
                  style={{ x, skewX: reduit ? 0 : inclinaison }}>
        {[0, 1, 2, 3].map((k) => (
          <span key={k} className="defilant-bloc" aria-hidden={k > 0 ? true : undefined}>
            {mots.map((m, i) => (
              <span key={i}><span className="defilant-mot">{m}</span><span className="defilant-etoile">✦</span></span>
            ))}
          </span>
        ))}
      </motion.div>
    </div>
  );
}

export default function Defilant({ mots, titre }: { mots: string[]; titre?: string }) {
  const liste = mots.filter(Boolean);
  if (!liste.length) return null;
  const moitie = Math.ceil(liste.length / 2);
  const seconde = [...liste.slice(moitie), ...liste.slice(0, moitie)];
  return (
    <section className="defilant grain" aria-label={titre || liste.join(", ")}>
      <Rangee mots={liste} vitesse={-2.2} />
      <Rangee mots={seconde} vitesse={2.2} contour />
    </section>
  );
}
