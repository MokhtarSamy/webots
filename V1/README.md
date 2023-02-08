# webots V1

Dans cettre première version du TP, nous avons implémenté un coordinateur de comportment pour le robot Khepera2 sur Webots.

Le coordinateur permet la transistion entre deux comportement, un d'évitement d'obstalce, et un de suivi de lumière. 

Chaque comportement est écrit sous la forme d'une classe, à laquelle est passée l'instance du robot à l'initialisation. Chaque classe défini une méthode "step", permettant le contrôle des moteurs du robots afin de suivre le comportement défini.

La classe "Coordinator" contient les références aux instances des classes de chaque comportement et implémente sa propre méthode "step". Celle-ci lit les valeurs des capteurs de distance du roboto et les compare à un "threshold" (limite minimum) lui étant passé en paramètre. Si l'un des capteurs de distance indique que le robot se trouve "proche" d'un obstacle, alors le comportement d'évitement d'obtsacle est activé. Sinon, c'est le comportement de suivi de lumière qui a la priorité.