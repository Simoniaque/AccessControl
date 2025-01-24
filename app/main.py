import tkinter as tk
from tkinter import messagebox
import os
import cv2
import face_recognition

# Fonction pour ajouter un étudiant
def add_student():
    student_id = entry_id.get()  # Récupère l'ID de l'étudiant depuis l'interface
    student_balance = entry_balance.get()  # Récupère le solde de l'étudiant

    if student_id and student_balance:  # Vérifie que les deux champs sont remplis
        try:
            balance = float(student_balance)  # Convertit le solde en nombre flottant
            capture_student_image(student_id)  # Capture une image de l'étudiant
            save_student_to_file(student_id, balance)  # Sauvegarde dans un fichier
            messagebox.showinfo("Succès", f"Étudiant {student_id} ajouté avec un solde de {balance:.2f}.")
        except ValueError:  # Si la conversion du solde échoue
            messagebox.showerror("Erreur", "Veuillez entrer un solde valide.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer un ID et un solde.")

# Fonction pour sauvegarder un étudiant dans un fichier
def save_student_to_file(student_id, balance, file_path="students.txt"):
    with open(file_path, "a") as file:
        file.write(f"{student_id},{balance:.2f}\n")  # Ajoute l'étudiant au fichier
    print(f"Étudiant {student_id} ajouté avec un solde de {balance:.2f}.")

# Fonction pour récupérer le solde d'un étudiant depuis le fichier
def get_student_balance(student_id, file_path="students.txt"):
    if not os.path.exists(file_path):  # Vérifie si le fichier existe
        print(f"Erreur : le fichier {file_path} n'existe pas.")
        return None

    with open(file_path, "r") as file:
        for line in file:
            stored_id, balance = line.strip().split(",")  # Sépare l'ID et le solde
            if stored_id == student_id:
                return float(balance)  # Retourne le solde de l'étudiant
    return None  # Si l'étudiant n'est pas trouvé, retourne None

# Fonction pour mettre à jour le solde d'un étudiant
def update_student_balance(student_id, amount, file_path="students.txt"):
    if not os.path.exists(file_path):  # Vérifie si le fichier existe
        print(f"Erreur : le fichier {file_path} n'existe pas.")
        return False

    updated = False
    lines = []

    with open(file_path, "r") as file:
        for line in file:
            stored_id, balance = line.strip().split(",")  # Sépare l'ID et le solde
            if stored_id == student_id:
                new_balance = float(balance) + amount  # Met à jour le solde
                lines.append(f"{stored_id},{new_balance:.2f}\n")  # Ajoute la ligne modifiée
                updated = True
            else:
                lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(lines)  # Réécrit toutes les lignes dans le fichier

    return updated

# Fonction pour vérifier l'accès d'un étudiant
def check_access():
    temp_image_path = "temp.jpg"

    camera = cv2.VideoCapture(0)  # Ouvre la caméra
    print("Appuyez sur 's' pour capturer une image pour vérification.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erreur caméra.")
            break

        cv2.imshow("Vérification Accès", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):  # Appuyez sur 's' pour capturer une image
            cv2.imwrite(temp_image_path, frame)  # Sauvegarde l'image capturée
            print("Image temporaire capturée pour vérification.")
            break

    camera.release()
    cv2.destroyAllWindows()

    student_id = verify_student(temp_image_path)  # Vérifie l'identité de l'étudiant
    if student_id:
        balance = get_student_balance(student_id)  # Récupère le solde de l'étudiant
        if balance is not None:
            if balance >= 3:
                if update_student_balance(student_id, -3):  # Déduit 3€ du solde
                    new_balance = get_student_balance(student_id)  # Récupère le nouveau solde
                    messagebox.showinfo(
                        "Accès autorisé",
                        f"Étudiant {student_id} identifié.\nNouveau solde : {new_balance:.2f} €"
                    )
                else:
                    messagebox.showerror("Erreur", "Impossible de mettre à jour le solde.")
            else:
                messagebox.showerror("Accès refusé", f"Solde insuffisant ({balance:.2f} €).")
        else:
            messagebox.showerror("Erreur", f"Solde pour l'étudiant {student_id} introuvable.")
    else:
        messagebox.showerror("Accès refusé", "Étudiant non reconnu.")

    if os.path.exists(temp_image_path):  # Supprime l'image temporaire après la vérification
        os.remove(temp_image_path)

# Fonction pour capturer l'image d'un étudiant
def capture_student_image(student_id, output_dir="app/images/"):
    os.makedirs(output_dir, exist_ok=True)  # Crée le répertoire si nécessaire
    camera = cv2.VideoCapture(0)

    print(f"Capture de l'image pour l'étudiant {student_id}. Appuyez sur 's' pour sauvegarder.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erreur caméra.")
            break

        cv2.imshow("Capture Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):  # Appuyez sur 's' pour sauvegarder l'image
            file_path = os.path.join(output_dir, f"{student_id}.jpg")  # Chemin du fichier image
            cv2.imwrite(file_path, frame)  # Sauvegarde l'image
            print(f"Image sauvegardée à {file_path}.")
            break

    camera.release()
    cv2.destroyAllWindows()

# Fonction pour vérifier l'identité d'un étudiant à partir d'une image
def verify_student(image_path, database_dir="app/images/"):
    # Vérifie si le fichier d'image spécifié existe
    if not os.path.exists(image_path):
        print(f"Erreur : le fichier {image_path} n'existe pas.")
        return None  # Retourne None si l'image d'entrée n'existe pas
    
    known_faces = []  # Liste pour stocker les encodages faciaux connus 
    known_ids = []  # Liste pour stocker les identifiants des étudiants correspondants

    # Parcourt chaque fichier dans le répertoire de la base de données d'images (fichier images)
    for file in os.listdir(database_dir):
        file_path = os.path.join(database_dir, file)  # Chemin complet du fichier
        image = face_recognition.load_image_file(file_path)  # Charge l'image à partir du fichier
        encodings = face_recognition.face_encodings(image)  # Crée les encodages faciaux à partir de l'image

        # Si des encodages faciaux sont détectés dans l'image
        if encodings:
            known_faces.append(encodings[0])  # Ajoute le premier encodage trouvé à la liste known_faces
            known_ids.append(file.split(".")[0])  # Ajoute l'ID de l'étudiant (extrait du nom de l'image) à la liste known_ids

    # Charge l'image d'entrée et crée les encodages faciaux
    input_image = face_recognition.load_image_file(image_path)  # Charge l'image d'entrée
    input_encodings = face_recognition.face_encodings(input_image)  # Crée les encodages faciaux de l'image d'entrée

    # Si des encodages sont trouvés dans l'image d'entrée
    if input_encodings:
        input_encoding = input_encodings[0]  # Prend le premier encodage trouvé dans l'image d'entrée et compare avec les encodages connus
        results = face_recognition.compare_faces(known_faces, input_encoding)  # Résultat de la comparaison

        # Si une correspondance est trouvée (True dans la liste des résultats)
        if True in results:
            match_index = results.index(True)  # Trouve l'index de la première correspondance (True)
            return known_ids[match_index]  # Retourne l'ID de l'étudiant correspondant
        else:
            print("Aucune correspondance trouvée.")  # Si aucune correspondance n'est trouvée
            return None  # Retourne None si aucune correspondance n'est trouvée
    else:
        print("Aucun visage détecté dans l'image d'entrée.")  # Si aucun visage n'est détecté dans l'image d'entrée
        return None  # Retourne None si aucun visage n'est trouvé

# Interface utilisateur
root = tk.Tk()
root.title("Contrôle d'accès")

tk.Label(root, text="ID Étudiant").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Solde initial (€)").pack()
entry_balance = tk.Entry(root)
entry_balance.pack()

tk.Button(root, text="Ajouter Étudiant", command=add_student).pack()
tk.Button(root, text="Vérifier Accès", command=check_access).pack()

root.mainloop()
