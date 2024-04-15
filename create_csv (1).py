# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for object_elem in root.findall('object'):
            class_name = object_elem.find('name').text
            xmin = int(object_elem.find('bndbox/xmin').text)
            xmax = int(object_elem.find('bndbox/xmax').text)
            ymin = int(object_elem.find('bndbox/ymin').text)
            ymax = int(object_elem.find('bndbox/ymax').text)
            filename = root.find('filename').text
            width = int(root.find('size/width').text)
            height = int(root.find('size/height').text)
            
            value = (filename, width, height, class_name, xmin, ymin, xmax, ymax)
            xml_list.append(value)
            
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train', 'validation']:
        image_path = os.path.join(os.getcwd(), 'images', folder)
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(os.path.join('images', f'{folder}_labels.csv'), index=None)
        print(f'Successfully converted xml to csv for {folder}.')

if __name__ == "__main__":
    main()

