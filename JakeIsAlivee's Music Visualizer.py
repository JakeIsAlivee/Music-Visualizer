import soundfile

import pygame
import numpy

import os
import sys

import easygui
import time

import gc

scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
if scriptdirfolder.find('\\') != -1:
    slash = '\\'
else:
    slash = '/'

workingmusicformats_list = [
    '.flac',                   #0.30-0.33sec to load
    '.mp3',                    #0.26sec to load
    '.mp2', #yes i checked     #0.16-0.17sec to load
    '.ogg',                    #0.34-0.38sec to load
    '.wav',                    #fastest 0.06-0.08sec to load
]


selectedfile = easygui.fileopenbox('Select your music file to visualize',"JakeIsAlivee's Visualizer",scriptdirfolder+slash)
if selectedfile == None:
    sys.exit()

while selectedfile[len(selectedfile)-4:len(selectedfile)] not in workingmusicformats_list and selectedfile[len(selectedfile)-5:len(selectedfile)] not in workingmusicformats_list:
    selectedfile = easygui.fileopenbox("This music format doesn't work for this program. Try selecting a .wav, .ogg, .mp3 or a .flac file instead.","JakeIsAlivee's Visualizer",scriptdirfolder+slash)
    if selectedfile == None:
        sys.exit()

pygame.init()


xwindow = 600
ywindow = 260
mainwindow = pygame.display.set_mode((xwindow,ywindow), pygame.RESIZABLE | pygame.NOFRAME)

pygame.display.set_caption("JakeIsAlivee's Visualizer")
jakeisalivee_cup = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'JakeIsAlivee coffee cup.ico')
pygame.display.set_icon(jakeisalivee_cup)

folder_icon = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'folder icon.png')
moveup_icon = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'moveup icon.png')
movedown_icon = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'movedown icon.png')
delete_icon = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'delete icon.png')


xposition = (pygame.display.get_desktop_sizes()[0][0]/2)-(xwindow/2)
yposition = (pygame.display.get_desktop_sizes()[0][1]/2)-(ywindow/2)
pygame.display.set_window_position((xposition,yposition))

desktopsize = pygame.display.get_desktop_sizes()

import win32api
import win32con
import win32gui
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)



mainwindow.fill((0,0,0))
loadingtext = pygame.font.SysFont('couriernew',64).render('Loading...',False,(255,255,255))
mainwindow.blit(loadingtext,((xwindow/2)-(loadingtext.get_width()/2),(ywindow/2)-(loadingtext.get_height()/2))) 
miniloadingtext1row = pygame.font.SysFont('couriernew',16).render("If it's not responding, it doesn't",False,(255,255,255))
miniloadingtext2row = pygame.font.SysFont('couriernew',16).render("mean that it's stuck doing nothing",False,(255,255,255))
mainwindow.blit(miniloadingtext1row,((xwindow/2)-(miniloadingtext1row.get_width()/2),(ywindow-miniloadingtext1row.get_height()*2))) 
mainwindow.blit(miniloadingtext2row,((xwindow/2)-(miniloadingtext2row.get_width()/2),(ywindow-miniloadingtext2row.get_height()))) 
                        
pygame.display.update()

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,0)), 0, win32con.LWA_COLORKEY)




win32gui.BringWindowToTop(hwnd)

win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
rect = win32gui.GetWindowRect(hwnd) 
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)


class Song:
    def __init__(self, songdir: str):
        self.songdir = songdir
        self.songlen = pygame.Sound(songdir).get_length()*1000

    def pygame_load(self, musicvolume: int):

        pygame.mixer_music.load(self.songdir)
        pygame.mixer_music.set_volume(musicvolume/100)
        pygame.mixer_music.play()
        pygame.mixer_music.pause()

        soundrawdata, rate = soundfile.read(self.songdir)
        soundduration = len(soundrawdata) / rate
        soundtime = numpy.arange(0,soundduration,1/rate)

        yield soundrawdata
        yield rate
        yield soundtime
        
        try:
            soundrawdata[0][0]
            yield 2
        except TypeError:
            yield 1

        del soundrawdata
        del rate
        del soundduration
        del soundtime



songsqueue = [Song(selectedfile)]
songnum = 0

musicvolume_percent = 50

soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

songpos = 0

lastsounddata = 0



devisionby = 1


userzoom_to_devision_dict = {
    'x1024': 1,
    'x512 ': 2,
    'x256 ': 4,
    'x128 ': 8,
    'x64  ': 16,
    'x32  ': 32,
    'x16  ': 64,
    'x8   ': 128,
    'x4   ': 256,
    'x2   ': 512,
    'x1   ': 1024,

    1:    'x1024',
    2:    'x512 ',
    4:    'x256 ',
    8:    'x128 ',
    16:   'x64  ',
    32:   'x32  ',
    64:   'x16  ',
    128:  'x8   ',
    256:  'x4   ',
    512:  'x2   ',
    1024: 'x1   ',

}

rendering_modes = {
    0: '<|<',
    1: '>|>',
    2: '>|<',
    3: '<|>',

    4: '|<<',
    5: '|>>',
    6: '>>|',
    7: '<<|',
}

renderingmode_num = 0


playing = False
holdinglmb = False
holdingrmb = False

visualizerscene = True
settingsscene = False
queuescene = False
scrollmovey = 0

WASplaying = False

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)

#i have a DECENT idea of what is this win32 shit

transparent_window = True
ontop_window = True

done_anim = 0
percentage_anim = 0
songnum_anim = 0

transparentwin_anim = 0
ontopwin_anim = 0
volchange_anim = 0
songchange_anim = 0

buttonsfont = pygame.font.SysFont('couriernew',16)
zoomfont = pygame.font.SysFont('couriernew',24)

prevtimesecond = time.localtime().tm_sec
frames = 0
last10secfps = [800]

tempnum = 0
avgfps = 0
while tempnum < len(last10secfps):
    avgfps += last10secfps[tempnum]
    tempnum += 1
avgfps = avgfps / len(last10secfps)

def globalevents(event):
    global mainwindow
    global holdinglmb
    global holdingrmb
    global xposition
    global yposition
    global holdingwindowstartx
    global holdingwindowstarty
    global ywindow
    global xwindow

    if event.type == pygame.WINDOWCLOSE:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:
        if event.key == 99 or event.key == 127: # c or del
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            holdingrmb = True
            holdingwindowstartx = event.pos[0]
            holdingwindowstarty = event.pos[1]
                
        if event.button == 4:

            if holdinglmb:
                if ywindow < desktopsize[0][1]:
                    ywindow += 10
                    holdingwindowstarty += 5
                    yposition -= 5

                    mainwindow = pygame.display.set_mode((xwindow,ywindow),pygame.NOFRAME)
                    pygame.display.set_window_position((xposition,yposition))

            if holdingrmb:
                if xwindow < desktopsize[0][0]:
                    xwindow += 10
                    holdingwindowstartx += 5
                    xposition -= 5
                    mainwindow = pygame.display.set_mode((xwindow,ywindow),pygame.NOFRAME)
                    pygame.display.set_window_position((xposition,yposition))
                            
                    

        if event.button == 5:
                    
            if holdinglmb:
                if ywindow > 10:
                    ywindow -= 10
                    holdingwindowstarty -= 5
                    yposition += 5

                    mainwindow = pygame.display.set_mode((xwindow,ywindow),pygame.NOFRAME)
                    pygame.display.set_window_position((xposition,yposition))

            if holdingrmb:
                if xwindow > 10:
                    xwindow -= 10
                    holdingwindowstartx -= 5
                    xposition += 5

                    mainwindow = pygame.display.set_mode((xwindow,ywindow),pygame.NOFRAME)
                    pygame.display.set_window_position((xposition,yposition))
                    

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            holdinglmb = False
        if event.button == 3:
            holdingrmb = False

                
    if event.type == pygame.MOUSEMOTION:
        if holdinglmb or holdingrmb:
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



while True:
    
    frames += 1
    if prevtimesecond != time.localtime().tm_sec:
        prevtimesecond = time.localtime().tm_sec
        if len(last10secfps) > 10:
            last10secfps.pop(0)

        last10secfps.append(frames)
        frames = 0

        tempnum = 0
        avgfps = 0
        while tempnum < len(last10secfps):
            avgfps += last10secfps[tempnum]
            tempnum += 1
        avgfps = int(avgfps / len(last10secfps))


    if visualizerscene:

        mainwindow.fill((0,0,254))


        songpos = pygame.mixer_music.get_pos()
        
        if songpos > songsqueue[songnum].songlen-5: #song ended
            pygame.mixer_music.unload()
            songpos = 0
            lastsounddata = 0
            if len(songsqueue)-1 > songnum:

                songnum += 1
                soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)
                
                playing = True
                pygame.mixer_music.unpause()
            else:
                songnum = 0
                soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                playing = False


        lastsounddata = int(songpos * soundrate/1000)
        
        xnum = 0
        while xnum < (xwindow):
            try:
                if renderingmode_num == 0: #<|< done
                    linesrender_formula = int(xnum)-(xwindow//2)+((lastsounddata)//devisionby)
                if renderingmode_num == 1: #>|> done
                    linesrender_formula = 0-int(xnum)+(xwindow//2)+((lastsounddata)//devisionby)

                if renderingmode_num == 2: #>|< done
                    linesrender_formula = 0-int(xnum)+(xwindow)+((lastsounddata)//devisionby)
                if renderingmode_num == 3: #<|> done
                    linesrender_formula = int(xnum)-(xwindow)+((lastsounddata)//devisionby)

                if renderingmode_num == 4: #|<< done
                    linesrender_formula = int(xnum)+((lastsounddata)//devisionby)
                if renderingmode_num == 5: #|>> done
                    linesrender_formula = 0-int(xnum)+((lastsounddata)//devisionby)
                if renderingmode_num == 6: #>>| done
                    linesrender_formula = 0-int(xnum)+(xwindow)+((lastsounddata)//devisionby)
                if renderingmode_num == 7: #<<| done
                    linesrender_formula = int(xnum)-(xwindow)+((lastsounddata)//devisionby)


                if linesrender_formula < 0:
                    xnum += 1
                    continue

                if renderingmode_num == 2 or renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    if soundchannels == 2:
                        pygame.draw.line(mainwindow,(255,255,255),
                                 (int(xnum)//2,(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][0]))),
                                 (int(xnum)//2,(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][1]))))
                        pygame.draw.line(mainwindow,(255,255,255),
                                 (xwindow-int(xnum)//2,(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][0]))),
                                 (xwindow-int(xnum)//2,(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][1]))))
                        
                    if soundchannels == 1:
                        
                        pygame.draw.line(mainwindow,(255,255,255),
                                 (int(xnum)//2,(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))),
                                 (int(xnum)//2,(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))))
                        pygame.draw.line(mainwindow,(255,255,255),
                                 (xwindow-int(xnum)//2,(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))),
                                 (xwindow-int(xnum)//2,(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))))
                        
                    xnum += 1
                    continue

                if soundchannels == 2:
                    pygame.draw.line(mainwindow,(255,255,255),
                                 (int(xnum),(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][0]))),
                                 (int(xnum),(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula][1]))))
                if soundchannels == 1:
                    pygame.draw.line(mainwindow,(255,255,255),
                                 (int(xnum),(ywindow/2)+((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))),
                                 (int(xnum),(ywindow/2)-((ywindow/2)*(soundrawdata[::devisionby][linesrender_formula]))))

                xnum += 1
            except IndexError:
                xnum += 1

        for event in pygame.event.get():
            
            globalevents(event)

            if event.type == pygame.KEYDOWN:
                if event.key == 32: #spacebar
                    if playing:
                        pygame.mixer_music.pause()
                        playing = False
                    else:
                        pygame.mixer_music.unpause()
                        playing = True

                if event.key == 27: #esc
                    pygame.mixer_music.pause()

                    WASplaying = playing

                    settingsscene = True
                    visualizerscene = False
                    
                if event.key == 116: #t
                    if transparent_window:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,255,0)), 0, win32con.LWA_COLORKEY)
                        transparent_window = False
                        done_anim = avgfps // 2
                        doneanim_division = done_anim / 255
                    else:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)
                        transparent_window = True
                        done_anim = avgfps // 2
                        doneanim_division = done_anim / 255
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
                        done_anim = avgfps // 2
                        doneanim_division = done_anim / 255
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
                        done_anim = avgfps // 2
                        doneanim_division = done_anim / 255
                        
                if event.key == 1073741904: #left arrow
                    pygame.mixer_music.unload()
                    songpos = 0
                    lastsounddata = 0
                    songnum_anim = avgfps // 2
                    songnumanim_division = songnum_anim / 255

                    
                    if songnum == 0:
                        songnum = len(songsqueue)-1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()
                    
                    else:
                        songnum -= 1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()

                if event.key == 1073741903: #right arrow
                    pygame.mixer_music.unload()
                    songpos = 0
                    lastsounddata = 0
                    songnum_anim = avgfps // 2
                    songnumanim_division = songnum_anim / 255

                    if len(songsqueue)-1 > songnum:
                        songnum += 1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()

                    else:
                        songnum = 0
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()
                    
                if event.key == 1073741906: #up arrow
                    if musicvolume_percent < 100:
                        percentage_anim = avgfps // 2
                        percentageanim_division = percentage_anim / 255
                        musicvolume_percent += 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)
                if event.key == 1073741905: #down arrow
                    if musicvolume_percent > 0:
                        percentage_anim = avgfps // 2
                        percentageanim_division = percentage_anim / 255
                        musicvolume_percent -= 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    holdinglmb = True
                    holdingwindowstartx = event.pos[0]
                    holdingwindowstarty = event.pos[1]


        if playing == False:
            pygame.draw.line(mainwindow,(0,0,0),((xwindow/2)-50,(ywindow/2)+80),((xwindow/2)-50,(ywindow/2)-80),10)
            pygame.draw.line(mainwindow,(0,0,0),((xwindow/2)+50,(ywindow/2)+80),((xwindow/2)+50,(ywindow/2)-80),10)
        
        if percentage_anim > 0:
            percentage_anim -= 1
            transparency = percentage_anim // percentageanim_division

            percentage_text = pygame.font.SysFont('couriernew',150).render(str(musicvolume_percent)+'%',False,(0,0,0))
            percentage_text.set_alpha(transparency)
            mainwindow.blit(percentage_text,((xwindow/2)-(percentage_text.get_width()/2),(ywindow/2)-(percentage_text.get_height()/2)))

        if done_anim > 0:
            done_anim -= 1
            transparency = done_anim // doneanim_division

            donetext = pygame.font.SysFont('couriernew',150).render('Done!',False,(0,0,0))
            donetext.set_alpha(transparency)
            mainwindow.blit(donetext,((xwindow/2)-(donetext.get_width()/2),(ywindow/2)-(donetext.get_height()/2)))

        if songnum_anim > 0:
            songnum_anim -= 1
            transparency = songnum_anim // songnumanim_division

            songnum_text = pygame.font.SysFont('couriernew',150).render(str(songnum+1),False,(0,0,0))
            songnum_text.set_alpha(transparency)
            mainwindow.blit(songnum_text,((xwindow/2)-(songnum_text.get_width()/2),(ywindow/2)-(songnum_text.get_height()/2)))


        if renderingmode_num < 4:
            pygame.draw.line(mainwindow,(0,0,128),((xwindow/2)-1,10),((xwindow/2)-1,ywindow-10))
            pygame.draw.line(mainwindow,(0,0,128),((xwindow/2),10),((xwindow/2),ywindow-10))



























    if settingsscene:
        mainwindow.fill((0,0,128))
        
        buttons_text =       buttonsfont.render('         Controls',False,(255,255,255))
        mainwindow.blit(buttons_text,      (4,2))


        if transparentwin_anim > 0:
            transparentwin_anim -= 1
            transparency = transparentwin_anim // transparentwinanim_division

            if transparent_window == True:
                t_transparent_text = buttonsfont.render('T: Transparent',False,(255,255,255))
                t_transparent_text.set_alpha(transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

                t_transparent_text = buttonsfont.render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(255-transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

            if transparent_window == False:
                t_transparent_text = buttonsfont.render('T: Not transparent',False,(255,255,255))
                t_transparent_text.set_alpha(transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

                t_transparent_text = buttonsfont.render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(255-transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

        else:
            t_transparent_text = buttonsfont.render('T: Transparent window',False,(255,255,255))
            mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))



        if ontopwin_anim > 0:
            ontopwin_anim -= 1
            transparency = ontopwin_anim // ontopwinanim_division

            if ontop_window == True:
                o_ontop_text =       buttonsfont.render('O: On top',False,(255,255,255))
                o_ontop_text.set_alpha(transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))
            
                o_ontop_text =       buttonsfont.render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(255-transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

            if ontop_window == False:
                o_ontop_text =       buttonsfont.render('O: Not on top',False,(255,255,255))
                o_ontop_text.set_alpha(transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))
            
                o_ontop_text =       buttonsfont.render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(255-transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        else:
            o_ontop_text =       buttonsfont.render('O: Always on top window',False,(255,255,255))
            mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        if volchange_anim > 0:
            volchange_anim -= 1
            transparency = volchange_anim // volchangeanim_devision


            ua_volup_text =      buttonsfont.render('Up arrow:    '+str(musicvolume_percent)+'%',False,(255,255,255))
            ua_volup_text.set_alpha(transparency)
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            ua_volup_text =      buttonsfont.render('Up arrow:    Volume up',False,(255,255,255))
            ua_volup_text.set_alpha(255-transparency)
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))


            da_voldown_text =      buttonsfont.render('Down arrow:  '+str(musicvolume_percent)+'%',False,(255,255,255))
            da_voldown_text.set_alpha(transparency)
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

            da_voldown_text =      buttonsfont.render('Down arrow:  Volume down',False,(255,255,255))
            da_voldown_text.set_alpha(255-transparency)
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))


        else:
            ua_volup_text =        buttonsfont.render('Up arrow:    Volume up',False,(255,255,255))
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            da_voldown_text =      buttonsfont.render('Down arrow:  Volume down',False,(255,255,255))
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

        if songchange_anim > 0:
            songchange_anim -= 1
            transparency = songchange_anim // songchangeanim_division

            ra_nextsong_text =   buttonsfont.render('Right arrow: '+str(songnum+1),False,(255,255,255))
            ra_nextsong_text.set_alpha(transparency)
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

            la_nextsong_text =   buttonsfont.render('Left arrow:  '+str(songnum+1),False,(255,255,255))
            la_nextsong_text.set_alpha(transparency)
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))

            ra_nextsong_text =   buttonsfont.render('Right arrow: Next song',False,(255,255,255))
            ra_nextsong_text.set_alpha(255-transparency)
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

            la_nextsong_text =   buttonsfont.render('Left arrow:  Previous song',False,(255,255,255))
            la_nextsong_text.set_alpha(255-transparency)
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))



        else:
            ra_nextsong_text =   buttonsfont.render('Right arrow: Next song',False,(255,255,255))
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))
        
            la_nextsong_text =   buttonsfont.render('Left arrow:  Previous song',False,(255,255,255))
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))

        movewin_text =           buttonsfont.render('Move window: Hold LMB or RMB',False,(255,255,255))
        mainwindow.blit(movewin_text,      ((4),((2*8)+buttons_text.get_height() +(t_transparent_text.get_height()*6))))
        changeresolution1_text = buttonsfont.render('Change resolution: Hold RMB or LMB',False,(255,255,255))
        mainwindow.blit(changeresolution1_text,      ((4),((2*9)+buttons_text.get_height() +(t_transparent_text.get_height()*7))))
        changeresolution2_text = buttonsfont.render('and scroll mouse wheel up or down',False,(255,255,255))
        mainwindow.blit(changeresolution2_text,      ((4),((2*10)+buttons_text.get_height() +(t_transparent_text.get_height()*8))))



        c_close_text =       buttonsfont.render('C: Close the window',False,(255,255,255))
        mainwindow.blit(c_close_text,      ((4),((2*11)+buttons_text.get_height() +(t_transparent_text.get_height()*9))))

        esc_back_text =      buttonsfont.render('Esc: Back to the visualizer',False,(255,255,255))
        mainwindow.blit(esc_back_text,     ((4),(ywindow-2-esc_back_text.get_height())))
        
        pygame.draw.line(mainwindow,(0,0,100),(changeresolution1_text.get_width()+8,0),(changeresolution1_text.get_width()+8,ywindow))


        zoom_text = zoomfont.render(' Zoom: ',False,(255,255,255))
        mainwindow.blit(zoom_text, (xwindow-4-zoom_text.get_width(),
                                    
                                    2))

        zoomxnum_text = zoomfont.render('<'+userzoom_to_devision_dict[devisionby]+'>',False,(255,255,255))
        mainwindow.blit(zoomxnum_text, (xwindow-4-zoomxnum_text.get_width(),
                                        
                                        2+zoom_text.get_height()+
                                        2))

        mode_text = zoomfont.render('Mode:  ',False,(255,255,255))
        mainwindow.blit(mode_text, (xwindow-4-mode_text.get_width(),
                                    
                                    2+zoom_text.get_height()+
                                    2+zoomxnum_text.get_height()+
                                    2))

        modevisual_text = zoomfont.render('< "'+str(rendering_modes[renderingmode_num])+'" >',False,(255,255,255))
        mainwindow.blit(modevisual_text, (xwindow-4-modevisual_text.get_width(),
                                          2+zoom_text.get_height()+
                                          2+zoomxnum_text.get_height()+
                                          2+mode_text.get_height()+
                                          2))
        
        songsqueue_text = zoomfont.render('Song Queue',False,(255,255,255))
        mainwindow.blit(songsqueue_text, (xwindow-4-songsqueue_text.get_width(),
                                          2+zoom_text.get_height()+
                                          2+zoomxnum_text.get_height()+
                                          2+mode_text.get_height()+
                                          2+modevisual_text.get_height()+
                                          2))

        mainwindow.blit(pygame.transform.scale(jakeisalivee_cup,(64,64)), (xwindow-68,ywindow-68))


        for event in pygame.event.get():

            globalevents(event)

            if event.type == pygame.KEYDOWN:
                if event.key == 27: #esc
                    if WASplaying:
                        pygame.mixer_music.unpause()
                        playing = True


                    settingsscene = False
                    visualizerscene = True



                if event.key == 116: #t
                    
                    transparentwin_anim = avgfps * 2
                    transparentwinanim_division = transparentwin_anim / 255

                    if transparent_window:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,255,0)), 0, win32con.LWA_COLORKEY)
                        transparent_window = False

                    else:
                        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*(0,0,254)), 0, win32con.LWA_COLORKEY)
                        transparent_window = True




                if event.key == 111: #o
                    ontopwin_anim = avgfps * 2
                    ontopwinanim_division = ontopwin_anim / 255

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


                if event.key == 1073741904: #left arrow
                    pygame.mixer_music.unload()
                    songpos = 0
                    lastsounddata = 0
                    songchange_anim = avgfps * 2
                    songchangeanim_division = songchange_anim / 255

                    if songnum == 0:
                        songnum = len(songsqueue)-1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)

                    else:
                        songnum -= 1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)


                if event.key == 1073741903: #right arrow
                    pygame.mixer_music.unload()
                    songpos = 0
                    lastsounddata = 0
                    songchange_anim = avgfps * 2
                    songchangeanim_division = songchange_anim / 255

                    if len(songsqueue)-1 > songnum:
                        songnum += 1
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)


                    else:
                        songnum = 0
                        soundrawdata, soundrate, soundtime, soundchannels = songsqueue[songnum].pygame_load(musicvolume_percent)


                if event.key == 1073741906: #up arrow
                    if musicvolume_percent != 100:
                        musicvolume_percent += 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

                        volchange_anim = avgfps * 2
                        volchangeanim_devision = volchange_anim / 255

                if event.key == 1073741905: #down arrow
                    if musicvolume_percent != 0:
                        musicvolume_percent -= 10
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

                        volchange_anim = avgfps * 2
                        volchangeanim_devision = volchange_anim / 255


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] in range(xwindow-68,xwindow-4) and event.pos[1] in range(ywindow-68,ywindow-4):
                        os.system('start https://github.com/JakeIsAlivee')

                    elif event.pos[0] in range(xwindow-106,xwindow-88) and event.pos[1] in range(32,56): #- zoom
                        if devisionby != 1024:
                            devisionby *= 2

                    elif event.pos[0] in range(xwindow-18,xwindow-2) and event.pos[1] in range(32,56): #+ zoom
                        if devisionby != 1:
                            devisionby //= 2

                    elif event.pos[0] in range(xwindow-134,xwindow-116) and event.pos[1] in range(94,116): #- mode
                        if renderingmode_num != 0:
                            renderingmode_num -= 1
                    
                    elif event.pos[0] in range(xwindow-18,xwindow-2) and event.pos[1] in range(94,116): #+ mode
                        if renderingmode_num != len(rendering_modes)-1:
                            renderingmode_num += 1

                    elif event.pos[0] in range(xwindow-148,xwindow-2) and event.pos[1] in range(124,150): #songsqueue scene
                        queuescene = True
                        settingsscene = False

                    else:
                        holdinglmb = True
                        holdingwindowstartx = event.pos[0]
                        holdingwindowstarty = event.pos[1]





    if queuescene:

        mainwindow.fill((0,0,128))

        songsqueue_text = zoomfont.render('Song queue',False,(255,255,255))
        mainwindow.blit(songsqueue_text,(4,2-scrollmovey))
        pygame.draw.line(mainwindow,(0,0,255),(0,4+songsqueue_text.get_height()-scrollmovey),(xwindow,4+songsqueue_text.get_height()-scrollmovey))

        mainwindow.blit(folder_icon,(xwindow-28,4-scrollmovey))

        songsrendernum = 1
        while songsrendernum <= len(songsqueue):

            songdir = os.path.split(songsqueue[songsrendernum-1].songdir)[1]
            if len(songdir) > 20:
                songdir = songdir[0:20]+'...'
            
            songdir_text = zoomfont.render(str(songsrendernum)+'. "'+str(songdir)+'"',False,(255,255,255))
            mainwindow.blit(songdir_text,(4,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollmovey))
            pygame.draw.line(mainwindow,(0,0,255),(0,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+songsqueue_text.get_height()-scrollmovey),(xwindow,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+songsqueue_text.get_height()-scrollmovey))
            
            mainwindow.blit(delete_icon,(xwindow-28,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollmovey))
            mainwindow.blit(movedown_icon,(xwindow-56,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollmovey))
            mainwindow.blit(moveup_icon,(xwindow-84,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollmovey))


            songsrendernum += 1

        addsong_text = zoomfont.render('+',False,(255,255,255))
        mainwindow.blit(addsong_text,(4,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollmovey))
            

        for event in pygame.event.get():

            globalevents(event)

            if event.type == pygame.KEYDOWN:
                if event.key == 27: #esc

                    settingsscene = True
                    queuescene = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if event.pos[0] in range(4,4+addsong_text.get_width()) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollmovey,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollmovey): #add song
                        #make not on top
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)

                        
                        addsong_file = easygui.fileopenbox('Select your music file to visualize',"JakeIsAlivee's Visualizer",scriptdirfolder+slash)
                        if addsong_file == None:
                            continue

                        while addsong_file[len(addsong_file)-4:len(addsong_file)] not in workingmusicformats_list and addsong_file[len(addsong_file)-5:len(addsong_file)] not in workingmusicformats_list:
                            addsong_file = easygui.fileopenbox("This music format doesn't work for this program. Try selecting a .wav, .ogg, .mp3 or a .flac file instead.","JakeIsAlivee's Visualizer",scriptdirfolder+slash)
                            if addsong_file == None:
                                continue

                        songsqueue.append(Song(addsong_file))

                        if ontop_window:
                            win32gui.BringWindowToTop(hwnd)
                            win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                            rect = win32gui.GetWindowRect(hwnd) 
                            x = rect[0]
                            y = rect[1]
                            w = rect[2] - x
                            h = rect[3] - y
                            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)


                    if event.pos[0] in range(xwindow-28,xwindow-4) and event.pos[1] in range(4-scrollmovey,28-scrollmovey): #folder import

                         #make not on top
                        win32gui.BringWindowToTop(hwnd)
                        win32gui.ShowWindow(hwnd, win32con.HWND_NOTOPMOST)
                        rect = win32gui.GetWindowRect(hwnd) 
                        x = rect[0]
                        y = rect[1]
                        w = rect[2] - x
                        h = rect[3] - y
                        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, x,y,w,h, 0)

                        import_folder = easygui.diropenbox('Choose the folder that you want to import .wav files from','Visualizer',scriptdirfolder+slash)
                        if import_folder == None:
                            if ontop_window:
                                win32gui.BringWindowToTop(hwnd)
                                win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                                rect = win32gui.GetWindowRect(hwnd) 
                                x = rect[0]
                                y = rect[1]
                                w = rect[2] - x
                                h = rect[3] - y
                                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)
                            continue

                        wavfiles = os.listdir(import_folder)
                        tempnum = 0
                        while tempnum < len(wavfiles):

                            if wavfiles[tempnum][len(wavfiles[tempnum])-5:len(wavfiles[tempnum])] not in workingmusicformats_list and wavfiles[tempnum][len(wavfiles[tempnum])-4:len(wavfiles[tempnum])] not in workingmusicformats_list:
                                wavfiles.pop(tempnum)
                                continue

                            tempnum += 1

                        if len(wavfiles) == 0:
                            if ontop_window:
                                win32gui.BringWindowToTop(hwnd)
                                win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                                rect = win32gui.GetWindowRect(hwnd) 
                                x = rect[0]
                                y = rect[1]
                                w = rect[2] - x
                                h = rect[3] - y
                                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)
                            continue
                        
                        
                        mainwindow.fill((0,0,0))
                        loadingtext = pygame.font.SysFont('couriernew',64).render('Loading...',False,(255,255,255))
                        mainwindow.blit(loadingtext,((xwindow/2)-(loadingtext.get_width()/2),(ywindow/2)-(loadingtext.get_height()/2))) 
                        miniloadingtext1row = pygame.font.SysFont('couriernew',16).render("If it's not responding, it doesn't",False,(255,255,255))
                        miniloadingtext2row = pygame.font.SysFont('couriernew',16).render("mean that it's stuck doing nothing",False,(255,255,255))
                        mainwindow.blit(miniloadingtext1row,((xwindow/2)-(miniloadingtext1row.get_width()/2),(ywindow-miniloadingtext1row.get_height()*2))) 
                        mainwindow.blit(miniloadingtext2row,((xwindow/2)-(miniloadingtext2row.get_width()/2),(ywindow-miniloadingtext2row.get_height()))) 
                        
                        pygame.display.update()

                        songsqueue = []
                        tempnum = 0
                        while tempnum < len(wavfiles):
                            songsqueue.append(Song(import_folder+slash+wavfiles[tempnum]))
                            tempnum += 1

                        if ontop_window:
                            win32gui.BringWindowToTop(hwnd)
                            win32gui.ShowWindow(hwnd, win32con.HWND_TOPMOST)
                            rect = win32gui.GetWindowRect(hwnd) 
                            x = rect[0]
                            y = rect[1]
                            w = rect[2] - x
                            h = rect[3] - y
                            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x,y,w,h, 0)



                    while songsrendernum > 1:
                        songsrendernum -= 1

                        #delete song
                        if event.pos[0] in range(xwindow-28,xwindow-4) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollmovey,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollmovey):
                            if len(songsqueue) > 1:
                                songsqueue.pop(songsrendernum-1)

                        #movedown song
                        if event.pos[0] in range(xwindow-56,xwindow-32) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollmovey,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollmovey):
                            movingsong = songsqueue[songsrendernum-1]
                            songsqueue.pop(songsrendernum-1)
                            songsqueue.insert(songsrendernum,movingsong)

                        #moveup song
                        if event.pos[0] in range(xwindow-84,xwindow-60) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollmovey,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollmovey):
                            movingsong = songsqueue[songsrendernum-1]
                            songsqueue.pop(songsrendernum-1)
                            songsqueue.insert(songsrendernum-2,movingsong)
                        

                    else:
                        holdinglmb = True
                        holdingwindowstartx = event.pos[0]
                        holdingwindowstarty = event.pos[1]

                if event.button == 4:
                    if not (holdingrmb or holdinglmb):
                        if scrollmovey != 0:
                            scrollmovey -= 16

                if event.button == 5:
                    if not (holdingrmb or holdinglmb):
                        if scrollmovey < (4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-ywindow+28:
                            scrollmovey += 16




    pygame.draw.lines(mainwindow,(0,0,255,255),False, [(0,0),(0,ywindow-1),(xwindow-1,ywindow-1),(xwindow-1,0),(0,0)])

    pygame.display.update()