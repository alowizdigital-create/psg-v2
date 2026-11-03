"use client";

import { Loader2, Send } from "lucide-react";
import { useState } from "react";

import type { EntrepriseResume } from "@/lib/types";

export type Envoi = {
  offre?: string;
  choix?: number[];
  /** Renvoie false pour bloquer l'envoi (ex. options obligatoires manquantes). */
  avantEnvoi?: () => boolean;
  surErreursGroupes?: (e: Record<string, string>) => void;
  surSucces: (reference: string) => void;
};

type Erreurs = Partial<Record<"nom" | "telephone" | "email" | "date_evenement" | "message" | "global", string>>;

/** « 20/12/2026 » → « 2026-12-20 » ; null si vide ; false si invalide. */
function dateIso(saisie: string): string | null | false {
  const v = saisie.trim();
  if (!v) return null;
  const m = v.match(/^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})$/);
  if (!m) return false;
  const [j, mo, a] = [Number(m[1]), Number(m[2]), Number(m[3])];
  const d = new Date(Date.UTC(a, mo - 1, j));
  if (d.getUTCDate() !== j || d.getUTCMonth() !== mo - 1) return false;
  return `${a}-${String(mo).padStart(2, "0")}-${String(j).padStart(2, "0")}`;
}

/** Ajoute les « / » pendant la saisie : 20122026 → 20/12/2026. */
function masqueDate(e: React.FormEvent<HTMLInputElement>) {
  const chiffres = e.currentTarget.value.replace(/\D/g, "").slice(0, 8);
  const parts = [chiffres.slice(0, 2), chiffres.slice(2, 4), chiffres.slice(4)].filter(Boolean);
  e.currentTarget.value = parts.join("/");
}

function premiereErreur(v: unknown): string | undefined {
  if (Array.isArray(v)) return String(v[0]);
  if (typeof v === "string") return v;
  return undefined;
}

export default function DemandeForm({ envoi, afficherDate = false, entreprises, libelleBouton = "Envoyer" }: {
  envoi: Envoi; afficherDate?: boolean; entreprises?: EntrepriseResume[]; libelleBouton?: string;
}) {
  const [enCours, setEnCours] = useState(false);
  const [erreurs, setErreurs] = useState<Erreurs>({});

  async function soumettre(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (envoi.avantEnvoi && !envoi.avantEnvoi()) return;
    const donnees = new FormData(e.currentTarget);
    const date = dateIso(String(donnees.get("date_evenement") || ""));
    if (date === false) {
      setErreurs({ date_evenement: "Date invalide : utilisez le format JJ/MM/AAAA (ex. 20/12/2026)." });
      return;
    }
    const corps = {
      offre: envoi.offre ?? "",
      entreprise: (donnees.get("entreprise") as string) || "",
      nom: donnees.get("nom"),
      telephone: donnees.get("telephone"),
      email: donnees.get("email") || "",
      date_evenement: date,
      lieu: donnees.get("lieu") || "",
      message: donnees.get("message") || "",
      choix: envoi.choix ?? [],
      site_web: donnees.get("site_web") || "",
    };
    setEnCours(true);
    setErreurs({});
    try {
      const r = await fetch("/api/demandes/", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(corps),
      });
      const json = await r.json().catch(() => ({}));
      if (r.status === 201) {
        envoi.surSucces(json.reference);
        return;
      }
      if (r.status === 429) {
        setErreurs({ global: "Trop de demandes envoyées depuis votre connexion. Réessayez plus tard ou appelez-nous." });
        return;
      }
      const n: Erreurs = {};
      for (const k of ["nom", "telephone", "email", "date_evenement", "message"] as const) {
        const m = premiereErreur(json[k]);
        if (m) n[k] = m;
      }
      if (json.groupes && envoi.surErreursGroupes) envoi.surErreursGroupes(json.groupes);
      n.global = premiereErreur(json.offre) || premiereErreur(json.choix) || premiereErreur(json.non_field_errors)
        || (json.groupes ? "Certaines options obligatoires ne sont pas choisies." : undefined)
        || (Object.keys(n).length ? undefined : "Une erreur est survenue. Réessayez ou contactez-nous par téléphone.");
      setErreurs(n);
    } catch {
      setErreurs({ global: "Connexion impossible. Vérifiez votre réseau puis réessayez." });
    } finally {
      setEnCours(false);
    }
  }

  const champ = (nom: keyof Erreurs) => `field ${erreurs[nom] ? "invalid" : ""}`;

  return (
    <form className="form" onSubmit={soumettre} noValidate>
      <div className="form-row">
        <div className={champ("nom")}>
          <label htmlFor="nom">Nom complet *</label>
          <input id="nom" name="nom" autoComplete="name" required placeholder="Votre nom" />
          {erreurs.nom && <p className="err">{erreurs.nom}</p>}
        </div>
        <div className={champ("telephone")}>
          <label htmlFor="telephone">Téléphone *</label>
          <input id="telephone" name="telephone" type="tel" autoComplete="tel" required placeholder="6 XX XX XX XX"
                 inputMode="tel" />
          {erreurs.telephone && <p className="err">{erreurs.telephone}</p>}
        </div>
      </div>
      <div className="form-row">
        <div className={champ("email")}>
          <label htmlFor="email">E-mail (facultatif)</label>
          <input id="email" name="email" type="email" autoComplete="email" placeholder="vous@exemple.com" />
          {erreurs.email && <p className="err">{erreurs.email}</p>}
        </div>
        {afficherDate ? (
          <div className={champ("date_evenement")}>
            <label htmlFor="date_evenement">Date souhaitée</label>
            <input id="date_evenement" name="date_evenement" type="text" inputMode="numeric"
                   placeholder="JJ/MM/AAAA" maxLength={10} autoComplete="off" onInput={masqueDate} />
            {erreurs.date_evenement && <p className="err">{erreurs.date_evenement}</p>}
          </div>
        ) : entreprises?.length ? (
          <div className="field">
            <label htmlFor="entreprise">Entreprise concernée</label>
            <select id="entreprise" name="entreprise" defaultValue="">
              <option value="">Je ne sais pas / général</option>
              {entreprises.map((e) => <option key={e.slug} value={e.slug}>{e.nom}</option>)}
            </select>
          </div>
        ) : null}
      </div>
      {afficherDate && (
        <div className="field">
          <label htmlFor="lieu">Lieu (ville, quartier)</label>
          <input id="lieu" name="lieu" placeholder="Ex. Yaoundé, Bastos" />
        </div>
      )}
      <div className={champ("message")}>
        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" rows={4} placeholder="Précisez votre projet, le nombre d'invités…" />
        {erreurs.message && <p className="err">{erreurs.message}</p>}
      </div>
      <div className="hp" aria-hidden="true">
        <label htmlFor="site_web">Ne pas remplir</label>
        <input id="site_web" name="site_web" tabIndex={-1} autoComplete="off" />
      </div>
      {erreurs.global && <p className="form-alert" role="alert">{erreurs.global}</p>}
      <button type="submit" className="btn btn-primary" disabled={enCours} style={{ justifySelf: "start" }}>
        {enCours ? <><Loader2 size={18} className="spin" /> Envoi en cours…</> : <>{libelleBouton} <Send size={18} /></>}
      </button>
      <p style={{ fontSize: ".8rem", color: "var(--muted)" }}>
        En envoyant ce formulaire, vous acceptez d&apos;être recontacté par PS GROUP SARL au sujet de votre demande.
      </p>
    </form>
  );
}
