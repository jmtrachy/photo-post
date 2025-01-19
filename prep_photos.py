import os
from dataclasses import dataclass

__FINAL_NAME = 'finals'
__JPG_NAME = 'JPGs'
__NEF_NAME = 'NEFs'
__PHOTOS_BASE_SOCCER_DIRECTORY = '/Users/james/Desktop/Photos/Soccer'
__PHOTOS_MTA_2024_5_DIR = 'MTA_2024_5'


@dataclass
class FolderStruct:
    base_dir: str
    final_dir: str
    jpg_dir: str
    nef_dir: str


def get_directories(dir_name: str) -> FolderStruct:
    nef_dir = os.path.join(dir_name, __NEF_NAME)
    if not os.path.exists(nef_dir):
        os.mkdir(nef_dir)

    jpg_dir = os.path.join(dir_name, __JPG_NAME)
    if not os.path.exists(jpg_dir):
        os.mkdir(jpg_dir)

    final_dir = os.path.join(dir_name, __FINAL_NAME)
    if not os.path.exists(final_dir):
        os.mkdir(final_dir)

    return FolderStruct(
        base_dir=dir_name,
        jpg_dir=jpg_dir,
        final_dir=final_dir,
        nef_dir=nef_dir,
    )


def prep_files_for_post(dir_name: str):
    folder_struct = get_directories(dir_name)

    all_nefs = {
        file_name for file_name in os.listdir(folder_struct.base_dir)
        if file_name.endswith('.NEF')
    }
    for file_name in all_nefs:
        current_name = os.path.join(folder_struct.base_dir, file_name)
        new_name = os.path.join(folder_struct.nef_dir, file_name)
        print(f'moving {current_name} to {new_name}')
        os.rename(current_name, new_name)

    all_jpgs = {
        file_name for file_name in os.listdir(folder_struct.base_dir)
        if file_name.endswith('.JPG')
    }
    for file_name in all_jpgs:
        current_name = os.path.join(folder_struct.base_dir, file_name)
        new_name = os.path.join(folder_struct.jpg_dir, file_name)
        print(f'moving {current_name} to {new_name}')
        os.rename(current_name, new_name)


def delete_nefs(dir_name: str):
    folder_struct = get_directories(dir_name)

    all_jpgs = {
        file_name.split('.')[0]
        for file_name in os.listdir(folder_struct.jpg_dir)
        if file_name.endswith('.JPG')
    }

    all_nefs = [
        file_name for file_name in os.listdir(folder_struct.nef_dir)
        if file_name.endswith('.NEF')
    ]
    all_nefs.sort()

    for nef_name in all_nefs:
        if nef_name.split('.')[0] not in all_jpgs:
            file_to_del = os.path.join(folder_struct.nef_dir, nef_name)
            print(f'about to remove {file_to_del}')
            os.remove(file_to_del)


if __name__ == '__main__':
    game_dir = input('Enter the name of the game directory: ') or 'MTA_vs_TCRush'
    photo_dir = os.path.join(__PHOTOS_BASE_SOCCER_DIRECTORY, __PHOTOS_MTA_2024_5_DIR, game_dir)

    proceed = input(f'Would you like to proceed on {photo_dir}? [Y] ') or 'Y'
    if proceed == 'Y':
        print('proceeding...')
    else:
        print('exiting without operating')
        exit(0)

    prep_or_del = input('Prep (prep) or Delete NEFs (del)? [prep] ') or 'prep'
    if prep_or_del == 'prep':
        prep_files_for_post(dir_name=photo_dir)
    elif prep_or_del == 'del':
        print('deleting')
        delete_nefs(dir_name=photo_dir)

