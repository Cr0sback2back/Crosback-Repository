# Crosback-Repository
Trop beau trop merveilleux

## ASTRO BLITZ (NumWorks)

Jeu de tir spatial pour calculatrice NumWorks : `astroblitz.py`.

**Installer :** copie le contenu du fichier dans un nouveau script sur
[my.numworks.com](https://my.numworks.com/python) puis envoie-le sur la calculatrice
(ou crée le script directement dans l'appli Python et colle le code).

**Commandes :**
- Flèches : déplacer le vaisseau
- OK / EXE : tirer
- Retour : quitter

**Ennemis :** rouge = rôdeur (10 pts), rose = zigzag (15 pts), vert = tank à 2 PV (30 pts, dès le niveau 2).
Un ennemi qui passe en bas te coûte 5 points.

**Boss de fin de niveau :** à 200 points, un boss arrive (« ALERTE : BOSS ! »). Les ennemis normaux
arrêtent d'apparaître, sa barre de vie s'affiche en haut et il te tire dessus en visant ton vaisseau.
Battre le boss rapporte 100 × niveau points, lâche un triple tir et une vie, et fait passer au niveau suivant.
À chaque niveau, le boss a plus de PV, bouge plus vite et tire plus (3 tirs en éventail dès le niveau 2).

**Bonus :** bleu `+` = triple tir pendant ~10 s, rouge = une vie en plus (max 5).
