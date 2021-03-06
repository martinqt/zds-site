============================
Eléments spécifiques au site
============================

Les boîtes modales
==================

Une boîte modale est une pseudo-fenêtre qui s'affiche au clique de certains boutons. Elle a pour but de faire confirmer un choix à l'utilisateur ou de permettre à celui-ci de remplir un formulaire.

.. figure:: ../images/design/boite-modale_mp.png
   :align: center

   La boîte modale pour ajouter un participant à un message privé

Une boîte modale est un élément HTML avec la classe CSS ``modal``. Mais ce ne serait pas drôle s'il n'y avait pas des
spécificités suivant les cas d'utilisation !

Cas courant : quand c'est un formulaire
---------------------------------------

On utilise souvent les boîtes modales avec un formulaire que ce soit pour confirmer une action (par exemple,
une suppression) ou pour demander à l'utilisateur de remplir des champs de texte (par exemple, ajout de nouveaux
participants à une discussion ou nouveaux auteurs à un tutoriel) !

Il arrive souvent d'avoir donc ceci :

.. sourcecode:: html

   <form action="{{ url }}" method="post" id="une-ancre" class="modal">
       Voici un formulaire !

       <textarea>Voici un champ de texte...</textarea>

       <input type="submit">Voici un bouton</input>
   </form>

On a ici un bouton pour envoyer le formulaire. Mais comment l'utilisateur ferme la boîte modale ?
Il peut cliquer en-dehors de la boîte ou bien presser la touche "Échape", mais il y a plus simple.
En effet, un bouton "Annuler" est automatiquement ajouté pour que l'utilisateur puisse fermer la
boîte modale très simplement !

Cas particulier : quand ce n'est pas un formulaire
--------------------------------------------------

On peut se dire qu'avec ce code tout va bien fonctionner :

.. sourcecode:: html

   <div id="une-ancre" class="modal">
       Une super boîte modale !
   </div>

Malheureusement, non : le bouton de fermeture ne prend que la moitié de la place ! Ce problème se résout
très rapidement en ajoutant l'attribut ``data-modal-close="Fermez-moi !"`` à le boîte modale. Le texte
de l'attribut (ici ``Fermez-moi !``) deviendra le texte du bouton.

.. sourcecode:: html

   <div id="une-ancre" class="modal" data-modal-close="Fermez-moi !">
       Une super boîte modale !
   </div>

Créer le lien
-------------

La création du lien affichant la boîte modale est tout aussi simple : il suffit de mettre une ancre correspondant à l'``id`` de la boîte modale ainsi que la classe ``open-modal`` :

.. sourcecode:: html

   <a href="#une-ancre" class="open-modal">
       Un super lien !
   </a>

.. Attention::

   Attention, le texte du lien sera le titre de la boîte modale.

Changer la taille de la boîte
-----------------------------

Par défaut, la boîte modale prend toute la place possible sur l'écran (avec quand même une petite marge). Pour
spécifier la taille, il faut simplement ajouter une classe CSS (du plus petit au plus grand) : ``modal-small``,
``modal-medium`` ou ``modal-big``.


La lecture zen
==============

La lecture zen est un mode d'affichage des tutoriels et des articles permettant à l'utilisateur de se concentrer sur sa lecture.
Elle cache l'en-tête et la barre latérale de la page pour ne laisser que le contenu principal.

.. figure:: ../images/design/lecture-zen_off.png
   :align: center

   Un tutoriel sans lecture zen


.. figure:: ../images/design/lecture-zen_on.png
   :align: center

   Ce même tutoriel avec lecture zen

Pour avoir la lecture zen, il suffit d'inclure le bouton "Lecture zen" là où vous voulez :

.. sourcecode:: html

   {% include "misc/zen_button.part.html" %}

Au clic du bouton, le Javascript se chargera de mettre ou d'enlever la classe ``zen-mode`` à ``.content-container``.

Les *items* représentant les contenus et les derniers sujets
============================================================

Les contenus (articles et tutoriels) ainsi que les derniers sujets de la page d'accueil sont représentés dans des *items*.

.. figure:: ../images/design/item-contenu.png
   :align: center

   En voici un exemple

Importation dans un gabarit
---------------------------

Article
~~~~~~~

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_article.part.html" %}

Vous pouvez passer trois arguments aux fichiers :

- ``public_article`` (ou ``article`` s'il n'est pas publié) : un objet de type ``PublishableContent``. **Obligatoire**
- ``show_description`` : un booléen pour afficher ou non la description de l'article. *Est à False par défaut.*
- ``type`` : doit avoir pour valeur ``"beta"`` pour afficher la version béta. *Est vide par défaut.*

Par exemple, pour afficher un article publié avec sa description :

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_article.part.html" with public_article=article show_description=True %}

Ou sinon, pour afficher un article en béta sans description :

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_article.part.html" with article=article type="beta" %}


Tutoriel
~~~~~~~~

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_tutoriel.part.html" %}

Vous pouvez passer quatre arguments aux fichiers :

- ``public_tutorial`` (ou ``tutorial`` s'il n'est pas publié) : un objet de type ``PublishableContent``. **Obligatoire**
- ``show_description`` : un booléen pour afficher ou non la description du tutoriel. *Est par défaut à False.*
- ``type`` : doit avoir pour valeur ``"beta"`` pour afficher la version béta. *Est vide par défaut.*
- ``item_class`` : ajoute des classes au tutoriel (par exemple, la classe "mini" pour afficher le tutoriel en plus petit). *Est vide par défaut.*

Par exemple, pour afficher un tutoriel publié avec sa description :

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_tutoriel.part.html" with public_tutorial=tutorial show_description=True %}

Ou sinon, pour afficher un tutoriel en béta sans description et en taille réduite :

.. sourcecode:: html

   {% include "tutorialv2/includes/content_item_type_tutoriel.part.html" with tutorial=tutorial type="beta" item_class="mini" %}


.. figure:: ../images/design/item-contenu-mini.png
   :align: center

   Voici deux tutoriels en taille réduite

Sujet
~~~~~

.. sourcecode:: html

   {% include "forum/includes/topic_item.part.html" %}

Vous devez passer en argument ``topic`` qui est un objet de type ``Topic``.

Faire une liste d'*items*
-------------------------

Si vous voulez faire une liste de tutoriels, il faut les regrouper dans une ``<div class="content-item-list"></div>``.

.. sourcecode:: html

   <div class="content-item-list">
       <!-- Mes tutoriels -->
   </div>

Ils sont répartis une ou des colonnes (une seule sur mobile jusqu'à quatre sur un écran haute définition).

Malheureusement, si les tutoriels sont affichés sur deux colonnes et qu'ils sont en nombre impair, le dernier tutoriel va prendre la même place que deux. Un exemple vaut mille mots :

.. sourcecode:: bash

   |   Tutoriel   | |   Tutoriel   |
   |           Tutoriel            |

.. figure:: ../images/design/item-contenu-sans-fill.png
   :align: center

   Voici trois tutoriels sur deux colonnes avec le problème

Pour y remédier, il faut toujours mettre à la fin de votre liste d'articles trois ``<div class="fill"></div>``. Cela donne au final ceci :


.. sourcecode:: html

   <div class="content-item-list">
       <!-- Mes tutoriels -->
       <div class="fill"></div>
       <div class="fill"></div>
       <div class="fill"></div>
   </div>

.. figure:: ../images/design/item-contenu-avec-fill.png
   :align: center

   Voici trois tutoriels sur deux colonnes sans le problème

(Pour l'explication technique, c'est dû à l'utilisation de *flexbox*.)
