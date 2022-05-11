import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import time
import numpy as np

#----------------------------------------------------------------------------- Matplotlib data analyser
class Control:
    def __init__(self):
        self.tempo = 0.005
        self.status_fig = True
        
    def stop_runing(self,event):
        print('Stop by botton')
        plt.close('all')
        self.status_fig = False
    def get_status_fig(self):
        return self.status_fig
    
    def increase(self,event):
        print('increase')
        self.tempo = self.tempo * 2
    def decrease(self,event):
        print('decrease')
        self.tempo = self.tempo / 2
    def get_tempo(self):
        return self.tempo

#----------------------------------------------------------------------------- update_data_eye_tracker()
def show(myTobii, center_r_e, center_l_e):
    myControl = Control()
    fig = plt.figure('Tobii eye tracker',figsize=(8, 6))

    ax_button1 = plt.axes([0.75, 0.35, 0.2, 0.1])
    button1 = Button(ax_button1, 'Stop')
    button1.on_clicked(myControl.stop_runing)
    
    ax_button2 = plt.axes([0.1, 0.35, 0.2, 0.1])
    button2 = Button(ax_button2, '+')
    button2.on_clicked(myControl.increase)
    
    ax_button3 = plt.axes([0.1, 0.5, 0.2, 0.1])
    button3 = Button(ax_button3, '-')
    button3.on_clicked(myControl.decrease)
    
    ax_info = plt.axes([0.75, 0.5, 0.2, 0.1])
    ax_info.axis('off')
    info_fps = ax_info.text(0,0.5,'', fontsize = 13)
    
    ax_r_eye = plt.axes([0.32, 0.35, 0.2, 0.2])
    ax_r_eye.axis('off')
    ax_r_eye.set_title("Right eye", va='bottom')
    theta = np.linspace(0, 2*np.pi, 100)
    ax_r_eye.plot(2*np.cos(theta),2*np.sin(theta))
    ax_r_eye.set_xlim(-2.1, 2.1)
    ax_r_eye.set_ylim(-2.1, 2.1)
       
    ax_l_eye = plt.axes([0.52, 0.35, 0.2, 0.2])
    ax_l_eye.axis('off')
    ax_l_eye.set_title("Left eye", va='bottom')
    theta = np.linspace(0, 2*np.pi, 100)
    ax_l_eye.plot(2*np.cos(theta),2*np.sin(theta))
    ax_l_eye.set_xlim(-2.1, 2.1)
    ax_l_eye.set_ylim(-2.1, 2.1)

    ax0 = plt.axes([0.07, 0.65, 0.2, 0.2])
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.axes.get_xaxis().set_visible(False)
    ax0.title.set_text('ax0')

    ax1 = plt.axes([0.4, 0.65, 0.2, 0.2])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.title.set_text('ax1')

    ax2 = plt.axes([0.07, 0.05, 0.2, 0.2])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.axes.get_xaxis().set_visible(False)
    ax2.title.set_text('ax2')

    ax3 = plt.axes([0.4, 0.05, 0.2, 0.2])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.axes.get_xaxis().set_visible(False)
    ax3.title.set_text('ax3')
    
    ax4 = plt.axes([0.75, 0.65, 0.2, 0.2])
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.axes.get_xaxis().set_visible(False)
    ax4.title.set_text('ax4')

    ax5 = plt.axes([0.75, 0.05, 0.2, 0.2])
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.axes.get_xaxis().set_visible(False)
    ax5.title.set_text('ax5')
    
    data0 = []
    data1 = []
    data2 = []
    data3 = []
    data4 = [[],[],[]]
    data5 = []
    data_time = []
    
    line_e_r, = ax_r_eye.plot([],[], color='black', marker='o', linestyle='dashed',linewidth=5, markersize=38)
    line_e_l, = ax_l_eye.plot([],[], color='black', marker='o', linestyle='dashed',linewidth=5, markersize=38)
    line0, = ax0.plot([], lw=1)
    line1, = ax1.plot([], lw=1)
    line2, = ax2.plot([], lw=1)
    line3, = ax3.plot([], lw=1)
    line40, = ax4.plot([], lw=1)
    line41, = ax4.plot([], lw=1)
    line42, = ax4.plot([], lw=1)
    line5, = ax5.plot([], lw=1)

    ax0.set_ylim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax3.set_ylim(-2, 2)
    ax4.set_ylim(-20, 20)
    ax5.set_ylim(-20, 20)
    
    ax0.set_xlim(0, 20)
    ax1.set_xlim(0, 20)
    ax2.set_xlim(0,20)
    ax3.set_xlim(0, 20)
    ax4.set_xlim(0, 20)
    ax5.set_xlim(0, 20)
    
    fig.canvas.draw()
    
    ax_infobackground = fig.canvas.copy_from_bbox(ax_info.bbox)
    ax_r_eyebackground = fig.canvas.copy_from_bbox(ax_r_eye.bbox)
    ax_l_eyebackground = fig.canvas.copy_from_bbox(ax_l_eye.bbox)
    ax0background = fig.canvas.copy_from_bbox(ax0.bbox)
    ax1background = fig.canvas.copy_from_bbox(ax1.bbox)
    ax2background = fig.canvas.copy_from_bbox(ax2.bbox)
    ax3background = fig.canvas.copy_from_bbox(ax3.bbox)
    ax4background = fig.canvas.copy_from_bbox(ax4.bbox)
    ax5background = fig.canvas.copy_from_bbox(ax5.bbox)
    
    plt.show(block=False)

    start_time = time.time()
    i = 0.
    counter = 0
    t = 1
    fps = 0
    
    x_r = 0
    y_r = 0
    x_l = 0
    y_l = 0
    
    while True:
        counter+=1
        if (time.time() - start_time) > t :
            fps = (counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
   
        info_fps.set_text('FPS:'+str("%.2f" % fps))

        myData = myTobii.get_data()
    
        if myData[0] != None:
            x_r = myData[0] - center_r_e[0]
            y_r = myData[1] - center_r_e[1]
            data0.append(x_r) 
            data1.append(y_r)
            x_l = myData[2] - center_l_e[0]
            y_l = myData[3] - center_l_e[1]
            data2.append(x_l)
            data3.append(y_l)
            data4[0].append(myData[4][0])
            data4[1].append(myData[4][1])
            data4[2].append(myData[4][2])
            data5.append(myData[5])
            data_time.append(i)
            
            line_e_r.set_data(x_r, y_r)
            line_e_l.set_data(x_l, y_l)
            line0.set_data(data_time, data0)
            line1.set_data(data_time, data1)
            line2.set_data(data_time, data2)
            line3.set_data(data_time, data3)
            line40.set_data(data_time, data4[0])
            line41.set_data(data_time, data4[1])
            line42.set_data(data_time, data4[2])
            line5.set_data(data_time, data5) 
                
        if i > 20 :
            ax0.set_xlim(i-18, i+2)
            ax1.set_xlim(i-18, i+2)
            ax2.set_xlim(i-18, i+2)
            ax3.set_xlim(i-18, i+2)
            ax4.set_xlim(i-18, i+2)
            ax5.set_xlim(i-18, i+2)
            
        i+=1
        
        fig.canvas.restore_region(ax_infobackground)
        fig.canvas.restore_region(ax_r_eyebackground)
        fig.canvas.restore_region(ax_l_eyebackground)
        fig.canvas.restore_region(ax0background)
        fig.canvas.restore_region(ax1background)
        fig.canvas.restore_region(ax2background)
        fig.canvas.restore_region(ax3background)
        fig.canvas.restore_region(ax4background)
        fig.canvas.restore_region(ax5background)

        ax_info.draw_artist(info_fps)
        
        ax_r_eye.draw_artist(line_e_r)
        ax_l_eye.draw_artist(line_e_l)
        ax0.draw_artist(line0)
        ax1.draw_artist(line1)
        ax2.draw_artist(line2)
        ax3.draw_artist(line3)
        ax4.draw_artist(line40)
        ax4.draw_artist(line41)
        ax4.draw_artist(line42)
        ax5.draw_artist(line5)
        
        fig.canvas.blit(fig.bbox)
        time.sleep(myControl.get_tempo())
        fig.canvas.flush_events()
        
        if myControl.get_status_fig() == False:
            break

print('data_analyser imported')