import AvisClients from "@/components/AvisClients";
import HeroSlider from "@/components/HeroSlider";
import Marquee from "@/components/Marquee";
import Sections from "@/components/Sections";
import { api } from "@/lib/api";

export default async function Accueil() {
  const [site, sections, offres, avis] = await Promise.all([
    api.site(), api.page("accueil"), api.offres("?mises_en_avant=1"), api.avis("?accueil=1"),
  ]);
  const vedettes = offres.length ? offres : await api.offres();
  const iCta = sections.map((x) => x.type).lastIndexOf("cta");
  const coupe = iCta === -1 ? sections.length : iCta;
  const avant = sections.slice(0, coupe);
  const apres = sections.slice(coupe);
  return (
    <div className="home">
      <HeroSlider slides={site.slides} titre={site.reglages.nom} />
      <Marquee items={site.entreprises} />
      {/* Les avis s'insèrent juste avant le bandeau final « Un projet en tête ? ». */}
      <Sections sections={avant} ctx={{ entreprises: site.entreprises, offres: vedettes }} />
      <AvisClients avis={avis} montrerOffre className="section-alt" />
      <Sections sections={apres} ctx={{ entreprises: site.entreprises, offres: vedettes }} />
    </div>
  );
}
