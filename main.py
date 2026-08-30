""" This program runs with a free-threaded python ver """

import sys
import os


sys.stderr = open("log", "w", encoding="utf-8")

import autoupdate as jia_autoupdate


scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep
VERSION = "v3.0.0"
AUTHORNAME = 'JakeIsAlivee'
REPONAME = 'Music-Visualizer'
icon_jakeisalivee_dir = scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee.ico'

jia_autoupdate.update_check(icon_jakeisalivee_dir,VERSION,REPONAME,AUTHORNAME)

import faulthandler
faulthandler.enable()
import psutil

"""
list of things changed compared to the release version so far:

Program functionality:
- Animations now depend on computer time instead of average program fps
- Settings interface rework
- New Customize panel  
- New Program panel  
- New Visualizer panel  
- Link to the telegram channel  
- More song queue functionality  
- Small song queue interface changes  
- All scenes fps optimizations

- The loading screen doesnt lag now at all
- The loading screen now shows the number of songs it has imported
- The loading screen can now be transparent

- Added a visual effect if the window resolution gets too low for a specific scene

- Removed animations for "transparent", "always on top", "next/previous song" and "volume up/down" options in settings
- Added a "Now playing: (song name)" animation for every time the song changes
- The program now doesnt let you just delete the music file that it loaded until you remove it from the song queue

- Settings now show the version of the program
- Added a check if youre OS is windows or not

- Added Oscilloscope mode and settings
- Added Waveform mode and settings
- Added more Classic Mode settings
- Added Bars mode and a lot of settings
- Added a visualization of frequency boost setting when you hover your mouse over it

- Added Credits in Program settings
- Added 2 funny easter eggs in Credits
- "I can do anything" sound is played when clicked on a dev icon in settings

- Added new controls

- Added a HIGHLOAD mode that makes the visualizer use multiple threads for rendering (unstable)
- Added a customizable fps cap in Program scene
- Added a bluetooth latency fix checkbox in Program scene

- Added effects for Classic and Waveform modes

- Critical errors now show much more info about the error
- Added a memory leak prevention just in case 

- Added a check for a new version of the program every time you open it



Technical stuff:
- Switched to tkinter filedialog instead of easygui (less .exe size i think)
- Got 1 whole file splitted into seprate ones
- Switched to pygame's message_box instead of tkinter's message_box > buttons became more customizable

- Not lagging loading screen animation


- Bug fixesssssssssss
- A lot of them
- Cant even count how many there was


"""










""" what to do: 

- fix the bug where pixels between lines start to tweak tf out


[practically not possible without additional drivers like virtual sound cards, and this programs needs to "just work" without any aditional steps or installations] 
add new visualizer mode that listens to your pc/program audio in real time 

-async .song s loading

"""


"""

сделать так чтобы следующая песня загружалась в оперативку параллельно вторым процессом за 10 сек до конца нынешней чтобы не подлагивало

загружать 2 песни сразу для плавного перехода и просмотра их зв. волн

чистка песни ДО, при выходе вывода зв. волны за экран, учитывая отдаление

режим воспроизведения песен из компонентов и их рисовка 

"""


    
#all of this is pretty stable but not done at all


import pygame #ce
os.environ["PYTHON_GIL"] = "0"

import time

import threading
from queue import Queue

pygame.init()

if __name__ == '__main__':

    if str(sys.platform).lower()[0:3] != 'win':
        proceed = pygame.display.message_box('Incompatible OS',
                                            'This program was made for the WINDOWS system.\nYour OS name is: '+str(sys.platform).capitalize()+'\nIt is highly recomended that you close the program because it was NOT made for the system youre on and might crash immediately.\nProceed anyway?',
                                            message_type='warn',
                                            buttons=('Yes','Close')) #returns the button index from 0 
        if proceed == 1:
            pygame.quit()
            sys.exit()

colors = {

    'window_border': (0,0,150,255),

    'visualizer_bg': (0,0,255,255),
    'visualizer_lines': (255,255,255,255),

    'program_notifs': (10,10,10,255),

    'settings_bg': (10,10,10,200),
    'settings_text': (255,255,255,255),

    'transparency_color': (0,0,255,255),

    'transparent_chromakey_win': (0,0,255), #should ALWAYS be last in the dict
    
}





icon_jakeisalivee = pygame.transform.scale(pygame.image.load(icon_jakeisalivee_dir),(64,64))
icon_jakeisalivee.set_colorkey((0,0,0))

surface1 = pygame.Surface((64,64))
surface1.fill((2,2,2))
surface1.blit(icon_jakeisalivee)
icon_jakeisalivee = surface1.copy()
del surface1


sound_icandoanything = pygame.Sound(scriptdirfolder+slash+'Data'+slash+'sound'+slash+'I can do anything!.mp3')
sound_icandoanything.set_volume(0.1)


unifont_dir = scriptdirfolder+slash+'Data'+slash+'unifont-17.0.04.otf'
def fonts_unifont(size):
    return pygame.Font(unifont_dir,size)

desktopsize = pygame.display.get_desktop_sizes()[0]


import ctypes
from ctypes import wintypes
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
LWA_COLORKEY = 0x00000001
user32 = ctypes.windll.user32

user32.FindWindowExW.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]
user32.FindWindowExW.restype = wintypes.HWND
user32.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
user32.GetWindowLongW.restype = ctypes.c_long
user32.SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
user32.SetWindowLongW.restype = ctypes.c_long
user32.SetLayeredWindowAttributes.argtypes = [wintypes.HWND, wintypes.COLORREF, wintypes.BYTE, wintypes.DWORD]
user32.SetLayeredWindowAttributes.restype = wintypes.BOOL

VULKAN = True
OPENGL = False

size = [600,260]
mainwindow = pygame.Window("JakeIsAlivee's Music Visualizer",
                        size=(600,260),
                        position=((desktopsize[0]//2)-(size[0]//2),(desktopsize[1]//2)-(size[1]//2)),
                        borderless=True,
                        resizable=False,
                        always_on_top=True,


                        
                        )
del size
mainwindow_surface = mainwindow.get_surface()
mainwindow.set_icon(icon_jakeisalivee)
mainwindow.opacity = 1


windowinfo = user32.FindWindowExW(None,None,None,mainwindow.title)

user32.SetWindowLongW(windowinfo, GWL_EXSTYLE,
                      user32.GetWindowLongW(windowinfo, GWL_EXSTYLE) | WS_EX_LAYERED)

def set_transparency(chromakey: tuple):
    rgb = chromakey[0] | (chromakey[1]<<8) | (chromakey[2]<<16)
    user32.SetLayeredWindowAttributes(windowinfo, rgb, 0, LWA_COLORKEY)

set_transparency(colors['transparent_chromakey_win'])
transparent = True




    
def loading_screen_surface(window_surface: pygame.Surface,
                           window: pygame.Window,
                           circleanim_start: float
                           ):
    window_surface.fill(colors['transparent_chromakey_win'])
    loadingtext = fonts_unifont(64).render('Loading...',False,(255,255,255))
    window_surface.blit(loadingtext,((window.size[0]/2)-(loadingtext.get_width()/2),
                                                            (window.size[1]/2)-(loadingtext.get_height()/2))) 
                        
    circle = pygame.Surface((64,64),pygame.SRCALPHA)

    pygame.draw.circle(circle,(0,255,255),(32,32),30,32)
    transparent = colors['transparent_chromakey_win']

    circleanim = time.perf_counter() - circleanim_start
    circleanim = circleanim %4
    if circleanim >= 0 and circleanim < 1:
        pos = (39,25+(14*circleanim))
        pygame.draw.circle(circle,transparent,pos,25,26)

    if circleanim >= 1 and circleanim < 2:
        pos = (39-(14*(circleanim-1)),39)
        pygame.draw.circle(circle,transparent,pos,25,26)
        
    if circleanim >= 2 and circleanim < 3:
        pos = (25,39-(14*(circleanim-2)))
        pygame.draw.circle(circle,transparent,pos,25,26)

    if circleanim >= 3 and circleanim < 4:
        pos = (25+(14*(circleanim-3)),25)
        pygame.draw.circle(circle,transparent,pos,25,26)

        
    window_surface.blit(circle,(window.size[0]-66,window.size[1]-66))
    
loading_thread_run = True   
def loading_screen_Thread(window_surface: pygame.Surface,
                          window: pygame.Window,
                          circleanim_start: float,
                          rendernumofsongs: bool = None,
                          numofsongs_queue: Queue = None,
                          songsleft: int = None,
                          ):
    global loading_thread_run
    while loading_thread_run:
        loading_screen_surface(window_surface,window,circleanim_start)

        if rendernumofsongs:
            try:
                num = numofsongs_queue.get_nowait()
            except:
                pass
            loadedsongs_render = fonts_unifont(64).render(str(num)+'/'+str(songsleft),False,colors['settings_text'])
            window_surface.blit(loadedsongs_render,
                                
                                ((mainwindow.size[0]//2)-(loadedsongs_render.get_width()//2),
                                  mainwindow.size[1]    - loadedsongs_render.get_height()))
            
        window.flip()

loadinganim = time.perf_counter()
loading_thread = threading.Thread(target=loading_screen_Thread,args=(mainwindow_surface,mainwindow,loadinganim))
loading_thread.start()




import settings as jia_settings
import song as jia_song
import visualizer as jia_visualizer



jia_settings.init(VERSION,icon_jakeisalivee)



import gc
import random

#venvpath = scriptdirfolder[0:len(scriptdirfolder)-30]
#os.add_dll_directory(venvpath+".venv"+slash+"vcpkg") #adding portaudio.dll for pyaudio

import pyaudio
import subprocess



def outputdevice_load_info():
    global outputdevice_name
    global latency

    p = pyaudio.PyAudio()

    outputdevice = p.get_default_output_device_info()
    outputdevice_name = outputdevice['name']
    latency = (outputdevice['defaultLowOutputLatency'])

    p.terminate()

from tkinter import filedialog
import tkinter as tk

if __name__ == '__main__':
    
    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(icon_jakeisalivee_dir) #for filedialog icon to show
    root.attributes("-topmost", True)

    outputdevice_load_info()











pygameclock = pygame.time.Clock()


def offscreen_check(windowpos: tuple, windowres: tuple, desktopsize: tuple) -> tuple: 
    """Returns new window position"""
    windowpos = list(windowpos)
    if windowpos[0] < 0-windowres[0]+20:
        windowpos[0] = 0-windowres[0]+20
    if windowpos[0]+20 > desktopsize[0]:
        windowpos[0] = desktopsize[0]-20

    if windowpos[1] < 0-windowres[1]+20:
        windowpos[1] = 0-windowres[1]+20
    if windowpos[1]+60 > desktopsize[1]:
        windowpos[1] = desktopsize[1]-60

    return((windowpos[0],windowpos[1]))





def events_global(event: pygame.Event):

    global devmode
    global devmodeactivation_list
    global devevents
    global devruler
    global devrulerpoints
    global devrulerpoint_index

    global displayupdate
    global mousebts_hold
    global mouseholddrag_startpos

    global lshifthold
    global lctrlhold


                
    if devmode:
        if devevents:
            print(event)
        if devruler:
            if event.type == pygame.MOUSEBUTTONDOWN:
                devrulerpoints[devrulerpoint_index] = event.pos
                devrulerpoint_index += 1
                if devrulerpoint_index == 2:
                    print('thats '+str(devrulerpoints[1][0]-devrulerpoints[0][0])+' for x')
                    print('and '+str(devrulerpoints[1][1]-devrulerpoints[0][1])+' for y')
                    print('from '+str(devrulerpoints[0])+' to '+str(devrulerpoints[1]))
                    print()
        

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
                print('OFF!')
            else:
                devmode = True
                print('ON!')

        if event.key == pygame.K_LSHIFT:
            lshifthold = True
        if event.key == pygame.K_LCTRL:
            lctrlhold = True

        if event.key == pygame.K_c or event.key == pygame.K_DELETE:
            pygame.quit()
            sys.exit()

    if event.type == pygame.KEYUP:

        if event.key == pygame.K_LSHIFT:
            lshifthold = False
        if event.key == pygame.K_LCTRL:
            lctrlhold = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == pygame.BUTTON_LEFT:
            mousebts_hold[0] = True
            mouseholddrag_startpos = [event.pos[0],event.pos[1]]
        if event.button == pygame.BUTTON_MIDDLE:
            mousebts_hold[1] = True
            mouseholddrag_startpos = [event.pos[0],event.pos[1]]
        if event.button == pygame.BUTTON_RIGHT:
            mousebts_hold[2] = True
            mouseholddrag_startpos = [event.pos[0],event.pos[1]]


        if event.button == pygame.BUTTON_WHEELUP:

            if mousebts_hold[0]:
                if mainwindow.size[1] < desktopsize[1]:
                    mainwindow.size = (mainwindow.size[0],mainwindow.size[1]+10)
                    mouseholddrag_startpos[1] += 5
                    mainwindow.position = (mainwindow.position[0],mainwindow.position[1]-5)

                    displayupdate = True

            if mousebts_hold[2]:
                if mainwindow.size[0] < desktopsize[0]:
                    mainwindow.size = (mainwindow.size[0]+10,mainwindow.size[1])
                    mouseholddrag_startpos[0] += 5
                    mainwindow.position = (mainwindow.position[0]-5,mainwindow.position[1])

                    displayupdate = True
        
                    

        if event.button == pygame.BUTTON_WHEELDOWN:
                    
            if mousebts_hold[0]:
                if mainwindow.size[1] > 10:
                    mainwindow.size = (mainwindow.size[0],mainwindow.size[1]-10)
                    mouseholddrag_startpos[1] -= 5
                    mainwindow.position = (mainwindow.position[0],mainwindow.position[1]+5)

                    displayupdate = True

            if mousebts_hold[2]:
                if mainwindow.size[0] > 10:
                    mainwindow.size = (mainwindow.size[0]-10,mainwindow.size[1])
                    mouseholddrag_startpos[0] -= 5
                    mainwindow.position = (mainwindow.position[0]+5,mainwindow.position[1])

                    displayupdate = True

    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            mousebts_hold[0] = False
        if event.button == pygame.BUTTON_MIDDLE:
            mousebts_hold[1] = False
        if event.button == pygame.BUTTON_RIGHT:
            mousebts_hold[2] = False

    if event.type == pygame.MOUSEMOTION:
        if mousebts_hold[0] or mousebts_hold[1] or mousebts_hold[2]:
            mainwindow.position = (mainwindow.position[0]+event.pos[0]-mouseholddrag_startpos[0],
                                   mainwindow.position[1]+event.pos[1]-mouseholddrag_startpos[1])

            mainwindow.position = offscreen_check(windowpos=mainwindow.position,
                                                  windowres=mainwindow.size,
                                                  desktopsize=desktopsize)

    if event.type == pygame.WINDOWFOCUSGAINED:
        mainwindow.position = offscreen_check(windowpos=mainwindow.position,
                                              windowres=mainwindow.size,
                                              desktopsize=desktopsize)

    if event.type == pygame.WINDOWRESTORED:
        displayupdate = True
    if event.type == pygame.WINDOWFOCUSLOST:
        mousebts_hold[0] = False
        mousebts_hold[1] = False
        mousebts_hold[2] = False

    events_visualizer(event)    




#                 lmb   mmb   rmb
mousebts_hold = [False,False,False]
mouseholddrag_startpos = [0,0]

lshifthold = False
lctrlhold = False

scene = 'visualizer'
"""
visualizer > settings > songqueue
                      > controls
                      > customize
                      > visual_modes
                      > program        > credits
"""










fpscap = 240
fpscapnum = 11

fpscap_allowed_values = [1, 2, 5, 8, 10, 12, 24, 30, 60, 120, 180, 240, 300, 360, 480, 600, 720, 1000, 0]








displayupdate = True


# 12 len list, write "jakeisalivee" to activate devmode
devmodeactivation_list = []
devmode = False

#what to get
devfps = False   
devevents = False 
devruler = False
devrulerpoints = [(0,0),(0,0)]
devrulerpoint_index = 0

timeNOW = time.perf_counter()

general_mode_num = 1

def windowres_toolow(x,y,
                     windowres: tuple,
                     ):

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

    exclamationmark_text = fonts_unifont(64).render('!',False,colors['window_border'])
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

    return surface


juststopped = False 

def events_visualizer(event):

    global displayupdate
    global transparent
    global juststopped

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if jia_song.playing:
                pygame.mixer_music.pause()
                jia_song.playing = False
                displayupdate = True
                juststopped = True
            else:
                pygame.mixer_music.unpause()
                jia_song.playing = True

        if event.key == pygame.K_t:
            jia_visualizer.anim_transparency = timeNOW

            if transparent:
                transparent = False
                set_transparency((0,0,0))
            else:
                transparent = True
                set_transparency(colors['transparent_chromakey_win'])

        if event.key == pygame.K_o:
            jia_visualizer.anim_ontop = timeNOW

            if mainwindow.always_on_top:
                mainwindow.always_on_top = False
            else:
                mainwindow.always_on_top = True


        if event.key == pygame.K_LEFT:
            if lshifthold:
                jia_song.songpos_sync = jia_song.songpos-5000
                pygame.mixer_music.stop()
                if jia_song.songpos_sync < 0:
                    jia_song.songpos_sync = 0
                pygame.mixer_music.play(0,(jia_song.songpos_sync)/1000)
                jia_song.songpos = jia_song.songpos_sync
                if not jia_song.playing:
                    pygame.mixer_music.pause()
                displayupdate = True
                jia_visualizer.anim_subtract5sec = timeNOW

                if jia_settings.pr_bluetooth_output_device:
                    jia_song.lastsounddata = int((jia_song.songpos-(latency*1000)) * jia_song.soundrate/1000)
                else:
                    jia_song.lastsounddata = int(jia_song.songpos * jia_song.soundrate/1000)
                            


            else:
                jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()

                jia_visualizer.anim_song = timeNOW

                if jia_song.songnum == 0:
                    jia_song.songnum = len(jia_song.songqueue)-1
                    jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

                    if jia_song.playing == True:
                        jia_visualizer.anim_nowplaying = timeNOW+1
                        pygame.mixer_music.unpause()
                                

                else:
                    jia_song.songnum -= 1
                    jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

                    if jia_song.playing == True:
                        jia_visualizer.anim_nowplaying = timeNOW+1
                        pygame.mixer_music.unpause()

        if event.key == pygame.K_RIGHT: #right arrow

            if lshifthold:
                jia_song.songpos_sync = jia_song.songpos+5000
                pygame.mixer_music.stop()
                pygame.mixer_music.play(0,(jia_song.songpos_sync)/1000)
                jia_song.songpos = jia_song.songpos_sync
                if jia_song.songpos_sync > jia_song.songqueue[jia_song.songnum].songlength:
                    pygame.mixer_music.pause()
                if not jia_song.playing:
                    pygame.mixer_music.pause()
                displayupdate = True
                jia_visualizer.anim_add5sec = timeNOW

                if jia_settings.pr_bluetooth_output_device:
                    jia_song.lastsounddata = int((jia_song.songpos-(latency*1000)) * jia_song.soundrate/1000)
                else:
                    jia_song.lastsounddata = int(jia_song.songpos * jia_song.soundrate/1000)
                            

            else:
                jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()

                jia_visualizer.anim_song = timeNOW

                if len(jia_song.songqueue)-1 > jia_song.songnum:
                    jia_song.songnum += 1
                                
                else:
                    jia_song.songnum = 0

                jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                            
                if jia_song.playing == True:
                    jia_visualizer.anim_nowplaying = timeNOW+1
                    pygame.mixer_music.unpause()

        if event.key == pygame.K_UP: #up arrow
            jia_visualizer.anim_volume = timeNOW

            if jia_song.musicvolume_percent < 100:
                jia_song.musicvolume_percent += 5
                pygame.mixer_music.set_volume(jia_song.musicvolume_percent/100)

        if event.key == pygame.K_DOWN: #down arrow
            jia_visualizer.anim_volume = timeNOW

            if jia_song.musicvolume_percent > 0:
                jia_song.musicvolume_percent -= 5
                pygame.mixer_music.set_volume(jia_song.musicvolume_percent/100)

        if event.key == pygame.K_r: 
            jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset() 
            jia_song.songnum = random.randint(0,len(jia_song.songqueue)-1)
            if jia_song.playing:
                jia_song.playing = True
                jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                pygame.mixer_music.unpause()
                jia_visualizer.anim_nowplaying = timeNOW+1
                jia_visualizer.anim_song = timeNOW
            else:
                jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                jia_song.playing = False
                jia_visualizer.anim_song = timeNOW
                


def events_program(event):
    global displayupdate
    global fpscap 
    global fpscapnum

    if event.type == pygame.MOUSEBUTTONDOWN:
                    
        if event.button == pygame.BUTTON_LEFT:
    
            if event.pos[0] in range(74,85) and event.pos[1] in range(34,50): #- fpscap
                if fpscapnum > 0:
                    fpscapnum -= 1
                    fpscap = fpscap_allowed_values[fpscapnum]
                    displayupdate = True
            elif event.pos[0] in range(85,94) and event.pos[1] in range(34,50): #+ fpscap
                if fpscapnum < len(fpscap_allowed_values)-1:
                    fpscapnum += 1
                    fpscap = fpscap_allowed_values[fpscapnum]
                    displayupdate = True
    
            elif event.pos[0] in range(184,200) and event.pos[1] in range(52,67): #bluetooth latency checkbox
                if jia_settings.pr_bluetooth_output_device:
                    jia_settings.pr_bluetooth_output_device = False
                else:
                    jia_settings.pr_bluetooth_output_device = True
                    outputdevice_load_info()
                displayupdate = True
                jia_settings.surface_static_new_program.cache_clear()

            elif event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(mainwindow.size[1]-76,mainwindow.size[1]-12):
                os.system('start '+jia_settings.contacts['GitHub'])
                sound_icandoanything.play()

            elif event.pos[0] in range(mainwindow.size[0]-136,mainwindow.size[0]-72) and event.pos[1] in range(mainwindow.size[1]-76, mainwindow.size[1]-12):
                os.system('start '+jia_settings.contacts['Telegram'])



def logic_visualizer():
    global displayupdate

    if jia_song.playing:
        displayupdate = True
    
        jia_song.songpos = pygame.mixer_music.get_pos() + jia_song.songpos_sync
    
        if jia_settings.pr_bluetooth_output_device:
            jia_song.lastsounddata = int((jia_song.songpos-(latency*1000)) * jia_song.soundrate/1000)
        else:
            jia_song.lastsounddata = int(jia_song.songpos * jia_song.soundrate/1000)
    
        if jia_song.songpos > jia_song.songqueue[jia_song.songnum].songlength: #song ended
            jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset() 
            if len(jia_song.songqueue)-1 > jia_song.songnum:
    
                jia_song.songnum += 1
                jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
    
                jia_song.playing = True
                pygame.mixer_music.unpause()
                jia_visualizer.anim_nowplaying = timeNOW+1
            else:
                jia_song.songnum = 0
                jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
    
                jia_song.playing = False
    
        if jia_song.songformat != '.wav':
            #songsync
            if jia_song.songpos % 10000 >= 9990:
                pygame.mixer_music.rewind()
                pygame.mixer_music.play(0,jia_song.songpos/1000)
                jia_song.songpos_sync = jia_song.songpos
    
    if jia_visualizer.anim_volume+1 > timeNOW or jia_visualizer.anim_transparency+1 > timeNOW or jia_visualizer.anim_ontop+1 > timeNOW or jia_visualizer.anim_song+1 > timeNOW or jia_visualizer.anim_add5sec+1 > timeNOW or jia_visualizer.anim_subtract5sec+1 > timeNOW:
        displayupdate = True
    
    if jia_visualizer.anim_nowplaying+3 > timeNOW:
        displayupdate = True


VISUALIZER_QUEUE_OUTPUT = Queue()
HIGHLOAD = False

visualizer_surface_ready = False

anim_settings_fadein = 0
anim_settings_fadeout = 0

settings_alpha = 150

typingnum = 0
typinglist = ['|',' ']


creditsanim_time = 0


def scenes():

    global HIGHLOAD
    global visualizer_surface_ready

    global fpscap
    global fpscapnum

    global scene
    global displayupdate
    global transparent
    global general_mode_num

    global mouseholddrag_startpos
    global mousebts_hold

    global loading_thread_run

    global anim_settings_fadein
    global anim_settings_fadeout 
    global settings_alpha

    global juststopped

    global creditsanim_time

    global colors
    
    if scene != 'songqueue':
        logic_visualizer()
        try:
            mainwindow_surface.blit(VISUALIZER_QUEUE_OUTPUT.get_nowait())
            visualizer_surface_ready = True    #prevents screen flickering in settings

        except:
            pass

        if displayupdate:
            if HIGHLOAD:
                if len(threading.enumerate())-1 != jia_settings.num_cores or juststopped:
                        visualizer_thread = threading.Thread(target=jia_visualizer.VISUALIZER_THREAD,
                                                        args=
                                                        [
                                                                                    mainwindow.size,
                                                                                    fonts_unifont,
                                                                                    colors['visualizer_bg'],
                                                                                    colors['window_border'],

                                                                                    general_mode_num,
                                                                                    colors['program_notifs'],

                                                                                    jia_song.playing,
                                                                                    jia_song.musicvolume_percent,
                                                                                    jia_song.songnum,
                                                                                    jia_song.songqueue,
                                                                                    jia_song.soundrate,

                                                                                    jia_settings.cl_rotate,
                                                                                    colors['visualizer_lines'],
                                                                                    jia_song.lastsounddata,
                                                                                    jia_settings.devisionby,
                                                                                    jia_settings.cl_line_space,
                                                                                    jia_settings.cl_linelength,
                                                                                    jia_settings.cl_renderingmode_num,
                                                                                    jia_settings.cl_onedimensional,
                                                                                    jia_settings.cl_mirrored,
                                                                                    jia_settings.wf_mono,
                                                                                    jia_settings.wf_merge,
                                                                                    jia_settings.wf_split,
                                                                                    jia_settings.osc_linesperframe,
                                                                                    jia_settings.osc_fadeout,

                                                                                    colors['settings_text'],


                                                                                    jia_settings.b_renderingmode_num,
                                                                                    jia_settings.b_boostfreq,
                                                                                    jia_settings.b_boostfreq_num,
                                                                                    jia_settings.b_boostfreq_graph_num,
                                                                                                                                                                                          
                                                                                    jia_settings.b_boostfreq_intensity_quad, 
                                                                                    jia_settings.b_boostfreq_intensity_sqrt,
                                                                                    jia_settings.b_boostfreq_mult,   

                                                                                    jia_settings.b_adaptive_linelen,


                                                                                    jia_settings.sounddataspeed_num,
                                                                                    jia_settings.sounddataspeed_intensity_sqrts,
                                                                                    jia_settings.sounddataspeed_intensity_quads,    
                                                                                    jia_settings.sounddataspeed_fadeout,

                                                            VISUALIZER_QUEUE_OUTPUT,
                                                        ])
                        visualizer_thread.start()
                        juststopped = False

                


            else:
                mainwindow_surface.blit(jia_visualizer.surface_static_new_visualizer(
                                                                                    windowres=mainwindow.size,
                                                                                    callable_font=fonts_unifont,
                                                                                    bgcolor=colors['visualizer_bg'],
                                                                                    windowbordercolor=colors['window_border'],
            
                                                                                    visualizergeneral_mode=general_mode_num,
                                                                                    programnotifscolor=colors['program_notifs'],

                                                                                    songplaying=jia_song.playing,
                                                                                    musicvolume_percent=jia_song.musicvolume_percent,
                                                                                    songnum=jia_song.songnum,
                                                                                    songqueue=jia_song.songqueue,
                                                                                    songsamplerate=jia_song.soundrate,

                                                                                    cl_rotate=jia_settings.cl_rotate,
                                                                                    linecolor=colors['visualizer_lines'],
                                                                                    lastsounddata=jia_song.lastsounddata,
                                                                                    devisionby=jia_settings.devisionby,
                                                                                    cl_line_space=jia_settings.cl_line_space,
                                                                                    cl_linelength=jia_settings.cl_linelength,
                                                                                    cl_renderingmode_num=jia_settings.cl_renderingmode_num,
                                                                                    cl_onedimensional=jia_settings.cl_onedimensional,
                                                                                    cl_mirrored=jia_settings.cl_mirrored,
                                                                                    wf_mono=jia_settings.wf_mono,
                                                                                    wf_merge=jia_settings.wf_merge,
                                                                                    wf_split=jia_settings.wf_split,
                                                                                    osc_linesperframe=jia_settings.osc_linesperframe,
                                                                                    osc_fadeout=jia_settings.osc_fadeout,

                                                                                    textcolor=colors['settings_text'],


                                                                                    b_renderingmode_num=jia_settings.b_renderingmode_num,
                                                                                    b_boostfreq=jia_settings.b_boostfreq,
                                                                                    b_boostfreq_num=jia_settings.b_boostfreq_num,
                                                                                    b_boostfreq_graph=jia_settings.b_boostfreq_graph_num,
                                                                                    b_boostfreq_intensity_quad=jia_settings.b_boostfreq_intensity_quad,
                                                                                    b_boostfreq_intensity_sqrt=jia_settings.b_boostfreq_intensity_sqrt,
                                                                                    b_boostfreq_mult=jia_settings.b_boostfreq_mult,
                                                                                    b_adaptive_linelen=jia_settings.b_adaptive_linelen,


                                                                                    sounddataspeednum=jia_settings.sounddataspeed_num,
                                                                                    sounddataspeed_intensity_sqrts=jia_settings.sounddataspeed_intensity_sqrts,
                                                                                    sounddataspeed_intensity_quads=jia_settings.sounddataspeed_intensity_quads,
                                                                                    sounddata_fadeout=jia_settings.sounddataspeed_fadeout
                                                                                    ))
                visualizer_surface_ready = True

    
    if scene == 'visualizer':

        if displayupdate:
            displayupdate = False

            if anim_settings_fadeout > timeNOW:

                bgcolor = colors['settings_bg']
                
                surface = jia_settings.surface_static_new_settings(windowres=mainwindow.size,
                                                                   callable_font=fonts_unifont,
                                                                   bgcolor=bgcolor,
                                                                   textcolor=colors['settings_text'],
                                                                   windowbordercolor=colors['window_border']
                                                                   )
            
                surface.set_alpha(((settings_alpha)*(((anim_settings_fadeout-timeNOW)*8)**0.5)))
                displayupdate = True
                
                mainwindow_surface.blit(surface)
                surface_restoolow = windowres_toolow(310,180,
                                                     mainwindow.size)
                alpha = surface_restoolow.get_alpha()
                surface_restoolow.set_alpha(((alpha)*(((anim_settings_fadeout-timeNOW)*8)**0.5)))

                mainwindow_surface.blit(surface_restoolow)

        if visualizer_surface_ready: 
            mainwindow.flip()
            visualizer_surface_ready = False

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True
                    anim_settings_fadein = timeNOW+0.125


                



































    elif scene == 'settings':

        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = False

            bgcolor = colors['settings_bg']

            surface = jia_settings.surface_static_new_settings(windowres=mainwindow.size,
                                                               callable_font=fonts_unifont,
                                                               bgcolor=bgcolor,
                                                               textcolor=colors['settings_text'],
                                                               windowbordercolor=colors['window_border']
                                                               )
            
            if anim_settings_fadein > timeNOW:
                surface.set_alpha(settings_alpha-((settings_alpha)*(((anim_settings_fadein-timeNOW)*8)**0.5)))
                displayupdate = True
            else:
                surface.set_alpha(settings_alpha)

            
            mainwindow_surface.blit(surface)
            mainwindow_surface.blit(windowres_toolow(310,180,
                                                     mainwindow.size))
            
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False
        



        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if jia_song.playing:
                        pygame.mixer_music.unpause()
                    
                    mainwindow_surface.fill(colors['settings_bg'])
                    displayupdate = True
                    scene = 'visualizer'
                    anim_settings_fadeout = timeNOW+0.125
                    


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range(1,140) and event.pos[1] in range(36,70):
                        scene = 'controls'
                        displayupdate = True

                    elif event.pos[0] in range(1,152) and event.pos[1] in range(68,100):
                        scene = 'customize'
                        displayupdate = True
                    
                    elif event.pos[0] in range(1,126) and event.pos[1] in range(100,132):
                        scene = 'program'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-156,mainwindow.size[0]-1) and event.pos[1] in range(40,70):
                        scene = 'visual_modes'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-156,mainwindow.size[0]-1) and event.pos[1] in range(76,102):
                        scene = 'songqueue'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(mainwindow.size[1]-76,mainwindow.size[1]-12):
                        sound_icandoanything.play()
                        os.system('start '+jia_settings.contacts['GitHub'])
                        

                    elif event.pos[0] in range(mainwindow.size[0]-136,mainwindow.size[0]-72) and event.pos[1] in range(mainwindow.size[1]-76, mainwindow.size[1]-12):
                        os.system('start '+jia_settings.contacts['Telegram'])









    elif scene == 'controls':
        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = False
            bgcolor = colors['settings_bg']
                            
            surface = jia_settings.surface_static_new_controls(windowres=mainwindow.size,
                                                               callable_font=fonts_unifont,
                                                               bgcolor=bgcolor,
                                                               textcolor=colors['settings_text'],
                                                               windowbordercolor=colors['window_border']
                                                               )
            surface.set_alpha(settings_alpha)
            mainwindow_surface.blit(surface)
            mainwindow_surface.blit(windowres_toolow(470,160,
                                                     mainwindow.size))
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False


        for event in pygame.event.get():
            events_global(event)

            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True


            


    elif scene == 'customize':
        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = False

            bgcolor = colors['settings_bg']
            surface = jia_settings.surface_static_new_customize(windowres=mainwindow.size,
                                                                callable_font=fonts_unifont,

                                                                bgcolor=colors['settings_bg'],
                                                                textcolor=colors['settings_text'],
                                                                windowbordercolor=colors['window_border'],
                                                                
                                                                allcolorkeys=tuple(colors.keys()),
                                                                allcolorvars=tuple(colors.values()),
                                                                )
            surface.set_alpha(settings_alpha)
            mainwindow_surface.blit(surface)

            mainwindow_surface.blit(windowres_toolow(400,200,
                                                     mainwindow.size))
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False

        typingnum = int((timeNOW - int(timeNOW))*2) #0->1.999
        
        if jia_settings.colors_RGBA_typing[0]:
            if jia_settings.colors_RGBA_typing_list[0][-1] != typinglist[typingnum]:
                jia_settings.colors_RGBA_typing_list[0][-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_customize.cache_clear()
        if jia_settings.colors_RGBA_typing[1]:
            if jia_settings.colors_RGBA_typing_list[1][-1] != typinglist[typingnum]:
                jia_settings.colors_RGBA_typing_list[1][-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_customize.cache_clear()
        if jia_settings.colors_RGBA_typing[2]:
            if jia_settings.colors_RGBA_typing_list[2][-1] != typinglist[typingnum]:
                jia_settings.colors_RGBA_typing_list[2][-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_customize.cache_clear()
        if jia_settings.colors_RGBA_typing[3]:
            if jia_settings.colors_RGBA_typing_list[3][-1] != typinglist[typingnum]:
                jia_settings.colors_RGBA_typing_list[3][-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_customize.cache_clear()

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True
                    colors = jia_settings.typing.cancel_colorsRGBA(colors)
                    jia_settings.surface_static_new_customize.cache_clear()

                if event.key == 13: #enter
                    colors = jia_settings.typing.cancel_colorsRGBA(colors)
                    jia_settings.surface_static_new_customize.cache_clear()
                    displayupdate = True
                
                if event.key == pygame.K_BACKSPACE:
                    displayupdate = True
                    jia_settings.surface_static_new_customize.cache_clear()

                    typing = False
                    typingnum = 0
                    for i in range(len(jia_settings.colors_RGBA_typing)):
                        if jia_settings.colors_RGBA_typing[i] == True:
                            typing = True
                            typingnum = i

                    if typing:
                        if len(jia_settings.colors_RGBA_typing_list[typingnum]) > 1:
                            jia_settings.colors_RGBA_typing_list[typingnum].pop(-2)

            if event.type == pygame.TEXTINPUT:
                try:
                    displayupdate = True
                    jia_settings.surface_static_new_customize.cache_clear()
                        
                    typing = False
                    typingnum = 0
                    for i in range(len(jia_settings.colors_RGBA_typing)):
                        if jia_settings.colors_RGBA_typing[i] == True:
                            typing = True
                            typingnum = i

                    if typing:
                        if len(jia_settings.colors_RGBA_typing_list[typingnum]) < 4:
                            jia_settings.colors_RGBA_typing_list[typingnum].insert(len(jia_settings.colors_RGBA_typing_list[typingnum])-1,int(event.text))
                                                
                except ValueError:
                    pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                displayupdate = True
                colors = jia_settings.typing.cancel_colorsRGBA(colors)
                jia_settings.surface_static_new_customize.cache_clear()

                if event.button == pygame.BUTTON_LEFT:

                    colorkeys = list(colors.keys())
                    colorvars = list(colors.values())

                    colorkeys.pop(-1)
                    colorvars.pop(-1)

                    for i in range(len(colorkeys)):
                        if event.pos[0] in range(212,246) and event.pos[1] in range(66+((i)*16),66+((i+1)*16)): #R
                            jia_settings.color_num = i
                            jia_settings.colors_RGBA_typing = [True,False,False,False]
                            jia_settings.colors_RGBA = list(colorvars[i])
                            jia_settings.colors_RGBA_typing_list = [list(str(jia_settings.colors_RGBA[0])+' '),
                                                                    list(str(jia_settings.colors_RGBA[1])+' '),
                                                                    list(str(jia_settings.colors_RGBA[2])+' '),
                                                                    list(str(jia_settings.colors_RGBA[3])+' ')]
                            
                        if event.pos[0] in range(260,294) and event.pos[1] in range(66+((i)*16),66+((i+1)*16)): #G
                            jia_settings.color_num = i
                            jia_settings.colors_RGBA_typing = [False,True,False,False]
                            jia_settings.colors_RGBA = list(colorvars[i])
                            jia_settings.colors_RGBA_typing_list = [list(str(jia_settings.colors_RGBA[0])+' '),
                                                                    list(str(jia_settings.colors_RGBA[1])+' '),
                                                                    list(str(jia_settings.colors_RGBA[2])+' '),
                                                                    list(str(jia_settings.colors_RGBA[3])+' ')]
                        if event.pos[0] in range(306,340) and event.pos[1] in range(66+((i)*16),66+((i+1)*16)): #B
                            jia_settings.color_num = i
                            jia_settings.colors_RGBA_typing = [False,False,True,False]
                            jia_settings.colors_RGBA = list(colorvars[i])
                            jia_settings.colors_RGBA_typing_list = [list(str(jia_settings.colors_RGBA[0])+' '),
                                                                    list(str(jia_settings.colors_RGBA[1])+' '),
                                                                    list(str(jia_settings.colors_RGBA[2])+' '),
                                                                    list(str(jia_settings.colors_RGBA[3])+' ')]
                        if event.pos[0] in range(356,390) and event.pos[1] in range(66+((i)*16),66+((i+1)*16)): #A
                            jia_settings.color_num = i
                            jia_settings.colors_RGBA_typing = [False,False,False,True]
                            jia_settings.colors_RGBA = list(colorvars[i])
                            jia_settings.colors_RGBA_typing_list = [list(str(jia_settings.colors_RGBA[0])+' '),
                                                                    list(str(jia_settings.colors_RGBA[1])+' '),
                                                                    list(str(jia_settings.colors_RGBA[2])+' '),
                                                                    list(str(jia_settings.colors_RGBA[3])+' ')]





    elif scene == 'program':
        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = False

            bgcolor = colors['settings_bg']
            surface = jia_settings.surface_static_new_program(windowres=mainwindow.size,
                                                              callable_font=fonts_unifont,
                                                              bgcolor=bgcolor,
                                                              textcolor=colors['settings_text'],
                                                              windowbordercolor=colors['window_border'],

                                                              fpscap=fpscap,
                                                              highload=HIGHLOAD,
                                                              )
            surface.set_alpha(settings_alpha)
            mainwindow_surface.blit(surface)

            mainwindow_surface.blit(windowres_toolow(350,240,
                                                     mainwindow.size))
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False

        typingnum = int((timeNOW - int(timeNOW))*2) #0->1.999

        if jia_settings.program_numcores_typing:
            if jia_settings.program_numcores_typing_list[-1] != typinglist[typingnum]:
                jia_settings.program_numcores_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_program.cache_clear()



        for event in pygame.event.get():
            events_global(event)

            events_program(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True

                    jia_settings.typing.cancel_numcores()
                    jia_settings.surface_static_new_program.cache_clear()
 
                if event.key == 13: #enter
                    jia_settings.typing.cancel_numcores()
                    jia_settings.surface_static_new_program.cache_clear()
                    displayupdate = True

                if event.key == pygame.K_BACKSPACE:
                    jia_settings.surface_static_new_program.cache_clear()
                    displayupdate = True

                    if jia_settings.program_numcores_typing:
                        if len(jia_settings.program_numcores_typing_list) > 1:
                            jia_settings.program_numcores_typing_list.pop(-2)
                            displayupdate = True  



            if event.type == pygame.TEXTINPUT:
                try:
                    jia_settings.surface_static_new_program.cache_clear()
                    displayupdate = True

                    if jia_settings.program_numcores_typing:
                        if len(jia_settings.program_numcores_typing_list) < 2:
                            jia_settings.program_numcores_typing_list.insert(len(jia_settings.program_numcores_typing_list)-1,int(event.text))

                except ValueError:
                    pass


                


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range(mainwindow.size[0]-56,mainwindow.size[0]) and event.pos[1] in range(mainwindow.size[1]-88,mainwindow.size[1]-76):
                        scene = 'credits'
                        displayupdate = True
                        creditsanim_time = timeNOW
                        jia_settings.confetti_played = False
                        jia_settings.yippee_played = False

                    jia_settings.typing.cancel_numcores()
                    jia_settings.surface_static_new_program.cache_clear()
                    displayupdate = True
                    
                    if event.pos[0] in range(80,94) and event.pos[1] in range(68,82):
                        if HIGHLOAD:
                            HIGHLOAD = False
                        else:
                            HIGHLOAD = True
                            wasitontop_before = mainwindow.always_on_top
                            mainwindow.always_on_top = False

                            pref = pygame.display.message_box('Warning',
                                                              'This option is highly unstable and can easily freeze your system if used incorrectly.',
                                                              'warn',
                                                              buttons=('Proceed','Abort'))
                            if pref == 1: #abort
                                HIGHLOAD = False

                            mainwindow.always_on_top = wasitontop_before
                    if HIGHLOAD:
                        if event.pos[0] in range(2,90) and event.pos[1] in range(84,100):
                            jia_settings.program_numcores_typing = True
                    
                    
                     
                            
            
            


    elif scene == 'credits':
        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = True

            bgcolor = colors['settings_bg']
            surface = jia_settings.surface_static_new_credits(windowres=mainwindow.size,
                                                              callable_font=fonts_unifont,
                                                              bgcolor=bgcolor,
                                                              textcolor=colors['settings_text'],
                                                              windowbordercolor=colors['window_border'],

                                                              timeanim_start=creditsanim_time,
                                                              timenow=timeNOW
                                                              )
            surface.set_alpha(settings_alpha)
            mainwindow_surface.blit(surface)

            mainwindow_surface.blit(windowres_toolow(350,240,
                                                     mainwindow.size))
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'program'
                    displayupdate = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if event.pos[0] in range((mainwindow.size[0]//2)-50,(mainwindow.size[0]//2)+50) and event.pos[1] in range(0,26):
                        jia_settings.fue_time = timeNOW
                        jia_settings.credits_fue_sound.set_volume(10)
                        jia_settings.credits_scary_sound.set_volume(0.5)
                        jia_settings.credits_fue_sound.play()
                        jia_settings.credits_scary_sound.play()

                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(74,90):
                        os.system('start '+jia_settings.contacts['Telegram'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(90,106):
                        os.system('start '+jia_settings.contacts['GitHub'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(106,122):
                        os.system('start '+jia_settings.contacts['Itch.io'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(122,138):
                        os.system('start '+jia_settings.contacts['Donations'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(138,154):
                        os.system('start '+jia_settings.contacts['Youtube'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(154,170):
                        os.system('start '+jia_settings.contacts['Tiktok'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(170,186):
                        os.system('start '+jia_settings.contacts['Twitter'])
                    if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(186,202):
                        os.system('start '+jia_settings.contacts['Steam'])


            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(4,68):
                    jia_settings.credits_mouseonsecret = True
                else:
                    jia_settings.credits_mouseonsecret = False



    elif scene == 'visual_modes':

        if not displayupdate and visualizer_surface_ready:
            displayupdate = True
        if displayupdate:
            displayupdate = False

            bgcolor = colors['settings_bg']
            surface = jia_settings.surface_static_new_visualmodes(windowres=mainwindow.size,
                                                                  callable_font=fonts_unifont,
                                                                  bgcolor=bgcolor,
                                                                  textcolor=colors['settings_text'],
                                                                  windowbordercolor=colors['window_border'],

                                                                  visualizergeneral_mode=general_mode_num,

                                                                  )
            
            surface.set_alpha(settings_alpha)
            mainwindow_surface.blit(surface)

            mainwindow_surface.blit(windowres_toolow(400,190,
                                                     mainwindow.size))
            if visualizer_surface_ready: 
                mainwindow.flip()
                visualizer_surface_ready = False

        
        if jia_settings.effects_anim_time_raw - timeNOW >= 0:
            jia_settings.effects_anim_time = 1-(((((jia_settings.effects_anim_time_raw - timeNOW)*4)-1))**2)
            jia_settings.surface_static_new_visualmodes.cache_clear()
            displayupdate = True
        if jia_settings.effects_anim_time_raw - timeNOW < 0 and jia_settings.effects_anim_time != 0:
            jia_settings.effects_anim_time = 0
            jia_settings.surface_static_new_visualmodes.cache_clear()
            displayupdate = True

        typingnum = int((timeNOW - int(timeNOW))*2) #0->1.999

        if jia_settings.cl_zoom_typing:
            if jia_settings.cl_zoom_typing_list[-1] != typinglist[typingnum]:
                jia_settings.cl_zoom_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()

        if jia_settings.cl_line_space_typing:
            if jia_settings.cl_line_space_typing_list[-1] != typinglist[typingnum]:
                jia_settings.cl_line_space_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()
                
        if jia_settings.cl_rotate_typing:
            if jia_settings.cl_rotate_typing_list[-1] != typinglist[typingnum]:
                jia_settings.cl_rotate_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()
                
        if jia_settings.cl_linelength_typing:
            if jia_settings.cl_linelength_typing_list[-1] != typinglist[typingnum]:
                jia_settings.cl_linelength_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()
                
        if jia_settings.osc_linesperframe_typing:
            if jia_settings.osc_linesperframe_typing_list[-1] != typinglist[typingnum]:
                jia_settings.osc_linesperframe_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()

        if jia_settings.b_boostfreq_mult_typing:
            if jia_settings.b_boostfreq_mult_typing_list[-1] != typinglist[typingnum]:
                jia_settings.b_boostfreq_mult_typing_list[-1] = typinglist[typingnum]
                displayupdate = True
                jia_settings.surface_static_new_visualmodes.cache_clear()
        

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True

                    jia_settings.typing.cancel_all()
                    jia_settings.surface_static_new_visualmodes.cache_clear()

                    if jia_visualizer.b_graphshow:
                        jia_visualizer.b_graphshow = False
                        displayupdate = True
                        jia_settings.surface_static_new_visualmodes.cache_clear()

                if event.key == 13: #enter
                    
                    jia_settings.typing.cancel_all()
                    jia_settings.surface_static_new_visualmodes.cache_clear()
                    displayupdate = True


                if event.key == pygame.K_BACKSPACE:
                    jia_settings.surface_static_new_visualmodes.cache_clear()
                    displayupdate = True

                    if jia_settings.cl_zoom_typing:
                        if len(jia_settings.cl_zoom_typing_list) > 1:
                            jia_settings.cl_zoom_typing_list.pop(-2)
                            displayupdate = True
                    
                    if jia_settings.cl_line_space_typing:
                        if len(jia_settings.cl_line_space_typing_list) > 1:
                            jia_settings.cl_line_space_typing_list.pop(-2)
                            displayupdate = True

                    if jia_settings.cl_rotate_typing:
                        if len(jia_settings.cl_rotate_typing_list) > 2:
                            jia_settings.cl_rotate_typing_list.pop(-3)
                            displayupdate = True
                    
                    if jia_settings.cl_linelength_typing:
                        if len(jia_settings.cl_linelength_typing_list) > 1:
                            jia_settings.cl_linelength_typing_list.pop(-2)
                            displayupdate = True

                    if jia_settings.osc_linesperframe_typing:
                        if len(jia_settings.osc_linesperframe_typing_list) > 1:
                            jia_settings.osc_linesperframe_typing_list.pop(-2)
                            displayupdate = True

                    if jia_settings.b_boostfreq_mult_typing:
                        if len(jia_settings.b_boostfreq_mult_typing_list) > 1:
                            jia_settings.b_boostfreq_mult_typing_list.pop(-2)
                            displayupdate = True



            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    jia_settings.typing.cancel_all()
                    jia_settings.surface_static_new_visualmodes.cache_clear()
                    displayupdate = True

                    if event.pos[0] in range(80,96) and event.pos[1] in range(40,60): #- general mode
                        if general_mode_num > 1:
                            general_mode_num -= 1
                            displayupdate = True
                        if general_mode_num == 2:
                            jia_settings.effects_workhere = True
                    

                    if event.pos[0] in range(96,112) and event.pos[1] in range(40,60): #+ general mode
                        if general_mode_num < len(jia_settings.general_mode_names):
                            general_mode_num += 1
                            displayupdate = True
                        if general_mode_num == 3:
                            jia_settings.effects_workhere = False
                    
                    match general_mode_num:
                        case 1:
                            if event.pos[0] in range(44,58) and event.pos[1] in range(88,100): #- cl mode
                                if jia_settings.cl_renderingmode_num > 0:
                                    jia_settings.cl_renderingmode_num -= 1
                                    displayupdate = True
                            elif event.pos[0] in range(90,104) and event.pos[1] in range(88,100): #+ cl mode
                                if jia_settings.cl_renderingmode_num < len(jia_settings.cl_rendering_modes)-1:
                                    jia_settings.cl_renderingmode_num += 1
                                    displayupdate = True

                            elif event.pos[0] in range(4,144) and event.pos[1] in range(100,112): #typing out zoom
                                jia_settings.cl_zoom_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,164) and event.pos[1] in range(112,124): #typing out space between lines
                                jia_settings.cl_line_space_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(111,121) and event.pos[1] in range(124,136): #One dimensional checkbox
                                displayupdate = True
                                if jia_settings.cl_onedimensional:
                                    jia_settings.cl_onedimensional = False
                                else:
                                    jia_settings.cl_onedimensional = True

                            elif event.pos[0] in range(66,76) and event.pos[1] in range(136,148): #mirrored checkbox
                                if jia_settings.cl_onedimensional:
                                    displayupdate = True
                                    if jia_settings.cl_mirrored:
                                        jia_settings.cl_mirrored = False
                                    else:
                                        jia_settings.cl_mirrored = True
        
                            elif event.pos[0] in range(4,146) and event.pos[1] in range(148,160): #rotate typing
                                jia_settings.cl_rotate_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,190) and event.pos[1] in range(160,172): #linelen typing
                                jia_settings.cl_linelength_typing = True
                                displayupdate = True



                        case 2:
                            if event.pos[0] in range(44,58) and event.pos[1] in range(88,100): #- cl mode
                                if jia_settings.cl_renderingmode_num > 0:
                                    jia_settings.cl_renderingmode_num -= 1
                                    displayupdate = True
                            elif event.pos[0] in range(90,104) and event.pos[1] in range(88,100): #+ cl mode
                                if jia_settings.cl_renderingmode_num < len(jia_settings.cl_rendering_modes)-1:
                                    jia_settings.cl_renderingmode_num += 1
                                    displayupdate = True

                            elif event.pos[0] in range(4,144) and event.pos[1] in range(100,112): #typing out zoom
                                jia_settings.cl_zoom_typing = True
                                displayupdate = True
                            
                            elif event.pos[0] in range(41,52) and event.pos[1] in range(112,123): #mono checkbox
                                if jia_settings.wf_mono:
                                    jia_settings.wf_mono = False
                                else:
                                    jia_settings.wf_mono = True
                                displayupdate = True

                            
                            elif event.pos[0] in range(48,60) and event.pos[1] in range(125,136): #merge checkbox
                                if not jia_settings.wf_mono:
                                    if jia_settings.wf_merge:
                                        jia_settings.wf_merge = False
                                    else:
                                        jia_settings.wf_merge = True
                                        jia_settings.wf_split = False
                                    displayupdate = True
                            
                            elif event.pos[0] in range(48,60) and event.pos[1] in range(136,147): #split checkbox
                                if not jia_settings.wf_mono:
                                    if jia_settings.wf_split:
                                        jia_settings.wf_split = False
                                    else:
                                        jia_settings.wf_split = True
                                        jia_settings.wf_merge = False
                                    displayupdate = True

                            elif event.pos[0] in range(4,146) and event.pos[1] in range(148,160): #rotate typing
                                jia_settings.cl_rotate_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,190) and event.pos[1] in range(160,172): #linelen typing
                                jia_settings.cl_linelength_typing = True
                                displayupdate = True



                        case 3:

                            if event.pos[0] in range(44,54) and event.pos[1] in range(88,100): #- bars mode
                                if jia_settings.b_renderingmode_num > 0:
                                    jia_settings.b_renderingmode_num -= 1
                                    displayupdate = True
                            elif event.pos[0] in range(54,64) and event.pos[1] in range(88,100): #+ bars mode
                                if jia_settings.b_renderingmode_num < len(jia_settings.b_rendering_modes)-1:
                                    jia_settings.b_renderingmode_num += 1
                                    displayupdate = True


                            elif event.pos[0] in range(4,164) and event.pos[1] in range(100,112): #typing out space between lines
                                jia_settings.cl_line_space_typing = True
                                displayupdate = True
                            
                            elif event.pos[0] in range(111,121) and event.pos[1] in range(112,124): #One dimensional checkbox
                                displayupdate = True
                                if jia_settings.cl_onedimensional:
                                    jia_settings.cl_onedimensional = False
                                else:
                                    jia_settings.cl_onedimensional = True

                            elif event.pos[0] in range(66,76) and event.pos[1] in range(124,136): #mirrored checkbox
                                if jia_settings.cl_onedimensional:
                                    displayupdate = True
                                    if jia_settings.cl_mirrored:
                                        jia_settings.cl_mirrored = False
                                    else:
                                        jia_settings.cl_mirrored = True
        
                            elif event.pos[0] in range(4,146) and event.pos[1] in range(136,148): #rotate typing
                                jia_settings.cl_rotate_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,190) and event.pos[1] in range(148,160): #linelen typing
                                if not jia_settings.b_adaptive_linelen:
                                    jia_settings.cl_linelength_typing = True
                                    displayupdate = True

                            elif event.pos[0] in range(135,145) and event.pos[1] in range(160,172): #adaptive len chackbox
                                if jia_settings.b_adaptive_linelen:
                                    jia_settings.b_adaptive_linelen = False
                                else:
                                    jia_settings.b_adaptive_linelen = True
                                displayupdate = True


                            elif event.pos[0] in range(mainwindow.size[0]-128,mainwindow.size[0]-116) and event.pos[1] in range(86,98): #boost freq checkbox
                                if jia_settings.b_boostfreq:
                                    jia_settings.b_boostfreq = False
                                else:
                                    jia_settings.b_boostfreq = True
                                displayupdate = True

                            if jia_settings.b_boostfreq:
                                if event.pos[0] in range(mainwindow.size[0]-126,mainwindow.size[0]-114) and event.pos[1] in range(98,110): # - boost what freq 
                                    if jia_settings.b_boostfreq_num > 0:
                                        jia_settings.b_boostfreq_num -= 1
                                elif event.pos[0] in range(mainwindow.size[0]-70,mainwindow.size[0]-58) and event.pos[1] in range(98,110): # + boost what freq 
                                    if jia_settings.b_boostfreq_num < len(jia_settings.b_boostfreq_desc)-1:
                                        jia_settings.b_boostfreq_num += 1

                                elif event.pos[0] in range(mainwindow.size[0]-206,mainwindow.size[0]-190) and event.pos[1] in range(110,124): # - boost graph
                                    if jia_settings.b_boostfreq_graph_num > 0:
                                        jia_settings.b_boostfreq_graph_num -= 1
                                elif event.pos[0] in range(mainwindow.size[0]-86,mainwindow.size[0]-72) and event.pos[1] in range(110,124): # + boost graph
                                    if jia_settings.b_boostfreq_graph_num < len(jia_settings.b_boostfreq_graph_desc)-1:
                                        jia_settings.b_boostfreq_graph_num += 1
                                                            
                                elif event.pos[0] in range(mainwindow.size[0]-168,mainwindow.size[0]-156) and event.pos[1] in range(124,136): # - boost intensity
                                    if jia_settings.b_boostfreq_graph_num in range(0,2):
                                        if jia_settings.b_boostfreq_intensity_quad > 1:
                                            jia_settings.b_boostfreq_intensity_quad -= 1
                                    if jia_settings.b_boostfreq_graph_num in range(2,3):
                                        if jia_settings.b_boostfreq_intensity_sqrt > 1:
                                            jia_settings.b_boostfreq_intensity_sqrt -= 1
                                elif event.pos[0] in range(mainwindow.size[0]-108,mainwindow.size[0]-96) and event.pos[1] in range(124,136): # + boost intensity
                                    if jia_settings.b_boostfreq_graph_num in range(0,2):
                                        if jia_settings.b_boostfreq_intensity_quad < 50:
                                            jia_settings.b_boostfreq_intensity_quad += 1
                                    if jia_settings.b_boostfreq_graph_num in range(2,3):
                                        if jia_settings.b_boostfreq_intensity_sqrt < 79:
                                            jia_settings.b_boostfreq_intensity_sqrt += 1                           

                                elif event.pos[0] in range(mainwindow.size[0]-110,mainwindow.size[0]) and event.pos[1] in range(136,148): #boost mult typing
                                    jia_settings.b_boostfreq_mult_typing = True
                                    displayupdate = True
                                                                


                        case 4:
                            if event.pos[0] in range(2,140) and event.pos[1] in range(86,98):
                                jia_settings.osc_linesperframe_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(64,74) and event.pos[1] in range(100,110):
                                if jia_settings.osc_fadeout:
                                    jia_settings.osc_fadeout = False
                                else: 
                                    jia_settings.osc_fadeout = True
                                displayupdate = True


                    if jia_settings.effects_workhere:
                        if jia_settings.effects_surface_visible:
                            if event.pos[0] in range(mainwindow.size[0]-214,mainwindow.size[0]-182) and event.pos[1] in range(mainwindow.size[1]-76,mainwindow.size[1]-60): #rollout effects
                                jia_settings.effects_anim_time_raw = timeNOW+0.25
                                jia_settings.effects_anim_time = 1
                                jia_settings.effects_surface_visible = False

                            if event.pos[0] in range(mainwindow.size[0]-130,mainwindow.size[0]-121) and event.pos[1] in range(mainwindow.size[1]-38,mainwindow.size[1]-26): #graph -
                                if jia_settings.sounddataspeed_num > 0:
                                    jia_settings.sounddataspeed_num -= 1
                            if event.pos[0] in range(mainwindow.size[0]-121,mainwindow.size[0]-114) and event.pos[1] in range(mainwindow.size[1]-38,mainwindow.size[1]-26): #graph +
                                if jia_settings.sounddataspeed_num < len(jia_settings.sounddatarenderspeed_desc)-1:
                                    jia_settings.sounddataspeed_num += 1

                            if event.pos[0] in range(mainwindow.size[0]-70,mainwindow.size[0]-58) and event.pos[1] in range(mainwindow.size[1]-24,mainwindow.size[1]-12): #intensity -
                                if jia_settings.sounddataspeed_num in range(1,3):
                                    if jia_settings.sounddataspeed_intensity_sqrts > 1:
                                        jia_settings.sounddataspeed_intensity_sqrts -= 1 
                                if jia_settings.sounddataspeed_num in range(3,5):
                                    if jia_settings.sounddataspeed_intensity_quads > 3:
                                        jia_settings.sounddataspeed_intensity_quads -= 2
                            if event.pos[0] in range(mainwindow.size[0]-10,mainwindow.size[0])    and event.pos[1] in range(mainwindow.size[1]-24,mainwindow.size[1]-12): #intensity +
                                if jia_settings.sounddataspeed_num in range(1,3):
                                    if jia_settings.sounddataspeed_intensity_sqrts < 79:
                                        jia_settings.sounddataspeed_intensity_sqrts += 1
                                if jia_settings.sounddataspeed_num in range(3,5):
                                    if jia_settings.sounddataspeed_intensity_quads < 100:
                                        jia_settings.sounddataspeed_intensity_quads += 2

                            if event.pos[0] in range(mainwindow.size[0]-12,mainwindow.size[0])    and event.pos[1] in range(mainwindow.size[1]-12,mainwindow.size[1]): #fadeout chackbox
                                if jia_settings.sounddataspeed_fadeout:
                                    jia_settings.sounddataspeed_fadeout = False
                                else:
                                    jia_settings.sounddataspeed_fadeout = True

                        else:
                            if event.pos[0] in range(mainwindow.size[0]-214,mainwindow.size[0]-182) and event.pos[1] in range(mainwindow.size[1]-16,mainwindow.size[1]):
                                jia_settings.effects_anim_time_raw = timeNOW+0.25
                                jia_settings.effects_anim_time = 1
                                jia_settings.effects_surface_visible = True

            if event.type == pygame.MOUSEMOTION:
                if jia_settings.b_boostfreq:
                    if event.pos[0] in range(mainwindow.size[0]-202,mainwindow.size[0]) and event.pos[1] in range(98,148):
                        if not jia_visualizer.b_graphshow:
                            jia_visualizer.b_graphshow = True
                            displayupdate = True
                            jia_settings.surface_static_new_visualmodes.cache_clear()
                    else:
                        if jia_visualizer.b_graphshow:
                            jia_visualizer.b_graphshow = False
                            displayupdate = True
                            jia_settings.surface_static_new_visualmodes.cache_clear()



            if event.type == pygame.TEXTINPUT:
                try:
                    jia_settings.surface_static_new_visualmodes.cache_clear()
                    displayupdate = True

                    if jia_settings.cl_zoom_typing:
                        if len(jia_settings.cl_zoom_typing_list) < 8:
                            jia_settings.cl_zoom_typing_list.insert(len(jia_settings.cl_zoom_typing_list)-1,int(event.text))

                    if jia_settings.cl_line_space_typing:
                        if len(jia_settings.cl_line_space_typing_list) < 4:
                            jia_settings.cl_line_space_typing_list.insert(len(jia_settings.cl_line_space_typing_list)-1,int(event.text))

                    if jia_settings.cl_rotate_typing:
                        if len(jia_settings.cl_rotate_typing_list) < 5:
                            jia_settings.cl_rotate_typing_list.insert(len(jia_settings.cl_rotate_typing_list)-2,int(event.text))
                
                    if jia_settings.cl_linelength_typing:
                        if event.text == '.':
                            if len(jia_settings.cl_linelength_typing_list) < 6:
                                jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,str(event.text))
                        else:
                            if str(jia_settings.cl_linelength_typing_list).find('.') == -1:
                                if len(jia_settings.cl_linelength_typing_list) < 3:
                                    jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,int(event.text))
                            else:
                                if len(jia_settings.cl_linelength_typing_list) < 6:
                                    jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,int(event.text))
                    
                    if jia_settings.osc_linesperframe_typing:
                        if len(jia_settings.osc_linesperframe_typing_list) < 5:
                            jia_settings.osc_linesperframe_typing_list.insert(len(jia_settings.osc_linesperframe_typing_list)-1,str(event.text))


                    if jia_settings.b_boostfreq_mult_typing:
                        if event.text == '.':
                            if len(jia_settings.b_boostfreq_mult_typing_list) < 6:
                                jia_settings.b_boostfreq_mult_typing_list.insert(len(jia_settings.b_boostfreq_mult_typing_list)-1,str(event.text))
                        else:
                            if str(jia_settings.b_boostfreq_mult_typing_list).find('.') == -1:
                                if len(jia_settings.b_boostfreq_mult_typing_list) < 3:
                                    jia_settings.b_boostfreq_mult_typing_list.insert(len(jia_settings.b_boostfreq_mult_typing_list)-1,int(event.text))
                            else:
                                if len(jia_settings.b_boostfreq_mult_typing_list) < 6:
                                    jia_settings.b_boostfreq_mult_typing_list.insert(len(jia_settings.b_boostfreq_mult_typing_list)-1,int(event.text))
                                        


                except ValueError:
                    pass






























    elif scene == 'songqueue':
        if displayupdate:
            displayupdate = False   
            surface = jia_settings.surface_static_new_songqueue(windowres=mainwindow.size,
                                                                callable_font=fonts_unifont,
                                                                bgcolor=colors['settings_bg'],
                                                                textcolor=colors['settings_text'],

                                                                windowbordercolor=colors['window_border'],
                                                                songqueue=jia_song.songqueue,
                                                                )
            mainwindow_surface.blit(surface)
            mainwindow_surface.blit(windowres_toolow(220,90,
                                                     mainwindow.size))


            mainwindow.flip()

        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    songsrendernum = len(jia_song.songqueue)

                    if event.pos[0] in range(4,4+28) and event.pos[1] in range((4*(songsrendernum+1))+(28*(songsrendernum+1))+2-jia_settings.scrollwheely,(4*(songsrendernum+1))+(28*(songsrendernum+1))+4+28-jia_settings.scrollwheely): #add song
                        wasitontop_before = mainwindow.always_on_top
                        wasittransparent = transparent
                        set_transparency(colors['transparent_chromakey_win'])

                        mainwindow.always_on_top = False #so the window doesnt cover the windows file manager
                        
                        mousebts_hold[0] = False
                        mousebts_hold[1] = False
                        mousebts_hold[2] = False

                        addsongs_files = filedialog.askopenfiles(
                                         filetypes=jia_song.filetypes,
                                         title="JakeIsAlivee's Visualizer - Select your music file(s) to add into the list",
                                         )
                        if addsongs_files == None:
                            mainwindow.always_on_top = wasitontop_before
                            continue


                        tempnum = 0
                        info = Queue()
                        info.put(tempnum)
                        loading_thread_run = True
                        loading_thread = threading.Thread(target=loading_screen_Thread,args=(mainwindow_surface,mainwindow,loadinganim,
                                                                                             True, info, len(addsongs_files)
                                                                                             ))
                        loading_thread.start()
                        
                        while tempnum < len(addsongs_files):
                            try:
                                jia_song.songqueue.append(jia_song.Song(addsongs_files[tempnum].name))
                                tempnum += 1
                                info.put(tempnum)
                            except:
                                buttonindex = pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                                         message_type='warn',
                                                                         message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nProblematic file directory:\n"+addsongs_files[tempnum].name,
                                                                         buttons=('Retry','Skip'))
                                if buttonindex == 0:
                                    continue # retry
                                else:
                                    tempnum += 1
                                    continue # skip
                            for event in pygame.event.get():
                                events_global(event)

                        loading_thread_run = False
                        loading_thread.join()
                        
                        mainwindow.always_on_top = wasitontop_before
                        if not wasittransparent:
                            set_transparency((0,0,0))

                        mainwindow.flash(pygame.FLASH_UNTIL_FOCUSED)
                        
                        displayupdate = True
                        continue


                    if event.pos[0] in range(mainwindow.size[0]-28,mainwindow.size[0]-4) and event.pos[1] in range(4,28): #folder import
                        wasitontop_before = mainwindow.always_on_top
                        wasittransparent = transparent
                        set_transparency(colors['transparent_chromakey_win'])

                        mousebts_hold[0] = False
                        mousebts_hold[1] = False
                        mousebts_hold[2] = False
                                       
                        mainwindow.always_on_top = False #so the window doesnt cover the windows file manager
                        
                        import_folder = filedialog.askdirectory(title="JakeIsAlivee's Visualizer - Choose the folder that you want to import your music files from")
                        if import_folder == '': #None
                            mainwindow.always_on_top = wasitontop_before
                            if not wasittransparent:
                                set_transparency((0,0,0))
                                                        
                            continue
                            
                        musicfiles = os.listdir(import_folder)

                        

                        tempnum = 0
                        while tempnum < len(musicfiles):
                                
                            if musicfiles[tempnum][len(musicfiles[tempnum])-5:len(musicfiles[tempnum])] not in jia_song.musicformats and musicfiles[tempnum][len(musicfiles[tempnum])-4:len(musicfiles[tempnum])] not in jia_song.musicformats:
                                musicfiles.pop(tempnum)
                                continue

                            tempnum += 1

                        if len(musicfiles) > 60:
                            areyousure = pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                                    message="Are you sure you want to import this folder?\nLooks like there's "+str(len(musicfiles))+" files.\nThis will take a long time.",
                                                                    message_type='info',
                                                                    buttons=('Yes','No'))
                                                                                            
                            if areyousure == 1:
                                mainwindow.always_on_top = wasitontop_before
                                if not wasittransparent:
                                    set_transparency((0,0,0))
                                                                 
                                continue
                            del areyousure


                        if len(musicfiles) == 0:
                            pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                       message="There is no music files in this folder",
                                                       message_type='info',
                                                       buttons=('Ok'))
                            mainwindow.always_on_top = wasitontop_before
                            if not wasittransparent:
                                set_transparency((0,0,0))
                                                             
                            continue



                        tempnum = 0
                        info = Queue()
                        info.put(tempnum)
                        loading_thread_run = True
                        loading_thread = threading.Thread(target=loading_screen_Thread,args=(mainwindow_surface,mainwindow,loadinganim,
                                                                                                                             True, info, len(musicfiles)
                                                                                                                             ))
                        loading_thread.start()
                        
                        for i in jia_song.songqueue:
                            i.rawfile.close()

                        jia_song.songqueue = []
                        while tempnum < len(musicfiles):
                            try:
                                jia_song.songqueue.append(jia_song.Song(import_folder+slash+musicfiles[tempnum]))
                                tempnum += 1
                                info.put(tempnum)
                            except:
                                buttonindex = pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                                         message_type='warn',
                                                                         message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nProblematic file directory:\n"+addsongs_files[tempnum].name,
                                                                         buttons=('Retry','Skip'))
                                if buttonindex == 0:
                                    continue # retry
                                else:
                                    tempnum += 1
                                    continue # skip

                            for event in pygame.event.get():
                                events_global(event)


                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                        jia_song.songnum = 0

                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

                        loading_thread_run = False
                        loading_thread.join()
                        
                        mainwindow.always_on_top = wasitontop_before
                        if not wasittransparent:
                            set_transparency((0,0,0))

                        mainwindow.flash(pygame.FLASH_UNTIL_FOCUSED)
                        
                        displayupdate = True
                        continue

                    if event.pos[0] in range(mainwindow.size[0]-60,mainwindow.size[0]-36) and event.pos[1] in range(4,28): #shuffle songs
                        tempnum = 0
                        songqueuecopy = jia_song.songqueue.copy()
                        lensongqueue = len(jia_song.songqueue)
                        jia_song.songqueue.clear()
                        while tempnum < lensongqueue:
                            randomnum = random.randint(0,len(songqueuecopy)-1)
                            jia_song.songqueue.append(songqueuecopy[randomnum])
                            songqueuecopy.pop(randomnum)
                            tempnum += 1
                        del tempnum
                        del songqueuecopy
                        del lensongqueue
                        del randomnum
                        displayupdate = True
                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                            

                    if event.pos[0] in range(mainwindow.size[0]-92,mainwindow.size[0]-68) and event.pos[1] in range(4,28): #reverse songs
                        tempnum = 0
                        reversedsongqueue = []
                        while tempnum < len(jia_song.songqueue):
                            reversedsongqueue.append(jia_song.songqueue[len(jia_song.songqueue)-tempnum-1])
                            tempnum += 1
                        jia_song.songqueue = reversedsongqueue.copy()
                        displayupdate = True
                        del tempnum
                        del reversedsongqueue
                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                            
                        


                    #this is so fucking bad
                    while songsrendernum+1 > 1:
                        #view file in explorer
                        if event.pos[0] in range(mainwindow.size[0]-28,mainwindow.size[0]-4) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-jia_settings.scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-jia_settings.scrollwheely):
                            os.system('explorer /select,"'+str(jia_song.songqueue[songsrendernum-1].songdir).replace('/','\\')+'"')

                        if len(jia_song.songqueue) != 1:
                            if event.pos[1] in range(28,mainwindow.size[1]-24):
                                
                                #delete song
                                if event.pos[0] in range(mainwindow.size[0]-56,mainwindow.size[0]-32) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-jia_settings.scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-jia_settings.scrollwheely):
                                    
                                    jia_song.songqueue[songsrendernum-1].rawfile.close()
                                    jia_song.songqueue.pop(songsrendernum-1)
                                    if jia_song.songnum > len(jia_song.songqueue)-1:

                                        jia_song.songnum = len(jia_song.songqueue)-1
                                        
                                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                                                
                                    if jia_song.songnum == songsrendernum-1:
                                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                                                                
                                    displayupdate = True

                                #movedown song
                                if event.pos[0] in range(mainwindow.size[0]-84,mainwindow.size[0]-60) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-jia_settings.scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-jia_settings.scrollwheely):
                                    movingsong = jia_song.songqueue[songsrendernum-1]
                                    jia_song.songqueue.pop(songsrendernum-1)
                                    jia_song.songqueue.insert(songsrendernum,movingsong)
                                    displayupdate = True

                                    if jia_song.songnum == songsrendernum-1 or jia_song.songnum == songsrendernum:
                                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                                                                
                                
                                if songsrendernum != 1:
                                    #moveup song
                                    if event.pos[0] in range(mainwindow.size[0]-112,mainwindow.size[0]-88) and event.pos[1] in range((4*songsrendernum)+(28*songsrendernum)+2-jia_settings.scrollwheely,(4*songsrendernum)+(28*songsrendernum)+4+28-jia_settings.scrollwheely):
                                        movingsong = jia_song.songqueue[songsrendernum-1]
                                        jia_song.songqueue.pop(songsrendernum-1)
                                        jia_song.songqueue.insert(songsrendernum-2,movingsong)
                                        displayupdate = True
                                        if jia_song.songnum == songsrendernum-1 or jia_song.songnum == songsrendernum-2:
                                            jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                                            jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)
                                                                                    

                        songsrendernum -= 1

                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                if event.button == pygame.BUTTON_WHEELUP:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if jia_settings.scrollwheely != 0:
                            jia_settings.scrollwheely -= 16
                            displayupdate = True
                        

                if event.button == pygame.BUTTON_WHEELDOWN:
                    if not (mousebts_hold[2] or mousebts_hold[0]):
                        if jia_settings.scrollwheely < (4*len(jia_song.songqueue))+(28*len(jia_song.songqueue))+2-mainwindow.size[1]+80:
                            jia_settings.scrollwheely += 16
                            displayupdate = True
                    



if __name__ == '__main__':
    try:
        file = open(scriptdirfolder+slash+'ERROR_RELOAD.jia_save','r',encoding='utf-8')
        for i in file.readlines():
            jia_song.songqueue.append(jia_song.Song(i.replace('\n','')))
        file.close()
        os.remove(scriptdirfolder+slash+'ERROR_RELOAD.jia_save')
    except FileNotFoundError:
        selectedfiles = filedialog.askopenfiles(
                filetypes=jia_song.filetypes,
                title="JakeIsAlivee's Visualizer - Select your music files to visualize",
                
                )
        if len(selectedfiles) == 0:
            loading_thread_run = False
            loading_thread.join()
            sys.exit()
        loading_thread_run = False
        loading_thread.join()
        loadinganim = time.perf_counter()
        tempnum = 0

        info = Queue()
        info.put(tempnum)
        loading_thread_run = True
        loading_thread = threading.Thread(target=loading_screen_Thread,args=(mainwindow_surface,mainwindow,loadinganim,
                                                                             True, info, len(selectedfiles)
                                                                             ))
        loading_thread.start()
        

        while tempnum < len(selectedfiles):

            try:
                jia_song.songqueue.append(jia_song.Song(selectedfiles[tempnum].name))
                tempnum += 1
                info.put(tempnum)
            except FileExistsError:
                buttonindex = pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                        message_type='warn',
                                                        message="There is something wrong with your file. It raises an error while importing.\n\nPlease don't mess with the file extensions. For example, if you rename your .m4a file to be .mp3 it would not magically start working.\n\nProblematic file directory:\n"+selectedfiles[tempnum].name,
                                                        buttons=('Retry','Skip'))
                if buttonindex == 0:
                    continue # retry
                else:
                    tempnum += 1
                    continue # skip

            for event in pygame.event.get():
                events_global(event)    

        del selectedfiles

    jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
    jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

    mainwindow.always_on_top = True                                      
    set_transparency(colors['transparent_chromakey_win'])
    
    loading_thread_run = False
    loading_thread.join()

    mainwindow.flash(pygame.FLASH_UNTIL_FOCUSED)

    while True:
        try:

            scenes()
            timeNOW = time.perf_counter()
            pygameclock.tick(fpscap)

            if timeNOW - int(timeNOW) < 0.01:
                process = psutil.Process(os.getpid())
                ram_used = process.memory_info().rss / (1024 * 1024)  # in mb
                if ram_used > 1500:
                    pygame.display.message_box('CRITICAL ERROR','MEMORY LEAK!!!','error',buttons=('QUIT',))
                    pygame.quit()
                    sys.exit()

            if devmode:
                if devfps:
                    if timeNOW - int(timeNOW) < 0.01:
                        print(pygameclock.get_fps())
                if devruler:
                    if devrulerpoint_index == 2:
                        devrulerpoint_index = devrulerpoint_index % 2
                        pygame.draw.line(mainwindow_surface,(255,0,0),devrulerpoints[0],devrulerpoints[1])
                        mainwindow.flip()

            
        except Exception as exc_traceback:
            mainwindow.always_on_top = False

            problematicline = sys.exc_info()[2]
            while problematicline.tb_next != None:
                problematicline = problematicline.tb_next

            buttonindex = pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                    message="An Error Occured!\nPlease make a screenshot of this error and send it to the creator of this program.\n\n"+
                                                    'VERSION: '+VERSION+'\n'+
                                                    'Exception: '+str(exc_traceback.__class__.__name__)+'\n'+
                                                    'Message: '+str(exc_traceback)+'\n'+
                                                    'Occured in module: '+str(problematicline.tb_frame.f_globals.get("__name__"))+'\n'+
                                                    'Occured at: '+str(problematicline.tb_lineno)+' line\n'+
                                                    'Problematic line:\n"'+open(problematicline.tb_frame.f_code.co_filename,'r').readlines()[problematicline.tb_lineno-1].replace('\n','').replace('    ','')+'"',

                                                    message_type='error',
                                                    buttons=('Pass','Reload while saving your Song Queue','Close'),
                                                    )
            if buttonindex == 0:
                errortext = fonts_unifont(16).render('Error',False,colors['settings_text'],colors['program_notifs'])
                scenetext = fonts_unifont(16).render('Scene: '+scene.capitalize(),False,colors['settings_text'],colors['program_notifs'])
                mainwindow_surface.blit(errortext,(0,mainwindow.size[1]-32))
                mainwindow_surface.blit(scenetext,(0,mainwindow.size[1]-16))
                mainwindow.flip()
                jia_song.playing = False
                pygame.mixer_music.pause()
                displayupdate = False
                continue # Pass
            if buttonindex == 1:
                # Reload while saving your Song Queue
                file = open(scriptdirfolder+slash+'ERROR_RELOAD.jia_save','w',encoding='utf-8')
                for i in jia_song.songqueue:
                    file.writelines(i.songdir+'\n')
                file.close()
                if sys.executable[-10:-4].lower() == 'python': #runs from a script
                    subprocess.Popen([sys.executable, __file__])
                else:
                    subprocess.Popen(['"'+__file__+'"']) #runs from an executable
                pygame.quit()
                sys.exit()
            else: 
                pygame.quit() #Close
                sys.exit()
        


