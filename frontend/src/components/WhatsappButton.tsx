"use client";

import { motion } from "motion/react";
import { usePathname } from "next/navigation";

import { WhatsappIcon } from "./Social";

export default function WhatsappButton({ numero }: { numero: string }) {
  const chemin = usePathname();
  if (!numero) return null;
  return (
    <motion.a
      href={`https://wa.me/${numero.replace(/\D/g, "")}`}
      target="_blank"
      rel="noopener noreferrer"
      className={`whatsapp ${chemin.startsWith("/catalogue/") ? "lift" : ""}`}
      aria-label="Contactez-nous sur WhatsApp"
      initial={{ scale: 0, rotate: -90 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ delay: 1.2, type: "spring", stiffness: 260, damping: 18 }}
      whileHover={{ scale: 1.1 }}
    >
      <WhatsappIcon />
    </motion.a>
  );
}
