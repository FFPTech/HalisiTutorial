from base64 import encode
import requests
import numpy as np
import cv2
import base64 as b64


def encodeImage(img):
    ret, img_enc = cv2.imencode('.jpg', img)
    if not ret:
        return None
    return b64.b64encode(img_enc).decode('utf-8', 'strict')


def decodeImage(img):
    img_dec = np.frombuffer(b64.b64decode(img.replace('data:image/jpeg;base64,', '').encode('utf-8')), np.uint8)
    return cv2.imdecode(img_dec, cv2.IMREAD_COLOR)

def display(img, face, color=(0, 255, 0)):
    img_display = img.copy()
    if face is not None:
        cv2.rectangle(img_display, (face[0], face[1]), (face[2], face[3]), color, thickness=-1)
        img_display = cv2.addWeighted(img, 0.7, img_display, 0.3, 0.0)
    return img_display

def detect(image, base_url, api_key, conf, iou, species='Human'):
    image_enc = encodeImage(image)
    data = {'image': image_enc, 'conf': conf, 'iou': iou}
    r = requests.post(base_url + '/Detect{}'.format(species), json=data, headers={'Ocp-Apim-Subscription-Key': api_key})
    if r.status_code == 200:
        resp = r.json()
        if resp is not None:
            score, face, t, msg = resp['detection_score'], resp['bbox'], resp['elapsed_time'], resp['message']
            face = eval(face)
            return True, face, score, t, msg, r.status_code
        else:
            msg = resp['message']
        return False, None, None, None, msg, r.status_code
    else:
        msg = resp['message']
        return False, None, None, None, msg, r.status_code
    return


def enroll(image, base_url, species='Cow'):
    image_enc = encodeImage(image)
    data = {'image': image_enc}
    r = requests.post(base_url + '/Enroll{}'.format(species), json=data)
    if r.status_code == 200:
        resp = r.json()
        bio, id = resp['signature'], resp['identifier']
        image = resp['image']
        enroll_img = decodeImage(image)
        enroll_img = cv2.cvtColor(enroll_img, cv2.COLOR_BGR2RGB)
        cv2.imshow('enrollment image', enroll_img)
        cv2.waitKey()
        return True, bio, id, r.status_code
    else:
        resp = r.json()
        return False, None, None, r.status_code
    return


def verify(signature, id, image, base_url, species='Cow'):
    image_enc = encodeImage(image)
    data = {'signature': signature, 'image': image_enc, 'id': id}
    r = requests.post(base_url + '/Verify{}'.format(species), json=data)
    if r.status_code == 200:
        resp = r.json()
        match = resp['match']
        image = resp['image']
        verify_img = decodeImage(image)
        verify_img = cv2.cvtColor(verify_img, cv2.COLOR_BGR2RGB)
        cv2.imshow('verification image', verify_img)
        cv2.waitKey()
        return True, match, r.status_code
    else:
        resp = r.json()
        return False, None, r.status_code
    return


def submit(record, base_url):
    data = {'record': record}
    r = requests.post(base_url + '/SubmitRecord', json=data)
    if r.status_code == 200:
        resp = r.json()
        success = resp['success']
        return True, success
    else:
        return False, None
    return