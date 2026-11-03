import type { Metadata } from "next";
import { notFound } from "next/navigation";

import Gallery from "@/components/Gallery";
import { Reveal } from "@/components/Motion";
import OfferConfigurator from "@/components/OfferConfigurator";
import PageHero from "@/components/PageHero";
import { api } from "@/lib/api";
import { fcfa } from "@/lib/format";

type Props = { params: Promise<{ slug: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const o = await api.offre((await params).slug);
  return o ? { title: o.titre, description: o.resume } : {};
}

export default async function PageOffre({ params }: Props) {
  const offre = await api.offre((await params).slug);
  if (!offre) notFound();
  const photos = [
    ...(offre.image ? [{ image: offre.image, legende: offre.titre }] : []),
    ...offre.galerie,
  ];
  return (
    <>
      <PageHero surTitre={offre.entreprise.nom} titre={offre.titre} texte={offre.resume} image={offre.image}
                fil={[{ href: "/catalogue", label: "Catalogue" },
                      { href: `/entreprises/${offre.entreprise.slug}`, label: offre.entreprise.nom }]}>
        {offre.prix_a_partir_de ? (
          <Reveal delay={0.35}>
            <p style={{ marginTop: 22 }}>
              <span className="badge" style={{ background: "var(--accent)", color: "var(--night)", fontSize: ".85rem", padding: "8px 14px" }}>
                À partir de {fcfa(offre.prix_a_partir_de)}
              </span>
            </p>
          </Reveal>
        ) : null}
      </PageHero>
      <section className="section" style={{ paddingTop: 50 }}>
        <div className="container">
          {(offre.description.length > 0 || photos.length > 1) && (
            <Reveal className="prose offer-intro">
              {offre.description.map((p, i) => <p key={i}>{p}</p>)}
              {photos.length > 1 && <Gallery images={photos} mode="thumbs" />}
            </Reveal>
          )}
          <OfferConfigurator offre={offre} />
        </div>
      </section>
    </>
  );
}
