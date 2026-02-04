
""" things to add: 

fix lag in song queue scene when theres too many songs

get this script to be more object oriented #done

add osciloscope mode

add a shuffle button for song queue
add a button to reverse the song order in song queue
add a button to view the song in windows explorer

make animation depend on pc time instead of avgfps #done

fix window not responding in loading scenes #done

add new visualizer mode that listens to your pc audio in real time

replace easygui with tkinter filedialog

add more scenes for bg color customization

add devmode that lists fps, all globals, etc. #done

fix lagging in settings for some reason

"""
#all of this is not stable and not done at all

import soundfile #not installing on android

import pygame #ce

import os
import sys

import easygui
import time

import gc


scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep

icons = {
    'jakeisalivee': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'JakeIsAlivee coffee cup.ico'),(64,64)),
    'telegram': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'Telegram.png'),(64,64)),
    'folder': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'folder icon.png'),
    'moveup': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'moveup icon.png'),
    'movedown': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'movedown icon.png'),
    'delete': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'delete icon.png'),
}

from tkinter import filedialog
import tkinter as tk
root = tk.Tk()
root.withdraw()
root.iconbitmap(scriptdirfolder+slash+'Data'+slash+'JakeIsAlivee coffee cup.ico') #for filedialog icon to show

contacts = {
    'GitHub':   'https://github.com/JakeIsAlivee',
    'Telegram': 'https://t.me/JakeCreations',
}

musicformats = {
    '.flac',
    '.mp3',
    '.mp2',
    '.ogg',
    '.wav',
}

"""

files len = 02:33
same files

loading for dtype float64
.flac        0.243-0.249
.mp3         0.208-0.211
.mp2         0.100-0.102
.ogg         0.385-0.392
.wav         0.075-0.082 #buggy with pygame.rewind

loading for dtype int32
.flac        0.234-0.238
.mp3         0.209-0.215
.mp2         0.099-0.101
.ogg         0.376-0.402
.wav         0.057-0.061 #buggy with pygame.rewind

loading for dtype int16 
.flac        0.230-0.244
.mp3         0.204-0.208
.mp2         0.095-0.098
.ogg         0.374-0.379
.wav         0.019-0.021 #buggy with pygame.rewind

"""
#int16 is the best one





pygame.init()

windowres = [600,260]
mainwindow = pygame.display.set_mode(windowres, pygame.NOFRAME)

pygame.display.set_caption("JakeIsAlivee's Visualizer")


pygame.display.set_icon(icons['jakeisalivee'])

desktopsize = pygame.display.get_desktop_sizes()[0]


windowpos = [(desktopsize[0]/2)-(windowres[0]/2),(desktopsize[1]/2)-(windowres[1]/2)]

pygame.display.set_window_position((windowpos[0],windowpos[1]))


windowinfo = pygame.display.get_wm_info()["window"]

import win32api
import win32con
import win32gui
win32gui.SetWindowLong(windowinfo, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(windowinfo, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)


def loading_render():

    mainwindow.fill((0,0,0))
    loadingtext = pygame.font.SysFont('couriernew',64).render('Loading...',False,(255,255,255))
    mainwindow.blit(loadingtext,((windowres[0]/2)-(loadingtext.get_width()/2),
                                 (windowres[1]/2)-(loadingtext.get_height()/2))) 

def set_transparency(chromakey: tuple):
    win32gui.SetLayeredWindowAttributes(windowinfo, win32api.RGB(*chromakey), 0, win32con.LWA_COLORKEY)

loading_render()
pygame.display.update()

set_transparency((0,0,0))
ontop = True
transparent = True

pygameclock = pygame.time.Clock()

def events_global(event):
    global windowinfo
    global windowpos
    global windowres
    global mainwindow
    global desktopsize
    global contacts

    global songpos
    global songpos_sync
    global songnum
    global songqueue
    global lastsounddata

    global musicvolume_percent
    global musicformats

    global soundrawdata
    global soundrate

    global mousebts_hold
    global mouseholddrag_startpos
    global scrollwheely

    global playing

    global rendering_modes
    global renderingmode_num
    global userzoom_to_devision_dict
    global devisionby


    global ontop
    global transparent

    global anim_ontop
    global anim_transparency
    global anim_song
    global anim_volume

    global devmode
    global devmodeactivation_list
    global lastevent

    lastevent = event

    if event.type == pygame.WINDOWCLOSE:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:

        if len(devmodeactivation_list) > 11:
            devmodeactivation_list.pop(0)
        devmodeactivation_list.append(event.unicode)

        if devmodeactivation_list == ['j','a','k','e','i','s','a','l','i','v','e','e']:
            devmodeactivation_list = ['h','e','l','l','o',' ','w','o','r','l','d','!']
            if devmode:
                devmode = False
            else:
                devmode = True

        

        if event.key == pygame.K_c or event.key == pygame.K_DELETE:
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONDOWN:
 
        if event.button == pygame.BUTTON_RIGHT:
            mousebts_hold[2] = True 
            mouseholddrag_startpos = [event.pos[0],event.pos[1]]
                
        if event.button == pygame.BUTTON_WHEELUP:

            if mousebts_hold[0]:
                if windowres[1] < desktopsize[1]:
                    windowres[1] += 10
                    mouseholddrag_startpos[1] += 5
                    windowpos[1] -= 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))

            if mousebts_hold[2]:
                if windowres[0] < desktopsize[0]:
                    windowres[0] += 10
                    mouseholddrag_startpos[0] += 5
                    windowpos[0] -= 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
        
                    

        if event.button == pygame.BUTTON_WHEELDOWN:
                    
            if mousebts_hold[0]:
                if windowres[1] > 10:
                    windowres[1] -= 10
                    mouseholddrag_startpos[1] -= 5
                    windowpos[1] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))

            if mousebts_hold[2]:
                if windowres[0] > 10:
                    windowres[0] -= 10
                    mouseholddrag_startpos[0] -= 5
                    windowpos[0] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            mousebts_hold[0] = False
        if event.button == pygame.BUTTON_RIGHT:
            mousebts_hold[2] = False

                
    if event.type == pygame.MOUSEMOTION:
        if mousebts_hold[0] or mousebts_hold[2]:
            windowpos[0] += event.pos[0] - mouseholddrag_startpos[0]
            windowpos[1] += event.pos[1] - mouseholddrag_startpos[1]
            pygame.display.set_window_position((windowpos[0],windowpos[1]))

    if event.type == pygame.WINDOWFOCUSLOST:
        set_ontop(ontop)

def set_ontop(bool: bool):
    if bool == True:
        
        win32gui.BringWindowToTop(windowinfo)

        win32gui.ShowWindow(windowinfo, win32con.HWND_TOPMOST)
        rect = win32gui.GetWindowRect(windowinfo) 
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        win32gui.SetWindowPos(windowinfo, win32con.HWND_TOPMOST, x,y,w,h, 0)


    if bool == False:
        win32gui.BringWindowToTop(windowinfo)

        win32gui.ShowWindow(windowinfo, win32con.HWND_NOTOPMOST)
        rect = win32gui.GetWindowRect(windowinfo) 
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        win32gui.SetWindowPos(windowinfo, win32con.HWND_NOTOPMOST, x,y,w,h, 0)


class Song:
    def __init__(self, songdir: str):
        self.songdir = songdir
        self.rawfile = open(songdir,'r') #so the user could not delete the song file while it is imported in the program #should ALWAYS get closed when deleted from the program
        self.songlength = pygame.Sound(self.songdir).get_length()*1000 #this one takes too much time to get length
        
    def load(self, musicvolume: int):
        globals()['songformat'] = os.path.splitext(self.songdir)[1]
        pygame.mixer_music.load(self.songdir)
        pygame.mixer_music.set_volume(musicvolume/100)
        pygame.mixer_music.play()   
        pygame.mixer_music.pause()

        soundrawdata, rate = soundfile.read(self.songdir, dtype='int16', always_2d=True)

        try:
            soundrawdata[0][0]
            return soundrawdata, rate
        except TypeError:
            return soundrawdata, rate

def songreset():
    pygame.mixer_music.unload()
    globals()['songpos'] = 0
    globals()['songpos_sync'] = 0
    globals()['lastsounddata'] = 0
        
songformat = ''

songnum = 0

musicvolume_percent = 50


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

# mmb has no use right now
#                 lmb   mmb   rmb
mousebts_hold = [False,False,False]
mouseholddrag_startpos = [0,0]

scene = 'visualizer'
"""
visualizer > settings > songqueue
                      > controls
                      > customize

"""


scrollwheely = 0

anim_transparency = 0
anim_ontop = 0

anim_volume = 0

anim_song = 0


def fonts_couriernew(size):
    return pygame.font.SysFont('couriernew',size)

def fonts_JhengHei(size):
    return pygame.font.SysFont('Microsoft JhengHei',size)

songpos_sync = 0

linelength = 0.2

# 12 len list, write "jakeisalivee" to activate devmode
devmodeactivation_list = []
devmode = False
devrender_num = 0
devrender_surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCCOLORKEY)
devrender_surface.set_colorkey((255,255,255))
devrender_surface.fill((255,255,255))
lastevent = ''


def render_devstuff():
    global mainwindow
    global devrender_num
    global windowres
    global devrender_surface
    global devrender_num
    global lastevent

    if devmodeactivation_list[len(devmodeactivation_list)-1] != '\x08':
        curglobals = [
            'desktopsize: '+str(globals()['desktopsize']),
            'windowpos: '+str(globals()['windowpos']),
            'windowres: '+str(globals()['windowres']),
            ' ',
            'mousebts_hold: '+str(globals()['mousebts_hold']),
            'mouseholddrag_startpos: '+str(globals()['mouseholddrag_startpos']),
            'musicvolume_percent: '+str(globals()['musicvolume_percent']),
            ' ',
            'scene: '+str(globals()['scene']),
            ' ',
            'playing: '+str(globals()['playing']),
            'songpos: '+str(globals()['songpos']),
            'songpos_sync: '+str(globals()['songpos_sync']),
            'songnum: '+str(globals()['songnum']),
            ' ',
            'soundrate: '+str(globals()['soundrate']),
            'lastsounddata: '+str(globals()['lastsounddata']),
            'devisionby: '+str(globals()['devisionby']),
            'songformat: '+str(globals()['songformat']),
            '(not customizable) linelength: '+str(globals()['linelength']),
            'renderingmode_num: '+str(globals()['renderingmode_num']),
            'scrollwheely: '+str(globals()['scrollwheely']),
            ' ',
            'cursongdir: '+str(globals()['songqueue'][globals()['songnum']].songdir),
            'cursonglength: '+str(globals()['songqueue'][globals()['songnum']].songlength),
            ' ',
            'transparent: '+str(globals()['transparent']),
            'ontop: '+str(globals()['ontop']),
        ]

        if devrender_surface.get_size()[0] != windowres[0] or devrender_surface.get_size()[1] != windowres[1]:
            devrender_surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCCOLORKEY)
            devrender_surface.set_colorkey((255,255,255))
            devrender_surface.fill((255,255,255))

        if devrender_num > len(curglobals)-1:
            devrender_num = 0
        else:
            showglobals = fonts_couriernew(12).render(str(curglobals[devrender_num]),False,(0,0,0))
            transparentbg = pygame.Surface((windowres[0],12))
            transparentbg.fill((255,255,255))
            devrender_surface.blit(transparentbg,(0,13*devrender_num))
            devrender_surface.blit(showglobals,(0,13*devrender_num))
            devrender_num += 1
    else:
        devrender_surface.fill((255,255,255))
    mainwindow.blit(devrender_surface,(0,0))

    showlastevent = fonts_couriernew(12).render(str(lastevent),False,(0,0,0))
    mainwindow.blit(showlastevent,(0,windowres[1]-13))

    showfps = fonts_couriernew(32).render('FPS: '+str(int(pygameclock.get_fps())),False,(0,0,0))
    mainwindow.blit(showfps,(windowres[0]-showfps.get_width(),
                             windowres[1]-showfps.get_height()))

def scenes():
    global windowinfo
    global windowpos
    global windowres
    global mainwindow
    global desktopsize
    global contacts
    global scene

    global songpos
    global songpos_sync
    global songnum
    global songqueue
    global lastsounddata
    global songformat
    
    global musicvolume_percent
    global musicformats

    global soundrawdata
    global soundrate

    global mousebts_hold
    global mouseholddrag_startpos
    global scrollwheely

    global playing

    global rendering_modes
    global renderingmode_num
    global linelength
    
    global userzoom_to_devision_dict
    global devisionby


    global ontop
    global transparent

    global anim_ontop
    global anim_transparency
    global anim_song
    global anim_volume

    if scene == 'visualizer':
       
        mainwindow.fill((0,0,254))

        songpos = pygame.mixer_music.get_pos() + songpos_sync

        if songpos > songqueue[songnum].songlength: #song ended
            songreset() 
            if len(songqueue)-1 > songnum:

                songnum += 1
                soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                playing = True
                pygame.mixer_music.unpause()
            else:
                songnum = 0
                soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                playing = False



        lastsounddata = int(songpos * soundrate/1000)



        if songformat != '.wav':
            #songsync
            if songpos % 10000 >= 9990:
                pygame.mixer_music.rewind()
                pygame.mixer_music.play(0,songpos/1000)
                songpos_sync = songpos


        xnum = 0
        while xnum < windowres[0]:
            try:
                
                rendering_formulas = [
                    int(xnum)-(windowres[0]//2)+((lastsounddata)//devisionby),
                    0-int(xnum)+(windowres[0]//2)+((lastsounddata)//devisionby),
                    0-int(xnum)+(windowres[0])+((lastsounddata)//devisionby),
                    int(xnum)-(windowres[0])+((lastsounddata)//devisionby),
                    int(xnum)+((lastsounddata)//devisionby),
                    0-int(xnum)+((lastsounddata)//devisionby),
                    0-int(xnum)+(windowres[0])+((lastsounddata)//devisionby),
                    int(xnum)-(windowres[0])+((lastsounddata)//devisionby),
                ]

                linesrender_formula = rendering_formulas[renderingmode_num]
               

                if linesrender_formula < 0:
                    xnum += 1
                    continue

                if renderingmode_num == 2 or renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    pygame.draw.line(mainwindow,(255,255,255),
                             (int(xnum)//2,(windowres[1]/2)+((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                             (int(xnum)//2,(windowres[1]/2)-((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))
                    pygame.draw.line(mainwindow,(255,255,255),
                             (windowres[0]-int(xnum)//2,(windowres[1]/2)+((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                             (windowres[0]-int(xnum)//2,(windowres[1]/2)-((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))

                    xnum += 1
                    continue


                pygame.draw.line(mainwindow,(255,255,255),
                             (int(xnum),(windowres[1]/2)+((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                             (int(xnum),(windowres[1]/2)-((windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))

                xnum += 1
            except IndexError:
                xnum += 1

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playing:
                        pygame.mixer_music.pause()
                        playing = False
                    else:
                        pygame.mixer_music.unpause()
                        playing = True

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer_music.pause()
                    scene = 'settings'

                if event.key == pygame.K_t:
                    anim_transparency = time.perf_counter()

                    if transparent:
                        set_transparency((0,255,0))
                        transparent = False
                    else:
                        set_transparency((0,0,254))
                        transparent = True

                if event.key == pygame.K_o:
                    anim_ontop = time.perf_counter()

                    if ontop:
                        ontop = False
                        set_ontop(ontop)
                    else:
                        ontop = True
                        set_ontop(ontop)


                if event.key == pygame.K_LEFT:
                    songreset()

                    anim_song = time.perf_counter()

                    if songnum == 0:
                        songnum = len(songqueue)-1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()

                    else:
                        songnum -= 1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        if playing == True:
                            pygame.mixer_music.unpause()

                if event.key == pygame.K_RIGHT: #right arrow
                    time1 = time.perf_counter()
                    songreset()
                    print('songreset = '+str(time.perf_counter()-time1))

                    anim_song = time.perf_counter()

                    if len(songqueue)-1 > songnum:
                        songnum += 1
                        
                    else:
                        songnum = 0

                    time1 = time.perf_counter()
                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                    print('load = '+str(time.perf_counter()-time1))

                    if playing == True:
                        pygame.mixer_music.unpause()

                if event.key == pygame.K_UP: #up arrow
                    anim_volume = time.perf_counter()

                    if musicvolume_percent < 100:
                        musicvolume_percent += 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

                if event.key == pygame.K_DOWN: #down arrow
                    anim_volume = time.perf_counter()

                    if musicvolume_percent > 0:
                        musicvolume_percent -= 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]


        if playing == False:
            pygame.draw.line(mainwindow,(0,0,0),((windowres[0]/2)-50,(windowres[1]/2)+80),((windowres[0]/2)-50,(windowres[1]/2)-80),10)
            pygame.draw.line(mainwindow,(0,0,0),((windowres[0]/2)+50,(windowres[1]/2)+80),((windowres[0]/2)+50,(windowres[1]/2)-80),10)

        if anim_volume+1 > time.perf_counter():

            text_transparency = int((anim_volume+1 - time.perf_counter()) * 255)

            percentage_text = fonts_couriernew(150).render(str(musicvolume_percent)+'%',False,(0,0,0))
            percentage_text.set_alpha(text_transparency)
            mainwindow.blit(percentage_text,((windowres[0]/2)-(percentage_text.get_width()/2),
                                             (windowres[1]/2)-(percentage_text.get_height()/2)))
            del percentage_text

        if anim_transparency+1 > time.perf_counter():

            text_transparency = int((anim_transparency+1 - time.perf_counter()) * 255)

            donetext = fonts_couriernew(150).render('Done!',False,(0,0,0))
            donetext.set_alpha(text_transparency)
            mainwindow.blit(donetext,((windowres[0]/2)-(donetext.get_width()/2),
                                      (windowres[1]/2)-(donetext.get_height()/2)))
            del donetext
        
        if anim_ontop+1 > time.perf_counter():

            text_transparency = int((anim_ontop+1 - time.perf_counter()) * 255)

            donetext = fonts_couriernew(150).render('Done!',False,(0,0,0))
            donetext.set_alpha(text_transparency)
            mainwindow.blit(donetext,((windowres[0]/2)-(donetext.get_width()/2),
                                      (windowres[1]/2)-(donetext.get_height()/2)))
            del donetext

        if anim_song+1 > time.perf_counter():

            text_transparency = int((anim_song+1 - time.perf_counter()) * 255)

            songnum_text = fonts_couriernew(150).render(str(songnum+1),False,(0,0,0))
            songnum_text.set_alpha(text_transparency)
            mainwindow.blit(songnum_text,((windowres[0]/2)-(songnum_text.get_width()/2),
                                          (windowres[1]/2)-(songnum_text.get_height()/2)))
            del songnum_text

        if renderingmode_num < 4:
            pygame.draw.line(mainwindow,(0,0,128),((windowres[0]/2)-1,10),((windowres[0]/2)-1,windowres[1]-10))
            pygame.draw.line(mainwindow,(0,0,128),((windowres[0]/2),10)  ,((windowres[0]/2),  windowres[1]-10))





































    elif scene == 'settings':
        mainwindow.fill((0,0,128))

        buttons_text =       fonts_couriernew(16).render('         Controls',False,(255,255,255))
        mainwindow.blit(buttons_text,      (4,2))
        

        if anim_transparency+1 > time.perf_counter():

            text_transparency = int((anim_transparency+1 - time.perf_counter()) * 255)


            if transparent == True:
                t_transparent_text = fonts_couriernew(16).render('T: Transparent',False,(255,255,255))
                t_transparent_text.set_alpha(text_transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

                t_transparent_text = fonts_couriernew(16).render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(255-text_transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

            if transparent == False:
                t_transparent_text = fonts_couriernew(16).render('T: Not transparent',False,(255,255,255))
                t_transparent_text.set_alpha(text_transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

                t_transparent_text = fonts_couriernew(16).render('T: Transparent window',False,(255,255,255))
                t_transparent_text.set_alpha(255-text_transparency)
                mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

        else:
            t_transparent_text = fonts_couriernew(16).render('T: Transparent window',False,(255,255,255))
            mainwindow.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))




        if anim_ontop+1 > time.perf_counter() > 0:

            text_transparency = int((anim_ontop+1 - time.perf_counter()) * 255)

            if ontop == True:
                o_ontop_text =       fonts_couriernew(16).render('O: On top',False,(255,255,255))
                o_ontop_text.set_alpha(text_transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

                o_ontop_text =       fonts_couriernew(16).render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(255-text_transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

            if ontop == False:
                o_ontop_text =       fonts_couriernew(16).render('O: Not on top',False,(255,255,255))
                o_ontop_text.set_alpha(text_transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

                o_ontop_text =       fonts_couriernew(16).render('O: Always on top window',False,(255,255,255))
                o_ontop_text.set_alpha(255-text_transparency)
                mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        else:
            o_ontop_text =       fonts_couriernew(16).render('O: Always on top window',False,(255,255,255))
            mainwindow.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

        if anim_volume+1 > time.perf_counter() > 0:

            text_transparency = int((anim_volume+1 - time.perf_counter()) * 255)


            ua_volup_text =      fonts_couriernew(16).render('Up arrow:    '+str(musicvolume_percent)+'%',False,(255,255,255))
            ua_volup_text.set_alpha(text_transparency)
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            ua_volup_text =      fonts_couriernew(16).render('Up arrow:    Volume up',False,(255,255,255))
            ua_volup_text.set_alpha(255-text_transparency)
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))


            da_voldown_text =      fonts_couriernew(16).render('Down arrow:  '+str(musicvolume_percent)+'%',False,(255,255,255))
            da_voldown_text.set_alpha(text_transparency)
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

            da_voldown_text =      fonts_couriernew(16).render('Down arrow:  Volume down',False,(255,255,255))
            da_voldown_text.set_alpha(255-text_transparency)
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

        else:
            ua_volup_text =        fonts_couriernew(16).render('Up arrow:    Volume up',False,(255,255,255))
            mainwindow.blit(ua_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

            da_voldown_text =      fonts_couriernew(16).render('Down arrow:  Volume down',False,(255,255,255))
            mainwindow.blit(da_voldown_text,      ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))


        if anim_song+1 > time.perf_counter() > 0 > 0:

            text_transparency = int((anim_song+1 - time.perf_counter()) * 255)

            ra_nextsong_text =   fonts_couriernew(16).render('Right arrow: '+str(songnum+1),False,(255,255,255))
            ra_nextsong_text.set_alpha(text_transparency)
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

            la_nextsong_text =   fonts_couriernew(16).render('Left arrow:  '+str(songnum+1),False,(255,255,255))
            la_nextsong_text.set_alpha(text_transparency)
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))

            ra_nextsong_text =   fonts_couriernew(16).render('Right arrow: Next song',False,(255,255,255))
            ra_nextsong_text.set_alpha(255-text_transparency)
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

            la_nextsong_text =   fonts_couriernew(16).render('Left arrow:  Previous song',False,(255,255,255))
            la_nextsong_text.set_alpha(255-text_transparency)
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))

        else:
            ra_nextsong_text =   fonts_couriernew(16).render('Right arrow: Next song',False,(255,255,255))
            mainwindow.blit(ra_nextsong_text,   ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))

            la_nextsong_text =   fonts_couriernew(16).render('Left arrow:  Previous song',False,(255,255,255))
            mainwindow.blit(la_nextsong_text,   ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))

        movewin_text =           fonts_couriernew(16).render('Move window: Hold LMB or RMB',False,(255,255,255))
        mainwindow.blit(movewin_text,      ((4),((2*8)+buttons_text.get_height() +(t_transparent_text.get_height()*6))))
        changeresolution1_text = fonts_couriernew(16).render('Change resolution: Hold RMB or LMB',False,(255,255,255))
        mainwindow.blit(changeresolution1_text,      ((4),((2*9)+buttons_text.get_height() +(t_transparent_text.get_height()*7))))
        changeresolution2_text = fonts_couriernew(16).render('and scroll mouse wheel up or down',False,(255,255,255))
        mainwindow.blit(changeresolution2_text,      ((4),((2*10)+buttons_text.get_height() +(t_transparent_text.get_height()*8))))



        c_close_text =       fonts_couriernew(16).render('C: Close the window',False,(255,255,255))
        mainwindow.blit(c_close_text,      ((4),((2*11)+buttons_text.get_height() +(t_transparent_text.get_height()*9))))

        esc_back_text =      fonts_couriernew(16).render('Esc: Back to the visualizer',False,(255,255,255))
        mainwindow.blit(esc_back_text,     ((4),(windowres[1]-2-esc_back_text.get_height())))

        pygame.draw.line(mainwindow,(0,0,100),(changeresolution1_text.get_width()+8,0),(changeresolution1_text.get_width()+8,windowres[1]))


        zoom_text = fonts_couriernew(24).render(' Zoom: ',False,(255,255,255))
        mainwindow.blit(zoom_text, (windowres[0]-4-zoom_text.get_width(),

                                    2))

        zoomxnum_text = fonts_couriernew(24).render('<'+userzoom_to_devision_dict[devisionby]+'>',False,(255,255,255))
        mainwindow.blit(zoomxnum_text, (windowres[0]-4-zoomxnum_text.get_width(),

                                        2+zoom_text.get_height()+
                                        2))

        mode_text = fonts_couriernew(24).render('Mode:  ',False,(255,255,255))
        mainwindow.blit(mode_text, (windowres[0]-4-mode_text.get_width(),

                                    2+zoom_text.get_height()+
                                    2+zoomxnum_text.get_height()+
                                    2))

        modevisual_text = fonts_couriernew(24).render('< "'+str(rendering_modes[renderingmode_num])+'" >',False,(255,255,255))
        mainwindow.blit(modevisual_text, (windowres[0]-4-modevisual_text.get_width(),
                                          2+zoom_text.get_height()+
                                          2+zoomxnum_text.get_height()+
                                          2+mode_text.get_height()+
                                          2))

        songsqueue_text = fonts_couriernew(24).render('Song Queue',False,(255,255,255))
        mainwindow.blit(songsqueue_text, (windowres[0]-4-songsqueue_text.get_width(),
                                          2+zoom_text.get_height()+
                                          2+zoomxnum_text.get_height()+
                                          2+mode_text.get_height()+
                                          2+modevisual_text.get_height()+
                                          2))

        mainwindow.blit(pygame.transform.scale(icons['jakeisalivee'],(64,64)), (windowres[0]-68,windowres[1]-68))
        mainwindow.blit(pygame.transform.scale(icons['telegram'],(64,64)),(windowres[0]-136,windowres[1]-68))

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if playing:
                        pygame.mixer_music.unpause()
                    
                    scene = 'visualizer'



                if event.key == pygame.K_t: #t
                    
                    anim_transparency = time.perf_counter()

                    if transparent:
                        set_transparency((0,255,0))
                        transparent = False

                    else:
                        set_transparency((0,0,254))
                        transparent = True




                if event.key == pygame.K_o: 
                    anim_ontop = time.perf_counter()

                    if ontop:
                        ontop = False
                        set_ontop(ontop)
                    else:
                        ontop = True
                        set_ontop(ontop)


                if event.key == pygame.K_LEFT:
                    songreset()

                    anim_song = time.perf_counter()

                    if songnum == 0:
                        songnum = len(songqueue)-1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    else:
                        songnum -= 1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)


                if event.key == pygame.K_RIGHT:
                    songreset()

                    anim_song = time.perf_counter()

                    if len(songqueue)-1 > songnum:
                        songnum += 1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    else:
                        songnum = 0
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)


                if event.key == pygame.K_UP:
                    anim_volume = time.perf_counter()

                    if musicvolume_percent != 100:
                        musicvolume_percent += 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

                if event.key == pygame.K_DOWN: #down arrow
                    anim_volume = time.perf_counter()

                    if musicvolume_percent != 0:
                        musicvolume_percent -= 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)



            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range(windowres[0]-68,windowres[0]-4) and event.pos[1] in range(windowres[1]-68,windowres[1]-4):
                        os.system('start '+contacts['GitHub'])

                    elif event.pos[0] in range(windowres[0]-136,windowres[0]-72) and event.pos[1] in range(windowres[1]-68, windowres[1]-4):
                        os.system('start '+contacts['Telegram'])
						
                    elif event.pos[0] in range(windowres[0]-106,windowres[0]-88) and event.pos[1] in range(32,56): #- zoom
                        if devisionby != 1024:
                            devisionby *= 2

                    elif event.pos[0] in range(windowres[0]-18,windowres[0]-2) and event.pos[1] in range(32,56): #+ zoom
                        if devisionby != 1:
                            devisionby //= 2

                    elif event.pos[0] in range(windowres[0]-134,windowres[0]-116) and event.pos[1] in range(94,116): #- mode
                        if renderingmode_num != 0:
                            renderingmode_num -= 1

                    elif event.pos[0] in range(windowres[0]-18,windowres[0]-2) and event.pos[1] in range(94,116): #+ mode
                        if renderingmode_num != len(rendering_modes)-1:
                            renderingmode_num += 1

                    elif event.pos[0] in range(windowres[0]-148,windowres[0]-2) and event.pos[1] in range(124,150): #songsqueue scene
                        scene = 'songqueue'

                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]





































    elif scene == 'songqueue':
        
        mainwindow.fill((0,0,128))

        songsqueue_text = fonts_couriernew(24).render('Song queue',False,(255,255,255))
        mainwindow.blit(songsqueue_text,(4,2-scrollwheely))
        pygame.draw.line(mainwindow,(0,0,255),(0,4+songsqueue_text.get_height()-scrollwheely),(windowres[0],4+songsqueue_text.get_height()-scrollwheely))

        mainwindow.blit(icons['folder'],(windowres[0]-28,4-scrollwheely))

        songsrendernum = 1
        while songsrendernum <= len(songqueue):

            songdir = os.path.split(songqueue[songsrendernum-1].songdir)[1]
            if len(songdir) > ((windowres[0]-90)/12):
                songdir = songdir[0:((windowres[0]-90)//12)]+'...'
                

            songdir_text = fonts_JhengHei(16).render(' '+str(songsrendernum)+'. "'+str(songdir)+'"',False,(255,255,255))

            mainwindow.blit(songdir_text,(4,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollwheely))
            pygame.draw.line(mainwindow,(0,0,255),(0,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+songsqueue_text.get_height()-scrollwheely),(windowres[0],(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+songsqueue_text.get_height()-scrollwheely))

            mainwindow.blit(icons['delete'],(windowres[0]-28,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollwheely))
            mainwindow.blit(icons['movedown'],(windowres[0]-56,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollwheely))
            mainwindow.blit(icons['moveup'],(windowres[0]-84,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4-scrollwheely))


            songsrendernum += 1

        addsong_text = fonts_couriernew(24).render('+',False,(255,255,255))
        mainwindow.blit(addsong_text,(4,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollwheely))


        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    if event.pos[0] in range(4,4+addsong_text.get_width()) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollwheely): #add song
                        set_ontop(False) #so the window doesnt cover the windows file manager

                        addsong_file = easygui.fileopenbox('Select your music file to visualize',"JakeIsAlivee's Visualizer")
                        if addsong_file == None:
                            continue
                            
                        while addsong_file[len(addsong_file)-4:len(addsong_file)] not in musicformats and addsong_file[len(addsong_file)-5:len(addsong_file)] not in musicformats:
                            addsong_file = easygui.fileopenbox("This music format doesn't work for this program. Try selecting a .wav, .ogg, .mp3 or a .flac file instead.","JakeIsAlivee's Visualizer")
                            if addsong_file == None:
                                break
                        if addsong_file == None:
                            continue

                        songqueue.append(Song(addsong_file))

                        set_ontop(ontop)


                    if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range(4-scrollwheely,28-scrollwheely): #folder import
                        set_ontop(False) #so the window doesnt cover the windows file manager

                        import_folder = easygui.diropenbox('Choose the folder that you want to import .wav files from','Visualizer',scriptdirfolder+slash)
                        if import_folder == None:
                            set_ontop(ontop)
                            continue
                            
                        songreset()
                        songnum = 0

                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        musicfiles = os.listdir(import_folder)
                        tempnum = 0
                        while tempnum < len(musicfiles):
                                
                            if musicfiles[tempnum][len(musicfiles[tempnum])-5:len(musicfiles[tempnum])] not in musicformats and musicfiles[tempnum][len(musicfiles[tempnum])-4:len(musicfiles[tempnum])] not in musicformats:
                                musicfiles.pop(tempnum)
                                continue

                            tempnum += 1

                        if len(musicfiles) == 0:
                            set_ontop(ontop)
                            continue

                        songqueue = []
                        tempnum = 0
                        while tempnum < len(musicfiles):
                            songqueue.append(Song(import_folder+slash+musicfiles[tempnum]))
                            tempnum += 1

                            loading_render()
                            loadedsongs_render = fonts_couriernew(64).render(str(tempnum+1)+'/'+str(len(musicfiles)),False,(255,255,255))
                            mainwindow.blit(loadedsongs_render,
                                            ((windowres[0]//2)-(loadedsongs_render.get_width()//2),
                                              windowres[1]    - loadedsongs_render.get_height()))
                                
                            for event in pygame.event.get():
                                events_global(event)
                            pygame.display.update()

                        set_ontop(ontop)
                        continue



                    while songsrendernum > 1:
                        songsrendernum -= 1

                        #delete song
                        if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollwheely):
                            if len(songqueue) > 1:
                                songqueue[songsrendernum-1].rawfile.close()
                                songqueue.pop(songsrendernum-1)
                                if songnum > len(songqueue)-1:

                                    songnum = len(songqueue)-1
                                        
                                    songreset()
                            
                                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)


                        #movedown song
                        if event.pos[0] in range(windowres[0]-56,windowres[0]-32) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollwheely):
                            movingsong = songqueue[songsrendernum-1]
                            songqueue.pop(songsrendernum-1)
                            songqueue.insert(songsrendernum,movingsong)

                        #moveup song
                        if event.pos[0] in range(windowres[0]-84,windowres[0]-60) and event.pos[1] in range((4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+4+addsong_text.get_height()-scrollwheely):
                            movingsong = songqueue[songsrendernum-1]
                            songqueue.pop(songsrendernum-1)
                            songqueue.insert(songsrendernum-2,movingsong)


                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                if event.button == pygame.BUTTON_WHEELUP:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely != 0:
                            scrollwheely -= 16

                if event.button == pygame.BUTTON_WHEELDOWN:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely < (4*songsrendernum)+(songsqueue_text.get_height()*songsrendernum)+2-windowres[1]+28:
                            scrollwheely += 16




for event in pygame.event.get():
    events_global(event)

try:
    selectedfile = filedialog.askopenfile(
        filetypes=[('MP3', '*.mp3'),
                   ('WAV', '*.wav'),
                   ('OGG', '*.ogg'),
                   ('FLAC','*.flac'),
                   ('mp2', '*.mp2')
                   ],
        title='Select your music file to visualize',
    ).name
except AttributeError: #NoneType file
    sys.exit()


songqueue = [Song(selectedfile)]
soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

set_ontop(True)
set_transparency((0,0,254))

while True:
    try:
        scenes()

        if devmode:
            render_devstuff()

        pygame.draw.lines(mainwindow,(0,0,255,255),False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)])

        pygame.display.update()

        pygameclock.tick()

    except Exception:
        easygui.exceptionbox('A Fatal Error Occured!\n\nPlease report this bug to the creator of this program.\nIm very sorry that this happened.\n\nThe program will now close.','Fatal Error!')
        pygame.quit()
        sys.exit()
       

