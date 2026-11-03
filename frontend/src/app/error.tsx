"use client";

export default function Erreur({ reset }: { error: Error; reset: () => void }) {
  return (
    <section className="page-hero grain" style={{ minHeight: "70vh", display: "grid", alignItems: "center" }}>
      <div className="container">
        <span className="eyebrow">Oups</span>
        <h1>Le site est momentanément indisponible</h1>
        <p>Merci de réessayer dans un instant, ou contactez-nous par WhatsApp.</p>
        <button className="btn btn-primary" style={{ marginTop: 28 }} onClick={reset}>Réessayer</button>
      </div>
    </section>
  );
}
