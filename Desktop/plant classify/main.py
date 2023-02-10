
import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template , session
from werkzeug.utils import secure_filename
from pathlib import Path
from keras_preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pandas import Series
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix , precision_score

class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        """
        Extract a deep feature from an input image
        Args:
            img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
        Returns:
            feature (np.ndarray): deep feature with the shape=(4096, )
        """
        img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
        img = img.convert('RGB')  # Make sure img is color
        x = image.img_to_array(img)  # To np.array. Height x Width x Channel. dtype=float32
        x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
        x = preprocess_input(x)  # Subtracting avg values for each pixel
        feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
        return feature / np.linalg.norm(feature)  # Normalize


app = Flask(__name__)

# two decorators, same function
@app.route('/',methods =["GET", "POST"])
def index():
    clas =[]
    image =""
    pat=""
    if request.method == "POST":
        image = request.files.get('img', '')
        filename = secure_filename(image.filename)
        image.save("./static/images/"+filename)
        pat = "./static/images/"+filename
        clas.append(filename)
        fe = FeatureExtractor()
        features = []
        img_paths = []
        for feature_path in Path("./static/npy_image").glob("*.npy"):
            features.append(np.load(feature_path))
            img_paths.append(Path("./static/image") / (feature_path.stem + ".jpeg"))
        features = np.array(features)
        img = Image.open("./static/images/"+filename)
        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:8]  # Top 8 results
        scores = [(dists[id], img_paths[id]) for id in ids]
        im_path = scores[0][1].stem
        
        if("german" in im_path):
            clas.append("german shepard")
        elif("golden" in im_path):
            clas.append("golden retriver")
    return render_template('index.html',clas = clas)
    
if __name__ == '__main__':
    app.run(debug=True)