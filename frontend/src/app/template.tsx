"use client";

import { motion, useReducedMotion } from "motion/react";
import type { ReactNode } from "react";

// Transition douce à chaque changement de page.
export default function Template({ children }: { children: ReactNode }) {
  const reduit = useReducedMotion();
  return (
    <motion.div initial={reduit ? false : { opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}>
      {children}
    </motion.div>
  );
}
