"use client";

import { Music, Pause, Play } from "lucide-react";
import { motion, useReducedMotion } from "motion/react";
import { type CSSProperties, useEffect, useRef, useState } from "react";

export type Chanson = {
  id: number; titre: string; artiste: string; pochette: string | null; audio: string | null; spotify: string | null;
};

const temps = (s: number) =>
  Number.isFinite(s) && s > 0 ? `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}` : "0:00";

/** Lien Spotify (open.spotify.com/track/ID?si=…) → adresse du lecteur intégré officiel. */
export function spotifyEmbed(lien: string): string | null {
  const m = lien.match(/open\.spotify\.com\/(?:intl-[a-z-]+\/)?(track|album|playlist|episode|artist)\/([A-Za-z0-9]+)/);
  return m ? `https://open.spotify.com/embed/${m[1]}/${m[2]}?utm_source=generator` : null;
}

function versHsl(r: number, g: number, b: number): [number, number] {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2, d = max - min;
  if (!d) return [0, 0];
  const s = d / (1 - Math.abs(2 * l - 1));
  const h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [(h * 60 + 360) % 360, Math.min(s, 1)];
}

/** Couleur dominante d'une pochette, pour le fond de la carte, comme Spotify. */
function useCouleur(src: string | null) {
  const [couleur, setCouleur] = useState<string | null>(null);
  useEffect(() => {
    if (!src) return;
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      try {
        const c = document.createElement("canvas");
        c.width = c.height = 12;
        const ctx = c.getContext("2d");
        if (!ctx) return;
        ctx.drawImage(img, 0, 0, 12, 12);
        const d = ctx.getImageData(0, 0, 12, 12).data;
        // Moyenne pondérée par la saturation : on garde la couleur marquante de la pochette.
        let r = 0, g = 0, b = 0, poids = 0;
        for (let i = 0; i < d.length; i += 4) {
          const max = Math.max(d[i], d[i + 1], d[i + 2]), min = Math.min(d[i], d[i + 1], d[i + 2]);
          const w = max === 0 ? 0 : ((max - min) / max) ** 2 + 0.02;
          r += d[i] * w; g += d[i + 1] * w; b += d[i + 2] * w; poids += w;
        }
        if (!poids) return;
        // Teinte de la pochette, saturation relevée, luminosité fixée (texte blanc lisible), comme Spotify.
        const [h, sat] = versHsl(r / poids, g / poids, b / poids);
        setCouleur(`hsl(${Math.round(h)} ${Math.round(Math.max(sat, 0.45) * 100)}% 34%)`);
      } catch { /* image d'une autre origine : couleur par défaut */ }
    };
    img.src = src;
  }, [src]);
  return couleur;
}

function Carte({ c, index, active, joue, position, duree, onBasculer, onChercher }: {
  c: Chanson; index: number; active: boolean; joue: boolean; position: number; duree: number;
  onBasculer: () => void; onChercher: (v: number) => void;
}) {
  const couleur = useCouleur(c.pochette);
  const reduit = useReducedMotion();
  return (
    <motion.article className={`chanson ${active ? "active" : ""} ${joue ? "joue" : ""}`}
                    style={couleur ? ({ "--fond": couleur } as CSSProperties) : undefined}
                    initial={reduit ? false : { opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, margin: "-40px" }} transition={{ duration: 0.55, delay: index * 0.1 }}>
      <div className="chanson-pochette">
        {c.pochette ? <img src={c.pochette} alt={`Pochette : ${c.titre}`} loading="lazy" /> : <Music size={38} />}
      </div>
      <div className="chanson-corps">
        <span className="chanson-marque" aria-hidden="true">PS ZIK</span>
        <h3>{c.titre}</h3>
        <p className="chanson-artiste"><span className="chanson-badge">Extrait</span>{c.artiste}</p>
        <div className="chanson-bas">
          <div className="chanson-piste">
            <input type="range" className="chanson-progression" min={0} max={duree || 1} step={0.1}
                   value={active ? position : 0} disabled={!active}
                   onChange={(ev) => onChercher(Number(ev.target.value))} aria-label={`Position dans « ${c.titre} »`}
                   style={{ backgroundSize: `${active && duree ? (position / duree) * 100 : 0}% 100%` }} />
            <span className="chanson-temps">{active ? `${temps(position)} / ${temps(duree)}` : " "}</span>
          </div>
          <span className="chanson-egaliseur" aria-hidden="true">
            {[0, 1, 2, 3].map((k) => <i key={k} />)}
          </span>
          <button type="button" className="chanson-bouton" onClick={onBasculer}
                  aria-label={joue ? `Mettre en pause « ${c.titre} »` : `Écouter « ${c.titre} »`}>
            {joue ? <Pause size={22} fill="currentColor" /> : <Play size={22} fill="currentColor" />}
          </button>
        </div>
      </div>
    </motion.article>
  );
}

/**
 * Chansons des artistes (3 au maximum), en cartes façon Spotify : pochette à gauche, titre, artiste,
 * bouton lecture rond à droite, fond de la couleur de la pochette. Une chanson avec un lien Spotify
 * affiche le lecteur Spotify officiel.
 */
export default function LecteurMusique({ chansons }: { chansons: Chanson[] }) {
  const audio = useRef<HTMLAudioElement>(null);
  const [actif, setActif] = useState<number | null>(null);
  const [lecture, setLecture] = useState(false);
  const [position, setPosition] = useState(0);
  const [duree, setDuree] = useState(0);

  useEffect(() => {
    const a = audio.current;
    if (!a) return;
    const maj = () => { setPosition(a.currentTime); setDuree(a.duration || 0); };
    const stop = () => setLecture(false);
    const go = () => setLecture(true);
    a.addEventListener("timeupdate", maj);
    a.addEventListener("loadedmetadata", maj);
    a.addEventListener("ended", stop);
    a.addEventListener("pause", stop);
    a.addEventListener("play", go);
    return () => {
      a.removeEventListener("timeupdate", maj); a.removeEventListener("loadedmetadata", maj);
      a.removeEventListener("ended", stop); a.removeEventListener("pause", stop); a.removeEventListener("play", go);
    };
  }, []);

  const basculer = (i: number) => {
    const a = audio.current;
    const src = chansons[i].audio;
    if (!a || !src) return;
    if (actif === i) {
      if (a.paused) a.play().catch(() => {}); else a.pause();
      return;
    }
    a.src = src;
    setActif(i); setPosition(0); setDuree(0);
    a.play().catch(() => {});
  };

  if (!chansons.length) {
    return (
      <div className="lecteur">
        {[1, 2, 3].map((k) => (
          <article key={k} className="chanson bientot" aria-label="Chanson bientôt disponible">
            <div className="chanson-pochette"><Music size={38} /></div>
            <div className="chanson-corps">
              <span className="chanson-marque" aria-hidden="true">PS ZIK</span>
              <h3>Nouveau titre</h3>
              <p className="chanson-artiste"><span className="chanson-badge">Bientôt</span>Bientôt disponible</p>
              <div className="chanson-bas">
                <div className="chanson-piste"><span className="chanson-ligne" /></div>
                <span className="chanson-bouton" aria-hidden="true"><Play size={22} fill="currentColor" /></span>
              </div>
            </div>
          </article>
        ))}
      </div>
    );
  }

  return (
    <div className="lecteur">
      <audio ref={audio} preload="none" />
      {chansons.map((c, i) => {
        const embed = !c.audio && c.spotify ? spotifyEmbed(c.spotify) : null;
        if (embed) {
          return (
            <iframe key={c.id} className="chanson-spotify" src={embed} title={`${c.titre} — ${c.artiste} (Spotify)`}
                    loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" />
          );
        }
        return (
          <Carte key={c.id} c={c} index={i} active={actif === i} joue={actif === i && lecture}
                 position={position} duree={duree} onBasculer={() => basculer(i)}
                 onChercher={(v) => { const a = audio.current; if (a && actif === i) { a.currentTime = v; setPosition(v); } }} />
        );
      })}
    </div>
  );
}
