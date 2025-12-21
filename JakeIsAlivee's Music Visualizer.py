import soundfile

import pygame
import numpy

import os
import sys

import easygui


scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
if scriptdirfolder.find('\\') != -1:
    slash = '\\'
else:
    slash = '/'

selectedfile = easygui.fileopenbox('Select a .wav file to visualize','Visualizer',scriptdirfolder+slash)
if selectedfile == None:
    sys.exit()

while selectedfile[len(selectedfile)-4:len(selectedfile)] != '.wav':
    selectedfile = easygui.fileopenbox('Not a .wav file. Try again.','Visualizer',scriptdirfolder+slash)
    if selectedfile == None:
        sys.exit()

pygame.init()

pygame.mixer_music.load(selectedfile)
musicvolume_percent = 50
pygame.mixer_music.set_volume(musicvolume_percent/100)

soundrawdata, rate = soundfile.read(selectedfile)
soundduration = len(soundrawdata) / rate
soundtime = numpy.arange(0,soundduration,1/rate)

soundrawdata = soundrawdata.tolist()
soundtime = soundtime.tolist()

xwindow = 600
ywindow = 200
mainwindow = pygame.display.set_mode((xwindow,ywindow),pygame.NOFRAME)

pygame.display.set_caption("JakeIsAlivee's Visualizer")
pygame.display.set_icon(pygame.image.load(scriptdirfolder+slash+'JakeIsAlivee coffee cup.bmp'))

xposition = (pygame.display.get_desktop_sizes()[0][0]/2)-(xwindow/2)
yposition = (pygame.display.get_desktop_sizes()[0][1]/2)-(ywindow/2)
pygame.display.set_window_position((xposition,yposition))

import win32api
import win32con
import win32gui
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)


mainwindow.fill((0,0,0))
loadingtext = pygame.font.SysFont('couriernew',64).render('Loading...',False,(255,255,255))
mainwindow.blit(loadingtext,((xwindow/2)-(loadingtext.get_width()/2),(ywindow/2)-(loadingtext.get_height()/2)))

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,0)), 0, win32con.LWA_COLORKEY)

win32gui.BringWindowToTop(hwnd)

win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
rect = win32gui.GetWindowRect(hwnd) 
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)


pygame.display.update()

songpos = 0
songlen = pygame.mixer.Sound(selectedfile).get_length() * 1000

lastsounddata = 0


soundrawdata_x2 = []
tempnum = 0
while tempnum < len(soundrawdata):
    if tempnum % 2 == 0:
        soundrawdata_x2.append(soundrawdata[tempnum])
    tempnum += 1

soundrawdata_x4 = []
tempnum = 0
while tempnum < len(soundrawdata_x2):
    if tempnum % 2 == 0:
        soundrawdata_x4.append(soundrawdata_x2[tempnum])
    tempnum += 1

soundrawdata_x8 = []
tempnum = 0
while tempnum < len(soundrawdata_x4):
    if tempnum % 2 == 0:
        soundrawdata_x8.append(soundrawdata_x4[tempnum])
    tempnum += 1

soundrawdata_x16 = []
tempnum = 0
while tempnum < len(soundrawdata_x8):
    if tempnum % 2 == 0:
        soundrawdata_x16.append(soundrawdata_x8[tempnum])
    tempnum += 1

soundrawdata_x32 = []
tempnum = 0
while tempnum < len(soundrawdata_x16):
    if tempnum % 2 == 0:
        soundrawdata_x32.append(soundrawdata_x16[tempnum])
    tempnum += 1

soundrawdata_x64 = []
tempnum = 0
while tempnum < len(soundrawdata_x32):
    if tempnum % 2 == 0:
        soundrawdata_x64.append(soundrawdata_x32[tempnum])
    tempnum += 1

soundrawdata_x128 = []
tempnum = 0
while tempnum < len(soundrawdata_x64):
    if tempnum % 2 == 0:
        soundrawdata_x128.append(soundrawdata_x64[tempnum])
    tempnum += 1

soundrawdata_x256 = []
tempnum = 0
while tempnum < len(soundrawdata_x128):
    if tempnum % 2 == 0:
        soundrawdata_x256.append(soundrawdata_x128[tempnum])
    tempnum += 1

soundrawdata_x512 = []
tempnum = 0
while tempnum < len(soundrawdata_x256):
    if tempnum % 2 == 0:
        soundrawdata_x512.append(soundrawdata_x256[tempnum])
    tempnum += 1

soundrawdata_x1024 = []
tempnum = 0
while tempnum < len(soundrawdata_x512):
    if tempnum % 2 == 0:
        soundrawdata_x1024.append(soundrawdata_x512[tempnum])
    tempnum += 1


devisionby = 1

devision_to_list_dict = {
    1:    soundrawdata,
    2:    soundrawdata_x2,
    4:    soundrawdata_x4,
    8:    soundrawdata_x8,
    16:   soundrawdata_x16,
    32:   soundrawdata_x32,
    64:   soundrawdata_x64,
    128:  soundrawdata_x128,
    256:  soundrawdata_x256,
    512:  soundrawdata_x512,
    1024: soundrawdata_x1024,
}

userzoom_to_devision_dict = {
    'x1024': 1,
    'x512' : 2,
    'x256' : 4,
    'x128' : 8,
    'x64'  : 16,
    'x32'  : 32,
    'x16'  : 64,
    'x8'   : 128,
    'x4'   : 256,
    'x2'   : 512,
    'x1'   : 1024,
}

pygame.mixer_music.play()

pygame.mixer_music.pause()

playing = False
holdinglmb = False

visualizerscene = True
settingsscene = False

musicnum = 0
musicqueue = [selectedfile]



s_transparent_anim = 60
s_ontop_anim = 60
s_volchange_anim = 60

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)

#i have a DECENT idea of what is this win32 shit

transparent_window = True
ontop_window = True

songpos_animstart = -2000
percentage_anim = -2000


while True:
    if visualizerscene:
        mainwindow.fill((0,0,254))

        songpos = pygame.mixer_music.get_pos()
        
        if songpos > songlen-5:
            playing = False
            pygame.mixer_music.unload()
            songpos_animstart = -2000
            percentage_anim = -2000
            songpos = 0
            lastsounddata = 0
            if len(musicqueue) > musicnum:
                pygame.mixer_music.load(musicqueue[musicnum])
                pygame.mixer_music.play()
                pygame.mixer_music.pause()
                playing = False
            else:
                musicnum = 0
                pygame.mixer_music.load(musicqueue[musicnum])
                pygame.mixer_music.play()
                pygame.mixer_music.pause()
                playing = False


        try:
            while (songpos)/1000 > soundtime[lastsounddata]:
                lastsounddata += 1 
            
        except IndexError:
            lastsounddata = 0


        

        
        
        
        
        xnum = 0
        while xnum < (xwindow):
            try:
                linesrender_formula = xnum-(xwindow//2)+((lastsounddata)//devisionby)
                if linesrender_formula < 0:
                    xnum += 1
                    continue
                renderinglist = devision_to_list_dict[devisionby]

                pygame.draw.line(mainwindow,(255,255,255),
                                 (xnum,(ywindow/2)+((ywindow/2)*(renderinglist[linesrender_formula][0]))),
                                 (xnum,(ywindow/2)-((ywindow/2)*(renderinglist[linesrender_formula][1]))))

                xnum += 1 
            except IndexError:
                xnum += 1

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 32: #spacebar
                    if playing:
                        pygame.mixer_music.pause()
                        playing = False
                    else:
                        pygame.mixer_music.unpause()
                        playing = True

                if event.key == 27: #esc
                    playing = False
                    pygame.mixer_music.pause()
                    settingsscene = True
                    visualizerscene = False

                if event.key == 99 or event.key == 127: # c or del
                    pygame.quit()
                    sys.exit()
                if event.key == 116: #t
                    if transparent_window:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,255,0)), 0, win32con.LWA_COLORKEY)
                        transparent_window = False
                        songpos_animstart = songpos
                    else:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)
                        transparent_window = True
                        songpos_animstart = songpos
                if event.key == 111: #o
                    if ontop_window:
                        ontop_window = False
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)
                        songpos_animstart = songpos
                    else:
                        ontop_window = True
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)
                        songpos_animstart = songpos
                        
               # if event.key == 1073741904: #left arrow
                #    songposrewinding -= 500
                #    songpos = pygame.mixer_music.get_pos() + songposrewinding
                #    if songpos < 0:
                #        songposrewinding += songpos
                #        pygame.mixer_music.set_pos(0)
                #    else:
                #        pygame.mixer_music.set_pos(songpos/1000)
                #this is bad
                #if event.key == 1073741903: #right arrow
                    #songposrewinding += 500
                    #songpos = pygame.mixer_music.get_pos() + songposrewinding
                    #pygame.mixer_music.set_pos(songpos/1000)
                    
                if event.key == 1073741906: #up arrow
                    if musicvolume_percent < 100:
                        percentage_anim = songpos
                        musicvolume_percent += 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)
                if event.key == 1073741905: #down arrow
                    if musicvolume_percent > 0:
                        percentage_anim = songpos
                        musicvolume_percent -= 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    holdinglmb = True
                    holdingwindowstartx = event.pos[0]
                    holdingwindowstarty = event.pos[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    holdinglmb = False
            if event.type == pygame.MOUSEMOTION:
                if holdinglmb:
                    xposition += event.pos[0] - holdingwindowstartx
                    yposition += event.pos[1] - holdingwindowstarty
                    pygame.display.set_window_position((xposition,yposition))
            
            if event.type == pygame.WINDOWFOCUSLOST:
                if ontop_window:
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                    rect = win32gui.GetWindowRect(hwnd) 
                    x = rect[0]
                    y = rect[1]
                    w = rect[2] - x
                    h = rect[3] - y
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)
                else:
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                    rect = win32gui.GetWindowRect(hwnd) 
                    x = rect[0]
                    y = rect[1]
                    w = rect[2] - x
                    h = rect[3] - y
                    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)


        if playing == False:
            pygame.draw.line(mainwindow,(0,0,0),((xwindow/2)-50,(ywindow/2)+80),((xwindow/2)-50,(ywindow/2)-80),10)
            pygame.draw.line(mainwindow,(0,0,0),((xwindow/2)+50,(ywindow/2)+80),((xwindow/2)+50,(ywindow/2)-80),10)
        
        if songpos - percentage_anim < 1000:
            transparency = 255 - ((songpos - percentage_anim) // 4)
            if transparency < 256:
                percentage_text = pygame.font.SysFont('couriernew',150).render(str(musicvolume_percent)+'%',False,(0,0,0))
                percentage_text.set_alpha(transparency)
                mainwindow.blit(percentage_text,((xwindow/2)-(percentage_text.get_width()/2),(ywindow/2)-(percentage_text.get_height()/2)))

        if songpos - songpos_animstart < 1000:
            transparency = 255 - ((songpos - songpos_animstart) // 4)
            if transparency < 256:
                donetext = pygame.font.SysFont('couriernew',150).render('Done!',False,(0,0,0))
                donetext.set_alpha(transparency)
                mainwindow.blit(donetext,((xwindow/2)-(donetext.get_width()/2),(ywindow/2)-(donetext.get_height()/2)))



        pygame.draw.lines(mainwindow,(0,0,255,255),False, [(0,0),(0,ywindow-1),(xwindow-1,ywindow-1),(xwindow-1,0),(0,0)])
        pygame.draw.line(mainwindow,(0,0,128),((xwindow/2)-1,10),((xwindow/2)-1,ywindow-10))
        pygame.draw.line(mainwindow,(0,0,128),((xwindow/2),10),((xwindow/2),ywindow-10))
        pygame.display.update()


























    if settingsscene:
        mainwindow.fill((0,0,128))
        
        buttons_text =       pygame.font.SysFont('couriernew',16).render('       Buttons       ',False,(255,255,255))
        mainwindow.blit(buttons_text,      (2,2))

        if s_transparent_anim < 60:
            s_transparent_anim += 1

            if transparent_window == True:
                t_transparent_text = pygame.font.SysFont('couriernew',16).render('T: Transparent',False,(255,255,255))
                t_transparent_text.set_alpha(255 - (s_transparent_anim * 4))
                mainwindow.blit(t_transparent_text,((2),((2*2)+buttons_text.get_height())))

                t_transparent_text = pygame.font.SysFont('couriernew',16).render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(s_transparent_anim * 4)
                mainwindow.blit(t_transparent_text,((2),((2*2)+buttons_text.get_height())))

            if transparent_window == False:
                t_transparent_text = pygame.font.SysFont('couriernew',16).render('T: Not transparent',False,(255,255,255))
                t_transparent_text.set_alpha(255 - (s_transparent_anim * 4))
                mainwindow.blit(t_transparent_text,((2),((2*2)+buttons_text.get_height())))

                t_transparent_text = pygame.font.SysFont('couriernew',16).render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(s_transparent_anim * 4)
                mainwindow.blit(t_transparent_text,((2),((2*2)+buttons_text.get_height())))

        else:
            t_transparent_text = pygame.font.SysFont('couriernew',16).render('T: Transparent window',False,(255,255,255))
            mainwindow.blit(t_transparent_text,((2),((2*2)+buttons_text.get_height())))



        if s_ontop_anim < 60:
            s_ontop_anim += 1

            if ontop_window == True:
                o_ontop_text =       pygame.font.SysFont('couriernew',16).render('O: On top',False,(255,255,255))
                o_ontop_text.set_alpha(255 - (s_ontop_anim * 4))
                mainwindow.blit(o_ontop_text,      ((2),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))
            
                o_ontop_text =       pygame.font.SysFont('couriernew',16).render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(s_ontop_anim * 4)
                mainwindow.blit(o_ontop_text,      ((2),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

            if ontop_window == False:
                o_ontop_text =       pygame.font.SysFont('couriernew',16).render('O: Not on top',False,(255,255,255))
                o_ontop_text.set_alpha(255 - (s_ontop_anim * 4))
                mainwindow.blit(o_ontop_text,      ((2),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))
            
                o_ontop_text =       pygame.font.SysFont('couriernew',16).render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(s_ontop_anim * 4)
                mainwindow.blit(o_ontop_text,      ((2),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        else:
            o_ontop_text =       pygame.font.SysFont('couriernew',16).render('O: Always on top window',False,(255,255,255))
            mainwindow.blit(o_ontop_text,      ((2),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        if s_volchange_anim < 60:
            s_volchange_anim += 1


            ua_volup_text =      pygame.font.SysFont('couriernew',16).render('Up arrow: '+str(musicvolume_percent)+'%',False,(255,255,255))
            ua_volup_text.set_alpha(255 - (s_volchange_anim * 4))
            mainwindow.blit(ua_volup_text,      ((2),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            ua_volup_text =      pygame.font.SysFont('couriernew',16).render('Up arrow: Volume up',False,(255,255,255))
            ua_volup_text.set_alpha(s_volchange_anim * 4)
            mainwindow.blit(ua_volup_text,      ((2),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))


            da_voldown_text =      pygame.font.SysFont('couriernew',16).render('Down arrow: '+str(musicvolume_percent)+'%',False,(255,255,255))
            da_voldown_text.set_alpha(255 - (s_volchange_anim * 4))
            mainwindow.blit(da_voldown_text,      ((2),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

            da_voldown_text =      pygame.font.SysFont('couriernew',16).render('Down arrow: Volume down',False,(255,255,255))
            da_voldown_text.set_alpha(s_volchange_anim * 4)
            mainwindow.blit(da_voldown_text,      ((2),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))


        else:
            ua_volup_text =      pygame.font.SysFont('couriernew',16).render('Up arrow: Volume up',False,(255,255,255))
            mainwindow.blit(ua_volup_text,      ((2),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            da_voldown_text =      pygame.font.SysFont('couriernew',16).render('Down arrow: Volume down',False,(255,255,255))
            mainwindow.blit(da_voldown_text,      ((2),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

        
        c_close_text =       pygame.font.SysFont('couriernew',16).render('C: Close the window',False,(255,255,255))
        mainwindow.blit(c_close_text,      ((2),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

        esc_back_text =      pygame.font.SysFont('couriernew',16).render('Esc: Back to the visualizer',False,(255,255,255))
        mainwindow.blit(esc_back_text,     ((2),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))
        


        for event in pygame.event.get():
            print(event)
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 27: #esc
                    settingsscene = False
                    visualizerscene = True

                if event.key == 99 or event.key == 127: # c or del
                    pygame.quit()
                    sys.exit()



                if event.key == 116: #t
                    if transparent_window:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,255,0)), 0, win32con.LWA_COLORKEY)
                        transparent_window = False
                        s_transparent_anim = 0
                    else:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)
                        transparent_window = True
                        s_transparent_anim = 0



                if event.key == 111: #o
                    s_ontop_anim = 0
                    if ontop_window:
                        ontop_window = False
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)
                    else:
                        ontop_window = True
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)

                        


               # if event.key == 1073741904: #left arrow
                #    songposrewinding -= 500
                #    songpos = pygame.mixer_music.get_pos() + songposrewinding
                #    if songpos < 0:
                #        songposrewinding += songpos
                #        pygame.mixer_music.set_pos(0)
                #    else:
                #        pygame.mixer_music.set_pos(songpos/1000)
                #this is bad
                #if event.key == 1073741903: #right arrow
                    #songposrewinding += 500
                    #songpos = pygame.mixer_music.get_pos() + songposrewinding
                    #pygame.mixer_music.set_pos(songpos/1000)
                    
                if event.key == 1073741906: #up arrow
                    if musicvolume_percent != 100:
                        musicvolume_percent += 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)
                        s_volchange_anim = 0
                if event.key == 1073741905: #down arrow
                    if musicvolume_percent != 0:
                        musicvolume_percent -= 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)
                        s_volchange_anim = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    holdinglmb = True
                    holdingwindowstartx = event.pos[0]
                    holdingwindowstarty = event.pos[1]
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    holdinglmb = False
            if event.type == pygame.MOUSEMOTION:
                if holdinglmb:
                    xposition += event.pos[0] - holdingwindowstartx
                    yposition += event.pos[1] - holdingwindowstarty
                    pygame.display.set_window_position((xposition,yposition))
            
            if event.type == pygame.WINDOWFOCUSLOST:
                if ontop_window:
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                    rect = win32gui.GetWindowRect(hwnd) 
                    x = rect[0]
                    y = rect[1]
                    w = rect[2] - x
                    h = rect[3] - y
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)
                else:
                    win32gui.BringWindowToTop(hwnd)
                    win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                    rect = win32gui.GetWindowRect(hwnd) 
                    x = rect[0]
                    y = rect[1]
                    w = rect[2] - x
                    h = rect[3] - y
                    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)

        pygame.draw.lines(mainwindow,(0,0,255,255),False, [(0,0),(0,ywindow-1),(xwindow-1,ywindow-1),(xwindow-1,0),(0,0)])

        pygame.display.update()

        pygame.Clock().tick(60)
