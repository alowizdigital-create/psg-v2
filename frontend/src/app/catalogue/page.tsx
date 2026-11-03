import type { Metadata } from "next";

import CatalogueGrid from "@/components/CatalogueGrid";
import PageHero from "@/components/PageHero";
import { CtaBanniere } from "@/components/Sections";
import { api } from "@/lib/api";

export const metadata: Metadata = {
  title: "Catalogue",
  description: "Composez votre prestation sur mesure : mariage, shooting, digital, formation, musique, média.",
};

type Props = { searchParams: Promise<{ entreprise?: string }> };

export default async function Catalogue({ searchParams }: Props) {
  const [site, offres, { entreprise }] = await Promise.all([api.site(), api.offres(), searchParams]);
  return (
    <>
      <PageHero surTitre="Catalogue" titre="Composez votre prestation"
                texte="Choisissez une offre, cochez les options qui vous intéressent et envoyez votre demande : un membre de notre équipe vous rappelle."
                image={site.slides[3]?.image ?? site.slides[0]?.image} />
      <section className="section">
        <div className="container">
          <CatalogueGrid offres={offres} entreprises={site.entreprises} initial={entreprise ?? ""} />
        </div>
      </section>
      <CtaBanniere titre="Vous ne trouvez pas ce qu'il vous faut ?"
                   texte="Décrivez-nous votre projet : nous construisons une offre sur mesure." />
    </>
  );
}
