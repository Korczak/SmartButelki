import xml.etree.ElementTree as ET
import os
from glob import glob

XML_PATH = './dataset/train_annotations_voc/'
XML_BASE_DIR = 'train_annotations_voc/'
CLASSES_PATH = './class_names/butelka_classes.txt'
TXT_PATH = './dataset/train_annotations/butelka.txt'


'''loads the classes'''
def get_classes(classes_path):
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def get_files(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            yield from get_files(fullPath)
        else:
            yield fullPath
                


classes = get_classes(CLASSES_PATH)
assert len(classes) > 0, 'no class names detected!'
print(f'num classes: {len(classes)}')

# output file
list_file = open(TXT_PATH, 'w')

for path in get_files(XML_PATH):
    in_file = open(path)
    fullpath_to_file = path.split(XML_BASE_DIR)[1]
    print(fullpath_to_file)
    # Parse .xml file
    tree = ET.parse(in_file)
    root = tree.getroot()
    # Write object information to .txt file
    file_name = root.find('filename').text
    print(file_name)
    list_file.write(fullpath_to_file.replace("\\", "/").replace('.xml', '.JPG'))
    for obj in root.iter('object'):
        cls = obj.find('name').text 
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    list_file.write('\n')
list_file.close()
