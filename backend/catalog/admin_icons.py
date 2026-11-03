"""Icônes Font Awesome 6 utilisées par l'interface d'administration."""

_FA = {
    "dashboard": "fa-solid fa-gauge-high",
    "entreprise": "fa-solid fa-building",
    "offre": "fa-solid fa-bag-shopping",
    "section": "fa-solid fa-table-cells-large",
    "heroslide": "fa-solid fa-images",
    "sitesettings": "fa-solid fa-gear",
    "demande": "fa-solid fa-inbox",
    "notification": "fa-solid fa-paper-plane",
    "user": "fa-solid fa-users",
    "group": "fa-solid fa-user-shield",
    "site": "fa-solid fa-arrow-up-right-from-square",
    "logout": "fa-solid fa-right-from-bracket",
    "key": "fa-solid fa-key",
    "bell": "fa-regular fa-bell",
    "plus": "fa-solid fa-plus",
    "menu": "fa-solid fa-bars",
    "money": "fa-solid fa-money-bill-wave",
    "calendar": "fa-regular fa-calendar",
    "alert": "fa-solid fa-triangle-exclamation",
    "today": "fa-regular fa-clock",
    "check": "fa-solid fa-phone",
    "brouillon": "fa-regular fa-file-lines",
    "default": "fa-solid fa-circle",
}

ICONES = {k: f'<i class="psg-i {v}" aria-hidden="true"></i>' for k, v in _FA.items()}
