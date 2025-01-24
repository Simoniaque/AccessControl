# 1. Prérequis
- Python : Assurez-vous que Python est installé sur votre machine.
Pour vérifier la version de Python :
```
  python --version
```
Si Python n'est pas installé, téléchargez-le depuis le site officiel [python.org](https://www.python.org/downloads/) ou depuis le microsoft store.

- pip : Un gestionnaire de paquets Python. Il est généralement inclus avec Python. Pour vérifier :
```
  pip --version
```
# 2. Installation des dépendances
- Créez un environnement virtuel (recommandé pour isoler les dépendances) :
```
  python -m venv venv
```
Activez l'environnement virtuel :
```
  Activate.ps1
```

- Installez les dépendances à partir du fichier requirements.txt :

Exécutez la commande suivante :
```
pip install -r requirements.txt
```
# 3. Problèmes spécifiques aux paquets
Si les dependances ne s'installe pas correcetement, faites une par une. Certains paquets, comme face_recognition, peuvent nécessiter des outils supplémentaires. Voici les étapes spécifiques :

- Installation de dlib :

Pour installer dlib, vous avez besoin des Visual Studio Build Tools.
Téléchargez-les depuis [Microsoft Visual Studio](https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/).
Pendant l'installation, sélectionnez :
Développement pour le bureau avec C++

![image](https://github.com/user-attachments/assets/86a93193-5a45-4e4e-abfd-68b7db4002c9)

Redémarrez votre ordinateur une fois l'installation terminée.

- Installation de CMake :
 ```
 pip install cmake
```

Et enfin

```
pip install dlib
```

