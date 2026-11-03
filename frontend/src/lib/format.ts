export function fcfa(montant: number | null | undefined) {
  if (!montant) return "";
  return `${new Intl.NumberFormat("fr-FR").format(montant).replace(/ | /g, " ")} FCFA`;
}

export function telLien(numero: string) {
  const chiffres = numero.replace(/\D/g, "");
  return `tel:+${chiffres.length === 9 ? `237${chiffres}` : chiffres}`;
}
