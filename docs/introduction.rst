*****************
Introduction (FR)
*****************

Besoin exprimé par le Client
============================
Vous venez d'intégrer une équipe DevOps en charge d'un nouveau projet au sein de votre entreprise. Le porteur du projet, une grande chaîne d'hôtellerie, souhaite mettre en place un système unique de réservation pour tous les hôtels et tous les canaux de ventes (téléphonique, accueil, site internet, application mobile).

Le rôle de votre équipe est de mettre en place une API de réservation hôtelière. Votre client souhaite pouvoir bénéficier rapidement d'un premier lot de fonctionnalités. Réservation de chambres, nombre de personnes par chambre réservée, petit-déjeuner, annulation des réservations, garage, lit bébé, wifi...

Besoin exprimé par le Client :
Le client possède deux hôtels de 5 et 3 chambres. Chaque hôtel a son propre site internet, mais le nouveau système de réservation doit être commun. On doit donc fournir une API de réservation.
Le client a précisé qu'il envisage de possibles extensions. De nouvelles chambres doivent donc pouvoir être ajoutées. Il réfléchit également à la construction d'un nouvel hôtel qui rejoindra le système de réservation. De nouveaux hôtels peuvent donc également être ajoutés.
Un hôtel a des caractéristiques : un nombre de chambres, une adresse, un numéro de téléphone...

Les chambres sont classées par catégories :

* Suite présidentielle (SR), jusqu'à 5 personnes, tarif de base 1000$
* Suite (S), jusqu'à 3 personnes, tarif de base 720$
* Junior Suite (JS), jusqu'à 2 personnes, tarif de base 500$
* Chambre de luxe (CD), jusqu'à deux personnes, tarif de base 300$
* Chambre standard (CS), jusqu'à deux personnes, tarif de base 150$


Des services additionnels peuvent être ajoutés lors d'une réservation :

* Place de garage (25$)
* Ajout d'un lit bébé (sans frais additionnels)
* Pack romance (50$), doit être réservé avec deux jours d'avance
* Petit déjeuner (30$)


Hôtel 1 :

* 5 chambres : 1 Suite, 1 Junior Suite, 1 Chambre de luxe, 2 Chambres standards
* 3 places de garages sont disponibles, une place coûte 25$ par nuit
* 2 lits bébé sont disponibles (sans supplément)

Hôtel 2 :

* 2 suites présidentielles
* 2 places de garage
* 2 lits bébé sont disponibles

Politique de prix :

* Le prix d'une chambre peut être modulé selon la période :
* Pour les nuits de vendredi et samedi le prix des chambres est majoré de 15%
* Les nuits du mercredi et jeudi sont minoré de 10%
* Si une seule personne occupe la chambre le prix est minoré de 5%

Le client se réserve le droit de modifier les règles de prix qu'il fixe dans son hôtel. Ne faites pas de tests en dur dans le code pour moduler vos prix.

Le client souhaiterait que les réservations donnent lieu à une confirmation par email.

Pour satisfaire le porteur du projet, vous devrez démontrer votre capacité à gérer des réservations simultanées.

Afin de s'inscrire dans le nouveau plan d'industrialisation de la mise en production des sites et applications de votre entreprise, votre responsable souhaite que vous mettiez en place, pour ce projet, un POC qui permettra d'automatiser la mise en production des sites et applications.

Votre chef d'équipe a déjà validé les choix techniques :
* Docker
* GitLab, GitLab-CI
* Ansible

Vous devrez mettre en place un cluster Docker Swarm multi-tenant et multi-environnement (preprod et prod).

A terme, vous devriez être capables, à partir d'un commit poussé dans une branche précise, de déclencher le pipeline d'intégration et déploiement continu.

Afin de pouvoir bénéficier au mieux de cette infrastructure, votre responsable vous impose également de concevoir votre API en "microservices". Il vous laisse la liberté de choisir les technologies que vous souhaitez mettre en oeuvre, mais vous devrez être en mesure de justifier vos choix. Un schéma technique de l'architecture de votre application vous sera demandé.

Votre responsable attend également que vous trouviez des solutions à :

* La répartition des fonctionnalités en service
* La collecte de logs d'exécution, les logs devront pouvoir être redirigés vers un serveur de traitement des logs
* La mise en place d'une documentation (RAML, SWAGGER, blueprint, ...)
* La mise en place de tests unitaires dans tous les dépôts de votre application

Outils / langages / technologies utilisées
==========================================
* Docker
* Ansible
* GitLab et GitLab-CI
* Langage libre

Mise en oeuvre
==============
* Vous devrez mettre en place un système de réservation sur le thème de l'Hôtellerie
* Vous devrez concevoir votre système selon une architecture de "microservices" que vous devrez détailler dans un schéma technique
* Vous aurez la responsabilité de choisir les technologies que vous allez utiliser pour l'application. Cependant, vous devrez être en mesure de justifier vos choix
* Vous devrez mettre en place les cycles d'intégration et de déploiement continus de votre application via GitLab-CI. Les runners GitLab-CI seront des conteneurs Docker. Tous les tests d'intégration se feront dans des conteneurs
* Le déploiement se fera via un playbook Ansible, qui sera exécuté par GitLab-CI sur l'une ou les 3 VM mises à disposition
* Des tests fonctionnels devront valider le déploiement et le fonctionnement de l'application Attention


.. note::

   Pour ce projet, *aucun front* développé par vous ne vous sera demandé, la correction se fera via des requêtes exécutées par défaut sur POSTMAN ou par un outil plus adapté (type documentation, ...) que vous aurez préparé.
