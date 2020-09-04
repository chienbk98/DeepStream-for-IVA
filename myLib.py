from datetime import datetime
import numpy as np
import cv2
import threading
from playsound import playsound
import time
import pyttsx3



pgie_classes_str= ["Person"]
center_point = [[],[(960, 540)],[]]
cap_width = 1920
cap_height = 1080

class warningMethod():
  def __init__(self, camera_idx):
    # super().__init__()
    self.running_flag = True
    self.camera_idx = camera_idx
  
  def terminate(self):
    self.running_flag = False
  def run(self):
    # e = pyttsx3.init()
    while self.running_flag:
      # e.say("Camera {} Someones are entering the restricted area".format(self.camera_idx))
      # e.runAndWait()
      playsound('warning.mp3')
      time.sleep(1)
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
    image=cv2.rectangle(image,(left,top),(left+width,top+height),(0,255,0),2)
    image=cv2.circle(image, center=(x_center, y_center), radius=0, color = (0, 255, 0), thickness=10)
    image=cv2.putText(image,obj_name+',ID'+str(track_id),(left-10,top-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    return image