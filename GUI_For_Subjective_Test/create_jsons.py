import json, io
from random import shuffle
import os
import pdb
#import str
import itertools



f_1 = io.open('static/data/JSONS/Example.json','w', encoding = 'utf-8')

f_2 = io.open('static/data/JSONS/Exp_1.json','w', encoding = 'utf-8')
# f_3 = io.open('static/data/JSONS/Exp_2.json','w', encoding = 'utf-8')
# f_4 = io.open('static/data/JSONS/Exp_3.json','w', encoding = 'utf-8')

f_5 = io.open('static/data/JSONS/Exp_1_dummy.json','w', encoding = 'utf-8')
# f_6 = io.open('static/data/JSONS/Exp_2_dummy.json','w', encoding = 'utf-8')
# f_7 = io.open('static/data/JSONS/Exp_3_dummy.json','w', encoding = 'utf-8')


def create_img_list_from_directory(dir_path, type):
    #pdb.set_trace()
    print ('Creating %s images from %s'%(type, dir_path))
    list_of_baselines = os.listdir(dir_path)
    image_lists = []
    for b in list_of_baselines:
        images = os.listdir(os.path.join(dir_path, b))
        image_lists.append([os.path.join(dir_path, b, i) for i in  images])
    #pdb.set_trace()
    img_pairs = []
    for i in range(len(image_lists) -1):
        for j in range(i+1, len(image_lists)):
            img_pairs += [*zip(image_lists[i], image_lists[j])]
    #pdb.set_trace()
    img_dict = {'Type':type,  'images':img_pairs}
    return img_dict

f_1.write(str(json.dumps(create_img_list_from_directory('static/data/', 'Examples'), ensure_ascii=False)))

f_2.write(str(json.dumps(create_img_list_from_directory('static/data/','Set_1'), ensure_ascii=False)))
#f_3.write(str(json.dumps(create_img_list_from_directory('static/data/E2/','Set_2'), ensure_ascii=False)))
#f_4.write(str(json.dumps(create_img_list_from_directory('static/data/E3/','Set_3'), ensure_ascii=False)))

f_5.write(str(json.dumps(create_img_list_from_directory('static/data/', 'Set_1_D'), ensure_ascii=False)))
#f_6.write(str(json.dumps(create_img_list_from_directory('static/data/E2_D/', 'Set_2_D'), ensure_ascii=False)))
#f_7.write(str(json.dumps(create_img_list_from_directory('static/data/E3_D/', 'Set_3_D'), ensure_ascii=False)))

