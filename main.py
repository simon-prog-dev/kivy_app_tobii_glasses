##############################################################################
#                                                                            #
#                     Simon LE BERRE      04/05/2022                         #
#                                                                            #
##############################################################################

#----------------------------------------------------------------------------- Import Kivy
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
#from kivymd.font_definitions import theme_font_styles
#from kivy.config import Config
#----------------------------------------------------------------------------- Import
import cv2, time, subprocess
import data_analyser, tobii_ctrl
from tobiiglassesctrl import TobiiGlassesController
import numpy as np
#----------------------------------------------------------------------------- Welcome Screen
class WelcomeScreen(Screen):
    def on_enter(self):
        pass
    def starting(self):
        time.sleep(0.5)
        self.manager.current = 'setting'
    def help(self):
        dialog = MDDialog(text="Tobi Glasses application: Help connection: \n \n"
                               "1. Active Wifi of your device \n"
                               "2. Connect you in Wifi to your Tobii Glasses\n"
                               "3. Start to use the application\n\n"
                               "Dev. SLB")
        dialog.open() 

#----------------------------------------------------------------------------- Setting Screen
class SettingScreen(Screen):      
    def refresh(self):
        global tobiiglasses, project_id, participant_id, ipv4_address, myTobii
        try:
            myTobii.stop()
            myTobii.join()
            try:
                tobiiglasses.close()
            except:
                pass
        except:
            pass
        
        process = subprocess.Popen(["iwgetid"], stdout=subprocess.PIPE)
        var = str(process.communicate()[0])
        self.btn1.md_bg_color = (130/255, 130/255, 130/255, 1)
        self.btn2.md_bg_color = (130/255, 130/255, 130/255, 1)        # grey
        self.btn3.md_bg_color = (130/255, 130/255, 130/255, 1)
        self.btn1.disabled = True
        self.btn2.disabled = True
        self.btn3.disabled = True
        
        if var.find('"') != -1:
            id_network = var[var.find('"') + 1:var.rfind('"')]
            self.label1.text = id_network
            self.id_tobii_glasses = id_network
            self.btn1.disabled = False
            self.btn1.md_bg_color = (33/255, 150/255, 245/255, 1)     # bleu
            
        else:
            self.label1.text = 'No Tobii Glasses found !'
            self.id_tobii_glasses = None
            
    def connect(self):  
        global tobiiglasses, project_id, participant_id, ipv4_address
        if self.project_name.text != "" and self.participant_name.text !="":
            try:
                print('Tobii glasses connection ...')
                ipv4_address = "192.168.71.50"
                tobiiglasses = TobiiGlassesController(ipv4_address, video_scene=True)
                
                if tobiiglasses.is_recording():
                    rec_id = tobiiglasses.get_current_recording_id()
                    tobiiglasses.stop_recording(rec_id)

                project_name = str(self.project_name.text)
                project_id = tobiiglasses.create_project(project_name)
                
                participant_name = str(self.participant_name.text)
                participant_id = tobiiglasses.create_participant(project_id, participant_name)
                
                self.btn1.text = 'Connected'
                self.btn1.md_bg_color = (100/255, 221/255, 23/255, 1)  # green
                self.tobii_connection = True
                self.btn2.disabled = False
                self.btn2.md_bg_color = (33/255, 150/255, 245/255, 1)  # bleu
                print('Connected !')
                battery_level = tobiiglasses.get_battery_info()
                battery_level = battery_level[battery_level.find(':') + 2 : battery_level.rfind('%')-4]
                if int(battery_level) < 25:
                    MDDialog(text="Low battery. \n\nRemember to replace your battery soon").open()                
            except:
                Snackbar(text="Error connection, retry in cas of no success swith off / swith on Tobii Glasses").open()
        else:
            Snackbar(text="Project ID and Participant Name should be complete ").open()
        
    def show_target(self):
        #display_dim = Window.size
        #print(display_dim)
        #width, height= pyautogui.size()
        #print(width, height)
        self.img4.pos_hint = {"center_x":0.5, "center_y":0.5}
        self.btn4.pos_hint = {"center_x":0.5, "center_y":0.23}
        self.btn4.disabled = False

    def calibration(self):
        global tobiiglasses, project_id, participant_id, center_r_e, center_l_e, status_calibration
        try:
            calibration_id = tobiiglasses.create_calibration(project_id, participant_id)
            tobiiglasses.start_calibration(calibration_id)
            res = tobiiglasses.wait_until_calibration_is_done(calibration_id)
            if res is False:
                self.img4.pos_hint = {"center_x":2, "center_y":2}
                self.btn4.pos_hint = {"center_x":2, "center_y":2}
                Snackbar(text="Error calibration, restart it and watch attentively the target").open()
                
            else:
                tobiiglasses.start_streaming()
                nb_mesure = 0
                while (nb_mesure < 10):
                    info_tobii_glasses = tobiiglasses.get_data()
                    dico_r_eye = info_tobii_glasses['right_eye']['pc']
                    dico_l_eye = info_tobii_glasses['left_eye']['pc']
                    list_r_eye_x = []
                    list_r_eye_y = []
                    list_l_eye_x = []
                    list_l_eye_y = []
                    center_r_e = []
                    center_l_e = []
                    if dico_r_eye['ts'] > 0 and dico_l_eye['ts'] > 0:
                        list_r_eye_x.append(dico_r_eye['pc'][0])
                        list_r_eye_y.append(dico_r_eye['pc'][1])
                        list_l_eye_x.append(dico_l_eye['pc'][0])
                        list_l_eye_y.append(dico_l_eye['pc'][1])
                        time.sleep(0.1)
                        nb_mesure += 1
                center_r_e.append(sum(list_r_eye_x) / len(list_r_eye_x))
                center_r_e.append(sum(list_r_eye_y) / len(list_r_eye_y))
                center_l_e.append(sum(list_l_eye_x) / len(list_l_eye_x))
                center_l_e.append(sum(list_l_eye_y) / len(list_l_eye_y))
                print('center right eye is: ', center_r_e)
                print('center left eye is: ', center_l_e)
                status_calibration = True
                self.btn2.md_bg_color = (100/255, 221/255, 23/255, 1) # green
                self.btn3.disabled = False
                self.btn3.md_bg_color = (33/255, 150/255, 245/255, 1) # bleu
                self.img4.pos_hint = {"center_x":2, "center_y":2}
                self.btn4.pos_hint = {"center_x":2, "center_y":2}
                self.btn4.disabled = True
                tobiiglasses.stop_streaming()
        except:
                Snackbar(text="Fatal error of calibration, restart Tobii Glasses").open()
                self.img4.pos_hint = {"center_x":2, "center_y":2}
                self.btn4.pos_hint = {"center_x":2, "center_y":2}
    def run(self):
        global myTobii, tobiiglasses, tobii_validation
        tobiiglasses.start_streaming()
        myTobii = tobii_ctrl.tobii_data(tobiiglasses)
        myTobii.start()
        tobii_validation = True
        self.manager.current = 'menu'

#----------------------------------------------------------------------------- Menu Screen
class MenuScreen(Screen):
    def call_page(self, page):
        self.manager.current = str(page)
        
#----------------------------------------------------------------------------- Data Screen
class DataScreen(Screen):
    def info(self):
        dialog = MDDialog(text="Tobi Glasses application: Help Data Analyser: \n\n"
                               "This mode will provide you \n"
                               "a graphical interface of data\n"
                               "provide by tobii application")
        dialog.open() 
        
    def open_plt(self):
        global myTobii, center_r_e, center_l_e
        data_analyser.show(myTobii, center_r_e, center_l_e)
        
    def call_menu(self):
        self.manager.current = 'menu'

#----------------------------------------------------------------------------- Video Screen
class VideoScreen(Screen):
    def info(self):
        dialog = MDDialog(text="Tobi Glasses application: Help Video Displayer: \n\n"
                               "This mode will provide you \n"
                               "a video window of Cumpter or Tobbi Glasses")
        dialog.open() 
    
    def call_menu(self):
        self.manager.current = 'menu'
        
    def PC_cam(self):
        global myTobii
        img = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
    
        while True:
            img = cv2.resize(img, (1280, 720))
            acc = myTobii.get_data()[4]
            acc_x = acc[0]
            acc_y = acc[1] + 9.81
            acc_z = acc[2]
            #acc [1.14, -9.84, -1.38]
            weight, width = img.shape[:2]
            x_pos = int(weight / 2)
            if acc_y !=0:
                y_pos = int((10*(width/2)/acc_y))
            else:
                y_pos = 0
            print(x_pos, y_pos)
            cv2.circle(img,(x_pos,y_pos), 50, (0,0,255), 5)
            #rint('acc', acc)
            cv2.imshow('sample image',img)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
    
    
    '''
    def PC_cam(self):
        vid = cv2.VideoCapture(0)
        while(True):
            
            ret, frame = vid.read()
            cv2.putText(frame, 'Press q to leave video', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.imshow('PC_camera', frame)
            #cv2.moveWindow('PC_camera',700,80)     # function of window size

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        vid.release()
        cv2.destroyAllWindows()
        '''
    def TG_cam_point(self):
        global ipv4_address, myTobii
        cap = cv2.VideoCapture("rtsp://%s:8554/live/scene" % ipv4_address)

        if (cap.isOpened()== False):
            print("Error opening video stream or file")
        
        while(cap.isOpened()):
            
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1280, 720))
            
            if ret == True:
                height, width = frame.shape[:2]
                data_gp  = myTobii.get_data()

            if data_gp[6] != [0,0]:    
                x_pos = int(data_gp[6][0]*width)
                y_pos = int(data_gp[6][1]*height)
                cv2.circle(frame,(x_pos,y_pos), 50, (0,0,255), 5)
                
            cv2.putText(frame, 'Press q to leave video', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)    
            cv2.imshow('Tobii Pro Glasses 2',frame)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
        
    def TG_cam_line(self):
        global ipv4_address, myTobii
        cap = cv2.VideoCapture("rtsp://%s:8554/live/scene" % ipv4_address)

        if (cap.isOpened()== False):
            print("Error opening video stream or file")
        gaze_pos = []
        while(cap.isOpened()):
            
            ret, frame = cap.read()
            frame = cv2.resize(frame, (1280, 720))
            
            if ret == True:
                height, width = frame.shape[:2]
                data_gp  = myTobii.get_data()

            if data_gp[6] != [0,0]:    
                x_pos = int(data_gp[6][0]*width)
                y_pos = int(data_gp[6][1]*height)
                gaze_pos.append([x_pos,y_pos])
                
                if len(gaze_pos)>1:
                    for i in range (len(gaze_pos)-1):
                        
                        point_a = (int(gaze_pos[i][0]),int(gaze_pos[i][1]))
                        point_b = (int(gaze_pos[i+1][0]), int(gaze_pos[i+1][1]))
                        frame = cv2.line(frame,point_a, point_b, (0,0,255), 5)
                
            cv2.putText(frame, 'Press q to leave video', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)    
            cv2.imshow('Tobii Pro Glasses 2',frame)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()

#----------------------------------------------------------------------------- Record Screen
class RecordScreen(Screen):
    def info(self):
        dialog = MDDialog(text="Tobi Glasses application: Info Records Screen: \n\n"
                               "With this mode you can record \n"
                               "tobii Glasses' data on the SD card.\n")
        dialog.open()      
    
    def start_record(self):
        global tobiiglasses, project_id, participant_id, recording_id
        
        try:
            print(self.recording_state)
        except:
            self.recording = False
            
        if self.recording == True:
            Snackbar(text="Already recording, stop first and start a new one")
            
        else:    
            recording_id = tobiiglasses.create_recording(participant_id)
            tobiiglasses.start_recording(recording_id)
            tobiiglasses.send_custom_event("start_recording", "Start of the recording ")
            self.recording_state = True
            message = "Start recording!" 
            dialog = MDDialog(text = message)
            dialog.open()
  
    def pause_record(self):
        message = "Recording paused   // do not working yet"
        dialog = MDDialog(text = message)
        dialog.open()
        '''global tobiiglasses
        try:
            print(self.recording_state)
        except:
            self.recording_state = False
            
        if self.recording_state ==  True:
            tobiiglasses.pause_recording(self.recording_id)
        else:
            Snackbar(text="Nothing is recording currently").open()'''

    def stop_record(self):
        global tobiiglasses, project_id, participant_id, recording_id
        try:
            print(self.recording_state)
        except:
            self.recording_state = False
            
        if self.recording_state ==  True:
            tobiiglasses.send_custom_event("stop_recording", "Stop of the recording " + str(recording_id))
            tobiiglasses.stop_recording(recording_id)
            self.recording =  False
            message = "Recording stoped \n\nThe recording will be stored in the SD folder projects/%s/recordings/%s" % (project_id, recording_id)
            dialog = MDDialog(text = message)
            dialog.open()
        else:
            Snackbar(text="Recording already stop").open()  

    def call_menu(self):
        self.manager.current = 'menu'

#----------------------------------------------------------------------------- Navigation List
class ContentNavigationDrawer(BoxLayout):
    nav_drawer = ObjectProperty()

#----------------------------------------------------------------------------- Main
display_dim = Window.size
#Window.size = (800,800)
#Window.maximize()

sm = ScreenManager(transition=NoTransition())
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(SettingScreen(name='setting'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(DataScreen(name='data'))
sm.add_widget(VideoScreen(name='video'))

#----------------------------------------------------------------------------- TobiiPro App
class TobiiProApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  #Dark
        return Builder.load_file('builder.kv')
    
    def on_start(self):
        self.root.ids.toolbar.title = 'Welcome to Tobii Pro application'
        global tobii_validation
        tobii_validation = False 
        
    def validation_connection(self):
        global tobii_validation
        if tobii_validation == False:
            Snackbar(text="You have to be connected to tobii glasses first.").open()
            self.root.ids.screen_manager.current = 'setting'

    def toolbar(self, screen_name):
        self.root.ids.toolbar.title = screen_name
    
    def battery_level(self):
        global myTobii
        try:
            battery_level = myTobii[7]
            self.root.ids.battery_level.text = str(battery_level)+' %'
            if int(battery_level) < 25:
                MDDialog(text="Low battery. \n\nRemember to replace your battery soon").open()
        except:
            pass

TobiiProApp().run()

