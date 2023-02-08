# Projet Webots

Dans le dossier V1, vous trouverez le projet, le controllerV1 pour la première partie du projet, et le controllerV2 pour la deuxième partie. Vous pouvez commencer par ouvrir le projet en lancant le fichier "kheperaV1" dans "\V1\worlds", ensuite en sélectionnant "controllerV1" comme controlleur et en lançant la simulation pour une démonstration de la première partie.

Pour la deuxième partie, sélectionnez "controllerV2" comme controlleur, toujours dans le dossier V1 et lancez la simulation pour lancer le serveur.

Ensuite, dans le dossier V2, vous trouverez trois dossiers correspondant à chaque conteneur, avec un Dockerfile pour construire les images, et un fichier docker-compose.yml pour lancer les trois conteneurs.

Une fois que les conteneurs sont lancés et que le serveur tourne sur Webots, une connexion sera établie automatiquement et le robot commencera à bouger.

Vous trouverez égalemet une vidéo dans le dossier V1 pour une démonstration de l'évitement des obstacles, cela est fait avec le troisième controlleur "coordination_controller.py" que lui aussi est pour la partie 1 mais avec quelques différences dans les paramètres que "controllerV1".

## V1

Pour la première version du rendu, nous avons implémenté un contrôleur qui comprend le mécanisme de coordination ainsi que les deux comportements (évitement d'obstacles et suivre la lumière).

### Mécanisme de coordination

Le mécanisme de coordination est basé sur des priorités données dynamiquement à chaque algorithme au cours de l'exécution en fonction des données récupérées des capteurs.
Nous avons choisi cette approche car nous avons juste deux comportements et donc nous n'avons pas besoin d'utiliser un algorithme plus complexe comme un algorithme basé sur des votes.
Les priorités sont 0 et 1, nous commençons avec 1 pour le comportement "suivre la lumière" et 0 pour "évitement d'obstacles". Les priorités peuvent être modifiées si le capteur de distance renvoie une valeur supérieure à 900, ce qui signifie que le robot est très proche d'un obstacle.

Le contrôleur comprend 4 classes, une classe mère "Algorithm" et deux classes pour les comportements qui héritent de celle-ci, ainsi qu'une classe "SubsumptionArchitecture" qui gère les changements de priorités et exécute l'algorithme prioritaire.

### Évitement d'obstacles

Nous avons utilisé l'algorithme de Braitenberg pour l'évitement d'obstacles.

### Suivre la lumière

Pour que le robot suive la source de lumière, nous changeons sa direction en fonction de la position du capteur de lumière qui a la valeur maximale.

## V2

### Serveur

Nous avons utilisé la bibliothèque "Socket" de Python pour lancer un serveur qui communique en protocole TCP et qui écoute en permanence les connexions entrantes pour envoyer les données des capteurs et recevoir les valeurs des vitesses provenant du mécanisme de coordination.

### Construction des images Docker

Chaque image docker est construite sur une image Python, et contient un seul script en Python.

### Communication entre les conteneurs

Il existe plusieurs méthodes pour établir la communication entre les conteneurs, telles que le protocole AMQP avec RabbitMQ, MQTT avec Mosquitto, créer des pipes ou des volumes partagés, créer un réseau pour les conteneurs ou bien communiquer en protocole HTTP.

Nous avons donc choisi de lancer un serveur Flask pour chaque conteneur, de définir "network_mode" sur "host" dans docker-compose, cela signifie que le conteneur partage le réseau de l'hôte, ensuite, nous échangons les données avec des requêtes HTTP.

## Les problèmes rencontrés

Nous avons rencontré de nombreux problèmes, en particulier pour la partie 2. Tout d'abord, nous avons eu des problèmes avec la communication entre les conteneurs. Nous avons commencé par mettre en place des sockets et défini le mode réseau sur "host" pour le conteneur "mecanismedecoordination", et ajouté un "link" dans docker-compose pour relier ce conteneur aux deux autres de comportements, mais il y avait toujours des problèmes de refus de connexion et d'échange de données entre eux.

Ensuite, nous avons décidé d'utiliser Flask, car nous voulions échanger des données avec un conteneur uniquement à un moment donné si l'algorithme est prioritaire. Le conteneur de coordination envoie les valeurs des capteurs reçues de webots à l'algorithme, et c'est à ce moment-là que nous recevons les données de vélocité et non pas en permanence.

Un autre problème a été causé par les types de données échangées, ce qui a généré de nombreuses erreurs et a ralenti notre avancement. Etant donnée la capacité limitée de nos ordinateurs, le développement a également été ralenti.
