<img src="./assets/image-20230514163219621.png" alt="image-20230514163219621" style="zoom:25%;" />

# Cahier des charges projet MLOps
*Le cahier des charges est primordial dans la réalisation d’un projet, ce dernier doit*
*vous permettre de suivre une ligne directrice tout au long de votre projet. Il ne doit*
*pas être négligé. Celui-ci devrait faire entre 3 et 7 pages.*

## 1) Contexte et Objectifs
*Le but de cette partie est de définir les parties prenantes, et le cadre dans lequel*
*s’intègre le projet. Soyez le plus précis possible, n’hésitez pas à être créatif. Il n’y a*
*pas une seule solution pour cette partie, et nous n’attendons pas à ce que vous*
*aboutissiez à quelque chose d’opérationnel à l’issue du projet. L’objectif est d’avoir*
*une ligne directrice pour le projet qui vous permettra de prendre des décisions au fur*
*et à mesure.*
*Cette partie devra répondre notamment aux questions suivantes :*

- ### A quelle problématique l’application doit-elle répondre ?

    Contexte :  Trading en position “swing trading” sur la base des cours de clôture sur des actions boursières. Ce qui signifie de devoir prendre des décisions d’achat ou de ventes (y compris ventes à découvert) en se basant sur les cours de clôture des marchés boursiers plutôt que sur les fluctuations intraday des cours. L‘objectif est de profiter des mouvements de prix pour générer une plus-value.

    ### Problématiques :  

    ​	Le nombre important d’actions existante ne permet pas à un individu de surveiller plus de 

    ### 			différents niveaux envisagés en fonction de l’avancé du projet :

    - **Niveau 1- Sur quels actions placer un ordre d’achat ou de vente (y compris à découvert) à l’instant de ma requête ?**  => proposition d’une liste ordonnée des choix possibles
    - **Niveau 2- Avec quel ordre précisément ?** en fonction de l’horizon d’investissement pour optimiser les propositions => (courts, volume, type, date des validité) des ordres à passer acheter / garder  /vendre / stop loss... tenir compte de la probabilité de réalisation de l’ordre
    - **Niveau 3- proposition faite en prenant en compte la composition du portefeuille de l’utilisateur** (faire entrer et sortir des valeurs)
    - **Niveau 4- En optimisant la composition du portefeuille ?** gestion des risques : minimiser les risques et maximiser les gains.
    - **Niveau 5- En prenant en compte les coûts** (frais, taxes, impôts ?) 

    

- ### Qui est le commanditaire de l’application ?

    L’application s’adresse à des petits porteurs qui n’on

- ### Qui sera l’utilisateur de l’application ?

- ### Qui sera l’administrateur de l’application ?

- ### Dans quel contexte l’application devra-t-elle s’intégrer (site web, software,
  serveur cloud…) ?

- ### Via quel support l’application sera-t-elle utilisée (interface graphique, terminal,
API…) ?
## 2) Modèle
Au cours de ce projet, vous ne serez pas évalués sur la complexité, la performance
et la vitesse d’exécution du modèle. En revanche, vous serez évalué sur votre
capacité à déployer, monitorer et maintenir ce dernier.
Cette partie devra détailler notamment :
- ### Le type de modèle employé et une rapide explication de son fonctionnement
ainsi que ses performances générales
- ### La définition des métriques d’évaluation du modèle vis à vis des contraintes
du projet (accuracy, robustesse, temps d’entraînement, temps de
prédiction…)
## 3) Base de données
Cette partie doit vous permettre de définir les données que vous utiliserez pour
réaliser ce projet. Bien souvent, vous aurez accès dans le cadre de ce projet à des
données “statiques”, qui n’évolueront pas tout au long du projet. Cependant, en
général dans le cadre d’un projet MLOps en entreprise, les données évoluent au
cours du temps (suite à l’ajout de nouvelles données et à la correction de certaines
anciennes). Il sera donc nécessaire de discuter à la fois de la base de données à
laquelle vous avez véritablement accès, et de celle à laquelle vous devriez avoir
accès dans l’hypothèse d’un projet d’entreprise.
Une attention particulière sera portée sur la gestion de l’ingestion de nouvelles
données.
Il est recommandé d’ajouter des images de la base de données (ou de son schéma
d’architecture) pour faciliter la compréhension.
## 4) API
L’API est l’interface entre le modèle, la base de données et l’utilisateur. Il n’est pas
obligatoire, dans le cadre de ce projet, d’y intégrer une interface graphique. En
revanche, cette API devra intégrer une notion d’authentification des différents types
d’utilisateurs/administrateurs qui devront l’utiliser.
Cette partie doit détailler les différents endpoints que vous souhaitez intégrer à votre
API, la manière dont cette dernière fera appel à la base de données, au modèle,
écrire dans les logs et éventuellement modifier la base de données.
## 5) Testing & Monitoring
Au cours du déploiement de l’application, il sera nécessaire de porter une attention
particulière au fait que les différentes parties du projet fonctionnent correctement
individuellement (tests unitaires), et que les performances de l’application soient
toujours en adéquation avec le cahier des charges.
Cette partie devra détailler les tests unitaires qu’il faudra mettre en oeuvre comme
par exemple :
- ### Tester le bon fonctionnement du modèle lors de l’entraînement
- ### Tester le bon fonctionnement du modèle lors de la prédiction
- ### Tester le bon fonctionnement des différents endpoints de l’API
- ### Tester le bon fonctionnement du process d’ingestion de nouvelles données
Mais également le monitoring du modèle et les décisions qui en découlent :
- ### Comment évaluer la performance du modèle à un instant donné ? (évaluation
sur l’intégralité du jeu de test, évaluation sur les données les plus récentes)
- ### Quand faut-il ré-entraîner le modèle ? (périodiquement, lorsque les
performances sont trop faibles)
- ### Sur quelles données faut-il ré-entraîner le modèle ? (sur l’intégralité du jeu de
données, sur un échantillon des données les plus récentes…)
- ### Que faire lorsque le modèle n’atteint pas le seuil de performance requis ?
(envoyer un mail d’alerte aux personnes concernées, bloquer l’application)
## 6) Schéma d’implémentation
Dans cette partie, vous devrez créer un schéma récapitulatif du projet, qui intègre les
différentes composantes du projet et leurs intéractions. Ce dernier n’a pas besoin
d’être normalisé mais devra respecter un code couleur compréhensible et se doit
d’être le plus exhaustif possible. Vous pourrez pour ce faire vous aider des outils
https://app.diagrams.net/ ou https://docs.google.com/drawings
Voici un exemple de Schéma d’implémentation :

![image-20230514163206743](./assets/image-20230514163206743.png)