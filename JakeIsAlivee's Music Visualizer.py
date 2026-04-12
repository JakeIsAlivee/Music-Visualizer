"""
list of things changed compared to the release version so far:
- Animations now depend on computer time instead of average program fps
- Settings interface rework
- New Customize panel
- New Program panel
- New Visualizer panel
- Link to the telegram channel
- More song queue functionality
- Small song queue interface changes
- All scenes fps optimizations

- Updated the loading screen so it doesnt confuse users like its not responding
- The loading screen now shows the number of songs it has imported
- The loading screen can now be transparent

- Added a visual effect if the window resolution gets too low for a specific scene

- Fixed bugs with audio positions

- Removed animations for "transparent", "always on top", "next/previous song" and "volume up/down" options in settings

- The program now doesnt let you just delete the music file that it loaded until you remove it from the song queue

- Small visualizer bug fixes

- Settings now show the version of the program
- Added a check if youre OS is windows or not

- Added Oscilloscope mode
- Added Waveform mode
- Added Waveform settings
- Added more Classic Mode settings

- Added Credits in Program settings (nothing there yet)


- Critical errors now show so much info about the error


- Switched to tkinter filedialog instead of easygui (less .exe size i think)


- Bug fixesssssssssss
- A lot of them
- Cant even count how many there was

"""



""" things to add: 

- Bars mode functionality and settings
- Oscilloscope mode options

- Write all controls in the controls scene
- Customization scene

- fix the bug where pixels between lines start to tweak tf out


[not possible/not compatible, or is it] add new visualizer mode that listens to your pc audio in real time 



"""

#all of this is pretty stable but not done at all

import soundfile #not installing on pydroid

import pygame #ce

import os
import sys

import time

import gc

import random

import pyaudio

VERSION = "WIP2.2.0"

scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep

def outputdevice_load_info():
    global outputdevice_name
    global latency

    p = pyaudio.PyAudio()

    outputdevice = p.get_default_output_device_info()
    outputdevice_name = outputdevice['name']
    latency = (outputdevice['defaultLowOutputLatency'])

    p.terminate()

outputdevice_load_info()

icons = {
    'jakeisalivee': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee coffee cup.ico'),(64,64)),
    'telegram': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Telegram.png'),(64,64)),

    'keyboard': pygame.transform.rotate(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Keyboard.png'),-15),
    'brush': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'draw.png'),
    'visualizer': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'visualizer icon.png'),
    'songqueue': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'music.png'),
    'program': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'program.png'),

    'folder': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'folder icon.png'),
    'shuffle': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'shuffle.png'),
    'reverse': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'reverse.png'),

    'moveup': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'moveup icon.png'),
    'movedown': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'movedown icon.png'),
    'delete': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'delete icon.png'),
    'view': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'view file.png'),
}

surface = pygame.Surface((64,64))
surface.fill((5,5,5))

icons['jakeisalivee'].set_colorkey((0,0,0))
surface.blit(icons['jakeisalivee'])

icons['jakeisalivee'] = surface
del surface

from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
root = tk.Tk()
root.withdraw()
root.iconbitmap(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee coffee cup.ico') #for filedialog icon to show

if str(sys.platform).lower()[0:3] != 'win':
    proceed = messagebox.askyesno('Incompatible OS',
                                  'This program was made for the WINDOWS system.\nYour system is: '+str(sys.platform).capitalize()+'\nIt is highly recomended that you close the program because it was NOT made for the system youre on and might crash immediately.\nProceed anyway?',
                                  icon='warning')
    if proceed == False:
        pygame.quit()
        sys.exit()

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


pygame.init()



windowres = [600,260]
mainwindow = pygame.display.set_mode(windowres, pygame.NOFRAME | pygame.SRCALPHA)

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

def offscreen_check():
    global windowpos
    global windowres
    global desktopsize

    if windowpos[0] < 0-windowres[0]+20:
        windowpos[0] = 0-windowres[0]+20
    if windowpos[0]+20 > desktopsize[0]:
        windowpos[0] = desktopsize[0]-20

    if windowpos[1] < 0-windowres[1]+20:
        windowpos[1] = 0-windowres[1]+20
    if windowpos[1]+60 > desktopsize[1]:
        windowpos[1] = desktopsize[1]-60

    pygame.display.set_window_position((windowpos[0],windowpos[1]))


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

    global soundrawdata
    global soundrate

    global mousebts_hold
    global mouseholddrag_startpos
    global scrollwheely

    global playing

    global devisionby


    global ontop
    global transparent

    global anim_ontop
    global anim_transparency
    global anim_song
    global anim_volume

    global devmode
    global devmodeactivation_list
    
    global displayupdate

    if devmode:
        print(event)

    if event.type == pygame.WINDOWCLOSE:
        pygame.quit()
        sys.exit()

    if event.type == pygame.KEYDOWN:

        if len(devmodeactivation_list) > 11:
            devmodeactivation_list.pop(0)
        devmodeactivation_list.append(event.unicode)

        if devmodeactivation_list == ['j','a','k','e','i','s','a','l','i','v','e','e']:
            devmodeactivation_list = ['b','l','e','h','h','h','h','h','h',' ',':','p']
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

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    displayupdate = True

            if mousebts_hold[2]:
                if windowres[0] < desktopsize[0]:
                    windowres[0] += 10
                    mouseholddrag_startpos[0] += 5
                    windowpos[0] -= 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    displayupdate = True
        
                    

        if event.button == pygame.BUTTON_WHEELDOWN:
                    
            if mousebts_hold[0]:
                if windowres[1] > 10:
                    windowres[1] -= 10
                    mouseholddrag_startpos[1] -= 5
                    windowpos[1] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    displayupdate = True

            if mousebts_hold[2]:
                if windowres[0] > 10:
                    windowres[0] -= 10
                    mouseholddrag_startpos[0] -= 5
                    windowpos[0] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    displayupdate = True

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            mousebts_hold[0] = False
        if event.button == pygame.BUTTON_RIGHT:
            mousebts_hold[2] = False

                
    if event.type == pygame.MOUSEMOTION:
        if mousebts_hold[0] or mousebts_hold[2]:
            windowpos[0] += event.pos[0] - mouseholddrag_startpos[0]
            windowpos[1] += event.pos[1] - mouseholddrag_startpos[1]

            offscreen_check()

    if event.type == pygame.WINDOWFOCUSLOST:
        set_ontop(ontop)
        
    if event.type == pygame.WINDOWFOCUSGAINED:
        offscreen_check()

    if event.type == pygame.WINDOWRESTORED:
        displayupdate = True


def set_ontop(bool: bool):
    if bool == True:
        win32gui.ShowWindow(windowinfo, win32con.HWND_TOPMOST)
        rect = win32gui.GetWindowRect(windowinfo) 
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        win32gui.SetWindowPos(windowinfo, win32con.HWND_TOPMOST, x,y,w,h, 0)

    if bool == False:
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

general_mode_names = {
    1: 'Classic',
    2: 'Waveform',
    3: 'Bars',
    4: 'Oscilloscope'
}


general_mode_num = 1

#classic and waveform have same rendering modes
cl_rendering_modes = {
    0: '<|<',
    1: '>|>',
    2: '>|<',
    3: '<|>',

    4: '|<<',
    5: '|>>',
    6: '>>|',
    7: '<<|',
}
cl_renderingmode_num = 0
cl_line_space = 0
cl_onedimensional = False
cl_mirrored = False
cl_rotate = 0
cl_linelength = 1.0

cl_zoom_typing = False
cl_zoom_typing_list = list(str(devisionby)+' ')
cl_line_space_typing = False
cl_line_space_typing_list = list(str(cl_line_space)+' ')
cl_rotate_typing = False
cl_rotate_typing_list = list(str(cl_rotate)+'° ')
cl_linelength_typing = False
cl_linelength_typing_list = list(str(cl_linelength)+' ')


#waveform mode has some of the same settings as classic
#cl_rendering_modes
#cl_rotate

wf_mono = True
wf_split = False
wf_merge = False


b_rendering_modes ={
    0: 'High to Low',
    1: 'Low to High',
    2: 'High to Low to High',
    3: 'Low to High to Low',
}
b_renderingmode_num = 0

"""
bars modes
1 - 0 range
0 - 1 range
1 - 0 - 1 range
0 - 1 - 0 range

"""


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
                      > visual_modes
                      > program        > credits
"""


scrollwheely = 0

anim_transparency = 0
anim_ontop = 0

anim_volume = 0

anim_song = 0

anim_nowplaying = 0


def fonts_couriernew(size):
    return pygame.font.SysFont('couriernew',size)

def fonts_JhengHei(size):
    return pygame.font.SysFont('Microsoft JhengHei',size)

unifont_dir = scriptdirfolder+slash+'Data'+slash+'unifont-17.0.04.otf'
def fonts_unifont(size):
    return pygame.Font(unifont_dir,size)

songpos_sync = 0


colors = {

    'window_border': (0,0,255,255),

    'visualizer_bg': (0,0,254,255),
    'visualizer_lines': (255,255,255,255),

    'program_notifs': (10,10,10,255),

    'settings_bg': (0,0,128,255),
    'settings_text': (255,255,255),

    'transparent_chromakey_win': (0,0,0),
    'transparent_chromakey': (0,0,0,255),
    
}

pr_bluetooth_output_device = False
fpscap = 0
fpscapnum = 18

fpscap_allowed_values = [1, 2, 5, 8, 10, 12, 24, 30, 60, 120, 180, 240, 300, 360, 480, 600, 720, 1000, 0]


#optimizations
def surface_static_new_visualizer(surfaceres):
    global timeNOW

    global colors

    global anim_ontop
    global anim_song
    global anim_transparency
    global anim_volume
    global anim_nowplaying

    global playing

    global general_mode_num

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    if transparent == False:
        surface.fill(colors['visualizer_bg'])
    if transparent == True:
        surface.fill(colors['transparent_chromakey'])
    
    if general_mode_num == 1:
        surface.blit(classic_renderer(surfaceres))
    if general_mode_num == 2:
        surface.blit(waveform_renderer(surfaceres))
    if general_mode_num == 3:
        surface.blit(bars_renderer(surfaceres))
    if general_mode_num == 4:
        surface.blit(oscilloscope_renderer(surfaceres))
    
    if anim_volume+1 > timeNOW:

        text_transparency = int((anim_volume+1 - timeNOW) * 255)

        percentage_text = fonts_couriernew(150).render(str(musicvolume_percent)+'%',False,colors['program_notifs'])
        percentage_text.set_alpha(text_transparency)
        surface.blit(percentage_text,((surfaceres[0]/2)-(percentage_text.get_width()/2),
                                             (surfaceres[1]/2)-(percentage_text.get_height()/2)))
        del percentage_text

    if anim_transparency+1 > timeNOW:

        text_transparency = int((anim_transparency+1 - timeNOW) * 255)

        donetext = fonts_couriernew(150).render('Done!',False,colors['program_notifs'])
        donetext.set_alpha(text_transparency)
        surface.blit(donetext,((surfaceres[0]/2)-(donetext.get_width()/2),
                                      (surfaceres[1]/2)-(donetext.get_height()/2)))
        del donetext
        
    if anim_ontop+1 > timeNOW:

        text_transparency = int((anim_ontop+1 - timeNOW) * 255)

        donetext = fonts_couriernew(150).render('Done!',False,colors['program_notifs'])
        donetext.set_alpha(text_transparency)
        surface.blit(donetext,((surfaceres[0]/2)-(donetext.get_width()/2),
                                      (surfaceres[1]/2)-(donetext.get_height()/2)))
        del donetext

    if anim_song+1 > timeNOW:

        text_transparency = int((anim_song+1 - timeNOW) * 255)

        songnum_text = fonts_couriernew(150).render(str(songnum+1),False,colors['program_notifs'])
        songnum_text.set_alpha(text_transparency)
        surface.blit(songnum_text,((surfaceres[0]/2)-(songnum_text.get_width()/2),
                                          (surfaceres[1]/2)-(songnum_text.get_height()/2)))
        del songnum_text

    if anim_nowplaying+3 > timeNOW:
        #really big fps drops
        #should optimize this later
        songname = os.path.splitext(os.path.split(songqueue[songnum].songdir)[1])[0]
        fontsize = 16

        
        nowplayingstr = 'Now playing: "'+songname+'"'
        nowplaying_text = fonts_unifont(fontsize).render(nowplayingstr,False,colors['settings_text'])

        pixelspersymbol = nowplaying_text.get_width()/len(nowplayingstr)
        sizemult = (len(nowplayingstr)*(pixelspersymbol))/(len(nowplayingstr)*fontsize)

        while len(nowplayingstr)*fontsize*sizemult > surfaceres[0] and fontsize != 1:
            fontsize -= 1

        nowplaying_text = fonts_unifont(fontsize-1).render(nowplayingstr,False,colors['settings_text'])


        nowplaying_surfacexy = [nowplaying_text.get_width()+4,nowplaying_text.get_height()+4]
        nowplaying_surface = pygame.Surface((nowplaying_surfacexy[0],nowplaying_surfacexy[1]))
        if transparent:
            nowplaying_surface.fill(colors['transparent_chromakey'])
        else:
            nowplaying_surface.fill(colors['visualizer_bg'])
        nowplaying_surface.blit(nowplaying_text, (2,2))
        pygame.draw.lines(nowplaying_surface,(0,0,255),False,
                          [(0,0),(nowplaying_surfacexy[0]-1,0),
                           (nowplaying_surfacexy[0]-1,nowplaying_surfacexy[1]-1),(0,nowplaying_surfacexy[1]-1),
                           (0,0)])
        
        nowplaying_surface = pygame.transform.rotate(nowplaying_surface,0-cl_rotate)

        #this was hell
        if int(((anim_nowplaying+3)-timeNOW)*1000) in range(2500,3000): #roll out animation
            if cl_rotate == 0:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                 (6+nowplaying_surfacexy[1])-(nowplaying_surfacexy[1]*((((anim_nowplaying+3)-timeNOW)-2)*2))))
            
            if cl_rotate == 90:
                surface.blit(nowplaying_surface,((surfaceres[0]-((6+nowplaying_surfacexy[1])*2))+((6+nowplaying_surfacexy[1])*((((anim_nowplaying+3)-timeNOW)-2)*2)),
                                                 (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2)))
            
            if cl_rotate == 180:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                 (surfaceres[1]-((6+nowplaying_surfacexy[1])*2))+((6+nowplaying_surfacexy[1])*((((anim_nowplaying+3)-timeNOW)-2)*2))))
                
            if cl_rotate == 270:
                surface.blit(nowplaying_surface,((6+nowplaying_surfacexy[1])-(nowplaying_surfacexy[1]*((((anim_nowplaying+3)-timeNOW)-2)*2)),
                                                 (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2),))
                
        if int(((anim_nowplaying+3)-timeNOW)*1000) in range(500,2500): #staying still
            if cl_rotate == 0:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                 (6)))

            if cl_rotate == 90:
                surface.blit(nowplaying_surface,((0-6-nowplaying_surfacexy[1]+surfaceres[0]),
                                                 (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2)))
            
            if cl_rotate == 180:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                 (0-6-nowplaying_surfacexy[1]+surfaceres[1])))
            
            if cl_rotate == 270:
                surface.blit(nowplaying_surface,((6),
                                                 (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2)))
                
        if int(((anim_nowplaying+3)-timeNOW)*1000) in range(0,500): #roll in animation
            if cl_rotate == 0:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                (6-nowplaying_surfacexy[1])+((nowplaying_surfacexy[1])/((((anim_nowplaying+3)-timeNOW))*2))))

            if cl_rotate == 90:
                surface.blit(nowplaying_surface,(((surfaceres[0]))-((6+nowplaying_surfacexy[1])/((((anim_nowplaying+3)-timeNOW))*2)),
                                                (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2)))
            
            if cl_rotate == 180:
                surface.blit(nowplaying_surface,((surfaceres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                ((surfaceres[1]))-((6+nowplaying_surfacexy[1])/((((anim_nowplaying+3)-timeNOW))*2))))
              
            if cl_rotate == 270:
                surface.blit(nowplaying_surface,((6-nowplaying_surfacexy[1])+((nowplaying_surfacexy[1])/((((anim_nowplaying+3)-timeNOW))*2)),
                                                 (surfaceres[1]//2)-(nowplaying_surfacexy[0]//2)))
                
    if playing == False:
        pygame.draw.line(surface,colors['program_notifs'],((surfaceres[0]/2)-(surfaceres[0]/12),(surfaceres[1]/2)+(surfaceres[1]/3)),((surfaceres[0]/2)-(surfaceres[0]/12),(surfaceres[1]/2)-(surfaceres[1]/3)),10)
        pygame.draw.line(surface,colors['program_notifs'],((surfaceres[0]/2)+(surfaceres[0]/12),(surfaceres[1]/2)+(surfaceres[1]/3)),((surfaceres[0]/2)+(surfaceres[0]/12),(surfaceres[1]/2)-(surfaceres[1]/3)),10)

    pygame.draw.lines(surface,(0,0,255,255),False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])
    
    return surface

def classic_renderer(surfaceres):
    global cl_line_space
    global cl_renderingmode_num
    global cl_onedimensional
    global cl_mirrored
    global cl_linelength
    global cl_rotate

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)

    

    #if else hell but works pretty fineee, no masive fps drops

    if cl_rotate == 0 or cl_rotate == 180:
        xnum = cl_line_space

        while xnum < surfaceres[0]:
            try:
                rendering_formulas = [
                  int(xnum)-(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum//2)+(surfaceres[0]//2)+   ((lastsounddata)//devisionby),
                  int(xnum//2)-(surfaceres[0]//2)+   ((lastsounddata)//devisionby),
                  int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0])+   ((lastsounddata)//devisionby),
                  int(xnum)-(surfaceres[0])+   ((lastsounddata)//devisionby),
                ]

                linesrender_formula = rendering_formulas[cl_renderingmode_num]
               
                if linesrender_formula < 0:
                    xnum = xnum+1+cl_line_space
                    continue
            

                if cl_rotate == 0:


                    if cl_onedimensional:
                        if cl_mirrored:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                                xnum = xnum+1+cl_line_space
                                
                                continue


                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum),(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,(surfaceres[1]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))),
                                         (int(xnum)//2,surfaceres[1])) 
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (surfaceres[0]-int(xnum)//2,surfaceres[1]))

                                xnum = xnum+1+cl_line_space
                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),surfaceres[1]-(surfaceres[1]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))),
                                         (int(xnum),surfaceres[1]))



                    else:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength))),
                                     (int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))),
                                     (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))
                        
                            xnum = xnum+1+cl_line_space

                            continue


                        pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),(surfaceres[1]//2)+(surfaceres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)),
                                         (int(xnum),(surfaceres[1]//2)-(surfaceres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))
                

                if cl_rotate == 180:
                    if cl_onedimensional:
                        if cl_mirrored:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                                xnum = xnum+1+cl_line_space

                                continue


                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum),(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (surfaceres[0]-int(xnum),(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))),
                                         (surfaceres[0]-int(xnum)//2,0)) 
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,(surfaceres[1])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum)//2,0))

                                xnum = xnum+1+cl_line_space
                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum),0+(surfaceres[1]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))),
                                         (surfaceres[0]-int(xnum),0))



                    else:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                     (surfaceres[0]-int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength))))
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (int(xnum)//2,(surfaceres[1]//2)+(surfaceres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))),
                                     (int(xnum)//2,(surfaceres[1]//2)-(surfaceres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))
                        
                            xnum = xnum+1+cl_line_space

                            continue


                        pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum),(surfaceres[1]//2)+(surfaceres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),
                                         (surfaceres[0]-int(xnum),(surfaceres[1]//2)-(surfaceres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)))
                


                xnum = xnum+1+cl_line_space

            except IndexError:
                xnum = xnum+1+cl_line_space

        
        if cl_renderingmode_num < 4:
            pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2)-1,10),((surfaceres[0]/2)-1,surfaceres[1]-10))
            pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2),10)  ,((surfaceres[0]/2),  surfaceres[1]-10))
    

    if cl_rotate == 90 or cl_rotate == 270:
        xnum = cl_line_space

        while xnum < surfaceres[1]:
            try:
                rendering_formulas = [
                  int(xnum)-(surfaceres[1]//2)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[1]//2)+((lastsounddata)//devisionby),
                0-int(xnum//2)+(surfaceres[1]//2)+   ((lastsounddata)//devisionby),
                  int(xnum//2)-(surfaceres[1]//2)+   ((lastsounddata)//devisionby),
                  int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[1])+   ((lastsounddata)//devisionby),
                  int(xnum)-(surfaceres[1])+   ((lastsounddata)//devisionby),
                ]

                linesrender_formula = rendering_formulas[cl_renderingmode_num]
               
                if linesrender_formula < 0:
                    xnum = xnum+1+cl_line_space
                    continue
            

                if cl_rotate == 90:


                    if cl_onedimensional:
                        if cl_mirrored:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2),
                                                 ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2)
                                                 )
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2),
                                                 ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2)
                                                 )

                                xnum = xnum+1+cl_line_space

                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum))
                                             )

                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),int(xnum)//2),
                                                 (0,int(xnum)//2)
                                                 )
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2),
                                                 (0,surfaceres[1]-int(xnum)//2)
                                                 )

                                xnum = xnum+1+cl_line_space
                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             (0+(surfaceres[0]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))),int(xnum)),
                                             (0,int(xnum))
                                             )


                    else:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)),int(xnum)//2)
                                             )
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2)
                                             )

                            xnum = xnum+1+cl_line_space

                            continue

                        pygame.draw.line(surface,colors['visualizer_lines'],
                                         ((surfaceres[0]//2)+(surfaceres[0]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength),int(xnum)),
                                         ((surfaceres[0]//2)-(surfaceres[0]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength),int(xnum))
                                         )

                if cl_rotate == 270:
                    if cl_onedimensional:
                        if cl_mirrored:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2),
                                                 ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2)
                                                 )
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2),
                                                 ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2)
                                                 )
                                
                                xnum = xnum+1+cl_line_space

                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum))
                                             )

                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),surfaceres[1]-int(xnum)//2),
                                                 (surfaceres[0],surfaceres[1]-int(xnum)//2)
                                                 )

                                pygame.draw.line(surface,colors['visualizer_lines'],
                                                 ((surfaceres[0])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),int(xnum)//2),
                                                 (surfaceres[0],int(xnum)//2)
                                                 )

                                xnum = xnum+1+cl_line_space
                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             (surfaceres[0]-(surfaceres[0]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))),surfaceres[1]-int(xnum)),
                                             (surfaceres[0],surfaceres[1]-int(xnum))
                                             )


                    else:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),surfaceres[1]-int(xnum)//2)
                                             )
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                             ((surfaceres[0]//2)+(surfaceres[0]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)),int(xnum)//2),
                                             ((surfaceres[0]//2)-(surfaceres[0]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)),int(xnum)//2)
                                             )

                            xnum = xnum+1+cl_line_space

                            continue


                        pygame.draw.line(surface,colors['visualizer_lines'],
                                         ((surfaceres[0]//2)+(surfaceres[0]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength),surfaceres[1]-int(xnum)),
                                         ((surfaceres[0]//2)-(surfaceres[0]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength),surfaceres[1]-int(xnum))
                                         )

                xnum = xnum+1+cl_line_space

            except IndexError:
                xnum = xnum+1+cl_line_space

        
        if cl_renderingmode_num < 4:
            pygame.draw.line(surface,(0,0,128),
                             (10,(surfaceres[1]/2)-1),
                             (surfaceres[0]-10,(surfaceres[1]/2)-1))
            pygame.draw.line(surface,(0,0,128),
                             (10,(surfaceres[1]/2))  ,
                             (surfaceres[0]-10,(surfaceres[1]/2)  ))
    


    return surface


#waveform drops the fps MASSIVELY rn
def waveform_renderer(surfaceres):

    global cl_rotate

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)

    if cl_rotate == 0 or cl_rotate == 180:
        xnum = 0

        while xnum < surfaceres[0]:
            try:
                rendering_formulas = [
                  int(xnum)-(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum//2)+(surfaceres[0]//2)+   ((lastsounddata)//devisionby),
                  int(xnum//2)-(surfaceres[0]//2)+   ((lastsounddata)//devisionby),
                  int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+                   ((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0])+   ((lastsounddata)//devisionby),
                  int(xnum)-(surfaceres[0])+   ((lastsounddata)//devisionby),
                ]

                linesrender_formula = rendering_formulas[cl_renderingmode_num]
                
                if cl_renderingmode_num in range(1,3) or cl_renderingmode_num in range(5,7):
                    formula_num = -1
                else:
                    formula_num = 1

                if linesrender_formula < 0:
                    xnum += 1
                    continue
            

                if cl_rotate == 0:

                    if wf_mono:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                                     (int(xnum)//2+1,(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                     (surfaceres[0]-int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                                     (surfaceres[0]-int(xnum)//2-1,(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                        
                            xnum += 1

                            continue

                        pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767),
                                         (int(xnum+1),(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767))
                    
                    else:
                        if wf_split:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                #1st channel
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,  ((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767))),
                                         (int(xnum)//2+1,((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767))))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,  ((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767))),
                                         (surfaceres[0]-int(xnum)//2-1,((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767))))
                                
                                #2nd channel
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,  ((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767))),
                                         (int(xnum)//2+1,((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767))))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,  ((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767))),
                                         (surfaceres[0]-int(xnum)//2-1,((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767))))
                                
                                xnum += 1

                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),  ((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1])/32767)),
                                         (int(xnum+1),((surfaceres[1]/2)+(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767)))
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),  ((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767)),
                                         (int(xnum+1),((surfaceres[1]/2)-(surfaceres[1]/2/2))+((surfaceres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767)))

                            pygame.draw.line(surface,colors['window_border'],(0,surfaceres[1]//2),(surfaceres[0],surfaceres[1]//2))

                        elif wf_merge:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,(surfaceres[1]/2)+(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][0])/32767)),
                                         (int(xnum)//2,(surfaceres[1]/2)-(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][1])/32767)))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)),
                                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]/2)-(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)))

                                xnum += 1

                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)),
                                         (int(xnum),(surfaceres[1]/2)-(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)))
                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                #1st channel
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula]  [0])/32767)),
                                         (int(xnum)//2+1,(surfaceres[1]/2)+(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767)))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                                         (surfaceres[0]-int(xnum)//2-1,(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                                
                                #2nd channel
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula]  [1])/32767)),
                                         (int(xnum)//2+1,(surfaceres[1]/2)+(surfaceres[1]/2)*((soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767)))
                                pygame.draw.line(surface,colors['visualizer_lines'],
                                         (surfaceres[0]-int(xnum)//2,  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767)),
                                         (surfaceres[0]-int(xnum)//2-1,(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767)))
                                
                                xnum += 1

                                continue

                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767),
                                         (int(xnum+1),(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767))
                            pygame.draw.line(surface,colors['visualizer_lines'],
                                         (int(xnum),  (surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [1])/32767),
                                         (int(xnum+1),(surfaceres[1]/2)+(surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767))
                    
                if cl_rotate == 180:
                    pass


                xnum += 1

            except IndexError:
                xnum += 1

        
        if cl_renderingmode_num < 4:
            pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2)-1,10),((surfaceres[0]/2)-1,surfaceres[1]-10))
            pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2),10)  ,((surfaceres[0]/2),  surfaceres[1]-10))
    

    if cl_rotate == 90 or cl_rotate == 270:
        pass
        #do that later


    return surface


def bars_renderer(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)

    #do that later

    return surface


def oscilloscope_renderer(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)

    linesperframe = 0
    while linesperframe < 1024:
        pygame.draw.line(surface,colors['visualizer_lines'],
                         ((surfaceres[0]//2)+((surfaceres[0]//2)*(soundrawdata[lastsounddata+linesperframe-1024][0]/32767))  ,(surfaceres[1]//2)+((surfaceres[1]//2)*(soundrawdata[lastsounddata+linesperframe-1024][1]/32767))),
                         ((surfaceres[0]//2)+((surfaceres[0]//2)*(soundrawdata[lastsounddata+linesperframe+1-1024][0]/32767)),(surfaceres[1]//2)+((surfaceres[1]//2)*(soundrawdata[lastsounddata+linesperframe+1-1024][1]/32767))))
        linesperframe += 1
    return surface


def surface_static_new_settings(surfaceres):
    global colors

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    settings_text =       fonts_couriernew(32).render('Settings',False,colors['settings_text'])
    surface.blit(settings_text,      ((surfaceres[0]//2)-(settings_text.get_width()//2),2))

    slightlygraycolor = []
    for i in colors['settings_text']:
        slightlygraycolor.append(i//2)
    slightlygraycolor = tuple(slightlygraycolor)

    surface.blit(pygame.transform.invert(icons['keyboard']),(0,36))
    controls_text = fonts_couriernew(24).render('Controls',False,colors['settings_text'])
    surface.blit(controls_text,(38,44))   
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,44),(152,44),
                                                      (152,68),(36,68),    (36,44)])

    
    
    surface.blit(pygame.transform.invert(icons['brush']),(2,68))
    customize_text = fonts_couriernew(24).render('Customize',False,colors['settings_text'])
    surface.blit(customize_text,(38,76))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,76),  (166,76),
                                                       (166,100),(36,100),   (36,76)])

    surface.blit(icons['program'],(2,104))
    program_text = fonts_couriernew(24).render('Program',False,colors['settings_text'])
    surface.blit(program_text,(38,107))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,108) ,(138,108),
                                                       (138,132),(36,132),        (36,108)
                                                       ])



    visualizer_text = fonts_couriernew(24).render('Visualizer',False,colors['settings_text'])
    surface.blit(icons['visualizer'], (surfaceres[0]-4-visualizer_text.get_width()-2-icons['visualizer'].get_width(),
                                       
                                       38))
    surface.blit(visualizer_text, (surfaceres[0]-4-visualizer_text.get_width(),
                                   
                                   44))
    pygame.draw.lines(surface,slightlygraycolor,False,[(surfaceres[0]-146,68),(surfaceres[0]-146,44),
                                                       (surfaceres[0]-2,44),(surfaceres[0]-2,68),   (surfaceres[0]-146,68)])

    

    songsqueue_text = fonts_couriernew(24).render('Song Queue',False,colors['settings_text'])
    surface.blit(icons['songqueue'],(surfaceres[0]-36-songsqueue_text.get_width(),
                                     
                                     72))
    surface.blit(songsqueue_text, (surfaceres[0]-4-songsqueue_text.get_width(),
                                   
                                    74))
    pygame.draw.lines(surface,slightlygraycolor,False,[(surfaceres[0]-146,76),(surfaceres[0]-2,76),
                                                       (surfaceres[0]-2,100),(surfaceres[0]-146,100),   (surfaceres[0]-146,76)])



    
    surface.blit(pygame.transform.scale(icons['jakeisalivee'],(64,64)), (surfaceres[0]-68,surfaceres[1]-76))
    surface.blit(pygame.transform.scale(icons['telegram'],(64,64)),(surfaceres[0]-136,surfaceres[1]-76))
    version_text = fonts_couriernew(10).render('Version: '+VERSION,False,colors['settings_text'])
    surface.blit(version_text,(surfaceres[0]-5-version_text.get_width(),surfaceres[1]-11))


    surface.blit(surface_static_settings_decorator(surfaceres))
    
    del slightlygraycolor
    return surface




def surface_static_new_controls(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])


    
    buttons_text =       fonts_couriernew(32).render('Controls',False,colors['settings_text'])
    surface.blit(buttons_text,      ((surfaceres[0]//2)-(buttons_text.get_width()//2),2))
        
    t_transparent_text = fonts_couriernew(16).render('T: Transparent window switch',False,colors['settings_text'])
    surface.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

    o_ontop_text =       fonts_couriernew(16).render('O: Always on top window switch',False,colors['settings_text'])
    surface.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

    uad_volup_text =        fonts_couriernew(16).render('Up/Down arrow: Volume control',False,colors['settings_text'])
    surface.blit(uad_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

    ra_nextsong_text =   fonts_couriernew(16).render('Right/Left arrow: Next/Previous song',False,colors['settings_text'])
    surface.blit(ra_nextsong_text,   ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

    movewin_text =           fonts_couriernew(16).render('Move window: Hold LMB or RMB and drag',False,colors['settings_text'])
    surface.blit(movewin_text,      ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))
    changeresolution1_text = fonts_couriernew(16).render('Change resolution: Hold RMB or LMB',False,colors['settings_text'])
    surface.blit(changeresolution1_text,      ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))
    changeresolution2_text = fonts_couriernew(16).render('and scroll mouse wheel up or down',False,colors['settings_text'])
    surface.blit(changeresolution2_text,      ((4),((2*8)+buttons_text.get_height() +(t_transparent_text.get_height()*6))))


    c_close_text =       fonts_couriernew(16).render('C: Close the window',False,colors['settings_text'])
    surface.blit(c_close_text,      ((4),((2*9)+buttons_text.get_height() +(t_transparent_text.get_height()*7))))
    

    wherecontrolswork_text_r1 = fonts_couriernew(16).render('Most of the controls  ',False,colors['settings_text'])
    wherecontrolswork_text_r2 = fonts_couriernew(16).render('work in the visualizer',False,colors['settings_text'])
    surface.blit(wherecontrolswork_text_r1, (surfaceres[0]-wherecontrolswork_text_r1.get_width(),
                                                surfaceres[1]-wherecontrolswork_text_r1.get_height()*2))
    surface.blit(wherecontrolswork_text_r2, (surfaceres[0]-wherecontrolswork_text_r2.get_width(),
                                                surfaceres[1]-wherecontrolswork_text_r2.get_height()))
    
    surface.blit(surface_static_settings_decorator(surfaceres))
    
    return surface


def surface_static_new_customize(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    surface.blit(surface_static_settings_decorator(surfaceres))
    
    return surface

def surface_static_new_songqueue(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    songsrendernum = 1
    while songsrendernum <= len(songqueue):

        if (4*songsrendernum)+(28*songsrendernum)+4 < scrollwheely:
            songsrendernum += 1
            continue

        songdir = os.path.split(songqueue[songsrendernum-1].songdir)[1]
        if len(songdir) > ((surfaceres[0]-150)/18):
            songdir = songdir[0:((surfaceres[0]-150)//18)]+'...'
                

        songdir_text = fonts_unifont(18).render(' '+str(songsrendernum)+'. "'+str(songdir)+'"',False,colors['settings_text'])

        surface.blit(songdir_text,(4,(4*songsrendernum)+(28*songsrendernum)+8-scrollwheely))
        pygame.draw.line(surface,colors['window_border'],(0,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely),(surfaceres[0],(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely))

        surface.blit(icons['view'],(surfaceres[0]-28,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icons['delete'],(surfaceres[0]-56,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icons['movedown'],(surfaceres[0]-84,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icons['moveup'],(surfaceres[0]-112,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))

        songsrendernum += 1
        
        if (4*songsrendernum)+(28*songsrendernum)+4-scrollwheely > surfaceres[1]:
            break

    addsong_text = fonts_couriernew(24).render('+',False,colors['settings_text'])
    surface.blit(addsong_text,(4,(4*songsrendernum)+(28*songsrendernum)+2-scrollwheely))

    songqueuebg = pygame.Surface((surfaceres[0],32))
    songqueuebg.fill(colors['settings_bg'])
    surface.blit(songqueuebg,(0,0))
    songsqueue_text = fonts_couriernew(24).render('Song queue',False,colors['settings_text'])
    surface.blit(songsqueue_text,(4,2))
    pygame.draw.line(surface,colors['window_border'],(0,4+songsqueue_text.get_height()),(surfaceres[0],4+songsqueue_text.get_height()))
    surface.blit(icons['folder'],(surfaceres[0]-28,4))
    surface.blit(icons['shuffle'],(surfaceres[0]-60,4))
    surface.blit(icons['reverse'],(surfaceres[0]-92,4))
    
    escbg = pygame.Surface((surfaceres[0],28))
    escbg.fill(colors['settings_bg'])
    surface.blit(escbg,(0,surfaceres[1]-28))
    pygame.draw.line(surface, colors['window_border'],(0,surfaceres[1]-25),(surfaceres[0],surfaceres[1]-25))

    surface.blit(surface_static_settings_decorator(surfaceres))
    
    return surface

def surface_static_new_visualmodes(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])
    
    visualizer_text =       fonts_couriernew(32).render('Visualizer',False,colors['settings_text'])
    surface.blit(visualizer_text,      ((surfaceres[0]//2)-(visualizer_text.get_width()//2),2))
    
    generalmodes_text = fonts_couriernew(26).render('Mode: <> "'+str(general_mode_names[general_mode_num])+'"',False,colors['settings_text'])
    surface.blit(generalmodes_text, (4,34))

    slightlygreycolor = []
    for i in colors['settings_text']:
        slightlygreycolor.append(i//2)
    slightlygreycolor = tuple(slightlygreycolor)

    if general_mode_num == 1:
        
        cl_setting = fonts_couriernew(16).render('Classic settings:',False,colors['settings_text'])
        surface.blit(cl_setting,(4,70))

        cl_mode_text = fonts_couriernew(12).render('Modes: < "'+str(cl_rendering_modes[cl_renderingmode_num])+'" >',False,colors['settings_text'])
        surface.blit(cl_mode_text, (4,86))

        cl_zoom_typing_str = ''
        for i in cl_zoom_typing_list:
            cl_zoom_typing_str += str(i)

        cl_zoom_text = fonts_couriernew(12).render('Zoom out by: x'+cl_zoom_typing_str,False,colors['settings_text']) #user should type numbers here
        surface.blit(cl_zoom_text, (4,98))

        cl_line_space_typing_str = ''
        for i in cl_line_space_typing_list:
            cl_line_space_typing_str += str(i)

        cl_space_between_lines_text = fonts_couriernew(12).render('Pixels between lines: '+cl_line_space_typing_str,False,colors['settings_text'])
        surface.blit(cl_space_between_lines_text,(4,110))
    
        cl_onedimensional_text = fonts_couriernew(12).render('One dimensional: ',False,colors['settings_text'])
        surface.blit(cl_onedimensional_text,(4,122))
        pygame.draw.lines(surface,colors['settings_text'],False,[(120,123),(130,123),
                                                                 (130,133),(120,133),
                                                                 (120,123)])
        if cl_onedimensional:
            pygame.draw.line(surface,colors['settings_text'],(120,123),(130,133))
            pygame.draw.line(surface,colors['settings_text'],(130,123),(120,133))
    
            cl_mirrored_text = fonts_couriernew(12).render('Mirrored: ',False,colors['settings_text'])
            surface.blit(cl_mirrored_text,(4,134))
            pygame.draw.lines(surface,colors['settings_text'],False,[(70,135),(80,135),
                                                                     (80,145),(70,145),
                                                                     (70,135)])
            if cl_mirrored:
                pygame.draw.line(surface,colors['settings_text'],(70,135),(80,145))
                pygame.draw.line(surface,colors['settings_text'],(80,135),(70,145))
        else:
            cl_mirrored_text = fonts_couriernew(12).render('Mirrored: ',False,slightlygreycolor)
            surface.blit(cl_mirrored_text,(4,134))
            pygame.draw.lines(surface,slightlygreycolor,False,[(70,135),(80,135),
                                                               (80,145),(70,145),
                                                               (70,135)])
            if cl_mirrored:
                pygame.draw.line(surface,slightlygreycolor,(70,135),(80,145))
                pygame.draw.line(surface,slightlygreycolor,(80,135),(70,145))


        cl_rotate_typing_str = ''
        for i in cl_rotate_typing_list:
            cl_rotate_typing_str += str(i)

        cl_rotate_text = fonts_couriernew(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,colors['settings_text'])
        surface.blit(cl_rotate_text,(4,146))


        cl_linelength_typing_str = ''
        for i in cl_linelength_typing_list:
            cl_linelength_typing_str += str(i)

        cl_linelength_text = fonts_couriernew(12).render('Line length multiplier: '+cl_linelength_typing_str,False,colors['settings_text'])
        surface.blit(cl_linelength_text,(4,158))

    if general_mode_num == 2:
        
        cl_setting = fonts_couriernew(16).render('Waveform settings:',False,colors['settings_text'])
        surface.blit(cl_setting,(4,70))

        cl_mode_text = fonts_couriernew(12).render('Modes: < "'+str(cl_rendering_modes[cl_renderingmode_num])+'" >',False,colors['settings_text'])
        surface.blit(cl_mode_text, (4,86))

        cl_zoom_typing_str = ''
        for i in cl_zoom_typing_list:
            cl_zoom_typing_str += str(i)

        cl_zoom_text = fonts_couriernew(12).render('Zoom out by: x'+cl_zoom_typing_str,False,colors['settings_text']) #user should type numbers here
        surface.blit(cl_zoom_text, (4,98))

        wf_mono_text = fonts_couriernew(12).render('Mono: ',False,colors['settings_text'])
        surface.blit(wf_mono_text, (4,110))
        pygame.draw.lines(surface,colors['settings_text'],False,[(41,112),(51,112),
                                                                 (51,122),(41,122),
                                                                 (41,112)])
        if wf_mono:
            pygame.draw.line(surface,colors['settings_text'],(41,112),(51,122))
            pygame.draw.line(surface,colors['settings_text'],(51,112),(41,122))



            wf_merge_text = fonts_couriernew(12).render('Merge: ',False,slightlygreycolor)
            surface.blit(wf_merge_text,(4,122))

            pygame.draw.lines(surface,slightlygreycolor,False,[(48,125),(58,125),
                                                                     (58,135),(48,135),
                                                                     (48,125)])
            if wf_merge:
                pygame.draw.line(surface,slightlygreycolor,(48,125),(58,135))
                pygame.draw.line(surface,slightlygreycolor,(58,125),(48,135))


            wf_split_text = fonts_couriernew(12).render('Split: ',False,slightlygreycolor)
            surface.blit(wf_split_text,(4,134))

            pygame.draw.lines(surface,slightlygreycolor,False,[(48,135),(58,135),
                                                                     (58,145),(48,145),
                                                                     (48,135)])
            if wf_split:
                pygame.draw.line(surface,slightlygreycolor,(48,135),(58,145))
                pygame.draw.line(surface,slightlygreycolor,(58,135),(48,145))
        else:

            wf_merge_text = fonts_couriernew(12).render('Merge: ',False,colors['settings_text'])
            surface.blit(wf_merge_text,(4,122))

            pygame.draw.lines(surface,colors['settings_text'],False,[(48,125),(58,125),
                                                               (58,135),(48,135),
                                                               (48,125)])
            if wf_merge:
                pygame.draw.line(surface,colors['settings_text'],(48,125),(58,135))
                pygame.draw.line(surface,colors['settings_text'],(58,125),(48,135))


            wf_split_text = fonts_couriernew(12).render('Split: ',False,colors['settings_text'])
            surface.blit(wf_split_text,(4,134))

            pygame.draw.lines(surface,colors['settings_text'],False,[(48,135),(58,135),
                                                               (58,145),(48,145),
                                                               (48,135)])
            if wf_split:
                pygame.draw.line(surface,colors['settings_text'],(48,135),(58,145))
                pygame.draw.line(surface,colors['settings_text'],(58,135),(48,145))



        cl_rotate_typing_str = ''
        for i in cl_rotate_typing_list:
            cl_rotate_typing_str += str(i)
        cl_rotate_text = fonts_couriernew(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,slightlygreycolor) #do later
        surface.blit(cl_rotate_text,(4,146))

    

    surface.blit(surface_static_settings_decorator(surfaceres))

    del slightlygreycolor
    return surface


def surface_static_new_program(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    program_text = fonts_couriernew(32).render('Program',False,colors['settings_text'])
    surface.blit(program_text,((surfaceres[0]//2)-(program_text.get_width()//2),2))

    if fpscap == 0:
        fpscapstr = 'Unlimited'
    else:
        fpscapstr = str(fpscap)
    fps_text = fonts_couriernew(16).render('Fps cap: <> '+fpscapstr,False,colors['settings_text'])
    surface.blit(fps_text,(4,34))
    bluetooth_latencyfix_text = fonts_couriernew(16).render('Bluetooth latency fix: ',False,colors['settings_text'])
    surface.blit(bluetooth_latencyfix_text,(4,50))
    pygame.draw.lines(surface,colors['settings_text'],False,[(228,51),(242,51),
                                                             (242,65),(228,65),
                                                             (228,51)])
    if pr_bluetooth_output_device:
        pygame.draw.line(surface,colors['settings_text'],(228,51),(242,65))
        pygame.draw.line(surface,colors['settings_text'],(242,51),(228,65))

    credits_text = fonts_couriernew(12).render('Credits',False,colors['settings_text'])
    surface.blit(credits_text,(surfaceres[0]-credits_text.get_width()-5,surfaceres[1]-76-12))

    surface.blit(pygame.transform.scale(icons['jakeisalivee'],(64,64)), (surfaceres[0]-68,surfaceres[1]-76))
    surface.blit(pygame.transform.scale(icons['telegram'],(64,64)),(surfaceres[0]-136,surfaceres[1]-76))
    version_text = fonts_couriernew(10).render('Version: '+VERSION,False,colors['settings_text'])
    surface.blit(version_text,(surfaceres[0]-5-version_text.get_width(),surfaceres[1]-11))

    surface.blit(surface_static_settings_decorator(surfaceres))

    return surface

def surface_static_new_credits(surfaceres):
    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    textt = fonts_unifont(16).render('all made by me. still Work In Progress tho',False,colors['settings_text'])
    surface.blit(textt,(2,2))

    surface.blit(surface_static_settings_decorator(surfaceres))

    return surface


def surface_static_settings_decorator(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    
    esc_back_text =      fonts_couriernew(16).render('Esc: Back',False,colors['settings_text'])
    surface.blit(esc_back_text,     ((4),(surfaceres[1]-2-esc_back_text.get_height())))

    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface


displayupdate = True


# 12 len list, write "jakeisalivee" to activate devmode
devmodeactivation_list = []
devmode = False





timeNOW = time.perf_counter()


def windowres_toolow(x,y):
    global windowres
    global mainwindow

    #600,260
    width = False
    height = False

    transparency = 0
    if windowres[0] < x or windowres[1] < y:
        transparency1 = 255*(1-(windowres[0]/x))*1.5
        if transparency1 > 0:
            width = True

        transparency2 = 255*(1-(windowres[1]/y))*1.5
        if transparency2 > 0:
            height = True

        transparency = max([transparency1,transparency2])

    if transparency < 0:
        transparency = 0

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill((1,1,1))

    exclamationmark_text = fonts_couriernew(64).render('!',False,colors['window_border'])
    surface.blit(exclamationmark_text,(windowres[0]//2-exclamationmark_text.get_width()//2,
                                       windowres[1]//2-exclamationmark_text.get_height()//2))

    if width:
        pygame.draw.line(surface,colors['window_border'],(4,windowres[1]//2),(12,windowres[1]//2-20))
        pygame.draw.line(surface,colors['window_border'],(4,windowres[1]//2),(12,windowres[1]//2+20))

        pygame.draw.line(surface,colors['window_border'],(windowres[0]-4,windowres[1]//2),(windowres[0]-12,windowres[1]//2+20))
        pygame.draw.line(surface,colors['window_border'],(windowres[0]-4,windowres[1]//2),(windowres[0]-12,windowres[1]//2-20))

    if height:
        pygame.draw.line(surface,colors['window_border'],(windowres[0]//2,4),(windowres[0]//2-20,12))
        pygame.draw.line(surface,colors['window_border'],(windowres[0]//2,4),(windowres[0]//2+20,12))

        pygame.draw.line(surface,colors['window_border'],(windowres[0]//2,windowres[1]-4),(windowres[0]//2-20,windowres[1]-12))
        pygame.draw.line(surface,colors['window_border'],(windowres[0]//2,windowres[1]-4),(windowres[0]//2+20,windowres[1]-12))


    surface.set_alpha(transparency)

    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)])

    mainwindow.blit(surface,(0,0))



#only for reusability, we use this so much
class cl_typing:

    def cancel_zoom():
        global cl_zoom_typing
        global cl_zoom_typing_list
        global devisionby

        cl_zoom_typing_list[-1] = ' '

        cl_zoom_typing = False
        cl_zoom_typing_str = ''
        for i in cl_zoom_typing_list:
            cl_zoom_typing_str += str(i)
                              
        try:
            devisionby = int(cl_zoom_typing_str)
            cl_zoom_typing_list = list(str(devisionby)+' ')
            if devisionby == 0:
                devisionby = 1
                cl_zoom_typing_list = ['1',' ']
        except ValueError:
            devisionby = 1
            cl_zoom_typing_list = ['1',' ']

    def cancel_linespace():
        global cl_line_space_typing
        global cl_line_space_typing_list
        global cl_line_space

        cl_line_space_typing_list[-1] = ' '

        cl_line_space_typing = False
        cl_line_space_typing_str = ''
        for i in cl_line_space_typing_list:
            cl_line_space_typing_str += str(i)

        try: 
            cl_line_space = int(cl_line_space_typing_str)
            cl_line_space_typing_list = list(str(cl_line_space)+' ')
        except ValueError:
            cl_line_space = 0
            cl_line_space_typing_list = ['0',' ']

    def cancel_rotate():
        global cl_rotate_typing
        global cl_rotate_typing_list
        global cl_rotate

        cl_rotate_typing_list[-1] = ' '

        cl_rotate_typing = False
        cl_rotate_typing_str = ''
        for i in cl_rotate_typing_list:
            cl_rotate_typing_str += str(i)

        try: 
            #ifif ifi ifi fifi i i fi iffii ifii fif if if i fi fi fi fif
            if int(cl_rotate_typing_str.replace('°', '')) in range(0,45):
                cl_rotate_typing_str = '0° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(45,90):
                cl_rotate_typing_str = '90° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(90,135):
                cl_rotate_typing_str = '90° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(135,180):
                cl_rotate_typing_str = '180° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(180,225):
                cl_rotate_typing_str = '180° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(225,270):
                cl_rotate_typing_str = '270° '
            if int(cl_rotate_typing_str.replace('°', '')) in range(270,1000):
                cl_rotate_typing_str = '270° '
        
        
        
            cl_rotate = int(cl_rotate_typing_str.replace('°', ''))
            cl_rotate_typing_list = list(str(cl_rotate)+'° ')
        except ValueError:
            cl_rotate = 0
            cl_rotate_typing_list = ['0','° ']

    def cancel_linelength():
        global cl_linelength_typing
        global cl_linelength_typing_list
        global cl_linelength

        cl_linelength_typing_list[-1] = ' '

        cl_linelength_typing = False
        cl_linelength_typing_str = ''
        for i in cl_linelength_typing_list:
            cl_linelength_typing_str += str(i)

        try: 
            cl_linelength = float(cl_linelength_typing_str)
            cl_linelength_typing_list = list(str(cl_linelength)+' ')
        except ValueError:
            cl_linelength = 1.0
            cl_linelength_typing_list = list(str(cl_linelength)+' ')


def scenes():
    global timeNOW

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
    
    global devisionby


    global ontop
    global transparent

    global anim_ontop
    global anim_transparency
    global anim_song
    global anim_volume
    global anim_nowplaying

    global colors   
    global displayupdate

    global general_mode_num
    global general_mode_names

    global cl_renderingmode_num
    global cl_rendering_modes
    global cl_line_space
    global cl_mirrored
    global cl_onedimensional
    global cl_rotate
    global cl_linelength

    global cl_zoom_typing
    global cl_zoom_typing_list

    global cl_line_space_typing
    global cl_line_space_typing_list

    global cl_rotate_typing
    global cl_rotate_typing_list

    global cl_linelength_typing
    global cl_linelength_typing_list

    global wf_merge
    global wf_mono
    global wf_split

    global latency
    global pr_bluetooth_output_device
    global fpscap
    global fpscapnum

    if scene == 'visualizer':
        
        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_visualizer(windowres))
            pygame.display.update()
            
        if playing:
            displayupdate = True
        
            songpos = pygame.mixer_music.get_pos() + songpos_sync

            if songpos > songqueue[songnum].songlength: #song ended
                songreset() 
                if len(songqueue)-1 > songnum:

                    songnum += 1
                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    playing = True
                    pygame.mixer_music.unpause()
                    anim_nowplaying = timeNOW+1
                else:
                    songnum = 0
                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    playing = False


            if pr_bluetooth_output_device:
                lastsounddata = int((songpos-(latency*1000)) * soundrate/1000)
            else:
                lastsounddata = int(songpos * soundrate/1000)
            

            if songformat != '.wav':
                #songsync
                if songpos % 10000 >= 9990:
                    pygame.mixer_music.rewind()
                    pygame.mixer_music.play(0,songpos/1000)
                    songpos_sync = songpos

        if anim_volume+1 > timeNOW or anim_transparency+1 > timeNOW or anim_ontop+1 > timeNOW or anim_song+1 > timeNOW:
            displayupdate = True

        if anim_nowplaying+3 > timeNOW:
            displayupdate = True




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
                    displayupdate = True

                if event.key == pygame.K_t:
                    anim_transparency = timeNOW

                    if transparent:
                        transparent = False
                    else:
                        transparent = True

                if event.key == pygame.K_o:
                    anim_ontop = timeNOW

                    if ontop:
                        ontop = False
                        set_ontop(ontop)
                    else:
                        ontop = True
                        set_ontop(ontop)


                if event.key == pygame.K_LEFT:
                    songreset()

                    anim_song = timeNOW

                    if songnum == 0:
                        songnum = len(songqueue)-1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        if playing == True:
                            anim_nowplaying = timeNOW+1
                            pygame.mixer_music.unpause()
                            

                    else:
                        songnum -= 1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        if playing == True:
                            anim_nowplaying = timeNOW+1
                            pygame.mixer_music.unpause()

                if event.key == pygame.K_RIGHT: #right arrow

                    songreset()

                    anim_song = timeNOW

                    if len(songqueue)-1 > songnum:
                        songnum += 1
                        
                    else:
                        songnum = 0

                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    if playing == True:
                        anim_nowplaying = timeNOW+1
                        pygame.mixer_music.unpause()

                if event.key == pygame.K_UP: #up arrow
                    anim_volume = timeNOW

                    if musicvolume_percent < 100:
                        musicvolume_percent += 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

                if event.key == pygame.K_DOWN: #down arrow
                    anim_volume = timeNOW

                    if musicvolume_percent > 0:
                        musicvolume_percent -= 5
                        pygame.mixer_music.set_volume(musicvolume_percent/100)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]



































    elif scene == 'settings':

        if displayupdate:
            displayupdate = False

            mainwindow.blit(surface_static_new_settings(windowres))
            windowres_toolow(600,260)
            pygame.display.update()
        



        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if playing:
                        pygame.mixer_music.unpause()
                    
                    mainwindow.fill(colors['settings_bg'])
                    displayupdate = True
                    scene = 'visualizer'
                    


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range(1,152) and event.pos[1] in range(36,70):
                        scene = 'controls'
                        displayupdate = True

                    elif event.pos[0] in range(1,166) and event.pos[1] in range(68,100):
                        scene = 'customize'
                        displayupdate = True
                    
                    elif event.pos[0] in range(1,132) and event.pos[1] in range(100,132):
                        scene = 'program'
                        displayupdate = True

                    elif event.pos[0] in range(windowres[0]-174,windowres[0]-1) and event.pos[1] in range(40,70):
                        scene = 'visual_modes'
                        displayupdate = True

                    elif event.pos[0] in range(windowres[0]-174,windowres[0]-1) and event.pos[1] in range(76,102):
                        scene = 'songqueue'
                        displayupdate = True

                    elif event.pos[0] in range(windowres[0]-68,windowres[0]-4) and event.pos[1] in range(windowres[1]-76,windowres[1]-12):
                        os.system('start '+contacts['GitHub'])

                    elif event.pos[0] in range(windowres[0]-136,windowres[0]-72) and event.pos[1] in range(windowres[1]-76, windowres[1]-12):
                        os.system('start '+contacts['Telegram'])


                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]









    elif scene == 'controls':
        
        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_controls(windowres))
            windowres_toolow(600,260)
            pygame.display.update()


        for event in pygame.event.get():
            events_global(event)

            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]

            


    elif scene == 'customize':

        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_customize(windowres))
            windowres_toolow(600,260)
            pygame.display.update()



        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]





    elif scene == 'program':

        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_program(windowres))
            windowres_toolow(600,260)
            pygame.display.update()

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    if event.pos[0] in range(93,104) and event.pos[1] in range(38,52): #- fpscap
                        if fpscapnum > 0:
                            fpscapnum -= 1
                            fpscap = fpscap_allowed_values[fpscapnum]
                            displayupdate = True
                    elif event.pos[0] in range(104,116) and event.pos[1] in range(38,52): #+ fpscap
                        if fpscapnum < len(fpscap_allowed_values)-1:
                            fpscapnum += 1
                            fpscap = fpscap_allowed_values[fpscapnum]
                            displayupdate = True

                    elif event.pos[0] in range(228,244) and event.pos[1] in range(52,67): #bluetooth latency checkbox
                        if pr_bluetooth_output_device:
                            pr_bluetooth_output_device = False
                        else:
                            pr_bluetooth_output_device = True
                            outputdevice_load_info()
                        displayupdate = True

                    elif event.pos[0] in range(544,600) and event.pos[1] in range(172,184):
                        scene = 'credits'
                        displayupdate = True

                    elif event.pos[0] in range(windowres[0]-68,windowres[0]-4) and event.pos[1] in range(windowres[1]-76,windowres[1]-12):
                        os.system('start '+contacts['GitHub'])

                    elif event.pos[0] in range(windowres[0]-136,windowres[0]-72) and event.pos[1] in range(windowres[1]-76, windowres[1]-12):
                        os.system('start '+contacts['Telegram'])
                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

    elif scene == 'credits':
        if displayupdate:
            mainwindow.blit(surface_static_new_credits(windowres))
            windowres_toolow(600,260)
            pygame.display.update()

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'program'
                    displayupdate = True
            



    elif scene == 'visual_modes':

        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_visualmodes(windowres))
            windowres_toolow(600,260)
            pygame.display.update()



        if cl_zoom_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if cl_zoom_typing_list[-1] == ' ':
                    cl_zoom_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if cl_zoom_typing_list[-1] == '|':
                    cl_zoom_typing_list[-1] = ' '
                    displayupdate = True



        if cl_line_space_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if cl_line_space_typing_list[-1] == ' ':
                    cl_line_space_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if cl_line_space_typing_list[-1] == '|':
                    cl_line_space_typing_list[-1] = ' '
                    displayupdate = True

        if cl_rotate_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if cl_rotate_typing_list[-1] == ' ':
                    cl_rotate_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if cl_rotate_typing_list[-1] == '|':
                    cl_rotate_typing_list[-1] = ' '
                    displayupdate = True

        if cl_linelength_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if cl_linelength_typing_list[-1] == ' ':
                    cl_linelength_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if cl_linelength_typing_list[-1] == '|':
                    cl_linelength_typing_list[-1] = ' '
                    displayupdate = True


        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True

                    if cl_zoom_typing:
                        cl_typing.cancel_zoom()

                    if cl_line_space_typing:
                        cl_typing.cancel_linespace()

                    if cl_rotate_typing:
                        cl_typing.cancel_rotate()
                        displayupdate = True

                    if cl_linelength_typing:
                        cl_typing.cancel_linelength()
                        displayupdate = True


                if event.key == 13: #enter
                    
                    if cl_zoom_typing:
                        cl_typing.cancel_zoom()
                        displayupdate = True

                    if cl_line_space_typing:
                        cl_typing.cancel_linespace()
                        displayupdate = True

                    if cl_rotate_typing:
                        cl_typing.cancel_rotate()
                        displayupdate = True

                    if cl_linelength_typing:
                        cl_typing.cancel_linelength()
                        displayupdate = True


                if event.key == pygame.K_BACKSPACE:

                    if cl_zoom_typing:
                        if len(cl_zoom_typing_list) > 1:
                            cl_zoom_typing_list.pop(-2)
                            displayupdate = True
                    
                    if cl_line_space_typing:
                        if len(cl_line_space_typing_list) > 1:
                            cl_line_space_typing_list.pop(-2)
                            displayupdate = True

                    if cl_rotate_typing:
                        if len(cl_rotate_typing_list) > 2:
                            cl_rotate_typing_list.pop(-3)
                            displayupdate = True
                    
                    if cl_linelength_typing:
                        if len(cl_linelength_typing_list) > 1:
                            cl_linelength_typing_list.pop(-2)
                            displayupdate = True
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    cl_typing.cancel_zoom()
                    cl_typing.cancel_linespace()
                    cl_typing.cancel_rotate()
                    cl_typing.cancel_linelength()


                    if event.pos[0] in range(100,116) and event.pos[1] in range(40,60): #- general mode
                        if general_mode_num > 1:
                            general_mode_num -= 1
                            displayupdate = True
                    if event.pos[0] in range(116,132) and event.pos[1] in range(40,60): #+ general mode
                        if general_mode_num < len(general_mode_names):
                            general_mode_num += 1
                            displayupdate = True

                    if general_mode_num == 1:
                        
                        if event.pos[0] in range(52,62) and event.pos[1] in range(88,100): #- cl mode
                            if cl_renderingmode_num > 0:
                                cl_renderingmode_num -= 1
                                displayupdate = True
                        elif event.pos[0] in range(108,118) and event.pos[1] in range(88,100): #+ cl mode
                            if cl_renderingmode_num < len(cl_rendering_modes)-1:
                                cl_renderingmode_num += 1
                                displayupdate = True

                        elif event.pos[0] in range(4,152) and event.pos[1] in range(100,112): #typing out zoom
                            cl_zoom_typing = True
                            displayupdate = True

                        elif event.pos[0] in range(4,180) and event.pos[1] in range(112,124): #typing out space between lines
                            cl_line_space_typing = True
                            displayupdate = True

                        elif event.pos[0] in range(121,131) and event.pos[1] in range(124,136): #One dimensional checkbox
                            displayupdate = True
                            if cl_onedimensional:
                                cl_onedimensional = False
                            else:
                                cl_onedimensional = True

                        elif event.pos[0] in range(71,81) and event.pos[1] in range(136,148): #mirrored checkbox
                            if cl_onedimensional:
                                displayupdate = True
                                if cl_mirrored:
                                    cl_mirrored = False
                                else:
                                    cl_mirrored = True
    
                        elif event.pos[0] in range(4,162) and event.pos[1] in range(148,160): #rotate typing
                            cl_rotate_typing = True
                            displayupdate = True

                        elif event.pos[0] in range(4,200) and event.pos[1] in range(160,172): #linelen typing
                            cl_linelength_typing = True
                            displayupdate = True

                        else:
                            displayupdate = True

                            mousebts_hold[0] = True
                            mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                    if general_mode_num == 2:

                        if event.pos[0] in range(52,62) and event.pos[1] in range(88,100): #- cl mode
                            if cl_renderingmode_num > 0:
                                cl_renderingmode_num -= 1
                                displayupdate = True
                        elif event.pos[0] in range(108,118) and event.pos[1] in range(88,100): #+ cl mode
                            if cl_renderingmode_num < len(cl_rendering_modes)-1:
                                cl_renderingmode_num += 1
                                displayupdate = True

                        elif event.pos[0] in range(4,152) and event.pos[1] in range(100,112): #typing out zoom
                            cl_zoom_typing = True
                            displayupdate = True
                        
                        elif event.pos[0] in range(41,52) and event.pos[1] in range(112,123): #mono checkbox
                            if wf_mono:
                                wf_mono = False
                            else:
                                wf_mono = True
                            displayupdate = True

                        
                        elif event.pos[0] in range(48,60) and event.pos[1] in range(125,136): #merge checkbox
                            if not wf_mono:
                                if wf_merge:
                                    wf_merge = False
                                else:
                                    wf_merge = True
                                    wf_split = False
                                displayupdate = True
                        
                        elif event.pos[0] in range(48,60) and event.pos[1] in range(136,147): #split checkbox
                            if not wf_mono:
                                if wf_split:
                                    wf_split = False
                                else:
                                    wf_split = True
                                    wf_merge = False
                                displayupdate = True

                        #no rotate typing yet

                        else:

                            mousebts_hold[0] = True
                            mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                    if general_mode_num == 3:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                    if general_mode_num == 4:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

            if event.type == pygame.TEXTINPUT:
                try:
                    if cl_zoom_typing:
                        if len(cl_zoom_typing_list) < 8:
                            cl_zoom_typing_list.insert(len(cl_zoom_typing_list)-1,int(event.text))
                            displayupdate = True

                    if cl_line_space_typing:
                        if len(cl_line_space_typing_list) < 4:
                            cl_line_space_typing_list.insert(len(cl_line_space_typing_list)-1,int(event.text))
                            displayupdate = True

                    if cl_rotate_typing:
                        if len(cl_rotate_typing_list) < 5:
                            cl_rotate_typing_list.insert(len(cl_rotate_typing_list)-2,int(event.text))
                            displayupdate = True
                
                    if cl_linelength_typing:
                        if event.text == '.':
                            if len(cl_linelength_typing_list) < 6:
                                cl_linelength_typing_list.insert(len(cl_linelength_typing_list)-1,str(event.text))
                                displayupdate = True
                        else:
                            if str(cl_linelength_typing_list).find('.') == -1:
                                if len(cl_linelength_typing_list) < 3:
                                    cl_linelength_typing_list.insert(len(cl_linelength_typing_list)-1,int(event.text))
                                    displayupdate = True
                            else:
                                if len(cl_linelength_typing_list) < 6:
                                    cl_linelength_typing_list.insert(len(cl_linelength_typing_list)-1,int(event.text))
                                    displayupdate = True
                        
                except ValueError:
                    pass






























    elif scene == 'songqueue':
        if displayupdate:
            displayupdate = False
            mainwindow.blit(surface_static_new_songqueue(windowres))
            pygame.display.update()

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    songsrendernum = len(songqueue)

                    if event.pos[0] in range(4,4+28) and event.pos[1] in range((4*(songsrendernum+1))+(28*(songsrendernum+1))+2-scrollwheely,(4*(songsrendernum+1))+(28*(songsrendernum+1))+4+28-scrollwheely): #add song
                        set_ontop(False) #so the window doesnt cover the windows file manager


                        addsongs_files = filedialog.askopenfiles(
                                    filetypes=[('MP3', '*.mp3'),
                                               ('WAV', '*.wav'),
                                               ('OGG', '*.ogg'),
                                               ('FLAC','*.flac'),
                                               ('mp2', '*.mp2')
                                               ],
                                    title="JakeIsAlivee's Visualizer - Select your music file to add into the list",
                                    )
                        if addsongs_files == None:
                            set_ontop(ontop)
                            continue
                        
                        tempnum = 0
                        while tempnum < len(addsongs_files):
                            try:
                                songqueue.append(Song(addsongs_files[tempnum].name))
                            except:
                                messagebox.showwarning(title="JakeIsAlivee's Visualizer",
                                                       message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nSkipping the file.\nProblematic file directory:\n"+addsongs_files[tempnum].name)
                                tempnum += 1
                                continue
                            
                            tempnum += 1

                            loading_render()
                            loadedsongs_render = fonts_couriernew(64).render(str(tempnum)+'/'+str(len(addsongs_files)),False,(255,255,255))
                            mainwindow.blit(loadedsongs_render,
                                            ((windowres[0]//2)-(loadedsongs_render.get_width()//2),
                                              windowres[1]    - loadedsongs_render.get_height()))
                            
                            pygame.display.update()

                            for event in pygame.event.get():
                                if event.type == pygame.WINDOWFOCUSLOST:
                                    continue
                                events_global(event)

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button == pygame.BUTTON_LEFT:
                                        mousebts_hold[0] = True
                                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]


                        set_ontop(ontop)
                        displayupdate = True
                        continue


                    if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range(4,28): #folder import
                        set_ontop(False) #so the window doesnt cover the windows file manager

                        import_folder = filedialog.askdirectory(title="JakeIsAlivee's Visualizer - Choose the folder that you want to import your music files from")
                        if import_folder == '': #None
                            set_ontop(ontop)
                            continue
                            
                        musicfiles = os.listdir(import_folder)

                        if len(musicfiles) > 60:
                            areyousure = messagebox.askyesno(title="JakeIsAlivee's Visualizer",
                                                message="Are you sure you want to import this folder?\nLooks like there's "+str(len(musicfiles))+" files.\nThis will take a long time.")
                            if areyousure == False:
                                set_ontop(ontop)
                                continue
                            del areyousure

                        tempnum = 0
                        while tempnum < len(musicfiles):
                                
                            if musicfiles[tempnum][len(musicfiles[tempnum])-5:len(musicfiles[tempnum])] not in musicformats and musicfiles[tempnum][len(musicfiles[tempnum])-4:len(musicfiles[tempnum])] not in musicformats:
                                musicfiles.pop(tempnum)
                                continue

                            tempnum += 1

                        if len(musicfiles) == 0:
                            messagebox.showinfo(title="JakeIsAlivee's Visualizer",
                                                message="There is no music files in this folder")
                            set_ontop(ontop)
                            continue
                        
                        for i in songqueue:
                            i.rawfile.close()

                        songqueue = []
                        tempnum = 0
                        while tempnum < len(musicfiles):
                            try:
                                songqueue.append(Song(import_folder+slash+musicfiles[tempnum]))
                            except:
                                messagebox.showwarning(title="JakeIsAlivee's Visualizer",
                                                       message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nSkipping the file.\nProblematic file directory:\n"+import_folder+slash+musicfiles[tempnum])
                                tempnum += 1
                                continue

                            tempnum += 1

                            loading_render()
                            loadedsongs_render = fonts_couriernew(64).render(str(tempnum)+'/'+str(len(musicfiles)),False,(255,255,255))
                            mainwindow.blit(loadedsongs_render,
                                            ((windowres[0]//2)-(loadedsongs_render.get_width()//2),
                                              windowres[1]    - loadedsongs_render.get_height()))
                            
                            pygame.display.update()

                            for event in pygame.event.get():
                                if event.type == pygame.WINDOWFOCUSLOST:
                                    continue
                                events_global(event)

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button == pygame.BUTTON_LEFT:
                                        mousebts_hold[0] = True
                                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                        songreset()
                        songnum = 0

                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        set_ontop(ontop)
                        displayupdate = True
                        continue

                    if event.pos[0] in range(windowres[0]-60,windowres[0]-36) and event.pos[1] in range(4,28): #shuffle songs
                        tempnum = 0
                        songqueuecopy = songqueue.copy()
                        lensongqueue = len(songqueue)
                        songqueue.clear()
                        while tempnum < lensongqueue:
                            randomnum = random.randint(0,len(songqueuecopy)-1)
                            songqueue.append(songqueuecopy[randomnum])
                            songqueuecopy.pop(randomnum)
                            tempnum += 1
                        del tempnum
                        del songqueuecopy
                        del lensongqueue
                        del randomnum
                        displayupdate = True
                        songreset()
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                    if event.pos[0] in range(windowres[0]-92,windowres[0]-68) and event.pos[1] in range(4,28): #reverse songs
                        tempnum = 0
                        reversedsongqueue = []
                        while tempnum < len(songqueue):
                            reversedsongqueue.append(songqueue[len(songqueue)-tempnum-1])
                            tempnum += 1
                        songqueue = reversedsongqueue.copy()
                        displayupdate = True
                        del tempnum
                        del reversedsongqueue
                        songreset()
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                        


                    #this is so fucking bad
                    while songsrendernum+1 > 1:
                        #view file in explorer
                        if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                            os.system('explorer /select,"'+str(songqueue[songsrendernum-1].songdir).replace('/','\\')+'"')

                        if len(songqueue) != 1:
                            if event.pos[1] in range(28,windowres[1]-24):
                                
                                #delete song
                                if event.pos[0] in range(windowres[0]-56,windowres[0]-32) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                    
                                    songqueue[songsrendernum-1].rawfile.close()
                                    songqueue.pop(songsrendernum-1)
                                    if songnum > len(songqueue)-1:

                                        songnum = len(songqueue)-1
                                        
                                        songreset()
                            
                                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                                    if songnum == songsrendernum-1:
                                        songreset()
                            
                                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                                        
                                    displayupdate = True

                                #movedown song
                                if event.pos[0] in range(windowres[0]-84,windowres[0]-60) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                    movingsong = songqueue[songsrendernum-1]
                                    songqueue.pop(songsrendernum-1)
                                    songqueue.insert(songsrendernum,movingsong)
                                    displayupdate = True

                                    if songnum == songsrendernum-1 or songnum == songsrendernum:
                                        songreset()
                            
                                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                                        
                                
                                if songsrendernum != 1:
                                    #moveup song
                                    if event.pos[0] in range(windowres[0]-112,windowres[0]-88) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                        movingsong = songqueue[songsrendernum-1]
                                        songqueue.pop(songsrendernum-1)
                                        songqueue.insert(songsrendernum-2,movingsong)
                                        displayupdate = True
                                        if songnum == songsrendernum-1 or songnum == songsrendernum-2:
                                            songreset()
                            
                                            soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                                        

                        songsrendernum -= 1

                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                if event.button == pygame.BUTTON_WHEELUP:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely != 0:
                            scrollwheely -= 16
                            displayupdate = True
                        

                if event.button == pygame.BUTTON_WHEELDOWN:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely < (4*len(songqueue))+(28*len(songqueue))+2-windowres[1]+80:
                            scrollwheely += 16
                            displayupdate = True
                        




for event in pygame.event.get():
    events_global(event)

    
selectedfiles = filedialog.askopenfiles(
        filetypes=[('MP3', '*.mp3'),
                   ('WAV', '*.wav'),
                   ('OGG', '*.ogg'),
                   ('FLAC','*.flac'),
                   ('mp2', '*.mp2')
                   ],
        title="JakeIsAlivee's Visualizer - Select your music files to visualize",
        
    )
if len(selectedfiles) == 0:
    sys.exit()

songqueue = []

tempnum = 0
while tempnum < len(selectedfiles):
    try:
        songqueue.append(Song(selectedfiles[tempnum].name))
    except:
        messagebox.showwarning(title="JakeIsAlivee's Visualizer",
                               message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nSkipping the file.\nProblematic file directory:\n"+selectedfiles[tempnum].name)
        tempnum += 1
        continue
                            
    tempnum += 1

    loading_render()
    loadedsongs_render = fonts_couriernew(64).render(str(tempnum)+'/'+str(len(selectedfiles)),False,(255,255,255))
    mainwindow.blit(loadedsongs_render,
                    ((windowres[0]//2)-(loadedsongs_render.get_width()//2),
                      windowres[1]    - loadedsongs_render.get_height()))
                            
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.WINDOWFOCUSLOST:
            continue
        events_global(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mousebts_hold[0] = True
                mouseholddrag_startpos = [event.pos[0],event.pos[1]]

songreset()
soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

set_ontop(True)
set_transparency(colors['transparent_chromakey_win'])

del selectedfiles

while True:
    try:
        scenes()
        timeNOW = time.perf_counter()
        pygameclock.tick(fpscap)
        
        if devmode:
            if timeNOW - int(timeNOW) < 0.01:
                print(pygameclock.get_fps())
        
    except Exception as exc_traceback:
        set_ontop(False)

        problematicline = sys.exc_info()[2]
        while problematicline.tb_next != None:
            problematicline = problematicline.tb_next
            

        messagebox.showerror(title="JakeIsAlivee's Visualizer",
                             message="A Fatal Error Occured!\nMake a screenshot of this error and send it to the creator of this program.\nThe program will now close.",
                             detail='VERSION: '+VERSION+'\n'+
                                    'Exception: '+str(exc_traceback.__class__.__name__)+'\n'+
                                    'Message: '+str(exc_traceback)+'\n'+
                                    'Occured at: '+str(problematicline.tb_lineno)+' line\n'+
                                    'Problematic line:\n"'+open(problematicline.tb_frame.f_code.co_filename,'r').readlines()[problematicline.tb_lineno-1].replace('\n','')+'"',
                             
                                    )
        

        pygame.quit()
        sys.exit()
       

