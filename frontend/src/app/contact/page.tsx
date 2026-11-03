import { Mail, MapPin, MessageCircle, Phone } from "lucide-react";
import type { Metadata } from "next";

import ContactForm from "@/components/ContactForm";
import { Socials } from "@/components/Footer";
import { Reveal } from "@/components/Motion";
import PageHero from "@/components/PageHero";
import Sections from "@/components/Sections";
import { api } from "@/lib/api";
import { telLien } from "@/lib/format";

export const metadata: Metadata = { title: "Contact" };

export default async function Contact() {
  const [site, sections] = await Promise.all([api.site(), api.page("contact")]);
  const { reglages } = site;
  const entete = sections.find((s) => s.type === "entete");
  return (
    <>
      <PageHero surTitre={entete?.sur_titre || "Contact"} titre={entete?.titre || "Parlons de votre projet"}
                texte={entete?.texte.join(" ")} image={site.slides[2]?.image ?? site.slides[0]?.image} />
      <section className="section">
        <div className="container grid grid-2" style={{ alignItems: "start" }}>
          <Reveal>
            <span className="eyebrow">Coordonnées</span>
            <h2 style={{ marginBottom: 20 }}>Nos informations de contact</h2>
            <ul className="contact-list">
              {reglages.adresse && (
                <li><span className="icon-badge"><MapPin /></span><div><strong>Adresse</strong>{reglages.adresse}</div></li>
              )}
              {reglages.telephones.length > 0 && (
                <li><span className="icon-badge"><Phone /></span><div><strong>Téléphone</strong>
                  {reglages.telephones.map((t, i) => (
                    <span key={t}>{i > 0 && " · "}<a href={telLien(t)}>{t}</a></span>
                  ))}
                </div></li>
              )}
              {reglages.email && (
                <li><span className="icon-badge"><Mail /></span><div style={{ wordBreak: "break-all" }}><strong>E-mail</strong>
                  <a href={`mailto:${reglages.email}`}>{reglages.email}</a></div></li>
              )}
              {reglages.whatsapp && (
                <li><span className="icon-badge"><MessageCircle /></span><div><strong>WhatsApp</strong>
                  <a href={`https://wa.me/${reglages.whatsapp}`} target="_blank" rel="noopener noreferrer">Écrivez-nous directement</a></div></li>
              )}
            </ul>
            <div style={{ color: "var(--primary)" }}><Socials reglages={reglages} /></div>
          </Reveal>
          <Reveal delay={0.15}>
            <div className="card" style={{ padding: "clamp(22px, 4vw, 36px)" }}>
              <h3 style={{ marginTop: 0, marginBottom: 20 }}>Envoyez-nous un message</h3>
              <ContactForm entreprises={site.entreprises} />
            </div>
          </Reveal>
        </div>
      </section>
      <Sections sections={sections} ctx={{ entreprises: site.entreprises }} />
    </>
  );
}
