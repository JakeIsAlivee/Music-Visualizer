
""" things to add: 

[done] fix lag in song queue scene when theres too many songs

[ongoing forever lol] get this script to be more object oriented 

add osciloscope mode

add a shuffle button for song queue
add a button to reverse the song order in song queue
add a button to view the song in windows explorer

[done] make animation depend on pc time instead of avgfps

[done] fix window not responding in loading scenes

[not possible/not compatible] add new visualizer mode that listens to your pc audio in real time 

[done] replace easygui with tkinter filedialog

add more scenes for bg color customization

[done] fix lagging in settings for some reason

add another scene for visualizer settings


add customizations in customization scene
write ALLLLL controls there is in the controls scene
replace jakeisalivees icon color so theres no black and the program doesnt pick it up as transparent color 
"""

#all of this is not stable and not done at all

import soundfile #not installing on pydroid

import pygame #ce

import os
import sys

import time

import gc

VERSION = "WIP2.2.0"

scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep

icons = {
    'jakeisalivee': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'JakeIsAlivee coffee cup.ico'),(64,64)),
    'telegram': pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'Telegram.png'),(64,64)),

    'keyboard': pygame.transform.rotate(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'Keyboard.png'),-15),
    'brush': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'draw.png'),
    'visualizer': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'visualizer icon.png'),

    'folder': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'folder icon.png'),

    'moveup': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'moveup icon.png'),
    'movedown': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'movedown icon.png'),
    'delete': pygame.image.load(scriptdirfolder+slash+'Data'+slash+'delete icon.png'),

}


from tkinter import filedialog
from tkinter import messagebox
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
    
    global surface_settings_update
    global surface_visualizer_update
    global surface_controls_update
    global surface_customize_update
    global surface_songqueue_update
                                    
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
                    surface_settings_update = True
                    surface_visualizer_update = True
                    surface_controls_update = True
                    surface_customize_update = True
                    surface_songqueue_update = True
                    

            if mousebts_hold[2]:
                if windowres[0] < desktopsize[0]:
                    windowres[0] += 10
                    mouseholddrag_startpos[0] += 5
                    windowpos[0] -= 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    surface_settings_update = True
                    surface_visualizer_update = True
                    surface_controls_update = True
                    surface_customize_update = True
                    surface_songqueue_update = True
                    
        
                    

        if event.button == pygame.BUTTON_WHEELDOWN:
                    
            if mousebts_hold[0]:
                if windowres[1] > 10:
                    windowres[1] -= 10
                    mouseholddrag_startpos[1] -= 5
                    windowpos[1] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    surface_settings_update = True
                    surface_visualizer_update = True
                    surface_controls_update = True
                    surface_customize_update = True
                    surface_songqueue_update = True
                    

            if mousebts_hold[2]:
                if windowres[0] > 10:
                    windowres[0] -= 10
                    mouseholddrag_startpos[0] -= 5
                    windowpos[0] += 5

                    mainwindow = pygame.display.set_mode((windowres[0],windowres[1]),pygame.NOFRAME | pygame.SRCALPHA)
                    pygame.display.set_window_position((windowpos[0],windowpos[1]))
                    surface_settings_update = True
                    surface_visualizer_update = True
                    surface_controls_update = True
                    surface_customize_update = True
                    surface_songqueue_update = True
                    

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
                      > visual_modes
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

linelength = 1


colors = {

    'window_border': (0,0,255,255),

    'visualizer_bg': (0,0,254,255),
    'visualizer_lines': (255,255,255,255),

    'program_notifs': (10,10,10,255),

    'settings_bg': (0,0,128,255),
    'settings_text': (255,255,255,255),

    'transparent_chromakey_win': (0,0,0),
    'transparent_chromakey': (0,0,0,255),
    
}

#optimizations
def surface_static_new_visualizer(surfaceres):
    global timeNOW

    global colors

    global anim_ontop
    global anim_song
    global anim_transparency
    global anim_volume

    global playing

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    if transparent == False:
        surface.fill(colors['visualizer_bg'])
    if transparent == True:
        surface.fill(colors['transparent_chromakey'])
    
    xnum = 0
    while xnum < surfaceres[0]:
        try:
                
            rendering_formulas = [
                int(xnum)-(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0]//2)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0])+((lastsounddata)//devisionby),
                int(xnum)-(surfaceres[0])+((lastsounddata)//devisionby),
                int(xnum)+((lastsounddata)//devisionby),
                0-int(xnum)+((lastsounddata)//devisionby),
                0-int(xnum)+(surfaceres[0])+((lastsounddata)//devisionby),
                int(xnum)-(surfaceres[0])+((lastsounddata)//devisionby),
            ]

            linesrender_formula = rendering_formulas[renderingmode_num]
               

            if linesrender_formula < 0:
                xnum += 1
                continue

            if renderingmode_num == 2 or renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                pygame.draw.line(surface,colors['visualizer_lines'],
                         (int(xnum)//2,(surfaceres[1]/2)+((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                         (int(xnum)//2,(surfaceres[1]/2)-((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))
                pygame.draw.line(surface,colors['visualizer_lines'],
                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]/2)+((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                         (surfaceres[0]-int(xnum)//2,(surfaceres[1]/2)-((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))

                xnum += 1
                continue


            pygame.draw.line(surface,colors['visualizer_lines'],
                         (int(xnum),(surfaceres[1]/2)+((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767*linelength))),
                         (int(xnum),(surfaceres[1]/2)-((surfaceres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767*linelength))))

            xnum += 1
        except IndexError:
            xnum += 1
    

    
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

    if renderingmode_num < 4:
        pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2)-1,10),((surfaceres[0]/2)-1,surfaceres[1]-10))
        pygame.draw.line(surface,(0,0,128),((surfaceres[0]/2),10)  ,((surfaceres[0]/2),  surfaceres[1]-10))

    if playing == False:
        pygame.draw.line(surface,colors['program_notifs'],((surfaceres[0]/2)-50,(surfaceres[1]/2)+80),((surfaceres[0]/2)-50,(surfaceres[1]/2)-80),10)
        pygame.draw.line(surface,colors['program_notifs'],((surfaceres[0]/2)+50,(surfaceres[1]/2)+80),((surfaceres[0]/2)+50,(surfaceres[1]/2)-80),10)

    pygame.draw.lines(surface,(0,0,255,255),False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface




def surface_static_new_settings(surfaceres):
    global colors

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    settings_text =       fonts_couriernew(32).render('Settings',False,colors['settings_text'])
    surface.blit(settings_text,      ((surfaceres[0]//2)-(settings_text.get_width()//2),2))

    surface.blit(pygame.transform.invert(icons['keyboard']),(0,36))
    controls_text = fonts_couriernew(24).render('Controls',False,colors['settings_text'])
    surface.blit(controls_text,(38,44))   
    pygame.draw.lines(surface,(128,128,128),False,[(36,44),(152,44),
                                                      (152,68),(36,68),    (36,44)])

    surface.blit(pygame.transform.invert(icons['brush']),(2,68))
    customize_text = fonts_couriernew(24).render('Customize',False,colors['settings_text'])
    surface.blit(customize_text,(38,76))
    pygame.draw.lines(surface,(128,128,128),False,[(36,76),(166,76),
                                                      (166,100),(36,100),   (36,76)])

    esc_back_text =      fonts_couriernew(16).render('Esc: Back',False,colors['settings_text'])
    surface.blit(esc_back_text,     ((4),(surfaceres[1]-2-esc_back_text.get_height())))

    zoom_text = fonts_couriernew(24).render(' Zoom: ',False,colors['settings_text'])
    surface.blit(zoom_text, (surfaceres[0]-4-zoom_text.get_width(),
                                
                                2))

    zoomxnum_text = fonts_couriernew(24).render('<'+userzoom_to_devision_dict[devisionby]+'>',False,colors['settings_text'])
    surface.blit(zoomxnum_text, (surfaceres[0]-4-zoomxnum_text.get_width(),

                                    2+zoom_text.get_height()+
                                    2))

    mode_text = fonts_couriernew(24).render('Mode:  ',False,colors['settings_text'])
    surface.blit(mode_text, (surfaceres[0]-4-mode_text.get_width(),

                                2+zoom_text.get_height()+
                                2+zoomxnum_text.get_height()+
                                2))

    modevisual_text = fonts_couriernew(24).render('< "'+str(rendering_modes[renderingmode_num])+'" >',False,colors['settings_text'])
    surface.blit(modevisual_text, (surfaceres[0]-4-modevisual_text.get_width(),
                                      2+zoom_text.get_height()+
                                      2+zoomxnum_text.get_height()+
                                      2+mode_text.get_height()+
                                      2))

    songsqueue_text = fonts_couriernew(24).render('Song Queue',False,colors['settings_text'])
    surface.blit(songsqueue_text, (surfaceres[0]-4-songsqueue_text.get_width(),
                                      2+zoom_text.get_height()+
                                      2+zoomxnum_text.get_height()+
                                      2+mode_text.get_height()+
                                      2+modevisual_text.get_height()+
                                      2))

    surface.blit(pygame.transform.scale(icons['jakeisalivee'],(64,64)), (surfaceres[0]-68,surfaceres[1]-68))
    surface.blit(pygame.transform.scale(icons['telegram'],(64,64)),(surfaceres[0]-136,surfaceres[1]-68))

    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface




def surface_static_new_controls(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])


    
    buttons_text =       fonts_couriernew(32).render('Controls',False,colors['settings_text'])
    surface.blit(buttons_text,      ((surfaceres[0]//2)-(buttons_text.get_width()//2),2))
        
    esc_back_text =      fonts_couriernew(16).render('Esc: Back',False,colors['settings_text'])
    surface.blit(esc_back_text,     ((4),(surfaceres[1]-2-esc_back_text.get_height())))

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
    
    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface


def surface_static_new_customize(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    esc_back_text =      fonts_couriernew(16).render('Esc: Back',False,colors['settings_text'])
    surface.blit(esc_back_text,     ((4),(surfaceres[1]-2-esc_back_text.get_height())))


    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface

def surface_static_new_songqueue(surfaceres):
    global songsrendernum

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])

    songsrendernum = 1
    while songsrendernum <= len(songqueue):

        if (4*songsrendernum)+(28*songsrendernum)+4 < scrollwheely:
            songsrendernum += 1
            continue

        songdir = os.path.split(songqueue[songsrendernum-1].songdir)[1]
        if len(songdir) > ((surfaceres[0]-90)/12):
            songdir = songdir[0:((surfaceres[0]-90)//12)]+'...'
                

        songdir_text = fonts_JhengHei(16).render(' '+str(songsrendernum)+'. "'+str(songdir)+'"',False,colors['settings_text'])

        surface.blit(songdir_text,(4,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        pygame.draw.line(surface,colors['window_border'],(0,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely),(surfaceres[0],(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely))

        surface.blit(icons['delete'],(surfaceres[0]-28,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icons['movedown'],(surfaceres[0]-56,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icons['moveup'],(surfaceres[0]-84,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))

        songsrendernum += 1
        
        if (4*songsrendernum)+(28*songsrendernum)+4-scrollwheely > surfaceres[1]:
            break

    addsong_text = fonts_couriernew(24).render('+',False,colors['settings_text'])
    surface.blit(addsong_text,(4,(4*songsrendernum)+(28*songsrendernum)+2-scrollwheely))


    songsqueue_text = fonts_couriernew(24).render('Song queue',False,colors['settings_text'])
    surface.blit(songsqueue_text,(4,2))
    pygame.draw.line(surface,colors['window_border'],(0,4+songsqueue_text.get_height()),(surfaceres[0],4+songsqueue_text.get_height()))

    surface.blit(icons['folder'],(surfaceres[0]-28,4))


    pygame.draw.line(surface, colors['window_border'],(0,surfaceres[1]-25),(surfaceres[0],surfaceres[1]-25))

    esc_back_text =      fonts_couriernew(16).render('Esc: Back',False,colors['settings_text'])
    surface.blit(esc_back_text,     ((4),(surfaceres[1]-2-esc_back_text.get_height())))

    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface

def surface_static_new_visualmodes(surfaceres):

    surface = pygame.Surface((surfaceres[0],surfaceres[1]),pygame.SRCALPHA)
    surface.fill(colors['settings_bg'])


    pygame.draw.lines(surface,colors['window_border'],False, [(0,0),(0,surfaceres[1]-1),(surfaceres[0]-1,surfaceres[1]-1),(surfaceres[0]-1,0),(0,0)])

    return surface



surface_visualizer_update = True

surface_settings_update = True

surface_controls_update = True

surface_customize_update = True

surface_visualmodes_update = True


surface_songqueue_update = True

# 12 len list, write "jakeisalivee" to activate devmode
devmodeactivation_list = []
devmode = False



timeNOW = time.perf_counter()


def windowres_toolow():
    global windowres
    global mainwindow

    #600,260
    width = False
    height = False

    transparency = 0
    if windowres[0] < 600 or windowres[1] < 260:
        transparency1 = 255*(1-(windowres[0]/600))*1.5
        if transparency1 > 0:
            width = True

        transparency2 = 255*(1-(windowres[1]/260))*1.5
        if transparency2 > 0:
            height = True

        if transparency1 > transparency2:
            transparency = transparency1
        else:
            transparency = transparency2
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
    
    global colors
    global surface_settings_update
    global surface_visualizer_update
    global surface_controls_update
    global surface_customize_update
    global surface_songqueue_update

    global songsrendernum

    if scene == 'visualizer':
        
        if surface_visualizer_update:
            surface_visualizer_update = False
            mainwindow.blit(surface_static_new_visualizer(windowres))
            pygame.display.update()

        if playing:
            surface_visualizer_update = True
        
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

        if anim_volume+1 > timeNOW:
            surface_visualizer_update = True

        if anim_transparency+1 > timeNOW:
            surface_visualizer_update = True
        
        if anim_ontop+1 > timeNOW:
            surface_visualizer_update = True

        if anim_song+1 > timeNOW:
            surface_visualizer_update = True






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
                    surface_settings_update = True

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
                            pygame.mixer_music.unpause()

                    else:
                        songnum -= 1
                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        if playing == True:
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

        if surface_settings_update:
            surface_settings_update = False

            mainwindow.blit(surface_static_new_settings(windowres))
            windowres_toolow()
            pygame.display.update()
        



        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if playing:
                        pygame.mixer_music.unpause()
                    
                    mainwindow.fill(colors['settings_bg'])
                    surface_visualizer_update = True
                    scene = 'visualizer'


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range(1,152) and event.pos[1] in range(36,70): #controls button
                        scene = 'controls'
                        surface_controls_update = True

                    if event.pos[0] in range(1,166) and event.pos[1] in range(68,100):
                        scene = 'customize'
                        surface_customize_update = True

                    if event.pos[0] in range(windowres[0]-68,windowres[0]-4) and event.pos[1] in range(windowres[1]-68,windowres[1]-4):
                        os.system('start '+contacts['GitHub'])

                    elif event.pos[0] in range(windowres[0]-136,windowres[0]-72) and event.pos[1] in range(windowres[1]-68, windowres[1]-4):
                        os.system('start '+contacts['Telegram'])
						
                    elif event.pos[0] in range(windowres[0]-106,windowres[0]-88) and event.pos[1] in range(32,56): #- zoom
                        if devisionby != 1024:
                            devisionby *= 2
                        surface_settings_update = True

                    elif event.pos[0] in range(windowres[0]-18,windowres[0]-2) and event.pos[1] in range(32,56): #+ zoom
                        if devisionby != 1:
                            devisionby //= 2
                        surface_settings_update = True

                    elif event.pos[0] in range(windowres[0]-134,windowres[0]-116) and event.pos[1] in range(94,116): #- mode
                        if renderingmode_num != 0:
                            renderingmode_num -= 1
                        surface_settings_update = True

                    elif event.pos[0] in range(windowres[0]-18,windowres[0]-2) and event.pos[1] in range(94,116): #+ mode
                        if renderingmode_num != len(rendering_modes)-1:
                            renderingmode_num += 1
                        surface_settings_update = True

                    elif event.pos[0] in range(windowres[0]-148,windowres[0]-2) and event.pos[1] in range(124,150): #songsqueue scene
                        scene = 'songqueue'
                        surface_songqueue_update = True
                    

                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]









    elif scene == 'controls':
        
        if surface_controls_update:
            surface_controls_update = False
            mainwindow.blit(surface_static_new_controls(windowres))
            windowres_toolow()
            pygame.display.update()


        for event in pygame.event.get():
            events_global(event)

            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    surface_settings_update = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]

            


    elif scene == 'customize':

        if surface_customize_update:
            surface_customize_update = False
            mainwindow.blit(surface_static_new_customize(windowres))
            windowres_toolow()
            pygame.display.update()



        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    surface_settings_update = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]



































    elif scene == 'songqueue':
        if surface_songqueue_update:
            surface_songqueue_update = False
            mainwindow.blit(surface_static_new_songqueue(windowres))
            pygame.display.update()

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    surface_settings_update = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    songsrendernum = len(songqueue)

                    if event.pos[0] in range(4,4+28) and event.pos[1] in range((4*(songsrendernum+1))+(28*(songsrendernum+1))+2-scrollwheely,(4*(songsrendernum+1))+(28*(songsrendernum+1))+4+28-scrollwheely): #add song
                        set_ontop(False) #so the window doesnt cover the windows file manager

                        try:
                            addsong_file = filedialog.askopenfile(
                                    filetypes=[('MP3', '*.mp3'),
                                               ('WAV', '*.wav'),
                                               ('OGG', '*.ogg'),
                                               ('FLAC','*.flac'),
                                               ('mp2', '*.mp2')
                                               ],
                                    title="JakeIsAlivee's Visualizer - Select your music file to add into the list",
                                    ).name
                        except AttributeError: #NoneType file
                            continue

                        songqueue.append(Song(addsong_file))

                        set_ontop(ontop)
                        surface_songqueue_update = True


                    if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range(4,28): #folder import
                        set_ontop(False) #so the window doesnt cover the windows file manager

                        import_folder = filedialog.askdirectory(title="JakeIsAlivee's Visualizer - Choose the folder that you want to import your music files from")
                        if import_folder == '': #None
                            set_ontop(ontop)
                            continue
                            
                        songreset()
                        songnum = 0

                        soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

                        musicfiles = os.listdir(import_folder)

                        if len(musicfiles) > 30:
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

                        songqueue = []
                        tempnum = 0
                        while tempnum < len(musicfiles):
                            songqueue.append(Song(import_folder+slash+musicfiles[tempnum]))
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


                            

                        set_ontop(ontop)
                        surface_songqueue_update = True
                        continue
                        



                    while songsrendernum > 1:
                        
                        if event.pos[1] in range(28,windowres[1]-24):
                            #delete song
                            if event.pos[0] in range(windowres[0]-28,windowres[0]-4) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                songqueue[songsrendernum-1].rawfile.close()
                                songqueue.pop(songsrendernum-1)
                                if songnum > len(songqueue)-1:

                                    songnum = len(songqueue)-1
                                        
                                    songreset()
                            
                                    soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)
                                surface_songqueue_update = True

                            #movedown song
                            if event.pos[0] in range(windowres[0]-56,windowres[0]-32) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                movingsong = songqueue[songsrendernum-1]
                                songqueue.pop(songsrendernum-1)
                                songqueue.insert(songsrendernum,movingsong)
                                surface_songqueue_update = True
                            #moveup song
                            if event.pos[0] in range(windowres[0]-84,windowres[0]-60) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely):
                                movingsong = songqueue[songsrendernum-1]
                                songqueue.pop(songsrendernum-1)
                                songqueue.insert(songsrendernum-2,movingsong)
                                surface_songqueue_update = True

                        songsrendernum -= 1

                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                if event.button == pygame.BUTTON_WHEELUP:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely != 0:
                            scrollwheely -= 16
                            surface_songqueue_update = True
                        

                if event.button == pygame.BUTTON_WHEELDOWN:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if scrollwheely < (4*len(songqueue))+(28*len(songqueue))+2-windowres[1]+80:
                            scrollwheely += 16
                            surface_songqueue_update = True
                        




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
        title="JakeIsAlivee's Visualizer - Select your music file to visualize",
        
    ).name
except AttributeError: #NoneType file
    sys.exit()


songqueue = [Song(selectedfile)]
soundrawdata, soundrate = songqueue[songnum].load(musicvolume_percent)

set_ontop(True)
set_transparency(colors['transparent_chromakey_win'])

while True:
    try:
        scenes()
        timeNOW = time.perf_counter()
        pygameclock.tick()

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
                                    'Problematic line:\n"'+open(problematicline.tb_frame.f_code.co_filename,'r').readlines()[problematicline.tb_lineno-1].replace('\n','').replace(' ','')+'"',
                                    )
        

        pygame.quit()
        sys.exit()
       

