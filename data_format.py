import os
import shutil
import yaml
import tqdm

def rename_and_move(src_folder,dst_folder,
                folder_name,file_extension):
    for filenames in os.listdir(src_folder):
        if filenames.endswith(file_extension):
            new_filenames = f'{folder_name}_{filenames}'
            shutil.move(os.path.join(src_folder,filenames),
                        os.path.join(dst_folder,new_filenames))

def move_file_and_rename_folderase_directory(base_directory):
    image_dirs = os.path.join(base_directory,'images')
    label_dirs = os.path.join(base_directory,'labels')

    os.makedirs(image_dirs,exist_ok=True)
    os.makedirs(label_dirs,exist_ok=True)

    for folder_name in os.listdir(base_directory):
        if folder_name in ['images','labels']:
            continue
        folder_path = os.path.join(base_directory,folder_name)

        rename_and_move(os.path.join(folder_path,'img1'),
                        image_dirs,
                        folder_name,'.jpg')
        rename_and_move(os.path.join(folder_path,'labels'),
                        label_dirs,
                        folder_name,'.txt')
def delete_subfolder(base_directory):
    for subfolder in os.listdir(base_directory):
        subfolder_path = os.path.join(base_directory,subfolder)
        if os.path.isdir(subfolder_path) is True and subfolder not in ['images','labels']:
            shutil.rmtree(subfolder_path)
            continue

move_file_and_rename_folderase_directory("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\MOT17\\train")
move_file_and_rename_folderase_directory("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\MOT17\\test")
delete_subfolder("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\MOT17\\train")
delete_subfolder("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\MOT17\\test")


            
