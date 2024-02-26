import unreal

# Define el nombre de la carpeta
folder_name = "/Game/Maps"

# Crea la carpeta
if not unreal.EditorAssetLibrary.does_directory_exist(folder_name):
    unreal.EditorAssetLibrary.make_directory(folder_name)
    print(f"La carpeta '{folder_name}' ha sido creada.")
else:
    print(f"La carpeta '{folder_name}' ya existe.")
