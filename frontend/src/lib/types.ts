export type Element = {
  id: number;
  titre: string;
  sous_titre: string;
  texte: string[];
  icone: string;
  image: string | null;
  lien: string;
  en_avant: boolean;
};

export type SectionType =
  | "entete" | "texte" | "cartes" | "tuiles" | "lignes" | "galerie" | "personnes"
  | "chiffres" | "liste" | "video" | "liens" | "entreprises" | "offres" | "cta";

export type Section = {
  id: number;
  type: SectionType;
  sur_titre: string;
  titre: string;
  texte: string[];
  titre_encadre: string;
  bouton_label: string;
  bouton_lien: string;
  fond_alterne: boolean;
  colonnes: number;
  elements: Element[];
};

export type EntrepriseResume = {
  id: number;
  nom: string;
  slug: string;
  resume: string;
  icone: string;
  banniere: string | null;
  accroche: string;
};

export type OffreResume = {
  id: number;
  titre: string;
  slug: string;
  resume: string;
  image: string | null;
  prix_a_partir_de: number | null;
  entreprise: EntrepriseResume;
  nb_options: number;
  mise_en_avant: boolean;
};

export type Option = {
  id: number;
  libelle: string;
  description: string;
  prix: number | null;
  image: string | null;
};

export type Groupe = {
  id: number;
  libelle: string;
  aide: string;
  type: "multiple" | "unique";
  obligatoire: boolean;
  icone: string;
  options: Option[];
};

export type Avis = {
  id: number;
  nom: string;
  qualite: string;
  texte: string;
  note: number;
  photo: string | null;
  date: string;
  offre: { titre: string; slug: string } | null;
  verifiable: boolean;
};

export type ResumeAvis = { total: number; moyenne: number; liste: Avis[] };

export type OffreDetail = OffreResume & {
  avis: ResumeAvis;
  description: string[];
  galerie: { id: number; image: string | null; legende: string }[];
  groupes: Groupe[];
};

export type EntrepriseDetail = EntrepriseResume & {
  sur_titre: string;
  cta_titre: string;
  cta_texte: string;
  sections: Section[];
  offres: OffreResume[];
};

export type Reglages = {
  nom: string;
  slogan: string;
  devise_pied: string;
  adresse: string;
  telephones: string[];
  email: string;
  whatsapp: string;
  facebook: string;
  instagram: string;
  tiktok: string;
  youtube: string;
};

export type Site = {
  reglages: Reglages;
  entreprises: EntrepriseResume[];
  slides: { id: number; image: string | null; legende: string }[];
};
