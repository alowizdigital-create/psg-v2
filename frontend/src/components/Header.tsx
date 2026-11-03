"use client";

import { ArrowRight, ChevronDown, Menu, X } from "lucide-react";
import { AnimatePresence, motion, useScroll, useSpring } from "motion/react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import type { EntrepriseResume } from "@/lib/types";

import Icon from "./Icon";
import { Logo } from "./Logo";

const LIENS = [
  { href: "/", label: "Accueil" },
  { href: "/a-propos", label: "À propos" },
  { href: "/#entreprises", label: "Nos entreprises", menu: true },
  { href: "/catalogue", label: "Catalogue" },
  { href: "/contact", label: "Contact" },
];

export default function Header({ entreprises }: { entreprises: EntrepriseResume[] }) {
  const chemin = usePathname();
  const [scrolle, setScrolle] = useState(false);
  const [ouvert, setOuvert] = useState(false);
  const [sousMenu, setSousMenu] = useState(false);
  const { scrollYProgress } = useScroll();
  const progression = useSpring(scrollYProgress, { stiffness: 120, damping: 30 });

  useEffect(() => {
    const f = () => setScrolle(window.scrollY > 40);
    f();
    window.addEventListener("scroll", f, { passive: true });
    return () => window.removeEventListener("scroll", f);
  }, []);

  useEffect(() => { setOuvert(false); setSousMenu(false); }, [chemin]);
  useEffect(() => { document.body.style.overflow = ouvert ? "hidden" : ""; }, [ouvert]);

  const actif = (href: string) =>
    href === "/" ? chemin === "/" : href.startsWith("/#") ? chemin.startsWith("/entreprises") : chemin.startsWith(href);

  return (
    <>
      <motion.div className="progress" style={{ scaleX: progression }} />
      <header className={`header ${scrolle ? "scrolled" : ""}`}>
        <nav className="nav container" aria-label="Navigation principale">
          <Link href="/" aria-label="PS GROUP SARL — Accueil"><Logo /></Link>
          <ul className="nav-links">
            {LIENS.map((l) => (
              <li key={l.href} onMouseEnter={() => l.menu && setSousMenu(true)}
                  onMouseLeave={() => l.menu && setSousMenu(false)}>
                <Link href={l.href} className={`nav-link ${actif(l.href) ? "active" : ""}`}
                      aria-haspopup={l.menu ? "true" : undefined} aria-expanded={l.menu ? sousMenu : undefined}
                      onFocus={() => l.menu && setSousMenu(true)}>
                  {l.label}
                  {l.menu && <ChevronDown size={15} />}
                </Link>
                {l.menu && (
                  <AnimatePresence>
                    {sousMenu && (
                      <motion.div className="dropdown" initial={{ opacity: 0, y: 12, scale: 0.97 }}
                                  animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 8, scale: 0.98 }}
                                  transition={{ duration: 0.25 }}>
                        {entreprises.map((e, i) => (
                          <motion.div key={e.slug} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }}
                                      transition={{ delay: i * 0.04 }}>
                            <Link href={`/entreprises/${e.slug}`} onBlur={() => i === entreprises.length - 1 && setSousMenu(false)}>
                              <span className="ico"><Icon name={e.icone} size={18} /></span>
                              <span><strong>{e.nom}</strong><small>{e.resume}</small></span>
                            </Link>
                          </motion.div>
                        ))}
                      </motion.div>
                    )}
                  </AnimatePresence>
                )}
              </li>
            ))}
          </ul>
          <div className="nav-cta">
            <Link href="/contact" className="btn btn-primary">Nous contacter <ArrowRight size={16} /></Link>
            <button className="burger" aria-label="Ouvrir le menu" onClick={() => setOuvert(true)}><Menu /></button>
          </div>
        </nav>
      </header>

      <AnimatePresence>
        {ouvert && (
          <motion.div className="mobile-menu" initial={{ clipPath: "circle(0% at 92% 4%)" }}
                      animate={{ clipPath: "circle(150% at 92% 4%)" }} exit={{ clipPath: "circle(0% at 92% 4%)" }}
                      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }} role="dialog" aria-modal="true"
                      aria-label="Menu">
            <button className="mobile-close" aria-label="Fermer le menu" onClick={() => setOuvert(false)}><X /></button>
            {LIENS.map((l, i) => (
              <motion.div key={l.href} initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.15 + i * 0.06 }}>
                <Link className="big" href={l.href} onClick={() => setOuvert(false)}>{l.label}</Link>
                {l.menu && (
                  <div className="sub">
                    {entreprises.map((e) => (
                      <Link key={e.slug} href={`/entreprises/${e.slug}`} onClick={() => setOuvert(false)}>
                        <Icon name={e.icone} size={18} /> {e.nom}
                      </Link>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }} style={{ marginTop: 20 }}>
              <Link href="/contact" className="btn btn-primary" onClick={() => setOuvert(false)}>
                Nous contacter <ArrowRight size={16} />
              </Link>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
