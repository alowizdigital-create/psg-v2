import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function NotFound() {
  return (
    <section className="page-hero grain" style={{ minHeight: "80vh", display: "grid", alignItems: "center" }}>
      <div className="container">
        <span className="eyebrow">Erreur 404</span>
        <h1>Page introuvable</h1>
        <p>Cette page n&apos;existe pas ou a été déplacée.</p>
        <div style={{ display: "flex", gap: 12, marginTop: 28, flexWrap: "wrap" }}>
          <Link href="/" className="btn btn-primary">Retour à l&apos;accueil <ArrowRight size={18} /></Link>
          <Link href="/catalogue" className="btn btn-outline">Voir le catalogue</Link>
        </div>
      </div>
    </section>
  );
}
