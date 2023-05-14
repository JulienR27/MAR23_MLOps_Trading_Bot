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

    - ll existe plus de 600 000 actions cotées dans le monde, réparties sur plus de 100 bourses dans plus de 80 pays. 

    - Il est communément admis qu'une personne seule et expérimentée peut suivre sans aide logicielle, un portefeuille d'environ 20 à 30, (en  fonction de la complexité de sa stratégie de trading, de la fréquence du trading, et de la quantité d'informations à analyser)

    - Dans ce contexte l'utilisation d'un logiciel de trading capable d’analyser rapidement  de grandes quantités de données, permet d’élargir les opportunités  parmi un nombre bien plus grand d'actions. Ce qui rend possible la mise en place de stratégies de trading plus complexes. 

    - La gestion du risque et de l’horizon d’investissement sont capitales pour construire un portefeuille. De la diversification des investissements et la gestion de la liquidité et la répartition du capital sur un certain nombre d'actions dépend la sécurité des investissements. L’aide apportée par un système intelligent capable d’analyser un nombre colossale de données de cours et/ou fondamentales permet de réduire les risques et de maximiser les chances de réaliser des bénéfices à long terme. 

    - La rentabilité ne dépend aussi des coûts : frais de courtage, coûts associés au trading, fiscalité...

        

    ### 			différents niveaux envisagés en fonction de l’avancé du projet :

    - **Niveau 1- Sur quels actions placer un ordre d’achat ou de vente (y compris à découvert) à l’instant de ma requête ?**  => proposition d’une liste ordonnée des choix possibles
    - **Niveau 2- Avec quel ordre précisément ?** en fonction de l’horizon d’investissement pour optimiser les propositions => (courts, volume, type, date des validité) des ordres à passer acheter / garder  /vendre / stop loss... tenir compte de la probabilité de réalisation de l’ordre
    - **Niveau 3- proposition faite en prenant en compte la composition du portefeuille de l’utilisateur** (faire entrer et sortir des valeurs)
    - **Niveau 4- En optimisant la composition du portefeuille ?** gestion des risques : minimiser les risques et maximiser les gains.
    - **Niveau 5- En prenant en compte les coûts** (frais, taxes, impôts ?) 

    

- ### Qui est le commanditaire de l’application ?

    Réalisé dans le cadre de notre formation de MLOps avec DataScientest

- ### Qui sera l’utilisateur de l’application ?

    L’application s’adresse à des tradeurs particuliers, qui n’ont pas la puissance des outils financiers mis à dispositions des tradeurs institutionnels et professionnels et qui désirent pouvoir augmenter leur scope pour détecter des opportunités d’investissement en action. (et minimiser les risques)

- ### Qui sera l’administrateur de l’application ?

    - Application administrée par notre groupe

    - utilisateurs :

        - création des comptes utilisateurs automatisés

        - modification des comptes par l’utilisateurs
        - gestion des licences / abonnements

    - gestion des données financières (cours, fondamentales...) (vérification et prétraitement des données)

    - gestion des modèles  (entraînement, mises en productions)

- ### Dans quel contexte l’application devra-t-elle s’intégrer (site web, software,
  serveur cloud…) ?

  Niveau 1 : site web / optionnel : +/- prototype application androïde

  Niveau 2 : serveur Cloud

- ### Via quel support l’application sera-t-elle utilisée (interface graphique, terminal,
  API…) ?

  Niveau 1 :  API

  NIveau 2 : interface graphique site internet

  
## 2) Modèle
*Au cours de ce projet, vous ne serez pas évalués sur la complexité, la performance*
*et la vitesse d’exécution du modèle. En revanche, vous serez évalué sur votre*
*capacité à déployer, monitorer et maintenir ce dernier.*
*Cette partie devra détailler notamment :*

- ### Le type de modèle employé et une rapide explication de son fonctionnement
  Tous les modèles sont des **modèle de régression LightGBM** visant à prédire la **variation future des prix des actions** américaines.

  Ils sont entraînés sur trois types de jeux de données :

  - uniquement les **données de marché** : ouverture, plus haut, plus bas, clôture, volume. Nous calculons ensuite diverses caractéristiques basées sur celles-ci : rendement logarithmique avec différents décalages, valeur de clôture à différentes moyennes mobiles, croisement de moyennes mobiles, volatilité historique, changements de volume avec différents décalages.
  - uniquement des **données fondamentales** (macroéconomiques, financières des actions) : obligations américaines à 10 ans, VIX, EPS, PEG, ratio cours/bénéfice, rendement des dividendes, surprise des annonces de bénéfices, secteur, etc.
  - à la fois sur les **données de marché** **et** les **données fondamentales**.

  <div style="border: 1px solid black; padding: 10px;">Les modèles sont entraînés pour <b>prédire la variation des prix des actions à différents horizons temporels</b>. Plus précisément, comme nous sommes censés obtenir les prix de clôture à la fin de la journée suivante, <b>tous les modèles sont en fait entraînés pour prédire l'horizon + 1 jour</b>.</div>

  **<u>liste des modèles actuels :</u>**

  * lgbm_market_1d: trained on market data only to predict tomorrow price variation

  * lgbm_market_1w: trained on market data only to predict price change in one week

  * lgbm_market_2w: trained on market data only to predict price change in two weeks

  * lgbm_market_1m: trained on market data only to predict price change in one month

  * lgbm_fundamental_1d: trained on fundamental data only to predict tomorrow price variation

  * lgbm_fundamental_1w: trained on fundamental data only to predict price change in one week

  * lgbm_fundamental_2w: trained on fundamental data only to predict price change in two weeks

  * lgbm_fundamental_1m: trained on fundamental data only to predict price change in one month

  * lgbm_market_and_fundamental_1d: trained on market and fundamental data to predict tomorrow price variation

  * lgbm_market_and_fundamental_1w: trained on market and fundamental data to predict price change in one week

  * lgbm_market_and_fundamental_2w: trained on market and fundamental data to predict price change in two weeks

  * lgbm_market_and_fundamental_data_1m: trained on market and fundamental data to predict price change in one month

  **<u>Performances générales :</u>**
  
  
  
  
  
- ### La définition des métriques d’évaluation du modèle vis à vis des contraintes
du projet (accuracy, robustesse, temps d’entraînement, temps de
prédiction…)
## 3) Base de données
*Cette partie doit vous permettre de définir les données que vous utiliserez pour*
*réaliser ce projet. Bien souvent, vous aurez accès dans le cadre de ce projet à des*
*données “statiques”, qui n’évolueront pas tout au long du projet. Cependant, en*
*général dans le cadre d’un projet MLOps en entreprise, les données évoluent au*
*cours du temps (suite à l’ajout de nouvelles données et à la correction de certaines*
*anciennes). Il sera donc nécessaire de discuter à la fois de la base de données à*
*laquelle vous avez véritablement accès, et de celle à laquelle vous devriez avoir*
*accès dans l’hypothèse d’un projet d’entreprise.*
*Une attention particulière sera portée sur la gestion de l’ingestion de nouvelles*
*données.*
*Il est recommandé d’ajouter des images de la base de données (ou de son schéma*
*d’architecture) pour faciliter la compréhension.*

* Donnée accessible via l’API de Tiingo ?
* Scrapping ?

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