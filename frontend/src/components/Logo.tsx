// Logo PS GROUP (Point Solutions Group), redessiné en SVG d'après le logo officiel :
// capsule à bord doré, monogramme « P » doré et nom de l'entreprise.
// À remplacer par le fichier officiel dès qu'il est disponible.
export function Logo({ compact = false }: { compact?: boolean }) {
  return (
    <svg className={`logo-svg ${compact ? "compact" : ""}`} viewBox="0 0 168 84" role="img"
         aria-label="PS GROUP — Point Solutions Group">
      <defs>
        <linearGradient id="psg-or" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#FFD84D" />
          <stop offset="0.55" stopColor="#F5B800" />
          <stop offset="1" stopColor="#C99400" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="164" height="80" rx="40" fill="rgba(109,13,12,0.35)" stroke="url(#psg-or)" strokeWidth="3" />
      {/* Monogramme « P » : barres horizontales, boucle et jambe inclinée */}
      <g fill="none" stroke="url(#psg-or)" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20 26 H50 a11 11 0 0 1 0 22 H34" strokeWidth="6" />
        <path d="M26 37 H48" strokeWidth="4" />
        <path d="M36 48 L28 64" strokeWidth="6" />
      </g>
      <path d="M41 56 l7-2 -3 4 6-1 -6 7" fill="none" stroke="url(#psg-or)" strokeWidth="2.6"
            strokeLinecap="round" strokeLinejoin="round" />
      <g fill="#fff" fontFamily="var(--font-display)">
        <text x="70" y="40" fontSize="20" fontWeight="800" letterSpacing="0.5">POINT</text>
        <text x="71" y="52" fontSize="9.6" fontWeight="700" letterSpacing="0.9">SOLUTIONS</text>
        <text x="71" y="62" fontSize="9.6" fontWeight="700" letterSpacing="0.9">GROUP</text>
      </g>
      <path d="M71 67 H96" stroke="#fff" strokeWidth="1.4" opacity="0.8" />
    </svg>
  );
}
