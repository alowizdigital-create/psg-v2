import Icon from "./Icon";

export default function Marquee({ items }: { items: { nom: string; icone: string }[] }) {
  const liste = [...items, ...items, ...items, ...items];
  return (
    <div className="marquee-wrap" aria-hidden="true">
      <div className="marquee">
      <div className="marquee-track">
        {liste.map((it, i) => (
          <span className="marquee-item" key={i}><Icon name={it.icone} size={22} /> {it.nom} <span>✦</span></span>
        ))}
      </div>
    </div>
    </div>
  );
}
