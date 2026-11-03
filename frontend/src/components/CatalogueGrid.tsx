"use client";

import { AnimatePresence, LayoutGroup, motion } from "motion/react";
import { useState } from "react";

import type { EntrepriseResume, OffreResume } from "@/lib/types";

import Icon from "./Icon";
import OfferCard from "./OfferCard";

export default function CatalogueGrid({ offres, entreprises, initial }: {
  offres: OffreResume[]; entreprises: EntrepriseResume[]; initial: string;
}) {
  const avecOffres = entreprises.filter((e) => offres.some((o) => o.entreprise.slug === e.slug));
  const [filtre, setFiltre] = useState(avecOffres.some((e) => e.slug === initial) ? initial : "");
  const visibles = filtre ? offres.filter((o) => o.entreprise.slug === filtre) : offres;

  function choisir(slug: string) {
    setFiltre(slug);
    const url = slug ? `?entreprise=${slug}` : window.location.pathname;
    window.history.replaceState(null, "", url);
  }

  if (!offres.length) {
    return <p className="empty-state">Le catalogue est en cours de préparation. Contactez-nous pour toute demande.</p>;
  }

  return (
    <>
      <LayoutGroup>
        <div className="filters" role="tablist" aria-label="Filtrer par entreprise">
          {[{ slug: "", nom: "Toutes les offres", icone: "sparkles" }, ...avecOffres].map((e) => (
            <button key={e.slug || "tout"} className={`chip ${filtre === e.slug ? "active" : ""}`} role="tab"
                    aria-selected={filtre === e.slug} onClick={() => choisir(e.slug)}>
              {filtre === e.slug && <motion.span layoutId="chip" className="chip-bg" transition={{ type: "spring", stiffness: 400, damping: 32 }} />}
              <span><Icon name={e.icone} size={16} />{e.nom}</span>
            </button>
          ))}
        </div>
      </LayoutGroup>
      <motion.div layout className="grid grid-3">
        <AnimatePresence mode="popLayout">
          {visibles.map((o, i) => (
            <motion.div key={o.slug} layout initial={{ opacity: 0, scale: 0.9, y: 30 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.9 }}
                        transition={{ duration: 0.45, delay: i * 0.04 }}>
              <OfferCard offre={o} />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
    </>
  );
}
