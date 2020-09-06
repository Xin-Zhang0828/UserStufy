from flask import Flask, request, render_template
import json, io
import csv
from random import shuffle
import time
import numpy as np
import pdb
#import torch

app = Flask(__name__)

example_json = json.load(io.open('static/data/JSONS/Example.json', encoding = 'utf-8'))['images'];
shuffle(example_json)
#pdb.set_trace()
exp_1_json = json.load(io.open('static/data/JSONS/Exp_1.json', encoding = 'utf-8'))['images']
shuffle(exp_1_json);
exp_1_dummy = json.load(io.open('static/data/JSONS/Exp_1_dummy.json', encoding = 'utf-8'))['images']
#pdb.set_trace()



json_names = ['Examples', 'Set 1 Dummy', 'Set 1']

#pdb.set_trace()
json_count = 0
img_count = 0
count_threshold_list = [3, 3, 54]
annotations = []
current_time = time.time()

def reset_timer():
    global current_time
    current_time = time.time()

def get_response_time():
    global current_time
    return time.time() - current_time

def show_stimuli(json, threshold):
    global img_count, json_count
    print('%d/%d, %d'%(img_count, threshold, json_count))
    if img_count < threshold:
        return json[img_count]
    else:
        json_count += 1
        img_count = 0
        return None


#import pdb;pdb.set_trace()
@app.route("/")
def hello():
    global exp_1_json, list_jsons

    list_jsons = [example_json, exp_1_dummy, exp_1_json]
    print("Shuffling Data")
    shuffle(exp_1_json);
    print(exp_1_json)
    #shuffle(exp_2_json);
    #shuffle(exp_3_json);
    global json_count, annotations, img_count
    json_count = 0
    img_count = 0
    annotations = []
    return render_template('index.html')
    #display_next_exp_stimuli

@app.route("/give_directions", methods=['POST'])
def give_directions():
    global json_count, img_count
    global participant_id, expertise, experiment;
    participant_id = request.form['participant_id']
    expertise = request.form['expertise']
    #print(img_count, json_count)
    next_img = show_stimuli(list_jsons[json_count], count_threshold_list[json_count])
    #pdb.set_trace()
    return render_template('Example_Basic.html', image_0 = next_img[0], image_1 = next_img[1])


@app.route("/display_next_example_stimuli", methods=['POST'])
def display_next_example_stimuli():
    global json_count, img_count
    img_count += 1
    next_img = show_stimuli(list_jsons[json_count], count_threshold_list[json_count])
    if next_img:
        #pdb.set_trace()
        return render_template('Example_Basic.html', image_0 = next_img[0], image_1 = next_img[1])
    else:
        #print(img_count, json_count)
        return render_template('start_experiment.html')
    

    
@app.route("/start_experiment", methods=['POST'])
def start_experiment():
    global participant_id,expertise, json_count, img_count;
    #import pdb; pdb.set_trace()
    #print(img_count, json_count)
    next_img = show_stimuli(list_jsons[json_count], count_threshold_list[json_count])
    reset_timer()
    #print('Starting exp with' + next_img)
    return render_template('Exp_Basic.html', image_0 = next_img[0], image_1 = next_img[1])



@app.route("/display_next_exp_stimuli", methods=['POST'])    
def display_next_exp_stimuli():
    global participant_id,expertise, json_count, img_count;
    last_response_time = get_response_time()
    if not json_count in [0, 1]:
        #pdb.set_trace()
        better_image = request.form['better_image']
        #score_2 = request.form['score_given_2']
        #score_3 = request.form['score_given_3']

        annotations.append({'set':json_names[json_count], 'imid_1' : list_jsons[json_count][img_count][0],\
                            'imid_2' : list_jsons[json_count][img_count][1], 'which_1': better_image, 'response': last_response_time})
    #pdb.set_trace()
    img_count +=1
    next_img = show_stimuli(list_jsons[json_count], count_threshold_list[json_count])
    if next_img:
        reset_timer()
        return render_template('Exp_Basic.html', image_0 = next_img[0], image_1 = next_img[1])
    else:
        if json_count < 3:
            next_img = show_stimuli(list_jsons[json_count], count_threshold_list[json_count])
            reset_timer()
            return render_template('Exp_Basic.html', image_0 = next_img[0], image_1 = next_img[1])
        else:
            with open('Results/'+participant_id + '_' + expertise + '_' +  '.csv', 'w') as f:
                writer = csv.DictWriter(f, fieldnames = ['set', 'imid_1', 'imid_2', 'which_1', 'response'], delimiter ="#" )
                #writer.writeheader()
                writer.writerows(annotations)
            #pdb.set_trace()
            return render_template('thank_you.html')
        
        
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
#    app.run(host= 'localhost',debug = True)
     app.run(host= '0.0.0.0', port =3134, debug = True)
     