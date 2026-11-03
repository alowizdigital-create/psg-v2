import HeroSlider from "@/components/HeroSlider";
import Marquee from "@/components/Marquee";
import Sections from "@/components/Sections";
import { api } from "@/lib/api";

export default async function Accueil() {
  const [site, sections, offres] = await Promise.all([
    api.site(), api.page("accueil"), api.offres("?mises_en_avant=1"),
  ]);
  const vedettes = offres.length ? offres : await api.offres();
  return (
    <>
      <HeroSlider slides={site.slides} titre={site.reglages.nom} slogan={site.reglages.slogan} />
      <Marquee items={site.entreprises} />
      <Sections sections={sections} ctx={{ entreprises: site.entreprises, offres: vedettes }} />
    </>
  );
}
