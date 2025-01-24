1. Prérequis
- Python : Assurez-vous que Python est installé sur votre machine.
Pour vérifier la version de Python :
```
  python --version
```
Si Python n'est pas installé, téléchargez-le depuis le site officiel "python.org" ou depuis le microsoft store.

- pip : Un gestionnaire de paquets Python. Il est généralement inclus avec Python. Pour vérifier :
  pip --version

2. Installation des dépendances
- Créez un environnement virtuel (recommandé pour isoler les dépendances) :
  python -m venv venv
Activez l'environnement virtuel :
  Activate.ps1

- Installez les dépendances à partir du fichier requirements.txt :

Exécutez la commande suivante :
pip install -r requirements.txt

3. Problèmes spécifiques aux paquets
Certains paquets, comme dlib et face_recognition, peuvent nécessiter des outils supplémentaires pour s'installer correctement. Voici les étapes spécifiques :

- Installation de CMake :
 pip install cmake

- Installation de dlib :
pip install dlib
