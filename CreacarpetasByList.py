import unreal

# Define los nombres de las carpetas
folders = ["/Game/Blueprints", "/Game/Blueprints/ActorComponents", "/Game/HUD", "/Game/HUD/Widgets"]

# Crea las carpetas
for folder_name in folders:
    if not unreal.EditorAssetLibrary.does_directory_exist(folder_name):
        unreal.EditorAssetLibrary.make_directory(folder_name)
        print(f"La carpeta '{folder_name}' ha sido creada.")
    else:
        print(f"La carpeta '{folder_name}' ya existe.")
