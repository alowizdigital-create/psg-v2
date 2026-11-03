"use client";

import { ArrowRight, Check, PhoneCall } from "lucide-react";
import { motion, useReducedMotion } from "motion/react";
import Link from "next/link";

import { fcfa } from "@/lib/format";

const COULEURS = ["#f5b800", "#6e1524", "#ffe08a", "#9a2438", "#ffffff"];

export default function Success({ reference, titre, choix = [], total }: {
  reference: string; titre?: string; choix?: string[]; total?: number;
}) {
  const reduit = useReducedMotion();
  return (
    <motion.div className="success" initial={{ opacity: 0, scale: 0.94 }} animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }} role="status">
      {!reduit && Array.from({ length: 36 }).map((_, i) => (
        <motion.span key={i} className="confetti"
                     style={{ left: `${(i * 37) % 100}%`, background: COULEURS[i % COULEURS.length] }}
                     initial={{ y: -20, rotate: 0, opacity: 1 }}
                     animate={{ y: 700, rotate: 360 + i * 40, opacity: 0 }}
                     transition={{ duration: 2.2 + (i % 5) * 0.3, delay: (i % 7) * 0.08, ease: "easeIn" }} />
      ))}
      <motion.div className="check" initial={{ scale: 0, rotate: -120 }} animate={{ scale: 1, rotate: 0 }}
                  transition={{ type: "spring", stiffness: 260, damping: 16, delay: 0.2 }}>
        <Check size={46} strokeWidth={3} />
      </motion.div>
      <h2>Merci, votre demande est envoyée !</h2>
      <div className="ref">{reference}</div>
      <p>
        <PhoneCall size={18} style={{ display: "inline", verticalAlign: "-3px", marginRight: 6 }} />
        <strong>Un membre de notre équipe va vous appeler</strong> très bientôt pour en discuter.
        Vous allez recevoir un SMS de confirmation avec votre référence.
      </p>
      {(titre || choix.length > 0) && (
        <div style={{ maxWidth: 480, margin: "26px auto 0", textAlign: "left", background: "var(--bg-alt)", borderRadius: 16, padding: 20 }}>
          {titre && <strong style={{ display: "block", marginBottom: 8 }}>{titre}</strong>}
          <ul style={{ display: "grid", gap: 6, color: "var(--muted)", fontSize: ".92rem" }}>
            {choix.map((c) => <li key={c}>✓ {c}</li>)}
          </ul>
          {total ? <p style={{ marginTop: 12, fontWeight: 700, color: "var(--primary)" }}>Total estimé : {fcfa(total)}</p> : null}
        </div>
      )}
      <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap", marginTop: 30 }}>
        <Link href="/catalogue" className="btn btn-dark">Voir d&apos;autres offres</Link>
        <Link href="/" className="btn btn-primary">Retour à l&apos;accueil <ArrowRight size={18} /></Link>
      </div>
    </motion.div>
  );
}
