
import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
# print(sys.path)

from skylark.core.clients import Service
from skylark.core.face_mask_stream import FaceMaskStreamClient
from skylark.core.face_detect_stream import FaceDetectStreamClient
from skylark.core.weapon_detection_stream import WeaponDetectionStreamClient
from skylark.core.facial_landmark_stream import FacialLandmarkStream
from skylark.core.lie_detection_stream import LieDetectionStreamClient
from skylark.core.night_day_stream import NightDayStreamClient
import time
from skylark.utils.utils import is_connected
from threading import Thread
from skylark.core.multi_stream import MultiStreamer




# user will add authorization token here
token = "abcd"

# user will send fps of incoming stream, size of batch that will be formed while processing ,

# user can continue to perform any further tasks as per need
if __name__ == '__main__':
    dict = {}
    dict['service_name'] = 'face_mask'
    dict['stream_url'] = "rtsp://admin:admin123@203.134.200.170:554/cam/realmonitor?channel=12&subtype=0"
    dict['fps'] = 5
    dict['batch_size']=1
    dict['sampling_rate']=1
    dict['show_processed_stream']=True
    dict['save_raw_frames'] = True
    dict['scale_percent'] = 35
    dict['quality'] = 40
    multi_stream = MultiStreamer(token, [dict,])


def ready():
    print("i am ready now")
try:
    i=0
    while True:
        print("in mian")
        if len(multi_stream.client) > 1:
            print("############## heyy got id ###################")
            print(multi_stream.client[0].response_jsons)
        time.sleep(1)
except KeyboardInterrupt:
	print("exiting")
	exit()
	
