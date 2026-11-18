"use client";

import { motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import { useRef } from "react";

import { BadgeRotatif } from "./BlocOuverture";

/**
 * Texte géant qui glisse avec le défilement de la page (inspiré de derin15.com) : une rangée
 * pleine part vers la gauche, une rangée évidée part vers la droite.
 */
export default function TexteGeant({ texte, second }: { texte: string; second?: string }) {
  const ref = useRef<HTMLElement>(null);
  const reduit = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] });
  const x1 = useTransform(scrollYProgress, [0, 1], ["5%", "-45%"]);
  const x2 = useTransform(scrollYProgress, [0, 1], ["-45%", "5%"]);
  const rangee = (t: string) => Array.from({ length: 6 }, (_, i) => (
    <span key={i}>{t}<span className="geant-etoile">✦</span></span>
  ));

  return (
    <section ref={ref} className="texte-geant" aria-label={texte}>
      <motion.div className="texte-geant-rangee plein" aria-hidden="true" style={reduit ? undefined : { x: x1 }}>
        {rangee(texte)}
      </motion.div>
      <motion.div className="texte-geant-rangee evide" aria-hidden="true" style={reduit ? undefined : { x: x2 }}>
        {rangee(second || texte)}
      </motion.div>
      <BadgeRotatif texte={`${texte} • Digital • Creative • Solutions • `} />
    </section>
  );
}
