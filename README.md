# Laboratoires des cours GLO-4001 et GLO-7021

**À distance:**: Seul ou en équipe. Matériel requis: ordinateur.

**En présentiel:** En équipe de deux ou plus. Matériel requis: un ordinateur portable
par équipe (pour la connexion wifi), une plate-forme robotique par équipe.

Le responsable des laboratoires est William Guimont-Martin (william.guimont-martin.1@ulaval.ca).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table des matières**

- [Introduction](#introduction)
- [Architecture logicielle](#architecture-logicielle)
- [Installation](#installation)
    - [Linux (ubuntu)](#linux-ubuntu)
        - [Création d'un environnement virtuel python3](#création-dun-environnement-virtuel-python3)
        - [Acquisition du code des laboratoires](#acquisition-du-code-des-laboratoires)
        - [Lancer jupyter](#lancer-jupyter-linux)
    - [Windows](#windows)
        - [Installation de anaconda](#installation-de-anaconda)
        - [Téléchargement du code du cours](#téléchargement-du-code-du-cours)
        - [Installation des librairies nécessaires](#installation-des-librairies-nécessaires)
        - [Lancer jupyter](#lancer-jupyter-windows)
- [Lancer un laboratoire](#lancer-un-laboratoire)

<!-- markdown-toc end -->


## Introduction

Cette série de laboratoires vous fera expérimenter certains aspects vus dans le
cours de robotique mobile. 

À distance, nous avons un simulateur permettant d'expérimenter avec des robots virtuel. Un simulateur 
de robotique est un outil extrêmement pratique pour, entre autres, 
tester des algorithmes, expérimenter dans différents environments, 
entraîner des modèles d'apprentissage automatique et valider son code.

En présentiel, nous disposons de vraies plate-formes robotiques
*Kobuki* de la compagnie iClebo. Toutes les plate-formes disposent d'un
ordinateur de bord *Kangaroo*, une paire de capteurs infra-rouge, une caméra
*Kinect* et un IMU intégré. Ce plus, certaines plate-formes sont équipées avec un
capteur LiDAR.

## Architecture logicielle

La façon dont nous interagirons avec les robots est un peu complexe, mais elle
est conçue d'une façon qui devrait être assez transparente aux étudiants. Vous
en trouverez un résumé dans le schéma suivant.

<img src="doc/software_architecture.png" width="800" ></img>

Votre ordinateur de bord communique avec la `kobuki` à travers un logiciel nommé ROS (pour *Robot Operating System*). Il nous suffit donc de parler à l'ordinateur de bord avec une connexion websocket, et le tour est joué.

Nous utiliserons le code python à travers un *jupyter notebook*. Jupyter est un
environnement interactif qui permet d'entremêler du code, le résultat de son
exécution et du texte. Voici un exemple de *jupyter notebook* à l'oeuvre.

<img src="doc/jupyterexample.png"></img>

## Machine virtuelle et simulateur

Il est aussi possible d'un simulateur plutôt que la base `kobuki`. 
Pour ce faire, veuillez télécharger la machine virtuelle 
disponible à [cette adresse](http://www2.ift.ulaval.ca/~pgiguere/download/glo4001-v2.zip).

Les instructions pour mettre en marche le simulateur se trouvent dans le laboratoire 0.

## Installation

Dans cette section nous verrons comment installer *jupyter* et la librairie
*robmob* sur votre ordinateur.

### Linux (Ubuntu)

Les instructions qui suivent sont spécifiques à Ubuntu mais devraient bien se 
généraliser à d'autres distributions (et peut-être même MacOS).

#### Création d'un environnement virtuel python3

Grâce à la ligne de commande, nous allons créer un `virtualenv` python qui
contient les logiciels nécessaires pour faire les laboratoires. Assurez-vous
d'abord d'avoir les paquets suivants:

```bash
$ sudo apt install python3-pip python3-venv python3-testresources
```

Ensuite, créez un environnement virtuel avec la commande suivante.

```
$ python3 -m venv venv
```

Activez l'environment avec:

```
$ source venv/bin/activate
```

Vous devrez activer l'environnement avant de débuter chaque laboratoire.

Si l'activation a réussi, vous verrez `(venv)` à la gauche de votre invite de commande.

#### Acquisition du code des laboratoires

Dans un autre dossier, lancez la commande

```
$ git clone https://github.com/norlab-ulaval/glo4001
```

Cette commande téléchargera le code nécessaire aux laboratoires. Il contient aussi un fichier
`requirements.txt` qui contient la liste des libraries python dont on a besoin pour exécuter
le code fourni. Heureusement, on peut les installer automatiquement avec une commande. Assurez-vous
d'avoir activé l'environnement virtuel avant de lancer cette commande.

```
$ cd glo4001
$ pip install -r requirements.txt
```

#### Lancer jupyter (linux)

Si tout a réussi, votre environnement virtuel contient désormais toutes les
librairies nécessaires. Vous pouvez le tester en tentant de lancer le *jupyter
notebook* (toujours avec l'environnement virtel activé). Lancez cette commande à
partir de l'intérieur du repo `glo4001`.

```
$ jupyter notebook
```

Avec un peu de chance, votre navigateur web devrait ouvrir un nouvel onglet pointant sur le notebook *jupyter*. 
Bien joué! Maintenant, vous pouvez ouvrir le fichier `Laboratoire 0.ipynb` et vous connecter à votre robot.

Si vous obtenez une erreur comme quoi jupyter n'est pas une commande, 
ouvrez le fichier `.bashrc` avec `gedit ~/.bashrc`. Ensuit, ajoutez-y la ligne suivante à la toute fin:

```
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
instructions, incluant comment interagir avec le robot, s'y trouve. Bonne
chance!
