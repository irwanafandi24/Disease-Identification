from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
# from flask_restful import Api, Resource
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import pandas as pd

# from tensorflow import tf

app = Flask(__name__, template_folder="client")
model = load_model("model/leaf_model.h5")
model.make_predict_function()
df_info = pd.read_csv("info_penyakit.csv")


def predict_label(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = np.vstack([img])
    classes = model.predict(img, batch_size=6)
    if int(classes[0][0]) == 1:
        return 4
    elif int(classes[0][1]) == 1:
        return 2
    elif int(classes[0][2]) == 1:
        return 3

def get_disease_info(disease_id):
    data_info = df_info[df_info.id == disease_id]
    disease = data_info.penyakit.values[0]
    disease_info = data_info.informasi.values[0]
    disease_treatment = data_info.treatment.values[0]
    return disease, disease_info, disease_treatment


@app.route("/", methods=['GET'])
def main():
    return render_template("app.html")


@app.route("/list_data", methods=['GET'])
def get_list():
    return {'name': 'irwan'}


@app.route("/leaf_analysis", methods=["POST"])
def leaf_analysis():
    landArea = int(request.form['landArea'])
    minPrice = int(request.form['minimumPrice'])
    maxPrice = int(request.form['maximumPrice'])

    leafImg = request.files['leafImage']
    img_path = "static/" + leafImg.filename
    leafImg.save(img_path)
    disease_id = predict_label(img_path)

    disease, disease_info, disease_treatment = get_disease_info(disease_id)


    response = jsonify({
        'disease_result': disease,
        'disease_info': disease_info,
        'treatment_info': disease_treatment,
        'recommendation': [
            {"pesticide": "pesticede", "price": 10000, "need": 5, "store": "store A", "url_store": "https://www.youtube.com/"},
            {"pesticide": "pesticede", "price": 10000, "need": 5, "store": "store A", "url_store": "https://www.youtube.com/"},
            {"pesticide": "pesticede", "price": 10000, "need": 5, "store": "store A", "url_store": "https://www.youtube.com/"}
        ]
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)
    return response


if __name__ == '__main__':
    app.run(debug=True)
