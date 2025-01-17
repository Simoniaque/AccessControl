import tkinter as tk
from tkinter import messagebox
import os
import cv2
import face_recognition

def add_student():
    student_id = entry_id.get()
    if student_id:
        capture_student_image(student_id)
        messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
    else:
        messagebox.showerror("Erreur", "Veuillez entrer un ID.")

def check_access():
    temp_image_path = "temp.jpg"  # Chemin pour l'image temporaire

    # Capture une photo avec la caméra
    camera = cv2.VideoCapture(0)
    print("Appuyez sur 's' pour capturer une image pour vérification.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erreur caméra.")
            break

        cv2.imshow("Vérification Accès", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(temp_image_path, frame)
            print(f"Image temporaire capturée pour vérification.")
            break

    camera.release()
    cv2.destroyAllWindows()

    # Vérification de l'accès
    student_id = verify_student(temp_image_path)
    if student_id:
        messagebox.showinfo("Accès autorisé", f"Étudiant {student_id} identifié.")
    else:
        messagebox.showerror("Accès refusé", "Étudiant non reconnu.")

    # Supprime l'image temporaire après vérification
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

def capture_student_image(student_id, output_dir="images/"):
    os.makedirs(output_dir, exist_ok=True)
    camera = cv2.VideoCapture(0)

    print(f"Capture de l'image pour l'étudiant {student_id}. Appuyez sur 's' pour sauvegarder.")
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erreur caméra.")
            break

        cv2.imshow("Capture Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            file_path = os.path.join(output_dir, f"{student_id}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"Image sauvegardée à {file_path}.")
            break

    camera.release()
    cv2.destroyAllWindows()

def verify_student(image_path, database_dir="images/"):
    if not os.path.exists(image_path):
        print(f"Erreur : le fichier {image_path} n'existe pas.")
        return None
    
    known_faces = []
    known_ids = []

    for file in os.listdir(database_dir):
        file_path = os.path.join(database_dir, file)
        image = face_recognition.load_image_file(file_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_faces.append(encodings[0])
            known_ids.append(file.split(".")[0])

    input_image = face_recognition.load_image_file(image_path)
    input_encodings = face_recognition.face_encodings(input_image)

    if input_encodings:
        input_encoding = input_encodings[0]
        results = face_recognition.compare_faces(known_faces, input_encoding)
        if True in results:
            match_index = results.index(True)
            return known_ids[match_index]
        else:
            print("Aucune correspondance trouvée.")
            return None
    else:
        print("Aucun visage détecté dans l'image d'entrée.")
        return None

root = tk.Tk()
root.title("Contrôle d'accès")

tk.Label(root, text="ID Étudiant").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Button(root, text="Ajouter Étudiant", command=add_student).pack()
tk.Button(root, text="Vérifier Accès", command=check_access).pack()

root.mainloop()
