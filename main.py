from PIL import Image
from keras.models import load_model
from imageio import imread
import numpy as np


def maxInDict(modelMap, file):
    max = 0
    maxClass = 'Default'

    for key, value in modelMap.items():
        if(value>max):
            max = value
            maxClass = key

    model=load_model('Cucumber_Lemon.h5')
    img = Image.open(file)
    new_img = img.resize((64, 64))
    new_img.save("car_resized.jpg", "JPEG", optimize=True)

    arr = imread('car_resized.jpg')
    np.save(str('car_resized'), arr)

    data = np.load('car_resized.npy')
    data = np.reshape(data, [1, 64, 64, 3])

    pred=model.predict_classes(data)
    if(pred==0):
        return 'Cucumber'
    else:
        return 'Lemon'
    return maxClass

def firstWord(str):
    x=str.find('_')
    print (str[0:x])


def predict(file):
    img = Image.open(file)
    new_img = img.resize((64, 64))
    new_img.save("car_resized.jpg", "JPEG", optimize=True)

    arr = imread('car_resized.jpg')
    np.save(str('car_resized'), arr)

    data = np.load('car_resized.npy')
    data = np.reshape(data, [1, 64, 64, 3])
    print(data.shape)

    model1 = load_model('Banana_Lemon.h5')
    model2 = load_model('Banana_Cucumber.h5')
    model3 = load_model('Cucumber_Lemon.h5')
    banana = 0
    lemon = 0
    cucumber = 0
    modelMap = {'Banana': banana, 'Lemon': lemon, 'Cucumber': cucumber}
    if (model1.predict_classes(data) == 0):
        modelMap['Banana'] = modelMap['Banana'] + 1
        banana += 1
    if (model1.predict_classes(data) == 1):
        modelMap['Lemon'] = modelMap['Lemon'] + 1
        lemon += 1

    if (model2.predict_classes(data) == 0):
        modelMap['Banana'] = modelMap['Banana'] + 1
        banana += 1
    if (model2.predict_classes(data) == 1):
        modelMap['Cucumber'] = modelMap['Cucumber'] + 1
        cucumber += 1

    if (model3.predict_classes(data) == 0):
        modelMap['Cucumber'] = modelMap['Cucumber'] + 1
        cucumber += 1
    if (model3.predict_classes(data) == 1):
        modelMap['Lemon'] = modelMap['Lemon'] + 1
        lemon += 1

    return (maxInDict(modelMap, file))