import { ArrowRight, ListChecks } from "lucide-react";
import Link from "next/link";

import { fcfa } from "@/lib/format";
import type { OffreResume } from "@/lib/types";

import Icon from "./Icon";

export default function OfferCard({ offre }: { offre: OffreResume }) {
  return (
    <Link href={`/catalogue/${offre.slug}`} className="offer-card">
      <div className="img">
        {offre.image && <img src={offre.image} alt="" loading="lazy" />}
        <span className="tag"><Icon name={offre.entreprise.icone} size={14} /> {offre.entreprise.nom}</span>
      </div>
      <div className="body">
        <h3>{offre.titre}</h3>
        {offre.resume && <p>{offre.resume}</p>}
        <div className="foot">
          <span className="price">
            {offre.prix_a_partir_de ? `Dès ${fcfa(offre.prix_a_partir_de)}` : (
              <span style={{ display: "inline-flex", gap: 6, alignItems: "center" }}>
                <ListChecks size={16} /> {offre.nb_options} options
              </span>
            )}
          </span>
          <span className="go">Composer <ArrowRight size={16} /></span>
        </div>
      </div>
    </Link>
  );
}
