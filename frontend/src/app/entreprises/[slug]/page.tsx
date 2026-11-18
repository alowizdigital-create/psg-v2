import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Reveal } from "@/components/Motion";
import OfferCard from "@/components/OfferCard";
import HeroEntreprise from "@/components/HeroEntreprise";
import HeroMusique from "@/components/HeroMusique";
import PageHero from "@/components/PageHero";
import Sections, { CtaBanniere } from "@/components/Sections";
import { api } from "@/lib/api";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const e = await api.entreprise((await params).slug);
  return e ? { title: e.nom, description: e.resume || e.accroche } : {};
}

export default async function PageEntreprise({ params }: Props) {
  const e = await api.entreprise((await params).slug);
  if (!e) notFound();
  return (
    <>
      {(e.slides?.length ?? 0) > 0 && e.hero_style === "musique" ? (
        <HeroMusique slides={e.slides} titre={e.hero_titre || e.nom} sousTitre={e.hero_sous_titre} />
      ) : (e.slides?.length ?? 0) > 0 ? (
        <HeroEntreprise slides={e.slides} nom={e.nom} logo={e.logo} slogan={e.accroche}
                        cta={{ href: e.offres[0] ? `/catalogue/${e.offres[0].slug}` : "/contact", label: "S'inscrire" }} />
      ) : (
        <PageHero surTitre={e.sur_titre} titre={e.nom} texte={e.accroche} image={e.banniere} icone={e.icone}
                  fil={[{ href: "/#entreprises", label: "Nos entreprises" }]} />
      )}
      <div id="contenu" />
      <Sections sections={e.sections} ctx={{ offres: e.offres.map((o) => ({ ...o, entreprise: e })) }} />
      {/* Grille des offres, sauf si la page présente déjà son catalogue (panneaux ou bloc d'offres). */}
      {e.offres.length > 0 && !e.sections.some((s) => s.type === "panneaux" || s.type === "offres") && (
        <section className="section section-alt">
          <div className="container">
            <Reveal className="section-head center">
              <span className="eyebrow">Catalogue {e.nom}</span>
              <h2>Demander un devis</h2>
              <p>Choisissez une offre, cochez les options qui vous intéressent : notre équipe vous rappelle.</p>
            </Reveal>
            <div className="grid grid-3">
              {e.offres.map((o, i) => (
                <Reveal key={o.slug} delay={(i % 3) * 0.1}><OfferCard offre={{ ...o, entreprise: e }} /></Reveal>
              ))}
            </div>
          </div>
        </section>
      )}
      <CtaBanniere titre={e.cta_titre} texte={e.cta_texte} />
    </>
  );
}
