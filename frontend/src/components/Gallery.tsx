"use client";

import { ChevronLeft, ChevronRight, X } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";

type Img = { image: string | null; legende: string };

export default function Gallery({ images, mode = "masonry" }: { images: Img[]; mode?: "masonry" | "thumbs" }) {
  const liste = images.filter((i) => i.image);
  const [ouvert, setOuvert] = useState<number | null>(null);

  useEffect(() => {
    if (ouvert === null) return;
    const touche = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOuvert(null);
      if (e.key === "ArrowRight") setOuvert((o) => (o! + 1) % liste.length);
      if (e.key === "ArrowLeft") setOuvert((o) => (o! - 1 + liste.length) % liste.length);
    };
    window.addEventListener("keydown", touche);
    return () => window.removeEventListener("keydown", touche);
  }, [ouvert, liste.length]);

  return (
    <>
      {mode === "masonry" ? (
        <div className="masonry">
          {liste.map((img, i) => (
            <motion.figure key={i} onClick={() => setOuvert(i)} initial={{ opacity: 0, y: 40 }}
                           whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: "-40px" }}
                           transition={{ duration: 0.7, delay: (i % 4) * 0.08 }}>
              <img src={img.image!} alt={img.legende} loading="lazy" />
              {img.legende && <figcaption>{img.legende}</figcaption>}
            </motion.figure>
          ))}
        </div>
      ) : (
        <div className="offer-gallery">
          {liste.map((img, i) => (
            <button key={i} onClick={() => setOuvert(i)} aria-label={`Agrandir ${img.legende || `la photo ${i + 1}`}`}>
              <img src={img.image!} alt={img.legende} loading="lazy" />
            </button>
          ))}
        </div>
      )}
      <AnimatePresence>
        {ouvert !== null && (
          <motion.div className="lightbox" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                      onClick={() => setOuvert(null)} role="dialog" aria-modal="true">
            <button className="round-btn" style={{ top: 20, right: 20 }} aria-label="Fermer"><X /></button>
            {liste.length > 1 && (
              <>
                <button className="round-btn" style={{ left: 20, top: "50%" }} aria-label="Précédente"
                        onClick={(e) => { e.stopPropagation(); setOuvert((ouvert - 1 + liste.length) % liste.length); }}>
                  <ChevronLeft />
                </button>
                <button className="round-btn" style={{ right: 20, top: "50%" }} aria-label="Suivante"
                        onClick={(e) => { e.stopPropagation(); setOuvert((ouvert + 1) % liste.length); }}>
                  <ChevronRight />
                </button>
              </>
            )}
            <motion.div key={ouvert} initial={{ scale: 0.92, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 0.35 }} onClick={(e) => e.stopPropagation()}>
              <img src={liste[ouvert].image!} alt={liste[ouvert].legende} />
              {liste[ouvert].legende && <p>{liste[ouvert].legende}</p>}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
