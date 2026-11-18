"use client";

import { ArrowRight } from "lucide-react";
import { motion, useReducedMotion } from "motion/react";
import Link from "next/link";
import { useState } from "react";

export type Panneau = {
  id: number | string; titre: string; texte: string; image: string | null; lien: string;
  etiquette?: string; prix?: string; bouton?: string;
};

/**
 * Panneaux d'images côte à côte (inspirés de derin15.com) : photos en noir et blanc avec le titre
 * écrit à la verticale ; au survol (ou au toucher sur mobile), le panneau s'élargit, passe en
 * couleur et affiche son texte et un bouton.
 */
export default function Panneaux({ panneaux }: { panneaux: Panneau[] }) {
  const [actif, setActif] = useState<number | null>(null);
  const reduit = useReducedMotion();
  if (!panneaux.length) return null;

  return (
    <div className="panneaux" onMouseLeave={() => setActif(null)}>
      {panneaux.map((p, i) => {
        const ouvert = actif === i;
        const externe = p.lien.startsWith("http");
        return (
          <motion.div
            key={p.id}
            className={`panneau ${p.image ? "" : "sans-image"} ${ouvert ? "ouvert" : ""} ${actif !== null && !ouvert ? "replie" : ""}`}
            onMouseEnter={() => setActif(i)}
            onClick={() => setActif(i)}
            initial={reduit ? false : { opacity: 0, y: 60 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-60px" }}
            transition={{ duration: 0.7, delay: i * 0.07, ease: [0.22, 1, 0.36, 1] }}
          >
            {p.image && <img src={p.image} alt="" loading="lazy" draggable={false} />}
            <span className="panneau-vertical" aria-hidden={ouvert}>{p.titre}</span>
            <div className="panneau-contenu" aria-hidden={!ouvert}>
              <span className="panneau-num">
                {String(i + 1).padStart(2, "0")}{p.etiquette && <span className="panneau-etiquette">{p.etiquette}</span>}
              </span>
              <h3>{p.titre}</h3>
              {p.texte && <p>{p.texte}</p>}
              {p.prix && <strong className="panneau-prix">{p.prix}</strong>}
              {p.lien && (
                <Link href={p.lien} className="btn btn-primary" tabIndex={ouvert ? 0 : -1}
                      onFocus={() => setActif(i)} {...(externe ? { target: "_blank", rel: "noopener" } : {})}>
                  {p.bouton || "Découvrir"} <ArrowRight size={18} />
                </Link>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
