# YOU REVIEW 

# CURRENTLY UNDER MAINTENANCE 🚧

use the app here : https://youreview.streamlit.app

La question au coeur de ce projet est : 

**Comment valoriser les retours clients via l’analyse automatisé des commentaires You Tube ?**

Comme pour toutes les entreprises, les feedbacks permettent d’avoir des éléments d’amélioration de l’expérience client sur un produit ou un service. Ainsi, on sait pourquoi le client est satisfait ou non et on peut arbitrer entre poursuivre la vente du produit / service en priorisant les améliorations ou simplement stopper la vente. De la même manière, un influenceur You Tube utilise les indicateurs à sa disposition pour savoir si son contenu est aimé, vu (par ses abonnés, des spectateurs occasionnels …), combien de temps ses vidéos sont regardées, l’âge et le genre des spectateurs, les autres chaînes qu’ils regardent …. Autant d’informations permettant de dresser le profil de ses spectateurs et de savoir ce qu’ils apprécient. Les informations présentes dans les commentaires ont donc tout à fait leur place au sein de ces indicateurs.
Par conséquent, notre objectif est de mettre en place une infrastructure d’extraction, de traitement et d’analyse automatisée des commentaires You Tube relatifs à une vidéo donnée. Puis de rendre les résultats disponibles et accessibles via une application pour le client.

Notons qu'il existe déjà des outils permettant aux créateurs de contenus d'analyser l’engagement ou leur influence.

**Enjeux et périmètre**

Les enjeux de ce projet sont dans un premier temps de valoriser les retours « clients ». En effet, les commentaires sont des feedbacks qui révèlent les clés, les leviers de la satisfaction « client » et permettant d’aligner le contenu avec les attentes des clients. De manière plus large, cela permet d’améliorer la connaissance de sa communauté et donc d’orienter, de faire évoluer le contenu et de mieux choisir les partenariats. Etant donné que le métier d'influenceur est d'avantage un métier de passion, il s'agit surtout ici d'être plus à l'écoute de sa communauté, d'y puiser l'inspiration et de savoir le contenu est toujours aligné avec l'identité et les centres d'intérêt de sa communauté, plutôt que de faire des choix purement stratégiques et calculés.

Dans un second temps, le flux de feedbacks étant continu et important, il s’agit de pouvoir mettre en place un processus de traitement et d’analyse scalable avec des mises à jour automatisées. 

Au-delà des enjeux stratégiques et opérationnels, il y a également des enjeux réglementaires et éthiques. Les commentaires postés sur les réseaux sociaux étant des données personnelles, leur traitement doit « respecter la loi Informatique et Libertés et le règlement général sur la protection des données personnelles (RGPD) » [source](https://www.cnil.fr/fr/communication-politique-quelles-regles-pour-la-collecte-de-donnees-sur-les-reseaux-sociaux) et « être loyal et licite ». En d’autres termes, l’analyse doit se faire selon une base légale qui l’autorise, traiter des données personnelles sans base légale est interdit. De plus, conformément aux règles RGPD sur la confidentialité / l’anonymat, l’analyse des commentaires doit se faire indépendamment de l’identité de son émetteur. Certains commentaires pourraient être qualifiés de données sensibles car il est possible de déterminer l’orientation sexuelle, l’opinion politique, l’origine ethnique ou l’état de santé d’une personne, d’où la nécessité d’anonymiser pour rendre impossible le profilage des personnes.

L’utilisation de l’IA est également réglementée, en fonction de son niveau de risque. Si le risque est trop élevé et donc porte atteinte aux droits fondamentaux, son utilisation est interdite. En fonction du niveau de risque, la réglementation diffère, il est donc essentiel d’identifier le niveau de risque associé au projet pour adopter la bonne approche. 

Un autre point de vigilance concerne l’une des parties prenantes, You Tube / Google en tant fournisseur de données. L’ensemble de notre projet repose sur l’API (application programming interface) de You Tube et notre capacité à récupérer d’analyser ces données. Nous sommes donc soumis aux règles d’accessibilités et d’utilisation de ces données. Les principaux risques sont la fermeture de l’API, la fin de son accès gratuit, les quotas d’extraction et les mises à jour de l’API. 

Ainsi, le périmètre du projet couvre l’extraction, le traitement, l’analyse et la mise à jour des analyses de commentaires français.
Il est exclu du périmètre l’analyse croisée avec les indicateurs de You Tube car il n’y a pas d’intégration prévu avec la plateforme. De plus, le projet couvre uniquement l’analyse des commentaires français (dans la limite de 200 commentaires minimum) et n’intègre donc pas l’analyse pour les autres langues. L’analyse du contenu de la vidéo est également exclue et l’interface client n’intégrera pas de chatbot. En définitive, notre projet s’inscrit dans un cadre réglementaire régit par le RGPD, l’IA Act et les règles d’accès et d’utilisation de l’API de You tube.
