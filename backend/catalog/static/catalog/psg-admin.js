// Bouton de choix de fichier en français : le bouton natif du navigateur
// (« Choose File / No file chosen ») suit la langue du système.
(function () {
  function franciser(input) {
    if (input.dataset.psgFile) return;
    input.dataset.psgFile = "1";
    var zone = document.createElement("span");
    zone.className = "psg-file";
    var bouton = document.createElement("button");
    bouton.type = "button";
    bouton.className = "psg-file-btn";
    bouton.innerHTML = '<i class="fa-solid fa-upload" aria-hidden="true"></i> Choisir un fichier';
    var nom = document.createElement("span");
    nom.className = "psg-file-name";
    nom.textContent = "Aucun fichier choisi";
    input.parentNode.insertBefore(zone, input);
    zone.appendChild(input);
    zone.appendChild(bouton);
    zone.appendChild(nom);
    bouton.addEventListener("click", function () { input.click(); });
    input.addEventListener("change", function () {
      nom.textContent = input.files && input.files.length ? input.files[0].name : "Aucun fichier choisi";
    });
  }
  function tout() { document.querySelectorAll('input[type="file"]').forEach(franciser); }
  document.addEventListener("DOMContentLoaded", tout);
  // Formulaires ajoutés dynamiquement (« Ajouter une option », galerie…)
  new MutationObserver(tout).observe(document.documentElement, { childList: true, subtree: true });
})();
