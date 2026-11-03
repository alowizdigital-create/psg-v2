import "server-only";

import type { EntrepriseDetail, OffreDetail, OffreResume, Section, Site } from "./types";

const BACKEND = process.env.BACKEND_INTERNAL_URL || "http://127.0.0.1:8000";

export class ApiIndisponible extends Error {}

async function get<T>(chemin: string): Promise<T | null> {
  let reponse: Response;
  try {
    reponse = await fetch(`${BACKEND}/api/${chemin}`, {
      // Cache de 60 s, vidé immédiatement à chaque modification dans l'admin
      // (voir app/revalidate/route.ts).
      next: { revalidate: 60, tags: ["cms"] },
      headers: { Accept: "application/json" },
    });
  } catch (err) {
    throw new ApiIndisponible(`Backend injoignable (${BACKEND}) : ${String(err)}`);
  }
  if (reponse.status === 404) return null;
  if (!reponse.ok) throw new ApiIndisponible(`API ${chemin} : ${reponse.status}`);
  return reponse.json() as Promise<T>;
}

export const api = {
  site: () => get<Site>("site/") as Promise<Site>,
  page: async (page: "accueil" | "a-propos" | "contact") =>
    (await get<{ sections: Section[] }>(`pages/${page}/`))?.sections ?? [],
  entreprise: (slug: string) => get<EntrepriseDetail>(`entreprises/${encodeURIComponent(slug)}/`),
  offres: async (params = "") => (await get<OffreResume[]>(`offres/${params}`)) ?? [],
  offre: (slug: string) => get<OffreDetail>(`offres/${encodeURIComponent(slug)}/`),
};
