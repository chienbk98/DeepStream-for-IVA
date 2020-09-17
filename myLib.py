from playsound import playsound
from twilio.rest import Client
from datetime import datetime
import numpy as np
import threading
import pyttsx3
import smtplib
import time
import cv2



pgie_classes_str= ["Person"]
center_point = [[],[],[]]
cap_width = 1920
cap_height = 1080

gmail_user = 'yoonalearning@gmail.com'
gmail_password = 'yeuyoona98'

sent_from = gmail_user
to = ['yoonachien@gmail.com']

def sendemail(camera_idx):
  subject = 'Warning Message'
  body = 'Someone are entering the restricted area camera number {}'.format(camera_idx)
  message = 'Subject: {}\n\n{}'.format(subject, body)
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(gmail_user, gmail_password)
  server.sendmail(sent_from, to, message)
  server.quit()


def sendSMS(camera_idx):
  body = 'Someone are entering the restricted area Camera number {}'.format(camera_idx) 
  account_sid = 'ACb0f57f89aed94e673c4d2ff094c53ff4'
  auth_token = 'c6d03596a44f79a8c0977cec20360910'
  client = Client(account_sid, auth_token)
  message = client.messages.create(
                                from_='+16075243663',
                                body=body,
                                to='+84812749258'
                            )
  print(message.sid)


def makeCall():
  account_sid = 'ACb0f57f89aed94e673c4d2ff094c53ff4'
  auth_token = 'c6d03596a44f79a8c0977cec20360910'
  client = Client(account_sid, auth_token)
  call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+84812749258',
                        from_='+16075243663'
                    )

  print(call.sid)


def soundWarning():
  playsound('warning.mp3')


class warningMethod():
  def __init__(self, camera_idx:int, warning_flag, type_warning:int):
    '''
    camera_idx: index of camera
    warning_flag: 1: warning, None: No Warning
    type: 1-Sound, 2-Email, 3-SMS, 4-Call
    '''
    self.running_flag = True
    self.camera_idx = camera_idx
    self.warning_flag = warning_flag
    self.type_warning = type_warning
  def terminate(self):
    self.running_flag = False
  def run(self):
    while True:
      # print("running!")
      while self.warning_flag:
          # playsound('warning.mp3')
          if self.type_warning == 1:
            soundWarning()
            # print("Co doi tuong di vao vung cam")
            time.sleep(2)
          elif self.type_warning == 2:
            sendemail(self.camera_idx)
            time.sleep(180)
          elif self.type_warning == 3:
            sendSMS(self.camera_idx)
            time.sleep(180)
          elif self.type_warning == 4:
            makeCall()
            time.sleep(180)

          if not self.running_flag:
            break
      else:
        pass 
        # print("Waiting !")
      if not self.running_flag:
        # print("Stop thread! ")
        break
    else:
      print("Warning ends")

def monitorProhibitedArea(points:list, center_point:list, source_id:int):
  '''
  Ham canh bao khi co mot Object nam trong vung canh bao
  '''
  point1 = []
  for point in points:
    x = point[0] * cap_width
    y = point[1] * cap_height
    point1.append((int(x), int(y))) # diem vung cam sau khi chuyen tuong ung voi kich thuoc cua frame hien tai
  # print("point area :", point1)
  for va in center_point[source_id]:
    x_center, y_center = va[0], va[1]
    if len(point1) > 2:
      dist = cv2.pointPolygonTest(np.array([point1]), (x_center, y_center), False)
      if dist > 0:
        # print('<<<<<<< Warning Camera {}>>>>>>>'.format(source_id), datetime.now())
        return 1
  return None


def remove_list(name_list):
  if(len(name_list)!=0):
    for i in range(len(name_list)):
      name_list.pop()


def rgba2rgb( rgba, background=(0,0,0) ):
    '''
    Do anh trong Buffer tra ve la anh BGRA nen dung ham nay de convert ve anh RGB
    Anh RGB se phuc vu cho viec hien thi len UI
    '''
    row, col, ch = rgba.shape

    if ch == 3:
        return rgba

    assert ch == 4, 'RGBA image has 4 channels.'

    rgb = np.zeros( (row, col, 3), dtype='float32' )
    b, g, r, a = rgba[:,:,0], rgba[:,:,1], rgba[:,:,2], rgba[:,:,3]

    a = np.asarray( a, dtype='float32' ) / 255.0

    R, G, B = background

    rgb[:,:,0] = r * a + (1.0 - a) * R
    rgb[:,:,1] = g * a + (1.0 - a) * G
    rgb[:,:,2] = b * a + (1.0 - a) * B

    return np.asarray(rgb, dtype='uint8')


def draw_bounding_boxes(image,obj_meta,track_id,source_id):
    '''
    Ham draw bounding boxes va object name len frame
    Dong thoi lay du lieu ve vi tri cua Object phuc vu cho ham monitorProhibitedArea
    '''
    global center_point
    rect_params=obj_meta.rect_params
    top=int(rect_params.top)
    left=int(rect_params.left)
    width=int(rect_params.width)
    height=int(rect_params.height)

    x_center, y_center = int(left + width/2), int(top+height)
    center_point[source_id].append((x_center, y_center))

    obj_name=pgie_classes_str[obj_meta.class_id]
    # image=cv2.rectangle(image,(left,top),(left+width,top+height),(0,255,0),2)
    image=cv2.circle(image, center=(x_center, y_center), radius=0, color = (0, 255, 0), thickness=10)
    # image=cv2.putText(image,obj_name+',ID'+str(track_id),(left-10,top-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    return image