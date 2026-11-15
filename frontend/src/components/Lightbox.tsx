"use client";

import { ChevronLeft, ChevronRight, X } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useEffect } from "react";

export type Img = { image: string | null; legende: string };

/** Visionneuse plein écran (Échap pour fermer, flèches du clavier pour naviguer). */
export default function Lightbox({ images, index, onClose, onChange }: {
  images: Img[]; index: number | null; onClose: () => void; onChange: (i: number) => void;
}) {
  const n = images.length;

  useEffect(() => {
    if (index === null) return;
    const touche = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") onChange((index + 1) % n);
      if (e.key === "ArrowLeft") onChange((index - 1 + n) % n);
    };
    window.addEventListener("keydown", touche);
    return () => window.removeEventListener("keydown", touche);
  }, [index, n, onClose, onChange]);

  return (
    <AnimatePresence>
      {index !== null && images[index] && (
        <motion.div className="lightbox" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                    onClick={onClose} role="dialog" aria-modal="true">
          <button className="round-btn" style={{ top: 20, right: 20 }} aria-label="Fermer"><X /></button>
          {n > 1 && (
            <>
              <button className="round-btn" style={{ left: 20, top: "50%" }} aria-label="Précédente"
                      onClick={(e) => { e.stopPropagation(); onChange((index - 1 + n) % n); }}>
                <ChevronLeft />
              </button>
              <button className="round-btn" style={{ right: 20, top: "50%" }} aria-label="Suivante"
                      onClick={(e) => { e.stopPropagation(); onChange((index + 1) % n); }}>
                <ChevronRight />
              </button>
            </>
          )}
          <motion.div key={index} initial={{ scale: 0.92, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.35 }} onClick={(e) => e.stopPropagation()}>
            <img src={images[index].image!} alt={images[index].legende} />
            {images[index].legende && <p>{images[index].legende}</p>}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
