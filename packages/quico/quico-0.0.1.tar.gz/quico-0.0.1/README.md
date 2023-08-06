# Quico
Quico ou quick-container est un raccourci pour docker. Il permet de compiler et lancer rapidement un conteneur.

### Environnement requis

- python 3
### Installation
```sh
$ ./install.sh
```

### Utilisation

```sh
$ quico [-h] -t TAG [-n NETWORK] [-f FILE] [-p PUBLISH] [-v VOLUME] directory

Quico ou quick-container permet de compiler puis lancer rapidement un
conteneur docker.

positional arguments:
  directory             Dossier ou compiler l'image docker.

optional arguments:
  -h, --help            show this help message and exit
  -t TAG, --tag TAG
  -n NETWORK, --network NETWORK
                        Réseau ou lancer le conteneur docker
  -f FILE, --file FILE  Chemin vers le Dockerfile à compiler
  -p PUBLISH, --publish PUBLISH
  -v VOLUME, --volume VOLUME
```