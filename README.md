# Laboratoires des cours GLO-4001 et GLO-7021

Les laboratoires sont conçus pour pouvoir être réalisés soit avec un vrai robot ou le simulateur.

**En simulateur :** Seul ou en équipe. Matériel requis: ordinateur.

**Avec une plate-forme robotique :** En équipe de deux ou plus. Matériel requis: un ordinateur portable
par équipe (pour la connexion wifi), une plate-forme robotique par équipe.

Le responsable des laboratoires est William Guimont-Martin (william.guimont-martin.1@ulaval.ca).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table des matières**

- [Laboratoires des cours GLO-4001 et GLO-7021](#laboratoires-des-cours-glo-4001-et-glo-7021)
  - [Introduction](#introduction)
  - [Machine virtuelle et simulateur](#machine-virtuelle-et-simulateur)
  - [Architecture logicielle](#architecture-logicielle)
  - [Installation](#installation)
    - [Linux (Ubuntu)](#linux-ubuntu)
      - [Acquisition du code des laboratoires](#acquisition-du-code-des-laboratoires)
      - [Création d'un environnement virtuel python3](#création-dun-environnement-virtuel-python3)
      - [Lancer jupyter (linux)](#lancer-jupyter-linux)
    - [Windows](#windows)
      - [Installation de anaconda](#installation-de-anaconda)
      - [Téléchargement du code du cours](#téléchargement-du-code-du-cours)
      - [Installation des librairies nécessaires](#installation-des-librairies-nécessaires)
      - [Lancer jupyter (windows)](#lancer-jupyter-windows)
  - [Lancer un laboratoire](#lancer-un-laboratoire)

<!-- markdown-toc end -->

## Introduction

Cette série de laboratoires vous fera expérimenter certains aspects vus dans le cours de robotique mobile.

**En simulation :** Nous avons un simulateur permettant d'expérimenter avec des robots virtuel. Un simulateur
de robotique est un outil extrêmement pratique pour, entre autres,
tester des algorithmes, expérimenter dans différents environments,
entraîner des modèles d'apprentissage automatique et valider son code.

**Avec une plate-forme robotique :** Nous disposons de plate-formes robotiques
*Kobuki* de la compagnie iClebo. Toutes les plate-formes disposent d'un
ordinateur de bord *Kangaroo*, une paire de capteurs infra-rouge, une caméra
*Kinect* et un IMU intégré. Ce plus, certaines plate-formes sont équipées avec un
capteur LiDAR.

## Machine virtuelle et simulateur

Il est aussi possible d'un simulateur plutôt que la base `kobuki`.

**Si vous utilisez votre propre ordinateur :**
Téléchargez la machine virtuelle pour **VirtualBox** disponible à [Machine Virtuelle VirtualBox v3](https://ulavaldti-my.sharepoint.com/personal/wigum_ulaval_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fwigum%5Fulaval%5Fca%2FDocuments%2Fglo4001%5Fvirtualbox%5Fv3%2Ezip&parent=%2Fpersonal%2Fwigum%5Fulaval%5Fca%2FDocuments&ga=1).

Lien de la VM v2: [glo4001-virtualbox-v2](http://www2.ift.ulaval.ca/~pgiguere/download/glo4001-v2.zip)


Lien de la VM v2: [glo4001-virtualbox-v2](http://www2.ift.ulaval.ca/~pgiguere/download/glo4001-v2.zip)

**Si vous utilisez un ordinateur du laboratoire informatique :**
Téléchargez la machine virtuelle pour **VMWare** disponible à [Machine Virtuelle VMWare v3](https://ulavaldti-my.sharepoint.com/personal/phgig4_ulaval_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fphgig4%5Fulaval%5Fca%2FDocuments%2Fglo4001%5Fvmware%5Fv3%2Ezip&parent=%2Fpersonal%2Fphgig4%5Fulaval%5Fca%2FDocuments&ga=1).


**IMPORTANT:**
Voici les informations de connexion :

```
Username: student
Password: student
```

Pour plus d'information sur la mise en place des machines virtuelles, voir le notebook `ConfigurationVM`.

**En simulation:** Dans la machine virtuelle, ouvrez un terminal (`CTRL-ALT-T`), et entrez les commandes:

```bash
cd ~/catkin_ws && git pull
cd ~/glo4001
git pull
source venv/bin/activate
jupyter notebook
```

## Architecture logicielle

La façon dont nous interagirons avec les robots est un peu complexe, mais elle
est conçue d'une façon qui devrait être assez transparente aux étudiants. Vous
en trouverez un résumé dans le schéma suivant.

<img src="doc/software_architecture.png" width="800" ></img>

Votre ordinateur de bord communique avec la `kobuki` à travers un logiciel nommé ROS (pour *Robot Operating System*).
Il nous suffit donc de parler à l'ordinateur de bord avec une connexion websocket, et le tour est joué.

**En simulation:** Le simulateur vient émuler la plate-forme robotique et l'ordinateur de bord du `kobuki`.
Le principe reste le même: on ouvre une connexion websocket avec le simulateur et l'on peut interagir avec ROS comme s'il
s'agissait d'une vraie plate-forme robotique.

Nous utiliserons le code python à travers un *jupyter notebook*. Jupyter est un
environnement interactif qui permet d'entremêler du code, le résultat de son
exécution et du texte. Voici un exemple de *jupyter notebook* à l'oeuvre.

<img src="doc/jupyterexample.png"></img>

## Installation

Dans cette section nous verrons comment installer *jupyter* et la librairie
*robmob* sur votre ordinateur.

**En simulation :** La machine virtuelle est déjà configurée avec tout ce qu'il faut. Vous n'avez donc pas à installer
ces dépendances sur votre propre ordinateur.

### Linux (Ubuntu)

Les instructions qui suivent sont spécifiques à Ubuntu mais devraient bien se
généraliser à d'autres distributions (et peut-être même MacOS).

#### Acquisition du code des laboratoires

Dans un terminal, exécutez les commandes suivantes:

```bash
git clone https://github.com/norlab-ulaval/glo4001
cd glo4001
```

#### Création d'un environnement virtuel python3

Grâce à la ligne de commande, nous allons créer un `virtualenv` python qui
contient les logiciels nécessaires pour faire les laboratoires. Assurez-vous
d'abord d'avoir les paquets suivants:

```bash
sudo apt update
sudo apt install python3-pip python3-venv python3-testresources
```

Ensuite, créez un environnement virtuel avec la commande suivante.

```bash
$ python3 -m venv venv
```

Activez l'environment avec:

```bash
$ source venv/bin/activate
```

**IMPORTANT :** Vous devrez activer l'environnement avant de commencer chaque laboratoire.

Si l'activation a réussi, vous verrez `(venv)` à la gauche de votre invite de commande.

Le dépôt contient un fichier `requirements.txt` qui contient la liste des libraries python dont on a besoin pour exécuter le code fourni.
Heureusement, on peut les installer automatiquement avec une commande.
Assurez-vous d'avoir activé l'environnement virtuel avant de lancer cette commande.

```bash
pip install -r requirements.txt
```

#### Lancer jupyter (linux)

Si tout a réussi, votre environnement virtuel contient désormais toutes les
librairies nécessaires. Vous pouvez le tester en tentant de lancer le *jupyter
notebook* (**toujours avec l'environnement virtuel activé**). Lancez cette commande à
partir de l'intérieur du dossier `glo4001`.

```bash
jupyter notebook
```

Avec un peu de chance, votre navigateur web devrait ouvrir un nouvel onglet pointant sur le notebook *jupyter*.
Bien joué! Maintenant, vous pouvez ouvrir le fichier `Laboratoire 0.ipynb` et vous connecter à votre robot.

Si vous obtenez une erreur comme quoi jupyter n'est pas une commande,
ouvrez le fichier `.bashrc` avec `gedit ~/.bashrc`. Ensuit, ajoutez-y la ligne suivante à la toute fin:

```bash
export PATH=$PATH:/home/student/.local/bin
```

Si vous obtenez une erreur de connexion au kernel, essayez la commande suivante:

```bash
pip3 install -I notebook
```

### Windows

#### Installation de anaconda

Visitez [ce site](https://www.continuum.io/downloads) pour télécharger la
distribution anaconda. Anaconda contient python ainsi qu'une série de librairies
utilisées dans les laboratoires. Assurez-vous de vous procurer la version *Python 3.5 ou plus*.

Installez anaconda, en conservant les options d'installation par défaut, qui sont

- Installation locale (single user)
- Ajout de anaconda au *PATH*
- Sélection de anaconda comme python par défaut

#### Téléchargement du code du cours

Visitez ensuite [cette adresse](https://github.com/norlab-ulaval/glo4001) et téléchargez
le code du cours. En appuyant sur le bouton *clone or download*, vous pourrez télécharger
une version `.zip` de repo. Faites l'extraction du code du cours à un endroit approprié.

#### Installation des librairies nécessaires

Avec le menu démarrer, ouvrez le logiciel *anaconda prompt*. Utilisez les
commandes `DIR` et `CHDIR` pour naviguer jusqu'au dossier contenant le code du
cours. À partir de là, lancez les commandes suivantes. Elles devraient installer les
librairies nécessaires à l'exécution du code du cours.

```
conda install -c pillow matplotlib
pip install -r requirements.txt
```

#### Lancer jupyter (windows)

Depuis la *anaconda prompt*, allez dans le dossier contenant le code du cours, puis exécutez

```
jupyter notebook
```

## Lancer un laboratoire

Dans le *jupyter notebook*, ouvrez le fichier *Laboratoire 0.ipynb*. La suite des
instructions, incluant comment interagir avec le robot, s'y trouve.

**En simulation :** Ouvrez un terminal (`CTRL-ALT-T`), et entrez les commandes:

```bash
cd glo4001
jupyter notebook
```

Bonne chance!
