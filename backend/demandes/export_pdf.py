"""Export PDF de la liste des demandes clients (action de l'admin)."""

from io import BytesIO
from xml.sax.saxutils import escape

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BORDEAU = colors.HexColor("#6D0D0C")
OR = colors.HexColor("#F5B800")
FOND = colors.HexColor("#F8F1EC")
GRIS = colors.HexColor("#6E5F60")

TEXTE = ParagraphStyle("texte", fontName="Helvetica", fontSize=8, leading=10)
GRAS = ParagraphStyle("gras", parent=TEXTE, fontName="Helvetica-Bold")
PETIT = ParagraphStyle("petit", parent=TEXTE, fontSize=7, leading=9, textColor=GRIS)
ENTETE = ParagraphStyle("entete", parent=TEXTE, fontName="Helvetica-Bold", textColor=colors.white)
TITRE = ParagraphStyle("titre", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=BORDEAU)
SOUS_TITRE = ParagraphStyle("sous-titre", fontName="Helvetica", fontSize=9, leading=12, textColor=GRIS)
DROITE = ParagraphStyle("droite", parent=TEXTE, alignment=TA_RIGHT)


def _p(texte, style=TEXTE):
    return Paragraph(escape(str(texte or "")).replace("\n", "<br/>"), style)


def _fcfa(montant):
    return f"{montant:,} FCFA".replace(",", " ") if montant else "Sur devis"


def demandes_pdf(queryset, nom_site="PS GROUP SARL"):
    """Renvoie le contenu (bytes) d'un PDF A4 paysage listant les demandes."""
    tampon = BytesIO()
    maintenant = timezone.localtime()

    def pied_de_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BORDEAU)
        canvas.rect(0, A4[0] - 6 * mm, A4[1], 6 * mm, stroke=0, fill=1)
        canvas.setFillColor(OR)
        canvas.rect(0, A4[0] - 7 * mm, A4[1], 1 * mm, stroke=0, fill=1)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GRIS)
        canvas.drawString(12 * mm, 8 * mm, f"{nom_site} — export du {maintenant:%d/%m/%Y à %H:%M}")
        canvas.drawRightString(A4[1] - 12 * mm, 8 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        tampon, pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm,
        topMargin=14 * mm, bottomMargin=14 * mm, title="Demandes clients", author=nom_site,
    )
    demandes = list(queryset.select_related("entreprise").prefetch_related("choix").order_by("-cree_le"))
    total = sum(d.total_estime or 0 for d in demandes)

    elements = [
        _p(f"{nom_site} — Demandes clients", TITRE),
        _p(f"{len(demandes)} demande(s) · total estimé {_fcfa(total)} · édité le {maintenant:%d/%m/%Y à %H:%M}",
           SOUS_TITRE),
        Spacer(0, 6 * mm),
    ]

    lignes = [[_p(t, ENTETE) for t in
               ("Référence", "Date", "Client", "Entreprise / offre", "Choix du client", "Total estimé", "Statut")]]
    for d in demandes:
        choix = "\n".join(f"• {c.groupe} : {c.libelle}" for c in d.choix.all()) or "—"
        client = f"{d.nom}\n{d.telephone}" + (f"\n{d.email}" if d.email else "")
        evenement = ""
        if d.date_evenement or d.lieu:
            evenement = "\nÉvénement : " + " · ".join(
                x for x in [d.date_evenement.strftime("%d/%m/%Y") if d.date_evenement else "", d.lieu] if x)
        lignes.append([
            _p(d.reference, GRAS),
            _p(f"{timezone.localtime(d.cree_le):%d/%m/%Y\n%H:%M}"),
            _p(client),
            [_p(d.entreprise or "—", GRAS), _p((d.offre_titre or "Demande de contact") + evenement, PETIT)],
            [_p(choix)] + ([_p(f"Message : {d.message}", PETIT)] if d.message else []),
            _p(_fcfa(d.total_estime), DROITE),
            _p(d.get_statut_display()),
        ])

    largeurs = [26 * mm, 20 * mm, 42 * mm, 50 * mm, 80 * mm, 26 * mm, 26 * mm]
    tableau = Table(lignes, colWidths=largeurs, repeatRows=1)
    tableau.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BORDEAU),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOND]),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, colors.HexColor("#E8DCD6")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(tableau if demandes else _p("Aucune demande sélectionnée."))
    doc.build(elements, onFirstPage=pied_de_page, onLaterPages=pied_de_page)
    return tampon.getvalue()
