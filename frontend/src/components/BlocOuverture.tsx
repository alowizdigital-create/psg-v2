"use client";

import { ArrowRight } from "lucide-react";
import { motion, useReducedMotion, useScroll, useTransform } from "motion/react";
import Link from "next/link";
import { type CSSProperties, useRef } from "react";

/**
 * « Bloc qui s'ouvre » (inspiré de derin15.com) : un très grand texte est coupé en deux à
 * l'horizontale ; en faisant défiler la page, un panneau s'ouvre entre les deux moitiés et révèle
 * une typographie animée (ou une image), d'abord floue puis nette, avec le titre et un bouton.
 */
export default function BlocOuverture({ mot, titre, texte, mots, image, bouton, badge }: {
  mot: string; titre: string; texte: string[]; mots: string[]; image?: string | null;
  bouton?: { label: string; lien: string }; badge: string;
}) {
  const ref = useRef<HTMLElement>(null);
  const reduit = useReducedMotion();
  const { scrollYProgress: p } = useScroll({ target: ref, offset: ["start start", "end end"] });

  const hauteur = useTransform(p, [0.06, 0.6], ["0vh", "74vh"]);
  const fondEchelle = useTransform(p, [0.06, 0.8], [1.3, 1]);
  const fondFlou = useTransform(p, [0.2, 0.68], ["blur(16px)", "blur(0px)"]);
  const fondOpacite = useTransform(p, [0.06, 0.3], [0, 1]);
  const contenuY = useTransform(p, [0.42, 0.78], [50, 0]);
  const contenuOpacite = useTransform(p, [0.45, 0.72], [0, 1]);
  const lettres = useTransform(p, [0.4, 0.8], ["0.4em", "0.02em"]);

  const liens = bouton?.lien?.startsWith("http") ? { target: "_blank", rel: "noopener" } : {};

  return (
    <section ref={ref} className={`ouverture ${reduit ? "fixe" : ""}`}
             style={{ "--n": Math.max([...mot].length, 4) } as CSSProperties}>
      <h2 className="sr-only">{mot} — {titre}</h2>
      <div className="ouverture-sticky">
        <div className="ouverture-moitie haut" aria-hidden="true"><span>{mot}</span></div>

        <motion.div className="ouverture-panneau" style={reduit ? { height: "74vh" } : { height: hauteur }}>
          <motion.div className="ouverture-fond"
                      style={reduit ? undefined : { scale: fondEchelle, filter: fondFlou, opacity: fondOpacite }}>
            {image ? <img src={image} alt="" /> : <Cinetique mots={mots} />}
          </motion.div>
          <motion.div className="ouverture-contenu"
                      style={reduit ? undefined : { y: contenuY, opacity: contenuOpacite }}>
            <motion.strong className="ouverture-titre" aria-hidden="true"
                           style={reduit ? undefined : { letterSpacing: lettres }}>
              {titre}
            </motion.strong>
            {texte.map((t, i) => <p key={i}>{t}</p>)}
            {bouton?.label && bouton.lien && (
              <Link href={bouton.lien} className="btn btn-primary" {...liens}>
                {bouton.label} <ArrowRight size={18} />
              </Link>
            )}
          </motion.div>
          <BadgeRotatif texte={badge} />
        </motion.div>

        <div className="ouverture-moitie bas" aria-hidden="true"><span>{mot}</span></div>
      </div>
    </section>
  );
}

/** Mots géants qui défilent en perspective (fond du panneau quand il n'y a pas d'image). */
function Cinetique({ mots }: { mots: string[] }) {
  const liste = mots.length ? mots : ["Digital", "Créatif", "Solutions"];
  return (
    <div className="cinetique" aria-hidden="true">
      {liste.map((m, i) => (
        <div key={i} className="cinetique-col" style={{ "--i": i - (liste.length - 1) / 2 } as CSSProperties}>
          <div className={`cinetique-piste ${i % 2 ? "inverse" : ""}`}>
            {Array.from({ length: 16 }, (_, j) => <span key={j}>{m}</span>)}
          </div>
        </div>
      ))}
    </div>
  );
}

/** Texte circulaire qui tourne en continu. */
export function BadgeRotatif({ texte }: { texte: string }) {
  return (
    <div className="badge-rotatif" aria-hidden="true">
      <svg viewBox="0 0 100 100">
        <defs>
          <path id="badge-cercle" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0" />
        </defs>
        <text><textPath href="#badge-cercle" textLength="230">{texte}</textPath></text>
      </svg>
      <span>✦</span>
    </div>
  );
}
