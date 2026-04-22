import kagglehub

def descargar_imagenes():
    print("Descargando dataset : workoutexercises-images (Imágenes)...")
    path3 = kagglehub.dataset_download("hasyimabdillah/workoutexercises-images")
    print(f"✅ ¡Completado! Los archivos están en: {path3}\n")

if __name__ == "__main__":
    descargar_imagenes()
