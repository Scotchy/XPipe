from models import Folder

def get_folder(path):
    root = Folder.objects.get(parent_folder=None)
    if path in ["/", ""]:
        return root

    splitted_path = path.split("/")
    folder = root
    for f in splitted_path[1:]:
        folder = filter(lambda x: x.name == f, folder.children_folders).__next__()

    return folder

def folder_exists(path):
    try:
        get_folder(path)
        return True
    except:
        return False