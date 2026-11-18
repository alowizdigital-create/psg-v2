"use client";

import { Music, Pause, Play } from "lucide-react";
import { motion, useReducedMotion } from "motion/react";
import { useEffect, useRef, useState } from "react";

export type Chanson = { id: number; titre: string; artiste: string; pochette: string | null; audio: string };

const temps = (s: number) =>
  Number.isFinite(s) ? `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}` : "0:00";

/**
 * Lecteur des chansons des artistes (3 au maximum) : une seule chanson joue à la fois ; la pochette
 * tourne comme un disque vinyle, un égaliseur s'anime et la barre de progression permet d'avancer.
 */
export default function LecteurMusique({ chansons }: { chansons: Chanson[] }) {
  const audio = useRef<HTMLAudioElement>(null);
  const [actif, setActif] = useState<number | null>(null);
  const [lecture, setLecture] = useState(false);
  const [position, setPosition] = useState(0);
  const [duree, setDuree] = useState(0);
  const reduit = useReducedMotion();

  useEffect(() => {
    const a = audio.current;
    if (!a) return;
    const maj = () => { setPosition(a.currentTime); setDuree(a.duration || 0); };
    const fin = () => setLecture(false);
    a.addEventListener("timeupdate", maj);
    a.addEventListener("loadedmetadata", maj);
    a.addEventListener("ended", fin);
    a.addEventListener("pause", fin);
    a.addEventListener("play", () => setLecture(true));
    return () => { a.removeEventListener("timeupdate", maj); a.removeEventListener("loadedmetadata", maj);
      a.removeEventListener("ended", fin); a.removeEventListener("pause", fin); };
  }, []);

  const basculer = (i: number) => {
    const a = audio.current;
    if (!a) return;
    if (actif === i) {
      if (a.paused) a.play().catch(() => {}); else a.pause();
      return;
    }
    a.src = chansons[i].audio;
    setActif(i); setPosition(0); setDuree(0);
    a.play().catch(() => {});
  };

  const chercher = (i: number, valeur: number) => {
    const a = audio.current;
    if (!a || actif !== i || !duree) return;
    a.currentTime = valeur;
    setPosition(valeur);
  };

  return (
    <div className="lecteur">
      <audio ref={audio} preload="none" />
      {chansons.map((c, i) => {
        const joue = actif === i && lecture;
        const pos = actif === i ? position : 0;
        const tot = actif === i ? duree : 0;
        return (
          <motion.article key={c.id} className={`chanson ${joue ? "joue" : ""} ${actif === i ? "active" : ""}`}
                          initial={reduit ? false : { opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }}
                          viewport={{ once: true, margin: "-60px" }} transition={{ duration: 0.6, delay: i * 0.12 }}>
            <div className="chanson-disque">
              <div className="chanson-vinyle" aria-hidden="true" />
              <div className="chanson-pochette">
                {c.pochette ? <img src={c.pochette} alt={`Pochette : ${c.titre}`} loading="lazy" /> : <Music size={44} />}
              </div>
              <button type="button" className="chanson-bouton" onClick={() => basculer(i)}
                      aria-label={joue ? `Mettre en pause « ${c.titre} »` : `Écouter « ${c.titre} »`}>
                {joue ? <Pause size={26} fill="currentColor" /> : <Play size={26} fill="currentColor" />}
              </button>
            </div>
            <div className="chanson-infos">
              <h3>{c.titre}</h3>
              {c.artiste && <p>{c.artiste}</p>}
              <div className="chanson-egaliseur" aria-hidden="true">
                {Array.from({ length: 14 }, (_, k) => <span key={k} style={{ animationDelay: `${(k * 0.09) % 0.6}s` }} />)}
              </div>
              <input type="range" className="chanson-progression" min={0} max={tot || 1} step={0.1} value={pos}
                     onChange={(ev) => chercher(i, Number(ev.target.value))} disabled={actif !== i}
                     aria-label={`Position dans « ${c.titre} »`}
                     style={{ backgroundSize: `${tot ? (pos / tot) * 100 : 0}% 100%` }} />
              <div className="chanson-temps"><span>{temps(pos)}</span><span>{temps(tot)}</span></div>
            </div>
          </motion.article>
        );
      })}
    </div>
  );
}
