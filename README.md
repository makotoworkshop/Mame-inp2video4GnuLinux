# Mame-inp2video4GnuLinux
Générer une vidéo à partir du fichier input d'une partie sauvegardée.

http://burogu.makotoworkshop.org/index.php?post/2020/04/16/Mame-inp2video4GnuLinux

Il est possible de mémoriser une partie jouée avec MAME sous forme de pointeur consistant en un fichier INP de quelques kio (inputs file) qu'il est alors possible de rejouer avec l'émulateur.
 
- Pour enregistrer une partie en va exécuter ceci :

mame nom_de_la_rom -record ma_partie.inp

- On va pouvoir rejouer la partie avec la commande suivante :

mame nom_de_la_rom -playback ma_partie.inp

Pour générer un fichier vidéo à partir du fichier INP, il faut passer par d'autres commandes.

Le Logiciel « Mame-inp2video4GnuLinux » se propose donc de réaliser celà, depuis n'importe quel ordinateur équipé de GNU/Linux de la famille Debian.
Il n'est pas nécessaire d'avoir MAME installé sur cette machine.
Vous aurez besoin cependant du fichier ROM et bien entendu du fichier INP correspondant.

Une interface graphique est là pour vous guider…


