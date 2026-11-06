// Logo PS GROUP (Point Solutions Group), redessiné en SVG d'après le logo officiel :
// capsule à bord doré, monogramme « P » doré avec le « 7S » en dessous, et nom de l'entreprise.
// À remplacer par le fichier officiel (SVG ou PNG transparent) dès qu'il est disponible.
export function Logo() {
  return (
    <svg className="logo-svg" viewBox="0 0 168 84" role="img" aria-label="PS GROUP — Point Solutions Group">
      <defs>
        <linearGradient id="psg-or" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#F4E04A" />
          <stop offset="1" stopColor="#E2BF17" />
        </linearGradient>
      </defs>
      <rect x="6" y="3" width="156" height="78" rx="39" fill="rgba(109,13,12,0.6)" stroke="#D9B92B" strokeWidth="1.8" />
      <g fill="url(#psg-or)">
        {/* Barre du haut et boucle du « P » */}
        <path d="M24 20 H62 A14 14 0 0 1 62 51.5 H45.5 L47.5 45.5 H62 A8 8 0 0 0 62 26 H26.5 Z" />
        {/* Barre du milieu, extrémité gauche biseautée */}
        <path d="M27 32.5 H60 L58.5 38 H31 Z" />
        {/* « 7 » : barre courte et jambe inclinée */}
        <path d="M37.5 54 H48.5 L47.3 57.4 L40.6 67.5 H35.8 L42.3 57.4 H36.4 Z" />
      </g>
      {/* « S » en italique */}
      <text x="47.5" y="67" fill="url(#psg-or)" fontFamily="var(--font-display)" fontWeight="800" fontSize="16"
            transform="skewX(-14) translate(16.5 0)">S</text>
      <g fill="#fff" fontFamily="var(--font-display)">
        <text x="83" y="39" fontSize="18" fontWeight="800" letterSpacing="0.3">POINT</text>
        <text x="84" y="48.5" fontSize="8.6" fontWeight="700" letterSpacing="0.7">SOLUTIONS</text>
        <text x="84" y="57.5" fontSize="8.6" fontWeight="700" letterSpacing="0.7">GROUP</text>
      </g>
      <path d="M84 63 H99" stroke="#fff" strokeWidth="1.2" opacity="0.75" />
      <g fill="#fff" opacity="0.7">
        <circle cx="103" cy="63" r="0.9" /><circle cx="108" cy="63" r="0.9" /><circle cx="113" cy="63" r="0.9" />
      </g>
    </svg>
  );
}
