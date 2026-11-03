import type { Metadata } from "next";

import PageHero from "@/components/PageHero";
import Sections from "@/components/Sections";
import { api } from "@/lib/api";

export const metadata: Metadata = { title: "À propos" };

export default async function APropos() {
  const [site, sections] = await Promise.all([api.site(), api.page("a-propos")]);
  const entete = sections.find((s) => s.type === "entete");
  return (
    <>
      <PageHero surTitre={entete?.sur_titre || "À propos"} titre={entete?.titre || "Qui sommes-nous ?"}
                texte={entete?.texte.join(" ")} image={site.slides[1]?.image ?? site.slides[0]?.image} />
      <Sections sections={sections} ctx={{ entreprises: site.entreprises }} />
    </>
  );
}
