import pandas as pd
import os
import shutil
import configparser
from tqdm import tqdm

def convert_to_yolo_format(bb,img_width,img_height):
    x_center = bb['bb_left'] + (bb['bb_width']/2)
    y_center = bb['bb_top'] + (bb['bb_height']/2)
    
    #normalize
    x_center /= img_width
    y_center /= img_height
    bb_width_normalize = bb['bb_width']/img_width
    bb_height_normalize = bb['bb_height']/img_height
    x_center = max(min(x_center,1),0)
    y_center = max(min(y_center,1),0)
    bb_width_normalize = max(min(bb_width_normalize,1),0)
    bb_height_normalize = max(min(bb_height_normalize,1),0)
    
    return x_center, y_center, bb_width_normalize,bb_height_normalize

def process_folder(folder_path):
    config = configparser.ConfigParser()
    config.read(os.path.join(folder_path,'seqinfo.ini'))
    img_width = int(config['Sequence']['imWidth'])
    img_height = int(config['Sequence']['imHeight'])
    
    gt_path = os.path.join(folder_path,'det/det.txt')
    gt_data = pd.read_csv(gt_path,header = None, names =['frame','id','bb_left','bb_top','bb_width','bb_height',
                                                        'conf','class','visibility'])
    label_folder = os.path.join(folder_path,'labels')
    os.makedirs(label_folder,exist_ok = True)
    
    for frame_number in gt_data['frame'].unique():
        frame_data = gt_data[gt_data['frame']==frame_number]
        label_file = os.path.join(label_folder,f'{frame_number:06}.txt')
        
        with open(label_file,'w') as file:
            for _,row in frame_data.iterrows():
                yolo_bb = convert_to_yolo_format(row,img_width,img_height )
                file.write(f'0 {yolo_bb[0]} {yolo_bb[1]} {yolo_bb[2]} {yolo_bb[3]}\n')
                            
def process_all_folders(base_directory):
    for folder_name in tqdm(os.listdir(base_directory)):
        folder_path = os.path.join(base_directory,folder_name)
        if 'FRCNN' not in folder_name:
            shutil.rmtree(folder_path)
            continue
        if os.path.isdir(folder_path):
            process_folder(folder_path)

process_all_folders("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\MOT17\\train")
process_all_folders("C:\\Users\\dhocking\\Documents\\hocmaycuoiky\\MOT17\\MOT17\\test")