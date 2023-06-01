# ocfp12_Metro_Quentin
OCfp12 - Développez une architecture back-end sécurisée en utilisant Django ORM

## LIRE AVEC ATTENTION ET EN ENTIER AVANT DE TENTER QUOI QUE CE SOIT:
Cette application est un CRM permettant de gérer des clients et leurs contrats et évènements. Cette application prend la forme d'une API et d'un site d'administration.

## Prérequis, installation, déploiement:
- Pour télécharger la dernière version, cliquer ci-dessus: Code -> Download ZIP
- apres avoir téléchargé et extraire le ZIP dans un nouveau dossier
- assurer d'avoir une version à jour de 'python'
- Ouvrir un terminal de commandes et placez-vous dans le dossier du projet
- lancer l'environnement virtuel `.\env\Scripts\activate`
- lancer la commande `pip install -r requirements.txt` afin d'installer les packages nécessaire
- lancer la commande `python .\SoftDesk_Project_API\manage.py migrate` pour initialiser la base de données
- puis la commande `python .\SoftDesk_Project_API\manage.py runserver` pour lancer le serveur.


## Utilisation
Vous pouvez accéder à cette API via des logiciels tels que POSTMAN ou via des request HTTP.
L'application est également configurée pour une utilisation sur le site admin `url/admin/`.
Divers utilisateurs sont configurés pour pouvoir test l'application (Ne pas garder en cas de production)
admin
    super_toto super_mdp
manager
    managerman1 mdp012345
    managerman2 mdp012345
vendeur
    salesman1 mdp012345
    salesman2 mdp012345
    salesman3 mdp012345
support
    supportman1 mdp012345
    supportman2 mdp012345
    supportman3 mdp012345