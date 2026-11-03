"use client";

import { ArrowRight, Check, Send } from "lucide-react";
import { AnimatePresence, animate, motion, useReducedMotion } from "motion/react";
import { useEffect, useMemo, useRef, useState } from "react";

import { fcfa } from "@/lib/format";
import type { Groupe, OffreDetail } from "@/lib/types";

import DemandeForm, { type Envoi } from "./DemandeForm";
import Icon from "./Icon";
import Success from "./Success";

function TotalAnime({ valeur }: { valeur: number }) {
  const ref = useRef<HTMLElement>(null);
  const precedent = useRef(valeur);
  const reduit = useReducedMotion();
  useEffect(() => {
    if (!ref.current) return;
    if (reduit) {
      ref.current.textContent = fcfa(valeur) || "Sur devis";
      return;
    }
    const c = animate(precedent.current, valeur, {
      duration: 0.6,
      ease: "easeOut",
      onUpdate: (v) => { if (ref.current) ref.current.textContent = fcfa(Math.round(v)) || "Sur devis"; },
    });
    precedent.current = valeur;
    return () => c.stop();
  }, [valeur, reduit]);
  return <strong ref={ref}>{fcfa(valeur) || "Sur devis"}</strong>;
}

export default function OfferConfigurator({ offre }: { offre: OffreDetail }) {
  const [choix, setChoix] = useState<Record<number, number[]>>({});
  const [erreursGroupes, setErreursGroupes] = useState<Record<string, string>>({});
  const [reference, setReference] = useState<string | null>(null);
  const formRef = useRef<HTMLDivElement>(null);

  const selection = useMemo(
    () => offre.groupes.flatMap((g) => g.options.filter((o) => choix[g.id]?.includes(o.id)).map((o) => ({ g, o }))),
    [choix, offre.groupes],
  );
  const total = (offre.prix_a_partir_de ?? 0) + selection.reduce((s, { o }) => s + (o.prix ?? 0), 0);

  function basculer(g: Groupe, optionId: number) {
    setErreursGroupes((e) => { const n = { ...e }; delete n[String(g.id)]; return n; });
    setChoix((c) => {
      const actuel = c[g.id] ?? [];
      if (g.type === "unique") return { ...c, [g.id]: actuel.includes(optionId) && !g.obligatoire ? [] : [optionId] };
      return { ...c, [g.id]: actuel.includes(optionId) ? actuel.filter((x) => x !== optionId) : [...actuel, optionId] };
    });
  }

  function verifier() {
    const erreurs: Record<string, string> = {};
    for (const g of offre.groupes) {
      if (g.obligatoire && !(choix[g.id]?.length)) erreurs[String(g.id)] = `Choisissez une option pour « ${g.libelle} ».`;
    }
    setErreursGroupes(erreurs);
    const premier = Object.keys(erreurs)[0];
    if (premier) document.getElementById(`groupe-${premier}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
    return !premier;
  }

  const envoi: Envoi = {
    offre: offre.slug,
    choix: selection.map(({ o }) => o.id),
    avantEnvoi: verifier,
    surErreursGroupes: setErreursGroupes,
    surSucces: setReference,
  };

  // Après l'envoi, la page se limite au message de remerciement : on masque
  // la description et la galerie de l'offre et on se place sur le message.
  useEffect(() => {
    if (!reference) return;
    document.body.classList.add("demande-envoyee");
    requestAnimationFrame(() =>
      document.getElementById("confirmation")?.scrollIntoView({ behavior: "smooth", block: "start" }));
    return () => document.body.classList.remove("demande-envoyee");
  }, [reference]);

  if (reference) {
    return (
      <Success reference={reference} titre={offre.titre}
               choix={selection.map(({ g, o }) => `${g.libelle} : ${o.libelle}`)}
               total={total} />
    );
  }

  return (
    <div className="offer-layout">
      <div>
        {offre.groupes.length > 0 && (
          <>
            <div className="step-title"><span className="n">1</span><h2 style={{ fontSize: "1.6rem" }}>Cochez ce qui vous intéresse</h2></div>
            <p style={{ color: "var(--muted)" }}>Vos choix sont envoyés à notre équipe, qui vous rappelle pour finaliser.</p>
            {offre.groupes.map((g, gi) => {
              const erreur = erreursGroupes[String(g.id)];
              return (
                <motion.div key={g.id} id={`groupe-${g.id}`} className={`group ${erreur ? "error" : ""}`}
                            initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true, margin: "-40px" }} transition={{ duration: 0.6, delay: gi * 0.05 }}
                            animate={erreur ? { x: [0, -8, 8, -5, 5, 0] } : undefined}>
                  <div className="group-head">
                    <h3>{g.icone && <Icon name={g.icone} size={20} />}{g.libelle}
                      <span className={`badge ${g.obligatoire ? "badge-req" : "badge-opt"}`}>
                        {g.obligatoire ? "Obligatoire" : "Facultatif"}
                      </span>
                    </h3>
                    <small>{g.aide || (g.type === "unique" ? "Un seul choix" : "Plusieurs choix possibles")}</small>
                  </div>
                  <div className="options" role={g.type === "unique" ? "radiogroup" : "group"} aria-label={g.libelle}>
                    {g.options.map((o) => {
                      const actif = choix[g.id]?.includes(o.id) ?? false;
                      return (
                        <motion.button type="button" key={o.id} className={`opt ${g.type === "unique" ? "radio" : ""} ${actif ? "on" : ""}`}
                                       onClick={() => basculer(g, o.id)} whileTap={{ scale: 0.97 }}
                                       role={g.type === "unique" ? "radio" : "checkbox"} aria-checked={actif}>
                          <span className="box">
                            <AnimatePresence>
                              {actif && (
                                <motion.span initial={{ scale: 0, rotate: -45 }} animate={{ scale: 1, rotate: 0 }}
                                             exit={{ scale: 0 }} transition={{ type: "spring", stiffness: 500, damping: 22 }}
                                             style={{ display: "grid" }}>
                                  <Check size={15} strokeWidth={3.5} />
                                </motion.span>
                              )}
                            </AnimatePresence>
                          </span>
                          <span style={{ flex: 1 }}>
                            <strong>{o.libelle}</strong>
                            {o.description && <small>{o.description}</small>}
                            {o.prix ? <span className="p">+ {fcfa(o.prix)}</span> : null}
                          </span>
                          {o.image && <img className="thumb" src={o.image} alt="" loading="lazy" />}
                        </motion.button>
                      );
                    })}
                  </div>
                  {erreur && <p className="err" role="alert">{erreur}</p>}
                </motion.div>
              );
            })}
          </>
        )}

        <div ref={formRef} id="vos-coordonnees">
          <div className="step-title"><span className="n">{offre.groupes.length ? 2 : 1}</span><h2 style={{ fontSize: "1.6rem" }}>Vos coordonnées</h2></div>
          <p style={{ color: "var(--muted)", marginBottom: 20 }}>
            Un membre de l&apos;équipe {offre.entreprise.nom} vous appelle rapidement. Vous recevez aussi un SMS de confirmation.
          </p>
          <DemandeForm envoi={envoi} afficherDate libelleBouton="Envoyer ma demande" />
        </div>
      </div>

      <aside className="summary grain" aria-label="Récapitulatif de votre demande">
        <div className="orb" style={{ width: 220, height: 220, background: "rgba(245,184,0,.22)", right: -80, top: -80 }} />
        <span className="eyebrow">Votre sélection</span>
        <h3>{offre.titre}</h3>
        <p className="sub">{offre.entreprise.nom}</p>
        <ul>
          {offre.prix_a_partir_de ? (
            <li><span>Prestation de base</span><span>{fcfa(offre.prix_a_partir_de)}</span></li>
          ) : null}
          <AnimatePresence initial={false}>
            {selection.map(({ g, o }) => (
              <motion.li key={o.id} layout initial={{ opacity: 0, x: 30, height: 0 }}
                         animate={{ opacity: 1, x: 0, height: "auto" }} exit={{ opacity: 0, x: -30, height: 0 }}>
                <span>{o.libelle}<small style={{ display: "block", color: "#b9a59f", fontSize: ".75rem" }}>{g.libelle}</small></span>
                <span>{o.prix ? `+ ${fcfa(o.prix)}` : "inclus"}</span>
              </motion.li>
            ))}
          </AnimatePresence>
        </ul>
        {!selection.length && <p className="empty">Cochez des options pour composer votre demande.</p>}
        <div className="total"><span>Total estimé</span><TotalAnime valeur={total} /></div>
        <p className="note">Montant indicatif, confirmé lors de l&apos;appel de notre équipe.</p>
        <button className="btn btn-primary" onClick={() => formRef.current?.scrollIntoView({ behavior: "smooth" })}>
          Je finalise ma demande <ArrowRight size={18} />
        </button>
      </aside>

      <div className="mobile-bar">
        <span>
          <small>{selection.length} option{selection.length > 1 ? "s" : ""} · total estimé</small>
          <strong>{fcfa(total) || "Sur devis"}</strong>
        </span>
        <button className="btn btn-primary" onClick={() => formRef.current?.scrollIntoView({ behavior: "smooth" })}>
          Finaliser <Send size={16} />
        </button>
      </div>
    </div>
  );
}
