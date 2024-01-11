import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import convert_wavelength


__name_to_number={}
__number_to_name={}
__model=None

def load_saved_artifacts():
    global __name_to_number
    global __number_to_name

    print('Loading..started')

    with open('./artifacts/class_dictionary.json','r') as f:
        __name_to_number=json.load(f)
        __number_to_name={v:k for k,v in __name_to_number.items()}

    global __model
    if __model is None:
        with open('./artifacts/saved_model.pkl','rb') as f:
            __model=joblib.load(f)

    print('Loading..Done')

def get_cv2_image_from_base64(b64str):
    encoded_data=b64str.split(',')[1]
    narray=np.frombuffer(base64.b64decode(encoded_data),np.uint8)
    img=cv2.imdecode(narray,cv2.IMREAD_COLOR)
    return img


def get_cropped_images(image_path,image_b64):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img= get_cv2_image_from_base64(image_b64)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cropped_faces=[]
    for (x, y, w, h) in faces:
        gray_roi = gray[y:y + h, x:x + w]
        color_roi = img[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(gray_roi)
        if len(eyes) >= 2:
            cropped_faces.append(color_roi)
    return cropped_faces

def classify_images(image_b64,image_path=None):
    imgs=get_cropped_images(image_path,image_b64)

    result=[]
    for img in imgs:
        raw_img = cv2.resize(img, (32, 32))
        trans_img = convert_wavelength(img, 'db1', 5)
        scaled_trans_img = cv2.resize(trans_img, (32, 32))
        combined_img = np.vstack((raw_img.reshape(32 * 32 * 3, 1), scaled_trans_img.reshape(32 * 32, 1)))
        len_img_array=32*32*3+32*32
        final=combined_img.reshape(1,len_img_array).astype(float)

        result.append({
            'Name':number_to_name(__model.predict(final)[0]),
            'Probability':np.round(__model.predict_proba(final)*100,2).tolist()[0],
            'Original':__name_to_number

        })
    return result


def number_to_name(number):
    return __number_to_name[number]

def for_test_image():
    with open('b64.txt') as f:
       return  f.read()

if __name__=='__main__':
    print("Reached here")
    load_saved_artifacts()
    #print(classify_images(for_test_image(),None))
    print(classify_images(None, "./test_images/img12.jpg"))