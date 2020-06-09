import os
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
import glob
import pickle
from datetime import datetime
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import codecs, json 
import base64
import time
import json
app = Flask(__name__)

with open('sku.json') as f:
    sku_data = json.load(f)

dir_path = os.path.dirname(os.path.realpath(__file__))
hostname = "http://localhost:5000/"
PORT = 5000

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
img_name = []
for feature_path in glob.glob("static/feature/*"):
    features.append(pickle.load(open(feature_path, 'rb')))
    img_paths.append('static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')
    img_name.append(os.path.splitext(os.path.basename(feature_path))[0])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static\\uploaded\\" +  str(int(round(time.time() * 1000))) + "_" + file.filename
        img.save(uploaded_img_path)

        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # Do search
        ids = np.argsort(dists)[:8] # Top 8 results

        for id in ids:
            if (0 <= dists[id] <= 1):
                scores = {(dists[id], img_paths[id]) for id in ids}

        return render_template('index.html', query_path=uploaded_img_path, scores=scores)
        
    else:
        return render_template('index.html')


@app.route('/img/<string:ip>')
def img(ip):
    image = "static/img/"+ip
    return send_file(image, mimetype='image/gif')


@app.route('/recognize', methods=['POST'])
def post_example():
    print(request)
    if not request.headers.get('Content-type') is None:
        if(request.headers.get('Content-type').split(';')[0] == 'multipart/form-data'):
            if 'image' in request.files.keys():
                print("inside get image statement")
                file = request.files['image']
                img = Image.open(file.stream)  # PIL image
                uploaded_img_path = "static\\uploaded\\" +  str(int(round(time.time() * 1000))) + "_" + file.filename
                img.save(uploaded_img_path)
                #print (img)
                query = fe.extract(img)
                dists = np.linalg.norm(features - query, axis=1)  # Do search
                ids = np.argsort(dists)[:8] # Top 8 results
                data ={ "details" : []}
                def add_info(info):
                    data["details"].append(info)
                for id in ids:
                    info = {}
                    info["score"]=str(dists[id])
                    info["path"]=img_paths[id]
                    info["name"]=img_name[id]
                    add_info(info)
                return jsonify(data)
            else:
                return jsonify(get_status_code("Invalid body", "Please provide valid format for Image 2")), 415

        elif(request.headers.get('Content-type') == 'application/json'):
            if(request.data == b''):
                return jsonify(get_status_code("Invalid body", "Please provide valid format for Image")), 415
            else:
                body = request.get_json()
                if "image_string" in body.keys():
                    img_string = body['image_string']
                    # str_image = img_string.split(',')[1]
                    imgdata = base64.b64decode(img_string)
                    img = "static\\uploaded\\" +  str(int(round(time.time() * 1000))) + "image_file.jpg"
                    with open(img, 'wb') as f:
                        f.write(imgdata)

                    image=Image.open(img)
                    #print (image)
                    #return send_file(img, mimetype='image/gif')

                    query = fe.extract(image)
                    dists = np.linalg.norm(features - query, axis=1)  # Do search
                    ids = np.argsort(dists)[:8] # Top 8 results
                    data ={ "details" : []}
                    # def add_info(info):
                        
                    for id in ids:
                        info = {}
                        info["score"]=str(round(dists[id], 2))
                        info["path"]=hostname + img_paths[id]
                        info["id"]= img_name[id]
                        
                        for sku in sku_data['sku']:
                            if str(sku['id']) == str(img_name[id]):
                                # print("Found SKU : ", sku)
                                info["skuName"] = sku['skuName']
                                info["skuCategory"] = sku['skuCategory']
                                info["ar"] = sku['ar']

                        data["details"].append(info)   

                    # print(data)   
                    return jsonify(data)

        else:
            return jsonify(get_status_code("Invalid header", "Please provide correct header with correct data")), 415

    else:
        return jsonify(get_status_code("Invalid Header", "Please provide valid header")), 401

def get_status_code(argument, message):
    res = {
        "error": {
            "code": argument,
            "message": message
        }
    }
    return res

if __name__=="__main__":
    app.run(host="0.0.0.0", port=PORT)
