"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { AnimatePresence, motion, useInView, useReducedMotion } from "motion/react";
import { useCallback, useEffect, useRef, useState } from "react";

import Lightbox, { type Img } from "./Lightbox";

const DELAI = 3800;
const EASE = [0.22, 1, 0.36, 1] as const;

/**
 * Slide « coverflow » 3D : l'image du centre est de face, les voisines sont inclinées en
 * perspective et s'éloignent. Défilement automatique, flèches, points, clavier, glissement
 * au doigt ; un clic sur une image voisine la ramène au centre, un clic sur l'image du centre
 * l'ouvre en plein écran.
 */
export default function Coverflow({ images, label = "Galerie photo" }: { images: Img[]; label?: string }) {
  const liste = images.filter((i) => i.image);
  const n = liste.length;
  const [actif, setActif] = useState(0);
  const [largeur, setLargeur] = useState(1100);
  const [pause, setPause] = useState(false);
  const [ouvert, setOuvert] = useState<number | null>(null);
  const scene = useRef<HTMLDivElement>(null);
  const reduit = useReducedMotion();
  const visible = useInView(scene, { margin: "-80px" });

  useEffect(() => {
    const el = scene.current;
    if (!el) return;
    const mesure = () => setLargeur(el.clientWidth);
    mesure();
    const obs = new ResizeObserver(mesure);
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const aller = useCallback((i: number) => setActif(((i % n) + n) % n), [n]);

  // Défilement automatique : seulement quand la galerie est à l'écran et non survolée.
  useEffect(() => {
    if (n < 2 || pause || reduit || !visible || ouvert !== null) return;
    const t = setInterval(() => setActif((a) => (a + 1) % n), DELAI);
    return () => clearInterval(t);
  }, [n, pause, reduit, visible, ouvert]);

  if (!n) return null;

  // Dimensions adaptées à la largeur disponible.
  const etroit = largeur < 700;
  const carte = Math.round(etroit ? largeur * 0.56 : Math.min(330, Math.max(200, largeur * 0.27)));
  const hauteur = Math.round(carte * 1.25);
  const portee = etroit ? 2 : 3;
  // Réglages par rang (0 = centre) d'après le modèle : voisines à ~40° sans chevauchement,
  // images lointaines presque de profil. x en largeurs de carte.
  const REGLAGES = [
    { x: 0, rot: 0, scale: 1 },
    { x: etroit ? 0.74 : 0.84, rot: 40, scale: 0.97 },
    { x: etroit ? 1.2 : 1.46, rot: 70, scale: 0.94 },
    { x: 1.82, rot: 76, scale: 0.9 },
  ];
  const reglage = (ad: number) => REGLAGES[Math.min(ad, REGLAGES.length - 1)];

  // Décalage circulaire de chaque image par rapport à l'image du centre.
  const decalage = (i: number) => {
    let d = (i - actif) % n;
    if (d > n / 2) d -= n;
    if (d < -n / 2) d += n;
    return d;
  };

  return (
    <div className="coverflow" onMouseEnter={() => setPause(true)} onMouseLeave={() => setPause(false)}>
      <motion.div
        ref={scene}
        className="coverflow-scene"
        style={{ height: hauteur + 56 }}
        tabIndex={0}
        role="group"
        aria-roledescription="carrousel"
        aria-label={label}
        onFocus={() => setPause(true)}
        onBlur={() => setPause(false)}
        onKeyDown={(e) => {
          if (e.key === "ArrowRight") { e.preventDefault(); aller(actif + 1); }
          if (e.key === "ArrowLeft") { e.preventDefault(); aller(actif - 1); }
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setOuvert(actif); }
        }}
        onPanEnd={(_, info) => {
          if (Math.abs(info.offset.x) < 50) return;
          aller(actif + (info.offset.x < 0 ? 1 : -1));
        }}
      >
        {liste.map((img, i) => {
          const d = decalage(i);
          const ad = Math.abs(d);
          const sens = Math.sign(d);
          const montre = ad <= portee;
          return (
            <motion.figure
              key={i}
              className="coverflow-carte"
              style={{ width: carte, height: hauteur, marginLeft: -carte / 2, zIndex: 50 - ad }}
              initial={false}
              animate={{
                x: sens * reglage(ad).x * carte,
                z: -ad * 30,
                rotateY: -sens * reglage(ad).rot,
                scale: reglage(ad).scale,
                opacity: montre ? (ad <= 1 ? 1 : ad === 2 ? 0.85 : 0.6) : 0,
              }}
              transition={reduit ? { duration: 0 } : { duration: 0.85, ease: EASE, opacity: { duration: 0.35 } }}
              onTap={() => (d === 0 ? setOuvert(i) : aller(i))}
              aria-hidden={montre ? undefined : true}
              aria-label={[img.legende, img.sous].filter(Boolean).join(", ") || `Photo ${i + 1}`}
              aria-current={d === 0 ? "true" : undefined}
              data-actif={d === 0}
            >
              <img src={img.image!} alt={img.legende} draggable={false} loading={ad <= 1 ? "eager" : "lazy"} />
            </motion.figure>
          );
        })}
        <span className="coverflow-sol" aria-hidden="true" style={{ width: carte * 1.4 }} />
      </motion.div>

      <div className="coverflow-pied">
        <AnimatePresence mode="wait">
          <motion.p key={actif} className="coverflow-legende" initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.25 }}>
            {liste[actif].legende || "\u00a0"}
            {liste[actif].sous && <small>{liste[actif].sous}</small>}
          </motion.p>
        </AnimatePresence>
        {n > 1 && (
          <div className="coverflow-commandes">
            <button className="round-btn coverflow-fleche" onClick={() => aller(actif - 1)} aria-label="Image précédente">
              <ChevronLeft />
            </button>
            <div className="coverflow-points" role="tablist" aria-label="Choisir une image">
              {liste.map((_, i) => (
                <button key={i} role="tab" aria-selected={i === actif} aria-label={`Image ${i + 1}`}
                        className={i === actif ? "actif" : ""} onClick={() => aller(i)} />
              ))}
            </div>
            <button className="round-btn coverflow-fleche" onClick={() => aller(actif + 1)} aria-label="Image suivante">
              <ChevronRight />
            </button>
          </div>
        )}
      </div>

      <Lightbox images={liste} index={ouvert} onClose={() => setOuvert(null)} onChange={setOuvert} />
    </div>
  );
}
