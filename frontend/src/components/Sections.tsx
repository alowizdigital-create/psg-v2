import { ArrowRight, ExternalLink } from "lucide-react";
import Link from "next/link";

import { fcfa } from "@/lib/format";
import type { EntrepriseResume, OffreResume, Section } from "@/lib/types";

import BlocOuverture from "./BlocOuverture";
import Coverflow from "./Coverflow";
import Defilant from "./Defilant";
import Icon from "./Icon";
import ListeSurvol from "./ListeSurvol";
import Losanges from "./Losanges";
import TexteGeant from "./TexteGeant";
import Panneaux from "./Panneaux";
import { Counter, Reveal, Spotlight, Tilt } from "./Motion";
import VideoCard from "./VideoCard";

type Contexte = { entreprises?: EntrepriseResume[]; offres?: OffreResume[] };

/** Typographie française : la ponctuation double (? ! : ; »)  reste collée au mot précédent. */
const fr = (t: string) => t.replace(/ ([?!:;»])/g, "\u00a0$1");

function Paragraphes({ texte }: { texte: string[] }) {
  return <>{texte.map((p, i) => <p key={i}>{p}</p>)}</>;
}

function Entete({ s, center = true }: { s: Section; center?: boolean }) {
  if (!s.sur_titre && !s.titre && !s.texte.length) return null;
  return (
    <Reveal className={`section-head ${center ? "center" : ""}`}>
      {s.sur_titre && <span className="eyebrow">{s.sur_titre}</span>}
      {s.titre && <h2>{fr(s.titre)}</h2>}
      <Paragraphes texte={s.texte} />
    </Reveal>
  );
}

function Bouton({ s, variante = "btn-primary" }: { s: Section; variante?: string }) {
  if (!s.bouton_label || !s.bouton_lien) return null;
  const externe = s.bouton_lien.startsWith("http");
  return (
    <Link href={s.bouton_lien} className={`btn ${variante}`} {...(externe ? { target: "_blank", rel: "noopener" } : {})}>
      {s.bouton_label} <ArrowRight size={18} />
    </Link>
  );
}

const grille = (n: number) => `grid grid-${Math.min(Math.max(n || 3, 2), 4)}`;

export function BlocSection({ s, ctx }: { s: Section; ctx: Contexte }) {
  switch (s.type) {
    case "entete":
      return null; // rendu par l'en-tête de page

    case "chiffres":
      return (
        <section className="section stats grain" style={{ padding: "clamp(48px, 7vw, 80px) 0" }}>
          <div className={`container ${grille(s.elements.length)}`}>
            {s.elements.map((e, i) => (
              <Reveal key={e.id} delay={i * 0.1}>
                <div className="stat-num"><Counter value={e.titre} /></div>
                <div className="stat-label">{e.sous_titre}</div>
              </Reveal>
            ))}
          </div>
        </section>
      );

    case "cartes":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            <div className={grille(s.colonnes)}>
              {s.elements.map((e, i) => (
                <Reveal key={e.id} delay={(i % s.colonnes) * 0.1}>
                  <Spotlight className="card">
                    {e.image && <div className="card-img"><img src={e.image} alt="" loading="lazy" /></div>}
                    {e.icone && !e.image && <div className="icon-badge"><Icon name={e.icone} /></div>}
                    {e.sous_titre && (
                      <span className="meta" style={{ display: "flex", gap: 6, alignItems: "center" }}>
                        {e.icone && e.image && <Icon name={e.icone} size={14} />}{e.sous_titre}
                      </span>
                    )}
                    <h3 style={e.icone || e.sous_titre ? undefined : { marginTop: 0 }}>{e.titre}</h3>
                    <Paragraphes texte={e.texte} />
                    {e.lien && (
                      <Link href={e.lien} className="go" style={{ display: "inline-flex", gap: 6, marginTop: 14, fontWeight: 600, color: "var(--primary)" }}>
                        En savoir plus <ArrowRight size={16} />
                      </Link>
                    )}
                  </Spotlight>
                </Reveal>
              ))}
            </div>
            {s.bouton_label && <div style={{ textAlign: "center", marginTop: 40 }}><Bouton s={s} /></div>}
          </div>
        </section>
      );

    case "tuiles":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            <div className={grille(s.colonnes)}>
              {s.elements.map((e, i) => (
                <Reveal key={e.id} delay={(i % s.colonnes) * 0.08}>
                  <div className="tile">
                    <span className="ico"><Icon name={e.icone} /></span>
                    <strong>{e.titre}</strong>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      );

    case "lignes":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            {s.elements.map((e) => (
              <div className="row" key={e.id}>
                {e.image && (
                  <Reveal className="row-img" y={60}><img src={e.image} alt={e.titre} loading="lazy" /></Reveal>
                )}
                <Reveal delay={0.15}>
                  {e.icone && <div className="icon-badge" style={{ marginBottom: 16 }}><Icon name={e.icone} /></div>}
                  <h3>{e.titre}</h3>
                  <Paragraphes texte={e.texte} />
                </Reveal>
              </div>
            ))}
          </div>
        </section>
      );

    case "galerie":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            <Coverflow images={s.elements.map((e) => ({ image: e.image, legende: e.titre }))} label={s.titre || "Galerie photo"} />
          </div>
        </section>
      );

    case "personnes":
      // Même slide 3D que les galeries : nom en légende, rôle / session dessous.
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            <Coverflow images={s.elements.map((e) => ({ image: e.image, legende: e.titre, sous: e.sous_titre }))}
                       label={s.titre || "Photos"} />
          </div>
        </section>
      );

    case "texte":
    case "liste": {
      const encadre = s.elements.length > 0;
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className={`container text-block ${encadre ? "" : "single"}`}>
            <Reveal className="prose">
              {s.sur_titre && <span className="eyebrow">{s.sur_titre}</span>}
              {s.titre && <h2>{s.titre}</h2>}
              <Paragraphes texte={s.texte} />
              {s.bouton_label && <div style={{ marginTop: 28 }}><Bouton s={s} /></div>}
            </Reveal>
            {encadre && (
              <Reveal delay={0.2} className="facts grain">
                {s.titre_encadre && <h3>{s.titre_encadre}</h3>}
                <ul>
                  {s.elements.map((e) => (
                    <li key={e.id}>
                      <span className="ico"><Icon name={e.icone} size={20} /></span>
                      <span>{e.titre}{e.texte.length > 0 && <small style={{ display: "block", color: "#cdbab4" }}>{e.texte.join(" ")}</small>}</span>
                    </li>
                  ))}
                </ul>
              </Reveal>
            )}
          </div>
        </section>
      );
    }

    case "video":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            {s.elements.filter((e) => e.lien).map((e) => (
              <Reveal key={e.id}><VideoCard url={e.lien} titre={e.titre} sousTitre={e.sous_titre} /></Reveal>
            ))}
          </div>
        </section>
      );

    case "liens":
      return (
        <section className={`section ${s.fond_alterne ? "section-alt" : ""}`} style={{ padding: "40px 0" }}>
          <div className="container">
            <Entete s={s} />
            <Reveal className="links-row">
              {s.elements.filter((e) => e.lien).map((e) => (
                <a key={e.id} href={e.lien} target="_blank" rel="noopener noreferrer" className="btn btn-dark">
                  {e.icone ? <Icon name={e.icone} size={18} /> : <ExternalLink size={18} />} {e.titre}
                </a>
              ))}
            </Reveal>
          </div>
        </section>
      );

    case "entreprises":
      return (
        <section id="entreprises" className={`section ${s.fond_alterne ? "section-alt" : ""}`}>
          <div className="container">
            <Entete s={s} />
            <div className="grid grid-3">
              {(ctx.entreprises ?? []).map((e, i) => (
                <Reveal key={e.slug} delay={(i % 3) * 0.12}>
                  <Link href={`/entreprises/${e.slug}`} aria-label={e.nom}>
                    <Tilt className="branch-card spotlight" max={10}>
                      {e.banniere && <div className="bg" style={{ backgroundImage: `url(${e.banniere})` }} />}
                      <span className="num">{String(i + 1).padStart(2, "0")}</span>
                      <div className="inner">
                        <div className="ico"><Icon name={e.icone} /></div>
                        <h3>{e.nom}</h3>
                        <p>{e.resume}</p>
                        <span className="go">Découvrir <ArrowRight size={16} /></span>
                      </div>
                    </Tilt>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      );

    case "offres": {
      // Catalogue en panneaux d'images qui s'ouvrent au survol (8 offres au plus).
      const offres = (ctx.offres ?? []).slice(0, 8);
      if (!offres.length) return null;
      return (
        <section className={`section section-panneaux ${s.fond_alterne ? "section-alt" : ""}`}>
          <Entete s={s} />
          <Panneaux panneaux={offres.map((o) => ({
            id: o.slug, titre: o.titre, texte: o.resume, image: o.image, lien: `/catalogue/${o.slug}`,
            etiquette: o.entreprise?.nom, prix: o.prix_a_partir_de ? `Dès ${fcfa(o.prix_a_partir_de)}` : "",
            bouton: "Composer",
          }))} />
          {s.bouton_label && <div className="panneaux-bouton"><Bouton s={s} variante="btn-dark" /></div>}
        </section>
      );
    }

    case "cta":
      return <CtaBanniere titre={s.titre} texte={s.texte.join(" ")} label={s.bouton_label} lien={s.bouton_lien} />;

    default:
      return null;
  }
}

export function CtaBanniere({ titre, texte, label = "Nous contacter", lien = "/contact" }: {
  titre: string; texte?: string; label?: string; lien?: string;
}) {
  if (!titre) return null;
  return (
    <section className="section" style={{ paddingTop: 20 }}>
      <div className="container">
        <Reveal y={60}>
          <div className="cta grain">
            <div className="orb" style={{ width: 300, height: 300, background: "rgba(245,184,0,.25)", right: -60, top: -80 }} />
            <div>
              <h2>{fr(titre)}</h2>
              {texte && <p>{texte}</p>}
            </div>
            <Link href={lien || "/contact"} className="btn btn-primary">{label || "Nous contacter"} <ArrowRight size={18} /></Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}

export default function Sections({ sections, ctx = {} }: { sections: Section[]; ctx?: Contexte }) {
  return <>{sections.map((s) => <BlocSection key={s.id} s={s} ctx={ctx} />)}</>;
}
