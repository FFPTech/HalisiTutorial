import cv2
from api import enroll, verify
import time

api_url = 'https://halisiapi-v1-test.azurewebsites.net/api' 

# read enroll and verify image
img_ref = cv2.imread("./images/face_01_01.png")
img_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2RGB)

img_tst = cv2.imread("./images/face_01_02.png")
img_tst = cv2.cvtColor(img_tst, cv2.COLOR_BGR2RGB)


species = "Human"

start_enroll = time.time()

print('[INFO] Start facial enrollment')
ret, biosignature, id, status = enroll(img_ref, api_url, species)

if ret:  
  print('[INFO] Facial enrollment succeeded :-)')

  print('[INFO] Start facial verification')
  ret, matching, status = verify(biosignature, id, img_tst, api_url, species)
  if ret:
    print('[INFO] Facial verification succeeded :-)')
    print("[INFO] verification result :", matching, "verification status :", status)
  else:
    print('[INFO] Face verification failed :-(')
else:
  print('[INFO] Face enrollment failed :-(')

