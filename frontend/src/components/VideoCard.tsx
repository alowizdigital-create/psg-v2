"use client";

import { Play } from "lucide-react";
import { useState } from "react";

function idYoutube(url: string) {
  const m = url.match(/(?:v=|youtu\.be\/|embed\/|shorts\/)([\w-]{11})/);
  return m?.[1];
}

export default function VideoCard({ url, titre, sousTitre }: { url: string; titre: string; sousTitre: string }) {
  const id = idYoutube(url);
  const [lecture, setLecture] = useState(false);
  if (!id) {
    return <a className="btn btn-dark" href={url} target="_blank" rel="noopener noreferrer">{titre || "Voir la vidéo"}</a>;
  }
  if (lecture) {
    return (
      <div className="video-card">
        <iframe src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1`} title={titre}
                allow="autoplay; encrypted-media; picture-in-picture" allowFullScreen />
      </div>
    );
  }
  return (
    <button className="video-card" onClick={() => setLecture(true)} aria-label={`Lire la vidéo ${titre}`} style={{ width: "100%" }}>
      <img src={`https://img.youtube.com/vi/${id}/hqdefault.jpg`} alt="" loading="lazy" />
      <span className="play"><span><Play size={34} fill="currentColor" /></span></span>
      <span className="caption"><strong style={{ display: "block", fontSize: "1.2rem" }}>{titre}</strong>{sousTitre}</span>
    </button>
  );
}
