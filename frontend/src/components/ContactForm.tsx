"use client";

import { useState } from "react";

import type { EntrepriseResume } from "@/lib/types";

import DemandeForm from "./DemandeForm";
import Success from "./Success";

export default function ContactForm({ entreprises }: { entreprises: EntrepriseResume[] }) {
  const [reference, setReference] = useState<string | null>(null);
  if (reference) return <Success reference={reference} />;
  return <DemandeForm entreprises={entreprises} libelleBouton="Envoyer mon message" envoi={{ surSucces: setReference }} />;
}
