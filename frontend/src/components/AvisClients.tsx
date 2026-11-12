"use client";

import { ChevronLeft, ChevronRight, Quote, Star } from "lucide-react";
import Link from "next/link";
import { useRef } from "react";

import type { ResumeAvis } from "@/lib/types";

import { Reveal } from "./Motion";
import { WhatsappIcon } from "./Social";

function Etoiles({ note, taille = 18 }: { note: number; taille?: number }) {
  return (
    <span className="etoiles" role="img" aria-label={`Note : ${note} sur 5`}>
      {[1, 2, 3, 4, 5].map((i) => (
        <Star key={i} size={taille} className={i <= Math.round(note) ? "on" : ""} aria-hidden="true" />
      ))}
    </span>
  );
}

/** Section « Avis des clients » : n'affiche rien s'il n'y a aucun avis publié. */
export default function AvisClients({ avis, titre = "Ce que disent nos clients", surTitre = "Avis clients",
                                      montrerOffre = false, className = "" }: {
  avis: ResumeAvis; titre?: string; surTitre?: string; montrerOffre?: boolean; className?: string;
}) {
  const piste = useRef<HTMLDivElement>(null);
  if (!avis.total) return null;

  const defiler = (sens: 1 | -1) => {
    const el = piste.current;
    if (el) el.scrollBy({ left: sens * Math.min(el.clientWidth, 420), behavior: "smooth" });
  };

  return (
    <section className={`section avis-section ${className}`} aria-labelledby="titre-avis">
      <div className="container">
        <Reveal className="section-head center">
          <span className="eyebrow">{surTitre}</span>
          <h2 id="titre-avis">{titre}</h2>
          <p className="avis-resume">
            <Etoiles note={avis.moyenne} taille={22} />
            <strong>{avis.moyenne.toLocaleString("fr-FR")}</strong> / 5 · {avis.total} avis
          </p>
        </Reveal>

        <div className="avis-piste-wrap">
          {avis.total > 3 && (
            <>
              <button className="round-btn avis-fleche prev" onClick={() => defiler(-1)} aria-label="Avis précédents">
                <ChevronLeft />
              </button>
              <button className="round-btn avis-fleche next" onClick={() => defiler(1)} aria-label="Avis suivants">
                <ChevronRight />
              </button>
            </>
          )}
          <div className={`avis-piste ${avis.total <= 3 ? "centre" : ""}`} ref={piste} tabIndex={0}
               aria-label="Avis des clients">
            {avis.liste.map((a, i) => (
              <Reveal key={a.id} delay={(i % 3) * 0.08} as="article" className="avis-carte">
                <Quote className="avis-guillemets" size={42} aria-hidden="true" />
                <Etoiles note={a.note} />
                <blockquote>{a.texte}</blockquote>
                {montrerOffre && a.offre && (
                  <Link className="avis-offre" href={`/catalogue/${a.offre.slug}`}>{a.offre.titre}</Link>
                )}
                <footer>
                  <span className="avis-avatar">
                    {a.photo ? <img src={a.photo} alt="" loading="lazy" /> : a.nom.trim().charAt(0).toUpperCase()}
                  </span>
                  <span>
                    <strong>{a.nom}</strong>
                    {a.qualite && <small>{a.qualite}</small>}
                  </span>
                  {a.verifiable && (
                    // Redirection côté serveur vers le WhatsApp du client : son numéro n'est jamais dans la page.
                    <a className="avis-verifier" href={`/api/avis/${a.id}/verifier/`} target="_blank"
                       rel="noopener noreferrer nofollow"
                       title="Vérifiez auprès du client que cet avis est authentique"
                       aria-label={`Confirmer l'avis de ${a.nom} : écrire au client sur WhatsApp (s'ouvre dans un nouvel onglet)`}>
                      <WhatsappIcon size={15} /> Confirmer l’avis
                    </a>
                  )}
                </footer>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
