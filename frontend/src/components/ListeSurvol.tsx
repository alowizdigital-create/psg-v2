"use client";

import { ArrowUpRight } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useState } from "react";

import type { Element } from "@/lib/types";

import Icon from "./Icon";

/**
 * Liste interactive : de grands titres numérotés ; au survol (ou au toucher sur mobile), la ligne se
 * remplit de bordeaux et le détail s'affiche dans le panneau de droite (sous la ligne sur mobile).
 */
export default function ListeSurvol({ elements }: { elements: Element[] }) {
  const [actif, setActif] = useState(0);
  const courant = elements[actif];
  if (!elements.length) return null;

  return (
    <div className="survol">
      <ol className="survol-liste">
        {elements.map((e, i) => (
          <li key={e.id} className={i === actif ? "actif" : ""} onMouseEnter={() => setActif(i)}>
            <button type="button" className="survol-tete" onClick={() => setActif(i)} onFocus={() => setActif(i)}
                    aria-expanded={i === actif}>
              <span className="survol-num">{String(i + 1).padStart(2, "0")}</span>
              <span className="survol-titre">{e.titre}</span>
              <ArrowUpRight className="survol-fleche" size={28} />
            </button>
            <div className="survol-corps">
              <div>{e.texte.map((t, j) => <p key={j}>{t}</p>)}</div>
            </div>
          </li>
        ))}
      </ol>

      <div className="survol-panneau grain" aria-live="polite">
        <AnimatePresence mode="wait">
          <motion.div key={actif} initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -16 }} transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}>
            <span className="survol-panneau-num">{String(actif + 1).padStart(2, "0")}</span>
            {courant.image ? <img src={courant.image} alt="" className="survol-panneau-img" />
              : courant.icone && <span className="survol-panneau-ico"><Icon name={courant.icone} size={26} /></span>}
            <h3>{courant.titre}</h3>
            {courant.texte.map((t, j) => <p key={j}>{t}</p>)}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
