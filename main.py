
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
- Added a "Now playing: (song name)" animation for every time the song changes
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

- Got 1 whole file splitted into seprate ones

- Switched to pygame's message_box instead of tkinter's message_box > buttons became more customizable

- Not lagging loading screen animation



- Bug fixesssssssssss
- A lot of them
- Cant even count how many there was

"""



""" things to add: 

- Bars mode functionality and settings

- Write all controls in the controls scene
- Customization scene

- fix the bug where pixels between lines start to tweak tf out


[not possible/not compatible, or is it] add new visualizer mode that listens to your pc audio in real time 

-async .song s loading

"""

"""
идеи из тг во время поездки когда пиздец скучно было

if pygame.WindowFocusLost
все boolean зажатия клавиш на false

при зажатии shift и нажатии на стрелки лево право меняется песня
без шифта меняется позиция песни на -5 +5 сек

сделать так чтобы следующая песня загружалась в оперативку параллельно вторым процессом за 10 сек до конца нынешней чтобы не подлагивало

применить эффект с показом названия нынешней песни на ВСЕ разы когда она меняется

загружать 2 песни сразу для плавного перехода и просмотра их зв. волн

чистка песни ДО, при выходе вывода зв. волны за экран, учитывая отдаление

режим воспроизведения песен из компонентов и их рисовка 

"""


    
#all of this is pretty stable but not done at all


import pygame #ce
import os
import sys

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


scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep

icon_jakeisalivee = pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee coffee cup.ico'),(64,64))
icon_loading = pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'loading.png'),(64,64))


unifont_dir = scriptdirfolder+slash+'Data'+slash+'unifont-17.0.04.otf'
def fonts_unifont(size):
    return pygame.Font(unifont_dir,size)

desktopsize = pygame.display.get_desktop_sizes()[0]


import win32api
import win32con
import win32gui
if __name__ == '__main__':

    size = [600,260]
    mainwindow = pygame.Window("JakeIsAlivee's Music Visualizer",
                            size=(600,260),
                            position=((desktopsize[0]//2)-(size[0]//2),(desktopsize[1]//2)-(size[1]//2)),
                            borderless=True,
                            resizable=False,
                            always_on_top=True)
    del size
    mainwindow_surface = mainwindow.get_surface()
    mainwindow.set_icon(icon_jakeisalivee)
    mainwindow.opacity = 1



    windowinfo = win32gui.FindWindowEx(None, None, None, mainwindow.title)

    win32gui.SetWindowLong(windowinfo, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(windowinfo, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    def set_transparency(chromakey: tuple):
        win32gui.SetLayeredWindowAttributes(windowinfo, win32api.RGB(*chromakey), 0, win32con.LWA_COLORKEY)

    set_transparency((0,0,0))
    transparent = True
    
def loading_screen_surface(window_surface: pygame.Surface,
                           window: pygame.Window,
                           circleanim_start: float
                           ):
    window_surface.fill((0,0,0))
    loadingtext = fonts_unifont(64).render('Loading...',False,(255,255,255))
    window_surface.blit(loadingtext,((window.size[0]/2)-(loadingtext.get_width()/2),
                                                            (window.size[1]/2)-(loadingtext.get_height()/2))) 
                        
    circlerotation = int(((time.perf_counter() - circleanim_start)*360)%360)
    circle = pygame.transform.rotozoom(icon_loading,circlerotation,1)
    rotateoffset = (circlerotation%90)/90
    rotateoffset = 0-4*(rotateoffset**2)+4*rotateoffset
    window_surface.blit(circle,(window.size[0]-(66+int(rotateoffset*12.8)),window.size[1]-(66+int(rotateoffset*12.8))))
    
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
                num = numofsongs_queue.get(timeout=0.001)
            except:
                pass
            loadedsongs_render = fonts_unifont(64).render(str(num)+'/'+str(songsleft),False,(255,255,255))
            window_surface.blit(loadedsongs_render,
                                
                                ((mainwindow.size[0]//2)-(loadedsongs_render.get_width()//2),
                                  mainwindow.size[1]    - loadedsongs_render.get_height()))
            
        window.flip()
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                sys.exit()

loadinganim = time.perf_counter()
loading_thread = threading.Thread(target=loading_screen_Thread,args=(mainwindow_surface,mainwindow,loadinganim))
loading_thread.start()


import autoupdate as jia_autoupdate
import settings as jia_settings
import song as jia_song
import visualizer as jia_visualizer


VERSION = "WIP2.2.0"
AUTHORNAME = 'JakeIsAlivee'
REPONAME = 'Music-Visualizer'
jia_settings.init(VERSION)

import gc
import random
import pyaudio
import subprocess
import multiprocessing

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
    root.iconbitmap(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee coffee cup.ico') #for filedialog icon to show

    outputdevice_load_info()











pygameclock = pygame.time.Clock()


def offscreen_check(windowpos: tuple, windowres: tuple, desktopsize: tuple) -> tuple: 
    """Returns new window position"""
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
    global displayupdate
    global mousebts_hold
    global mouseholddrag_startpos

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


fpscap = 0
fpscapnum = 18

fpscap_allowed_values = [1, 2, 5, 8, 10, 12, 24, 30, 60, 120, 180, 240, 300, 360, 480, 600, 720, 1000, 0]








displayupdate = True


# 12 len list, write "jakeisalivee" to activate devmode
devmodeactivation_list = []
devmode = False


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
    surface.fill((0,0,0))

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


def scenes():
    global fpscap

    global scene
    global displayupdate
    global transparent
    global general_mode_num

    global mouseholddrag_startpos
    global mousebts_hold

    global loading_thread_run
    
    if scene == 'visualizer':
        
        if displayupdate:
            displayupdate = False
            
            mainwindow_surface.blit(jia_visualizer.surface_static_new_visualizer(windowres=mainwindow.size,
                                                                                 callable_font=fonts_unifont,
                                                                                 bgcolor=colors['visualizer_bg'],
                                                                                 windowbordercolor=colors['window_border'],

                                                                                 transparent=transparent,
                                                                                 transparencycolor=colors['transparent_chromakey'],
                                                                                 visualizergeneral_mode=general_mode_num,
                                                                                 programnotifscolor=colors['program_notifs'],

                                                                                 songplaying=jia_song.playing,
                                                                                 musicvolume_percent=jia_song.musicvolume_percent,
                                                                                 songnum=jia_song.songnum,
                                                                                 songqueue=jia_song.songqueue,

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
                                                                                 ))
            mainwindow.flip()
            
        if jia_song.playing:
            displayupdate = True

            jia_song.songpos = pygame.mixer_music.get_pos() + jia_song.songpos_sync

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


            if jia_settings.pr_bluetooth_output_device:
                jia_song.lastsounddata = int((jia_song.songpos-(latency*1000)) * jia_song.soundrate/1000)
            else:
                jia_song.lastsounddata = int(jia_song.songpos * jia_song.soundrate/1000)
            

            if jia_song.songformat != '.wav':
                #songsync
                if jia_song.songpos % 10000 >= 9990:
                    pygame.mixer_music.rewind()
                    pygame.mixer_music.play(0,jia_song.songpos/1000)
                    jia_song.songpos_sync = jia_song.songpos

        if jia_visualizer.anim_volume+1 > timeNOW or jia_visualizer.anim_transparency+1 > timeNOW or jia_visualizer.anim_ontop+1 > timeNOW or jia_visualizer.anim_song+1 > timeNOW:
            displayupdate = True

        if jia_visualizer.anim_nowplaying+3 > timeNOW:
            displayupdate = True




        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if jia_song.playing:
                        pygame.mixer_music.pause()
                        jia_song.playing = False
                    else:
                        pygame.mixer_music.unpause()
                        jia_song.playing = True

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer_music.pause()
                    scene = 'settings'
                    displayupdate = True

                if event.key == pygame.K_t:
                    jia_visualizer.anim_transparency = timeNOW

                    if transparent:
                        transparent = False
                    else:
                        transparent = True

                if event.key == pygame.K_o:
                    jia_visualizer.anim_ontop = timeNOW

                    if mainwindow.always_on_top:
                        mainwindow.always_on_top = False
                    else:
                        mainwindow.always_on_top = True


                if event.key == pygame.K_LEFT:
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mousebts_hold[0] = True
                    mouseholddrag_startpos = [event.pos[0],event.pos[1]]



































    elif scene == 'settings':

        if displayupdate:
            displayupdate = False

            mainwindow_surface.blit(jia_settings.surface_static_new_settings(windowres=mainwindow.size,
                                                                             callable_font=fonts_unifont,
                                                                             bgcolor=colors['settings_bg'],
                                                                             textcolor=colors['settings_text'],
                                                                             windowbordercolor=colors['window_border']
                                                                             ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()
        



        for event in pygame.event.get():

            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if jia_song.playing:
                        pygame.mixer_music.unpause()
                    
                    mainwindow_surface.fill(colors['settings_bg'])
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

                    elif event.pos[0] in range(mainwindow.size[0]-174,mainwindow.size[0]-1) and event.pos[1] in range(40,70):
                        scene = 'visual_modes'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-174,mainwindow.size[0]-1) and event.pos[1] in range(76,102):
                        scene = 'songqueue'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(mainwindow.size[1]-76,mainwindow.size[1]-12):
                        os.system('start '+jia_settings.contacts['GitHub'])

                    elif event.pos[0] in range(mainwindow.size[0]-136,mainwindow.size[0]-72) and event.pos[1] in range(mainwindow.size[1]-76, mainwindow.size[1]-12):
                        os.system('start '+jia_settings.contacts['Telegram'])


                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]









    elif scene == 'controls':
        
        if displayupdate:
            displayupdate = False
            mainwindow_surface.blit(jia_settings.surface_static_new_controls(windowres=mainwindow.size,
                                                                             callable_font=fonts_unifont,
                                                                             bgcolor=colors['settings_bg'],
                                                                             textcolor=colors['settings_text'],
                                                                             windowbordercolor=colors['window_border']
                                                                             ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()


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
            mainwindow_surface.blit(jia_settings.surface_static_new_customize(windowres=mainwindow.size,
                                                                              callable_font=fonts_unifont,
                                                                              bgcolor=colors['settings_bg'],
                                                                              textcolor=colors['settings_text'],
                                                                              windowbordercolor=colors['window_border']
                                                                              ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()



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
            mainwindow_surface.blit(jia_settings.surface_static_new_program(windowres=mainwindow.size,
                                                                            callable_font=fonts_unifont,
                                                                            bgcolor=colors['settings_bg'],
                                                                            textcolor=colors['settings_text'],
                                                                            windowbordercolor=colors['window_border'],

                                                                            fpscap=fpscap
                                                                            ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()

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
                        if jia_settings.pr_bluetooth_output_device:
                            jia_settings.pr_bluetooth_output_device = False
                        else:
                            jia_settings.pr_bluetooth_output_device = True
                            outputdevice_load_info()
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-56,mainwindow.size[0]) and event.pos[1] in range(mainwindow.size[1]-88,mainwindow.size[1]-76):
                        scene = 'credits'
                        displayupdate = True

                    elif event.pos[0] in range(mainwindow.size[0]-68,mainwindow.size[0]-4) and event.pos[1] in range(mainwindow.size[1]-76,mainwindow.size[1]-12):
                        os.system('start '+jia_settings.contacts['GitHub'])

                    elif event.pos[0] in range(mainwindow.size[0]-136,mainwindow.size[0]-72) and event.pos[1] in range(mainwindow.size[1]-76, mainwindow.size[1]-12):
                        os.system('start '+jia_settings.contacts['Telegram'])
                    else:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]

    elif scene == 'credits':
        if displayupdate:
            mainwindow_surface.blit(jia_settings.surface_static_new_credits(windowres=mainwindow.size,
                                                                            callable_font=fonts_unifont,
                                                                            bgcolor=colors['settings_bg'],
                                                                            textcolor=colors['settings_text'],
                                                                            windowbordercolor=colors['window_border']
                                                                            ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()

        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'program'
                    displayupdate = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        mousebts_hold[0] = True
                        mouseholddrag_startpos = [event.pos[0],event.pos[1]]




    elif scene == 'visual_modes':

        if displayupdate:
            displayupdate = False
            mainwindow_surface.blit(jia_settings.surface_static_new_visualmodes(windowres=mainwindow.size,
                                                                                callable_font=fonts_unifont,
                                                                                bgcolor=colors['settings_bg'],
                                                                                textcolor=colors['settings_text'],
                                                                                windowbordercolor=colors['window_border'],

                                                                                visualizergeneral_mode=general_mode_num,
                                                                                ))
            windowres_toolow(600,260,
                             mainwindow.size)
            mainwindow.flip()



        if jia_settings.cl_zoom_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if jia_settings.cl_zoom_typing_list[-1] == ' ':
                    jia_settings.cl_zoom_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if jia_settings.cl_zoom_typing_list[-1] == '|':
                    jia_settings.cl_zoom_typing_list[-1] = ' '
                    displayupdate = True



        if jia_settings.cl_line_space_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if jia_settings.cl_line_space_typing_list[-1] == ' ':
                    jia_settings.cl_line_space_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if jia_settings.cl_line_space_typing_list[-1] == '|':
                    jia_settings.cl_line_space_typing_list[-1] = ' '
                    displayupdate = True

        if jia_settings.cl_rotate_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if jia_settings.cl_rotate_typing_list[-1] == ' ':
                    jia_settings.cl_rotate_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if jia_settings.cl_rotate_typing_list[-1] == '|':
                    jia_settings.cl_rotate_typing_list[-1] = ' '
                    displayupdate = True

        if jia_settings.cl_linelength_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if jia_settings.cl_linelength_typing_list[-1] == ' ':
                    jia_settings.cl_linelength_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if jia_settings.cl_linelength_typing_list[-1] == '|':
                    jia_settings.cl_linelength_typing_list[-1] = ' '
                    displayupdate = True

        if jia_settings.osc_linesperframe_typing:
            if float(timeNOW - int(timeNOW)) >= 0.5:
                if jia_settings.osc_linesperframe_typing_list[-1] == ' ':
                    jia_settings.osc_linesperframe_typing_list[-1] = '|'
                    displayupdate = True
            else:
                if jia_settings.osc_linesperframe_typing_list[-1] == '|':
                    jia_settings.osc_linesperframe_typing_list[-1] = ' '
                    displayupdate = True


        for event in pygame.event.get():
            events_global(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scene = 'settings'
                    displayupdate = True

                    if jia_settings.cl_zoom_typing:
                        jia_settings.typing.cancel_clzoom()

                    if jia_settings.cl_line_space_typing:
                        jia_settings.typing.cancel_cllinespace()

                    if jia_settings.cl_rotate_typing:
                        jia_settings.typing.cancel_clrotate()
                        displayupdate = True

                    if jia_settings.cl_linelength_typing:
                        jia_settings.typing.cancel_cllinelength()
                        displayupdate = True

                    if jia_settings.osc_linesperframe_typing:
                        jia_settings.typing.cancel_osclinesperframe()
                        displayupdate = True

                if event.key == 13: #enter
                    
                    if jia_settings.cl_zoom_typing:
                        jia_settings.typing.cancel_clzoom()
                        displayupdate = True

                    if jia_settings.cl_line_space_typing:
                        jia_settings.typing.cancel_cllinespace()
                        displayupdate = True

                    if jia_settings.cl_rotate_typing:
                        jia_settings.typing.cancel_clrotate()
                        displayupdate = True

                    if jia_settings.cl_linelength_typing:
                        jia_settings.typing.cancel_cllinelength()
                        displayupdate = True
                    
                    if jia_settings.osc_linesperframe_typing:
                        jia_settings.typing.cancel_osclinesperframe()
                        displayupdate = True


                if event.key == pygame.K_BACKSPACE:

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:

                    jia_settings.typing.cancel_clzoom()
                    jia_settings.typing.cancel_cllinespace()
                    jia_settings.typing.cancel_clrotate()
                    jia_settings.typing.cancel_cllinelength()
                    jia_settings.typing.cancel_osclinesperframe()
                    displayupdate = True

                    if event.pos[0] in range(100,116) and event.pos[1] in range(40,60): #- general mode
                        if general_mode_num > 1:
                            general_mode_num -= 1
                            displayupdate = True
                    if event.pos[0] in range(116,132) and event.pos[1] in range(40,60): #+ general mode
                        if general_mode_num < len(jia_settings.general_mode_names):
                            general_mode_num += 1
                            displayupdate = True
                    
                    match general_mode_num:
                        case 1:
                            if event.pos[0] in range(52,62) and event.pos[1] in range(88,100): #- cl mode
                                if jia_settings.cl_renderingmode_num > 0:
                                    jia_settings.cl_renderingmode_num -= 1
                                    displayupdate = True
                            elif event.pos[0] in range(108,118) and event.pos[1] in range(88,100): #+ cl mode
                                if jia_settings.cl_renderingmode_num < len(jia_settings.cl_rendering_modes)-1:
                                    jia_settings.cl_renderingmode_num += 1
                                    displayupdate = True

                            elif event.pos[0] in range(4,152) and event.pos[1] in range(100,112): #typing out zoom
                                jia_settings.cl_zoom_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,180) and event.pos[1] in range(112,124): #typing out space between lines
                                jia_settings.cl_line_space_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(121,131) and event.pos[1] in range(124,136): #One dimensional checkbox
                                displayupdate = True
                                if jia_settings.cl_onedimensional:
                                    jia_settings.cl_onedimensional = False
                                else:
                                    jia_settings.cl_onedimensional = True

                            elif event.pos[0] in range(71,81) and event.pos[1] in range(136,148): #mirrored checkbox
                                if jia_settings.cl_onedimensional:
                                    displayupdate = True
                                    if jia_settings.cl_mirrored:
                                        jia_settings.cl_mirrored = False
                                    else:
                                        jia_settings.cl_mirrored = True
        
                            elif event.pos[0] in range(4,162) and event.pos[1] in range(148,160): #rotate typing
                                jia_settings.cl_rotate_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(4,200) and event.pos[1] in range(160,172): #linelen typing
                                jia_settings.cl_linelength_typing = True
                                displayupdate = True

                            else:
                                displayupdate = True

                                mousebts_hold[0] = True
                                mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                        case 2:
                            if event.pos[0] in range(52,62) and event.pos[1] in range(88,100): #- cl mode
                                if jia_settings.cl_renderingmode_num > 0:
                                    jia_settings.cl_renderingmode_num -= 1
                                    displayupdate = True
                            elif event.pos[0] in range(108,118) and event.pos[1] in range(88,100): #+ cl mode
                                if jia_settings.cl_renderingmode_num < len(jia_settings.cl_rendering_modes)-1:
                                    jia_settings.cl_renderingmode_num += 1
                                    displayupdate = True

                            elif event.pos[0] in range(4,152) and event.pos[1] in range(100,112): #typing out zoom
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

                            #no rotate typing yet

                            else:

                                mousebts_hold[0] = True
                                mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                        case 3:
                            mousebts_hold[0] = True
                            mouseholddrag_startpos = [event.pos[0],event.pos[1]]

                        case 4:
                            if event.pos[0] in range(2,162) and event.pos[1] in range(86,98):
                                jia_settings.osc_linesperframe_typing = True
                                displayupdate = True

                            elif event.pos[0] in range(64,74) and event.pos[1] in range(100,110):
                                if jia_settings.osc_fadeout:
                                    jia_settings.osc_fadeout = False
                                else: 
                                    jia_settings.osc_fadeout = True
                                displayupdate = True

                            else:
                                mousebts_hold[0] = True
                                mouseholddrag_startpos = [event.pos[0],event.pos[1]]

            if event.type == pygame.TEXTINPUT:
                try:
                    if jia_settings.cl_zoom_typing:
                        if len(jia_settings.cl_zoom_typing_list) < 8:
                            jia_settings.cl_zoom_typing_list.insert(len(jia_settings.cl_zoom_typing_list)-1,int(event.text))
                            displayupdate = True

                    if jia_settings.cl_line_space_typing:
                        if len(jia_settings.cl_line_space_typing_list) < 4:
                            jia_settings.cl_line_space_typing_list.insert(len(jia_settings.cl_line_space_typing_list)-1,int(event.text))
                            displayupdate = True

                    if jia_settings.cl_rotate_typing:
                        if len(jia_settings.cl_rotate_typing_list) < 5:
                            jia_settings.cl_rotate_typing_list.insert(len(jia_settings.cl_rotate_typing_list)-2,int(event.text))
                            displayupdate = True
                
                    if jia_settings.cl_linelength_typing:
                        if event.text == '.':
                            if len(jia_settings.cl_linelength_typing_list) < 6:
                                jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,str(event.text))
                                displayupdate = True
                        else:
                            if str(jia_settings.cl_linelength_typing_list).find('.') == -1:
                                if len(jia_settings.cl_linelength_typing_list) < 3:
                                    jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,int(event.text))
                                    displayupdate = True
                            else:
                                if len(jia_settings.cl_linelength_typing_list) < 6:
                                    jia_settings.cl_linelength_typing_list.insert(len(jia_settings.cl_linelength_typing_list)-1,int(event.text))
                                    displayupdate = True
                    
                    if jia_settings.osc_linesperframe_typing:
                        if len(jia_settings.osc_linesperframe_typing_list) < 5:
                            jia_settings.osc_linesperframe_typing_list.insert(len(jia_settings.osc_linesperframe_typing_list)-1,str(event.text))
                            displayupdate = True

                except ValueError:
                    pass






























    elif scene == 'songqueue':
        if displayupdate:
            displayupdate = False
            mainwindow_surface.blit(jia_settings.surface_static_new_songqueue(windowres=mainwindow.size,
                                                                              callable_font=fonts_unifont,
                                                                              bgcolor=colors['settings_bg'],
                                                                              textcolor=colors['settings_text'],

                                                                              windowbordercolor=colors['window_border'],
                                                                              songqueue=jia_song.songqueue,
                                                                              ))
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
                        
                        mainwindow.always_on_top = False #so the window doesnt cover the windows file manager
                        
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

                        loading_thread_run = False
                        loading_thread.join()
                        
                        mainwindow.always_on_top = wasitontop_before
                        displayupdate = True
                        continue


                    if event.pos[0] in range(mainwindow.size[0]-28,mainwindow.size[0]-4) and event.pos[1] in range(4,28): #folder import
                        wasitontop_before = mainwindow.always_on_top
                                                
                        mainwindow.always_on_top = False #so the window doesnt cover the windows file manager
                        
                        import_folder = filedialog.askdirectory(title="JakeIsAlivee's Visualizer - Choose the folder that you want to import your music files from")
                        if import_folder == '': #None
                            mainwindow.always_on_top = wasitontop_before
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
                                continue
                            del areyousure


                        if len(musicfiles) == 0:
                            pygame.display.message_box(title="JakeIsAlivee's Visualizer",
                                                       message="There is no music files in this folder",
                                                       message_type='info',
                                                       buttons=('Ok'))
                            mainwindow.always_on_top = wasitontop_before
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


                        jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
                        jia_song.songnum = 0

                        jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

                        loading_thread_run = False
                        loading_thread.join()
                        
                        mainwindow.always_on_top = wasitontop_before
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
                                    
        del selectedfiles

    jia_song.songpos, jia_song.songpos_sync, jia_song.lastsounddata = jia_song.songreset()
    jia_visualizer.soundrawdata, jia_song.soundrate, jia_song.songformat = jia_song.songqueue[jia_song.songnum].load(jia_song.musicvolume_percent)

    mainwindow.always_on_top = True                                      
    set_transparency(colors['transparent_chromakey_win'])

    loading_thread_run = False
    loading_thread.join()

    while True:
        try:
            scenes()
            timeNOW = time.perf_counter()
            pygameclock.tick(fpscap)
            
            if devmode:
                if timeNOW - int(timeNOW) < 0.01:
                    print(pygameclock.get_fps())

            
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
                                                    'Problematic line:\n"'+open(problematicline.tb_frame.f_code.co_filename,'r').readlines()[problematicline.tb_lineno-1].replace('\n','')+'"',

                                                    message_type='error',
                                                    buttons=('Pass','Reload while saving your Song Queue','Close'),
                                                    )
            if buttonindex == 0:
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
        


