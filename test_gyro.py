import time, subprocess, cv2
import tobii_ctrl
from tobiiglassesctrl import TobiiGlassesController
import numpy as np

ipv4_address = "192.168.71.50"
tobiiglasses = TobiiGlassesController(ipv4_address, video_scene=True)

if tobiiglasses.is_recording():
    rec_id = tobiiglasses.get_current_recording_id()
    tobiiglasses.stop_recording(rec_id)

project_name = str('vision')
project_id = tobiiglasses.create_project(project_name)       
participant_name = str('sim')
participant_id = tobiiglasses.create_participant(project_id, participant_name)

tobiiglasses.get_battery_info()

print('start calibration')
time.sleep(1)

calibration_id = tobiiglasses.create_calibration(project_id, participant_id)
tobiiglasses.start_calibration(calibration_id)
res = tobiiglasses.wait_until_calibration_is_done(calibration_id)
if res is True:
    print('calibration done')
    
tobiiglasses.start_streaming()
myTobii = tobii_ctrl.tobii_data(tobiiglasses)
myTobii.start()   
time.sleep(3)

while True: 
    img = 255 *np.ones(shape=[512, 512, 3], dtype=np.uint8)
    
    data_gyro = myTobii.get_data()[7]
    gyro_r = data_gyro[0]
    gyro_t = data_gyro[1]
    gyro_p = data_gyro[2]
    img = cv2.resize(img, (600, 600))
    var = int(0.6*(gyro_r + 500))
    img = cv2.rectangle(img, (0,var), (200,600), (0,1,1), -1)
    var = int(0.6*(gyro_t + 500))
    img = cv2.rectangle(img, (200,var), (400,600), (0,1,1), -1)
    var = int(0.6*(gyro_p + 500))
    img = cv2.rectangle(img, (400,var), (600,600), (0,1,1), -1)
    
    cv2.putText(img, 'R', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)  
    cv2.putText(img, 'T', (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)  
    cv2.putText(img, 'P', (500, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)  
    
    weight, width = img.shape[:2]
     
    #cv2.circle(img,(x_pos,y_pos), 50, (0,0,255), 5)
    #rint('acc', acc)
    cv2.imshow('Gyroscope val',img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()