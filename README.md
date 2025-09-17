# Laboratoires des cours GLO-4001 et GLO-7021

Les laboratoires doivent être réalisés en équipe de quatre ou plus.

Matériel requis: un ordinateur portable par équipe (pour la connexion wifi), une plate-forme robotique par équipe.

Les responsables des laboratoires sont William Guimont-Martin (william.guimont-martin@norlab.ulaval.ca) et William
Larrivée-Hardy (william.larrivee-hardy@norlab.ulaval.ca).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Laboratoires des cours GLO-4001 et GLO-7021](#laboratoires-des-cours-glo-4001-et-glo-7021)
    - [Introduction](#introduction)
    - [Lancer les laboratoires](#lancer-les-laboratoires)
    - [Architecture logicielle](#architecture-logicielle)
- [Machine virtuelle et simulateur](#machine-virtuelle-et-simulateur)

<!-- markdown-toc end -->

## Introduction

Cette série de laboratoires vous fera expérimenter certains aspects vus dans le cours de robotique mobile.

**Avec une plate-forme robotique:** Nous disposons de plate-formes robotiques
*Wave Rover* de la compagnie Waveshare. Toutes les plate-formes disposent d'un
ordinateur de bord *Jetson Orin*, une paire de capteurs infra-rouge, une caméra
*OAK-D Lite*, un IMU intégré et un capteur LiDAR 2D.

## Lancer les laboratoires
1. Brancher l'alimentation du robot et l'allumer avec le bouton à l'arrière de la plateforme.
2. Se connecter au Wi-Fi du robot
    - SSID: `team[numéro-du-robot]-wifi`
    - Le numéro du robot se trouve à l'avant de la plateforme
3. Depuis votre ordinateur, lancer une ligne de commande et entrer:
   ```shell
   ssh -L 8888:localhost:8888 norlab@192.168.0.101
   cd glo4001/scripts/
   git reset --hard
   ./ros_rover.sh
   # CTRL-A + D pour détacher le terminal
   ./jupyter.sh
   ```
4. Ouvrir l'URL affichée dans le terminal dans votre navigateur internet.
5. Vous pouvez maintenant faire les laboratoires!

À la fin des laboratoires, sauvegardez une copie de votre notebook (`File -> Download`) et éteignez le robot:

```shell
sudo shutdown now
```

## Laboratoires sans la base robotique

Pour faire les laboratoires, vous pouvez utilisez les données déjà collectées.
Le dossier `offline` contient les données nécessaires pour faire les laboratoires sans la base robotique.

Pour installer les dépendances nécessaires, exécutez les commandes suivantes:

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
juptyer notebook
```

## Architecture logicielle

La façon dont nous interagirons avec les robots est un peu complexe, mais elle
est conçue d'une façon qui devrait être assez transparente aux étudiants. 
L'ordinateur de bord communique avec ses capteurs à travers un logiciel nommé [ROS](https://www.ros.org/) (pour *Robot Operating System*).
Pour éviter d'avoir à installer toutes les dépendances sur votre ordinateur, la communication entre celui-ci et le robot s'effectue via un rosbridge, qui utilise une connexion websocket.
Notre bibliothèque `robmob` gère la connection websocket et transforme les messages ROS vers du Python standard.

Nous utiliserons le code python à travers un *jupyter notebook*. Jupyter est un
environnement interactif qui permet d'entremêler du code, le résultat de son
exécution et du texte. Voici un exemple de *jupyter notebook* à l'oeuvre.

<img src="doc/jupyterexample.png"></img>

# Machine virtuelle et simulateur

<details id="simulation">
<summary><b>Instruction seulement pour la machine virtuelle</b></summary>
Entre les années 2020 et 2023, nous utilisions un simulateur.
Les laboratoires restent pour la majorité compatibles avec Gazebo, mais nous n'offrons pas de support pour le faire fonctionner.

**En simulation:** Le simulateur vient émuler la plate-forme robotique et l'ordinateur de bord du `kobuki`.
Le principe reste le même: on ouvre une connexion websocket avec le simulateur et l'on peut interagir avec ROS comme s'
il
s'agissait d'une vraie plate-forme robotique.

**Si vous utilisez votre propre ordinateur:**
Téléchargez la machine virtuelle pour **VirtualBox** disponible
à [Machine Virtuelle VirtualBox v3](https://ulavaldti-my.sharepoint.com/:u:/g/personal/wigum_ulaval_ca/EYQpkPsRKL1GlxzyoQQNUj8B-GOfM4oa2a5-BQnWEbkf9A?e=eS72gP).

Lien de la VM v2: [glo4001-virtualbox-v2](http://www2.ift.ulaval.ca/~pgiguere/download/glo4001-v2.zip)

**Si vous utilisez un ordinateur du laboratoire informatique:**
Téléchargez la machine virtuelle pour **VMWare** disponible
à [Machine Virtuelle VMWare v3](https://ulavaldti-my.sharepoint.com/:u:/g/personal/wigum_ulaval_ca/EZkfr_HfKLJAsYOqXYXnAIkBkjhUWwmjHitjCkG8OISnVA?e=uO7EXK).
Tous les fichiers que vous désirez conserver doivent être dans votre dossier OneDrive, **sinon ils seront supprimés par
le système informatique.**

**IMPORTANT:**
Voici les informations de connexion :

```
Username: student
Password: student
```

**IMPORTANT:** Ne pas faire les mises-à-jour sur les machines virtuelles.

Pour plus d'information sur la mise en place des machines virtuelles, voir le notebook `ConfigurationVM`.

Dans la machine virtuelle, ouvrez un terminal (`CTRL-ALT-T`), et entrez les commandes:

```bash
cd ~/catkin_ws && git pull
cd ~/glo4001
git pull
source venv/bin/activate
jupyter notebook
```

**Vous devrez exécuter ces lignes à chaque début de laboratoire!**

Dans le *jupyter notebook*, ouvrez le fichier *Laboratoire 0.ipynb*. La suite des
instructions, incluant comment interagir avec le robot, s'y trouve.
</details>
