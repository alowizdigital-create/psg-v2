"use client";

import { motion } from "motion/react";
import { useState } from "react";

import Lightbox, { type Img } from "./Lightbox";

export default function Gallery({ images, mode = "masonry" }: { images: Img[]; mode?: "masonry" | "thumbs" }) {
  const liste = images.filter((i) => i.image);
  const [ouvert, setOuvert] = useState<number | null>(null);

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
      <Lightbox images={liste} index={ouvert} onClose={() => setOuvert(null)} onChange={setOuvert} />
    </>
  );
}
