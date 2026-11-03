import Link from "next/link";
import type { ReactNode } from "react";

import Icon from "./Icon";
import { Parallax, Reveal, SplitTitle } from "./Motion";

export default function PageHero({ surTitre, titre, texte, image, icone, fil, children }: {
  surTitre?: string; titre: string; texte?: string; image?: string | null; icone?: string;
  fil?: { href: string; label: string }[]; children?: ReactNode;
}) {
  return (
    <section className="page-hero grain">
      {image && <Parallax src={image} className="bg" />}
      <div className="orb" style={{ width: 380, height: 380, background: "rgba(245,184,0,.16)", right: "-6%", top: "-10%" }} />
      <div className="container">
        {fil && (
          <Reveal y={10}>
            <nav className="breadcrumb" aria-label="Fil d'Ariane">
              <Link href="/">Accueil</Link>
              {fil.map((f) => (
                <span key={f.href}>/ <Link href={f.href}>{f.label}</Link></span>
              ))}
            </nav>
          </Reveal>
        )}
        {surTitre && <Reveal y={10}><span className="eyebrow">{surTitre}</span></Reveal>}
        {icone ? (
          <Reveal y={20}><h1><span className="ico"><Icon name={icone} size={30} /></span>{titre}</h1></Reveal>
        ) : (
          <SplitTitle text={titre} delay={0.05} />
        )}
        {texte && <Reveal delay={0.25}><p>{texte}</p></Reveal>}
        {children}
      </div>
    </section>
  );
}
