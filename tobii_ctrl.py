import threading, time

class tobii_data(threading.Thread):
    def __init__(self, tobiiglasses):
        threading.Thread.__init__(self)
        self.stop_loop = False
        self.a0 = 0
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0
        self.a4 = [[],[],[]]
        self.a5 = 0
        self.reception = False
        self.a6 =[[],[]]
        self.a7 = [[],[],[]]
        self.tobiiglasses = tobiiglasses
       
    def run(self):
        print('tobii_data.run')
        start_time = time.time()
        t = 15
        i = 0
        counter = 0
        n = 5
        
        data0 = []
        data1 = []
        data2 = []
        data3 = []
        data4 = [[],[],[]]
        data5 = []
        #data6 = [[],[]]
        data7 = [[],[],[]]

        while True:
            try:
                info_tobii_glasses = self.tobiiglasses.get_data()
                dico_r_eye  = info_tobii_glasses['right_eye']['pc']
                if dico_r_eye['ts'] > 0:
                    data = dico_r_eye['pc']
                    
                    data0.append(data[0])
                    data0 = data0[-n:]
                    self.a0 = sum(data0)/len(data0)
                    
                    data1.append(data[1])
                    data1 = data1[-n:]
                    self.a1 = sum(data1)/len(data1)
                    
                    dico_l_eye  = info_tobii_glasses['left_eye']['pc']
                    data = dico_l_eye['pc']
                    
                    data2.append(data[0])
                    data2 = data2[-n:]
                    self.a2 = sum(data2)/len(data2)
                    
                    data3.append(data[1])
                    data3 = data3[-n:]
                    self.a3 = sum(data3)/len(data3)
                    
                    # acc x,y,z
                    dico_acc = info_tobii_glasses['mems']['ac']
                    data = dico_acc['ac']
                    data4[0].append(data[0])
                    data4[0] = data4[0][-n:]
                    self.a4[0] = float("{:.2f}".format(sum(data4[0])/len(data4[0])))
                    
                    data4[1].append(data[1])
                    data4[1] = data4[1][-n:]
                    self.a4[1] = float("{:.2f}".format(sum(data4[1])/len(data4[1])))
                    
                    data4[2].append(data[2])
                    data4[2] = data4[2][-n:]
                    self.a4[2] =float("{:.2f}".format(sum(data4[2])/len(data4[2])))
                    
                    #sum acc
                    sum_acc =  abs(data[0])+abs(data[1])+abs(data[2])
                    data5.append(sum_acc)
                    data5 = data5[-n:]
                    self.a5 = sum(data5)/len(data5)
                    
                    # gaze position
                    dico_gp = info_tobii_glasses['gp']
                    data = dico_gp['gp']
                    self.a6 = data
                    
                    # gyto r, theta, phi
                    dico_acc = info_tobii_glasses['mems']['gy']
                    data = dico_acc['gy']
                    data7[0].append(data[0])
                    data7[0] = data7[0][-n:]
                    self.a7[0] = float("{:.2f}".format(sum(data7[0])/len(data7[0])))
                    
                    data7[1].append(data[1])
                    data7[1] = data7[1][-n:]
                    self.a7[1] = float("{:.2f}".format(sum(data7[1])/len(data7[1])))
                    
                    data7[2].append(data[2])
                    data7[2] = data7[2][-n:]
                    self.a7[2] =float("{:.2f}".format(sum(data7[2])/len(data7[2])))
                    
                    i+=1
                
                    self.reception = True
                    time.sleep(0.005)
                    
                else:
                    print('No data yet')
                    time.sleep(1)
                    self.reception = False
                counter+=1
                if (time.time() - start_time) > t :
                    print("FPS of data reception: ", int(counter / (time.time() - start_time)))
                    counter = 0
                    start_time = time.time()
                if self.stop_loop == True:
                    break
            except:
                print('error reading')
                time.sleep(1)
            
    def get_data(self):
        all_data = []
        all_data.append(self.a0)
        all_data.append(self.a1)
        all_data.append(self.a2)
        all_data.append(self.a3)
        all_data.append(self.a4)
        all_data.append(self.a5)
        all_data.append(self.a6)
        all_data.append(self.a7)
        return all_data
    
    def stop(self):
        self.stop_loop = True

print('tobii_ctrl imported')