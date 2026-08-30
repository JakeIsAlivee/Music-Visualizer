import pygame
import time
import os
import numpy


anim_transparency = 0
anim_ontop = 0

anim_volume = 0

anim_song = 0

anim_nowplaying = 0


anim_add5sec = 0
anim_subtract5sec = 0



def surface_static_new_visualizer(windowres: tuple,
                                  callable_font,
                                  bgcolor: tuple,
                                  windowbordercolor: tuple,

                                  visualizergeneral_mode: int,
                                  programnotifscolor: tuple,
                                  songplaying: bool,
                                  musicvolume_percent: int,
                                  songnum: int,
                                  songqueue: list,
                                  songsamplerate: float,

                                  cl_rotate: int,



                                  linecolor: tuple,
                                  lastsounddata: int,
                                  devisionby: int,

                                  cl_line_space: int,
                                  cl_linelength: int,
                                  cl_renderingmode_num: int,
                                  cl_onedimensional: bool,
                                  cl_mirrored: bool,

                                  wf_mono: bool,
                                  wf_merge: bool,
                                  wf_split: bool,

                                  osc_linesperframe: int,
                                  osc_fadeout: bool,


                                  b_renderingmode_num: int,
                                  b_boostfreq: bool,
                                  b_boostfreq_num: int, #index
                                  b_boostfreq_graph: int, #index
                                  
                                  b_boostfreq_intensity_quad: int, 
                                  b_boostfreq_intensity_sqrt: int, 
                                  b_boostfreq_mult: float,

                                  b_adaptive_linelen: bool,


                                  textcolor: tuple,


                                  sounddataspeednum: int,
                                  sounddataspeed_intensity_sqrts: int,
                                  sounddataspeed_intensity_quads: int,
                                  sounddata_fadeout: bool,
                                  ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)


    if visualizergeneral_mode == 1:
        surface.blit(classic_renderer(windowres,
                                      linecolor,
                                      windowbordercolor,

                                      lastsounddata,
                                      devisionby,

                                      cl_line_space,
                                      cl_linelength,
                                      cl_renderingmode_num,

                                      cl_onedimensional,
                                      cl_mirrored,
                                      cl_rotate,

                                      sounddataspeednum,
                                      sounddataspeed_intensity_sqrts,
                                      sounddataspeed_intensity_quads,
                                      sounddata_fadeout
                                      ))

    if visualizergeneral_mode == 2:
        surface.blit(waveform_renderer(windowres,
                                       linecolor,
                                       windowbordercolor,

                                       lastsounddata,
                                       devisionby,

                                       cl_renderingmode_num,
                                       cl_rotate,
                                       cl_linelength,

                                       wf_mono,
                                       wf_merge,
                                       wf_split,

                                       sounddataspeednum,
                                       sounddataspeed_intensity_sqrts,
                                       sounddataspeed_intensity_quads,
                                       sounddata_fadeout
                                       ))
    if visualizergeneral_mode == 3:
        surface.blit(bars_renderer(windowres,
                                   linecolor,
                                   lastsounddata,
                                   songsamplerate,

                                   cl_onedimensional,
                                   cl_mirrored,
                                   cl_line_space,
                                   cl_rotate,
                                   cl_linelength,

                                   b_renderingmode_num,
                                   b_boostfreq,
                                   b_boostfreq_num, 
                                   b_boostfreq_graph, 
                                   
                                   b_boostfreq_intensity_quad, 
                                   b_boostfreq_intensity_sqrt, 
                                   b_boostfreq_mult,

                                   b_adaptive_linelen,
                                   
                                   ))
    if visualizergeneral_mode == 4:
        surface.blit(oscilloscope_renderer(windowres,
                                           linecolor,

                                           lastsounddata,

                                           osc_linesperframe,
                                           osc_fadeout,

                                           ))

    curtime = time.perf_counter()
    
    if anim_nowplaying+3 > curtime:
                
        #really big fps drops
        #should optimize this later
        songname = os.path.splitext(os.path.split(songqueue[songnum].songdir)[1])[0]
        fontsize = 16

            
        nowplayingstr = 'Now playing: "'+songname+'"'
        nowplaying_text = callable_font(fontsize).render(nowplayingstr,False,textcolor)

        pixelspersymbol = nowplaying_text.get_width()/len(nowplayingstr)
        sizemult = (len(nowplayingstr)*(pixelspersymbol))/(len(nowplayingstr)*fontsize)

        if cl_rotate == 90 or cl_rotate == 270:
            windowres = (windowres[1],windowres[0])

        while len(nowplayingstr)*fontsize*sizemult > windowres[0] and fontsize != 1:
            fontsize -= 1

        if cl_rotate == 90 or cl_rotate == 270:
            windowres = (windowres[1],windowres[0])
                        

        nowplaying_text = callable_font(fontsize-1).render(nowplayingstr,False,textcolor)


        nowplaying_surfacexy = [nowplaying_text.get_width()+4,nowplaying_text.get_height()+4]
        nowplaying_surface = pygame.Surface((nowplaying_surfacexy[0],nowplaying_surfacexy[1]))

        nowplaying_surface.fill(bgcolor)
        nowplaying_surface.blit(nowplaying_text, (2,2))
        pygame.draw.lines(nowplaying_surface,windowbordercolor,False,
                        [(0,0),(nowplaying_surfacexy[0]-1,0),
                        (nowplaying_surfacexy[0]-1,nowplaying_surfacexy[1]-1),(0,nowplaying_surfacexy[1]-1),
                        (0,0)])

        nowplaying_surface = pygame.transform.rotate(nowplaying_surface,0-cl_rotate)

        #this was hell
        anim_nowplaying_time = int(((anim_nowplaying+3)-curtime)*1000)
        if anim_nowplaying_time in range(2500,3000): #roll out animation
            match cl_rotate:
                case 0:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                (6+nowplaying_surfacexy[1])-(nowplaying_surfacexy[1]*((((anim_nowplaying+3)-curtime)-2)*2))))
                case 90:
                    surface.blit(nowplaying_surface,((windowres[0]-((6+nowplaying_surfacexy[1])*2))+((6+nowplaying_surfacexy[1])*((((anim_nowplaying+3)-curtime)-2)*2)),
                                                (windowres[1]//2)-(nowplaying_surfacexy[0]//2)))
                case 180:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                (windowres[1]-((6+nowplaying_surfacexy[1])*2))+((6+nowplaying_surfacexy[1])*((((anim_nowplaying+3)-curtime)-2)*2))))
                case 270:
                    surface.blit(nowplaying_surface,((6+nowplaying_surfacexy[1])-(nowplaying_surfacexy[1]*((((anim_nowplaying+3)-curtime)-2)*2)),
                                                (windowres[1]//2)-(nowplaying_surfacexy[0]//2),))

        if anim_nowplaying_time in range(500,2500): #staying still
            match cl_rotate:
                case 0:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                    (6)))
                case 90:
                    surface.blit(nowplaying_surface,((0-6-nowplaying_surfacexy[1]+windowres[0]),
                                                    (windowres[1]//2)-(nowplaying_surfacexy[0]//2)))
                case 180:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                    (0-6-nowplaying_surfacexy[1]+windowres[1])))
                case 270:
                    surface.blit(nowplaying_surface,((6),
                                                    (windowres[1]//2)-(nowplaying_surfacexy[0]//2)))
            
        if anim_nowplaying_time in range(0,500): #roll in animation
            match cl_rotate:
                case 0:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                    (6-nowplaying_surfacexy[1])+((nowplaying_surfacexy[1])/((((anim_nowplaying+3)-curtime))*2))))
                case 90:
                    surface.blit(nowplaying_surface,(((windowres[0]))-((6+nowplaying_surfacexy[1])/((((anim_nowplaying+3)-curtime))*2)),
                                                    (windowres[1]//2)-(nowplaying_surfacexy[0]//2)))
                case 180:
                    surface.blit(nowplaying_surface,((windowres[0]//2)-(nowplaying_surfacexy[0]//2),
                                                    ((windowres[1]))-((6+nowplaying_surfacexy[1])/((((anim_nowplaying+3)-curtime))*2))))
                case 270:
                    surface.blit(nowplaying_surface,((6-nowplaying_surfacexy[1])+((nowplaying_surfacexy[1])/((((anim_nowplaying+3)-curtime))*2)),
                                                    (windowres[1]//2)-(nowplaying_surfacexy[0]//2)))
                
    
                        
    if anim_volume+1 > curtime:
    
        text_transparency = int((anim_volume+1 - curtime) * 255)
    
        percentage_text = callable_font(150).render(str(musicvolume_percent)+'%',False,programnotifscolor)
        percentage_text.set_alpha(text_transparency)
        surface.blit(percentage_text,((windowres[0]/2)-(percentage_text.get_width()/2),
                                                (windowres[1]/2)-(percentage_text.get_height()/2)))
        del percentage_text
        
    if anim_transparency+1 > curtime:
    
        text_transparency = int((anim_transparency+1 - curtime) * 255)
    
        donetext = callable_font(150).render('Done!',False,programnotifscolor)
        donetext.set_alpha(text_transparency)
        surface.blit(donetext,((windowres[0]/2)-(donetext.get_width()/2),
                                        (windowres[1]/2)-(donetext.get_height()/2)))
        del donetext
                
    if anim_ontop+1 > curtime:
    
        text_transparency = int((anim_ontop+1 - curtime) * 255)
    
        donetext = callable_font(150).render('Done!',False,programnotifscolor)
        donetext.set_alpha(text_transparency)
        surface.blit(donetext,((windowres[0]/2)-(donetext.get_width()/2),
                                    (windowres[1]/2)-(donetext.get_height()/2)))
        del donetext
        
    if anim_song+1 > curtime:
    
        text_transparency = int((anim_song+1 - curtime) * 255)
    
        songnum_text = callable_font(150).render(str(songnum+1),False,programnotifscolor)
        songnum_text.set_alpha(text_transparency)
        surface.blit(songnum_text,((windowres[0]/2)-(songnum_text.get_width()/2),
                                            (windowres[1]/2)-(songnum_text.get_height()/2)))
        del songnum_text

    if anim_add5sec+1 > curtime:
        text_transparency = int((anim_add5sec+1 - curtime) * 255)
            
        add5_text = callable_font(150).render('+5sec',False,programnotifscolor)
        add5_text.set_alpha(text_transparency)
        surface.blit(add5_text,((windowres[0]/2)-(add5_text.get_width()/2),
                                (windowres[1]/2)-(add5_text.get_height()/2)))
        del add5_text
    if anim_subtract5sec+1 > curtime:
        text_transparency = int((anim_subtract5sec+1 - curtime) * 255)
                
        subtract5_text = callable_font(150).render('-5sec',False,programnotifscolor)
        subtract5_text.set_alpha(text_transparency)
        surface.blit(subtract5_text,((windowres[0]/2)-(subtract5_text.get_width()/2),
                                    (windowres[1]/2)-(subtract5_text.get_height()/2)))
        del subtract5_text

    if songplaying == False:
        pygame.draw.line(surface,programnotifscolor,((windowres[0]/2)-(windowres[0]/12),(windowres[1]/2)+(windowres[1]/3)),((windowres[0]/2)-(windowres[0]/12),(windowres[1]/2)-(windowres[1]/3)),10)
        pygame.draw.line(surface,programnotifscolor,((windowres[0]/2)+(windowres[0]/12),(windowres[1]/2)+(windowres[1]/3)),((windowres[0]/2)+(windowres[0]/12),(windowres[1]/2)-(windowres[1]/3)),10)
        
    
    pygame.draw.lines(surface,windowbordercolor,False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)])
    
    return surface



from queue import Queue

def VISUALIZER_THREAD(
                                  windowres: tuple,
                                  callable_font,
                                  bgcolor: tuple,
                                  windowbordercolor: tuple,

                                  visualizergeneral_mode: int,
                                  programnotifscolor: tuple,
                                  songplaying: bool,
                                  musicvolume_percent: int,
                                  songnum: int,
                                  songqueue: list,
                                  songsamplerate: float,

                                  cl_rotate: int,



                                  linecolor: tuple,
                                  lastsounddata: int,
                                  devisionby: int,

                                  cl_line_space: int,
                                  cl_linelength: int,
                                  cl_renderingmode_num: int,
                                  cl_onedimensional: bool,
                                  cl_mirrored: bool,

                                  wf_mono: bool,
                                  wf_merge: bool,
                                  wf_split: bool,

                                  osc_linesperframe: int,
                                  osc_fadeout: bool,

                                  textcolor: tuple,

                                  b_renderingmode_num: int,
                                  b_boostfreq: bool,
                                  b_boostfreq_num: int, #index
                                  b_boostfreq_graph: int, #index
                                                                    
                                  b_boostfreq_intensity_quad: int, 
                                  b_boostfreq_intensity_sqrt: int, 
                                  b_boostfreq_mult: float,

                                  b_adaptive_linelen: bool,

                                  sounddataspeednum: int,
                                  sounddataspeed_intensity_sqrts: int,
                                  sounddataspeed_intensity_quads: int,     
                                  sounddata_fadeout: bool,

                                  
                                  QUEUE: Queue,
                                  ):
    #surface_static_new_visualizer args + queue for surfaces


    surface = surface_static_new_visualizer(
                                  windowres,
                                  callable_font,
                                  bgcolor,
                                  windowbordercolor,

                                  visualizergeneral_mode,
                                  programnotifscolor,
                                  songplaying,
                                  musicvolume_percent,
                                  songnum,
                                  songqueue,
                                  songsamplerate,

                                  cl_rotate,



                                  linecolor,
                                  lastsounddata,
                                  devisionby,

                                  cl_line_space,
                                  cl_linelength,
                                  cl_renderingmode_num,
                                  cl_onedimensional,
                                  cl_mirrored,

                                  wf_mono,
                                  wf_merge,
                                  wf_split,

                                  osc_linesperframe,
                                  osc_fadeout,

                                  textcolor,

                                  b_renderingmode_num,
                                  b_boostfreq,
                                  b_boostfreq_num,
                                  b_boostfreq_graph,
                                  
                                  b_boostfreq_intensity_quad,
                                  b_boostfreq_intensity_sqrt,
                                  b_boostfreq_mult,
  
                                  b_adaptive_linelen,

                                  sounddataspeednum,
                                  sounddataspeed_intensity_sqrts,
                                  sounddataspeed_intensity_quads,    
                                  sounddata_fadeout,)
    
    QUEUE.put_nowait(surface)


    



soundrawdata = None


def classic_renderer(truewindowres: tuple,
                     linecolor: tuple,
                     windowbordercolor: tuple,

                     lastsounddata: int,
                     devisionby: int,

                     cl_line_space: int,
                     cl_linelength: int,
                     cl_renderingmode_num: int,

                     cl_onedimensional: bool,
                     cl_mirrored: bool,

                     cl_rotate: int,

                     sounddataspeednum: int,
                     sounddataspeed_intensity_sqrts: int,
                     sounddataspeed_intensity_quads: int,
                     sounddata_fadeout: bool,
                     ):


    surface = pygame.Surface((truewindowres[0],truewindowres[1]),pygame.SRCALPHA)

    if cl_rotate == 0 or cl_rotate == 180: #depend on x axis
        windowres = truewindowres
        
    if cl_rotate == 90 or cl_rotate == 270: #depend on y axis
        windowres = (truewindowres[1],truewindowres[0])

    if cl_rotate == 0 or cl_rotate == 180:
        var = tuple
    if cl_rotate == 90 or cl_rotate == 270: # we need to reverse the tuple so xnum is y instead of x
        var = reversed



    xnum = cl_line_space

    while xnum < windowres[0]:
        desmosshenanigans = 0 #sometimes when we use threading with no GIL the thread starts when all lines of code declaring this var are already passed but the func is not done so it returns an exception

        try:
            colortransition = linecolor
            match sounddataspeednum: #all of the graphs are y = x, not the other way
                case 0:
                    
                    if cl_rotate == 0 or cl_rotate == 180:
                        rendering_formulas = [
                                              int(xnum)-(windowres[0]//2)+(lastsounddata//devisionby),
                                            0-int(xnum)+(windowres[0]//2)+(lastsounddata//devisionby),
                                            0-int(xnum//2)+(windowres[0]//2)+   (lastsounddata//devisionby),
                                              int(xnum//2)-(windowres[0]//2)+   (lastsounddata//devisionby),
                                              int(xnum)+                   (lastsounddata//devisionby),
                                            0-int(xnum)+                   (lastsounddata//devisionby),
                                            0-int(xnum)+(windowres[0])+   (lastsounddata//devisionby),
                                              int(xnum)-(windowres[0])+   (lastsounddata//devisionby),
                        ]
                                                    
                    if cl_rotate == 90 or cl_rotate == 270:
                        rendering_formulas = [
                                            0-int(xnum)+(windowres[0]//2)+((lastsounddata)//devisionby),
                                              int(xnum)-(windowres[0]//2)+((lastsounddata)//devisionby),
                                            0-int(xnum//2)+(windowres[0]//2)+   ((lastsounddata)//devisionby),
                                              int(xnum//2)-(windowres[0]//2)+   ((lastsounddata)//devisionby),
                                            0-int(xnum)+(windowres[0])+   ((lastsounddata)//devisionby), 
                                              int(xnum)-(windowres[0])+   ((lastsounddata)//devisionby),  
                                              int(xnum)+                   ((lastsounddata)//devisionby), 
                                            0-int(xnum)+                   ((lastsounddata)//devisionby), 
                                                ]

                    



                case 1: #squareroot #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = 1-(abs(((xnum/windowres[0])*2)-2)**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = 1-(abs(((xnum/windowres[0])*2)-2)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                        colordesmos = 1-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = (abs((((xnum//2)/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                        colordesmos = (abs((((xnum)/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(4,6): #|<<
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = 1-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 1-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(6,8): #>>|
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            colordesmos = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))


                case 2: #reversesquareroot #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = 0-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = 0-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        colordesmos = (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = 0-(abs((((xnum//2)/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        colordesmos = (abs((((xnum//2)/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))


                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans =   (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans =   (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = 1-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = 0-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos =  (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos =  1-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))

                
                    


                case 3: #quad #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = (0-(((((xnum/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                                                    
                        colordesmos = 1-((((xnum/windowres[0])*2)-1)**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                        colordesmos = 1-(((((xnum//2)/windowres[0])*2)-1)**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0])))**(sounddataspeed_intensity_quads-1))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-(((((xnum/windowres[0])-1))**sounddataspeed_intensity_quads))
                            colordesmos = ((((xnum/windowres[0])))**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = (((((xnum/windowres[0])-1))**(sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0]))-1)**(sounddataspeed_intensity_quads-1))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = ((((xnum/windowres[0]))-1)**(sounddataspeed_intensity_quads-1))

                    

                case 4: #reversequad #all done with rotations

                    
                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = ((((((xnum/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = ((((((xnum/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = (0-(((((xnum/windowres[0])*2))**sounddataspeed_intensity_quads)))+1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = (0-(((((xnum/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))-1
                        colordesmos = ((((xnum/windowres[0])*2)-1)**2)

                    if cl_renderingmode_num in range(2,4):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum//2 < windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum//2 >= windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum//2 < windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum//2 >= windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        colordesmos = (((((xnum//2)/windowres[0])*2)-1)**2)

                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0]))-1)**sounddataspeed_intensity_quads)))+1
                            colordesmos = ((((xnum/windowres[0])))**2)
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 1-((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0])))**2)

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))-1
                            colordesmos = ((((xnum/windowres[0]))-1)**2)
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-((((((xnum/windowres[0])-1))**sounddataspeed_intensity_quads)))-1
                            colordesmos = 1-((((xnum/windowres[0]))-1)**2)




            if sounddataspeednum != 0:
                if sounddataspeednum in range(1,3):
                    effectrange = ((((windowres[0])*64))*devisionby)
                if sounddataspeednum in range(3,5):
                    effectrange = ((((windowres[0])*64)*(sounddataspeed_intensity_quads-2))*devisionby)
                
                rendering_formulas = [
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                                                                        
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                     ]

                if sounddata_fadeout:
                    colortransition = []
                    for i in linecolor:
                        colortransition.append(int(i/2)+int((i/2)*colordesmos))
                    colortransition = tuple(colortransition)

                                
            linesrender_formula = rendering_formulas[cl_renderingmode_num]

            if linesrender_formula < 0:
                xnum = xnum+1+cl_line_space
                continue

            if cl_onedimensional:
                if cl_mirrored:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                        pygame.draw.line(surface,colortransition,
                                tuple(var((int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))),
                                tuple(var((int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                tuple(var((windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))),
                                tuple(var((windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))))

                        xnum = xnum+1+cl_line_space
                                    
                        continue


                    pygame.draw.line(surface,colortransition,
                                tuple(var((int(xnum),(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))),
                                tuple(var((int(xnum),(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))))

                else:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        pygame.draw.line(surface,colortransition,
                                tuple(var((int(xnum)//2,windowres[1]-(windowres[1]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))))),
                                tuple(var((int(xnum)//2,windowres[1]))))
                        pygame.draw.line(surface,colortransition,
                                tuple(var((windowres[0]-int(xnum)//2,windowres[1]-(windowres[1])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))),
                                tuple(var((windowres[0]-int(xnum)//2,windowres[1]))))

                        xnum = xnum+1+cl_line_space
                        continue

                    pygame.draw.line(surface,colortransition,
                                tuple(var((int(xnum),windowres[1]-(windowres[1]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))),
                                tuple(var((int(xnum),windowres[1]))))



            else:
                if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    pygame.draw.line(surface,colortransition,
                            tuple(var((int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength))))),
                            tuple(var((int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))))
                    pygame.draw.line(surface,colortransition,
                            tuple(var((windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))),
                            tuple(var((windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))))
                            
                    xnum = xnum+1+cl_line_space

                    continue

                pygame.draw.line(surface,colortransition,
                                tuple(var((int(xnum),(windowres[1]//2)+(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)))),
                                tuple(var((int(xnum),(windowres[1]//2)-(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))))


            xnum = xnum+1+cl_line_space

        except IndexError:
            xnum = xnum+1+cl_line_space
        except ZeroDivisionError:
            xnum = xnum+1+cl_line_space

    if cl_rotate == 180 or cl_rotate == 90:
        surface = pygame.transform.rotozoom(surface,180,1)

    if cl_renderingmode_num < 4:
        pygame.draw.line(surface,windowbordercolor,tuple(var((((windowres[0]/2)-1,10)))),
                                                   tuple(var((((windowres[0]/2)-1,windowres[1]-10)))))
        pygame.draw.line(surface,windowbordercolor,tuple(var((((windowres[0]/2),10))))  ,
                                                   tuple(var((((windowres[0]/2),  windowres[1]-10)))))

    return surface



#waveform drops the fps MASSIVELY rn #i dont think its possible to optimize unless we switch from pygame to a new library
def waveform_renderer(truewindowres: tuple,
                      linecolor: tuple,
                      windowbordercolor: tuple,

                      lastsounddata: int,
                      devisionby: int,

                      cl_renderingmode_num: int,
                      cl_rotate: int,
                      cl_linelength: int,

                      wf_mono: bool,    
                      wf_merge: bool,
                      wf_split: bool,

                      sounddataspeednum: int,
                      sounddataspeed_intensity_sqrts: int,
                      sounddataspeed_intensity_quads: int,
                      sounddata_fadeout: bool,
                      ):


    surface = pygame.Surface((truewindowres[0],truewindowres[1]),pygame.SRCALPHA)

    if cl_rotate == 0 or cl_rotate == 180: #depend on x axis
        windowres = truewindowres
            
    if cl_rotate == 90 or cl_rotate == 270: #depend on y axis
        windowres = (truewindowres[1],truewindowres[0])
    
    if cl_rotate == 0 or cl_rotate == 180:
        var = tuple
    if cl_rotate == 90 or cl_rotate == 270: # we need to reverse the tuple so xnum is y instead of x
        var = reversed

    

    xnum = 0

    while xnum < windowres[0]:
        desmosshenanigans = 0 #sometimes when we use threading with no GIL the thread starts when all lines of code declaring this var are already passed but the func is not done so it returns an exception

        try:
            try:
                prevlinesrender_formula = rendering_formulas[cl_renderingmode_num]
            except:
                prevlinesrender_formula = 0

            colortransition = linecolor
            match sounddataspeednum: #all of the graphs are y = x, not the other way
                case 0:
                    
                    if cl_rotate == 0 or cl_rotate == 180:
                        rendering_formulas = [
                                              int(xnum)-(windowres[0]//2)+(lastsounddata//devisionby),
                                            0-int(xnum)+(windowres[0]//2)+(lastsounddata//devisionby),
                                            0-int(xnum//2)+(windowres[0]//2)+   (lastsounddata//devisionby),
                                              int(xnum//2)-(windowres[0]//2)+   (lastsounddata//devisionby),
                                              int(xnum)+                   (lastsounddata//devisionby),
                                            0-int(xnum)+                   (lastsounddata//devisionby),
                                            0-int(xnum)+(windowres[0])+   (lastsounddata//devisionby),
                                              int(xnum)-(windowres[0])+   (lastsounddata//devisionby),
                        ]
                                                    
                    if cl_rotate == 90 or cl_rotate == 270:
                        rendering_formulas = [
                                            0-int(xnum)+(windowres[0]//2)+((lastsounddata)//devisionby),
                                              int(xnum)-(windowres[0]//2)+((lastsounddata)//devisionby),
                                            0-int(xnum//2)+(windowres[0]//2)+   ((lastsounddata)//devisionby),
                                              int(xnum//2)-(windowres[0]//2)+   ((lastsounddata)//devisionby),
                                            0-int(xnum)+(windowres[0])+   ((lastsounddata)//devisionby), 
                                              int(xnum)-(windowres[0])+   ((lastsounddata)//devisionby),  
                                              int(xnum)+                   ((lastsounddata)//devisionby), 
                                            0-int(xnum)+                   ((lastsounddata)//devisionby), 
                                                ]

                    



                case 1: #squareroot #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = 1-(abs(((xnum/windowres[0])*2)-2)**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = 1-(abs(((xnum/windowres[0])*2)-2)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                        colordesmos = 1-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = (abs((((xnum//2)/windowres[0])*2))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                        colordesmos = (abs((((xnum)/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(4,6): #|<<
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = 1-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 1-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(6,8): #>>|
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))-1
                            colordesmos = (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))


                case 2: #reversesquareroot #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = 0-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans =   (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = 0-(abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        colordesmos = (abs(((xnum/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = 0-(abs((((xnum//2)/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))
                        colordesmos = (abs((((xnum//2)/windowres[0])*2)-1)**(1-(sounddataspeed_intensity_sqrts/80)))


                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans =   (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = (abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans =   (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos = 1-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = 0-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos =  (abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-(abs(((xnum/windowres[0])))**(1-(sounddataspeed_intensity_sqrts/80)))
                            colordesmos =  1-(abs(((xnum/windowres[0])-1))**(1-(sounddataspeed_intensity_sqrts/80)))

                
                    


                case 3: #quad #all done with rotations

                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = (0-(((((xnum/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                                                    
                        colordesmos = 1-((((xnum/windowres[0])*2)-1)**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(2,4):
                        desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-1)**sounddataspeed_intensity_quads)))
                        colordesmos = 1-(((((xnum//2)/windowres[0])*2)-1)**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0])))**(sounddataspeed_intensity_quads-1))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-(((((xnum/windowres[0])-1))**sounddataspeed_intensity_quads))
                            colordesmos = ((((xnum/windowres[0])))**(sounddataspeed_intensity_quads-1))

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = (((((xnum/windowres[0])-1))**(sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0]))-1)**(sounddataspeed_intensity_quads-1))
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = ((((xnum/windowres[0]))-1)**(sounddataspeed_intensity_quads-1))

                    

                case 4: #reversequad #all done with rotations

                    
                    if cl_renderingmode_num in range(0,2):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = ((((((xnum/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = ((((((xnum/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum < windowres[0]//2:
                                desmosshenanigans = (0-(((((xnum/windowres[0])*2))**sounddataspeed_intensity_quads)))+1
                            if xnum >= windowres[0]//2:
                                desmosshenanigans = (0-(((((xnum/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))-1
                        colordesmos = ((((xnum/windowres[0])*2)-1)**2)

                    if cl_renderingmode_num in range(2,4):
                        if cl_rotate == 0 or cl_rotate == 180:
                            if xnum//2 < windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum//2 >= windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        if cl_rotate == 90 or cl_rotate == 270:
                            if xnum//2 < windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2))**sounddataspeed_intensity_quads)))-1
                            if xnum//2 >= windowres[0]//2:
                                desmosshenanigans = (((((((xnum//2)/windowres[0])*2)-2)**sounddataspeed_intensity_quads)))+1
                        colordesmos = (((((xnum//2)/windowres[0])*2)-1)**2)

                    if cl_renderingmode_num in range(4,6):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0]))-1)**sounddataspeed_intensity_quads)))+1
                            colordesmos = ((((xnum/windowres[0])))**2)
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 1-((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))
                            colordesmos = 1-((((xnum/windowres[0])))**2)

                    if cl_renderingmode_num in range(6,8):
                        if cl_rotate == 0 or cl_rotate == 180:
                            desmosshenanigans = ((((((xnum/windowres[0])))**sounddataspeed_intensity_quads)))-1
                            colordesmos = ((((xnum/windowres[0]))-1)**2)
                        if cl_rotate == 90 or cl_rotate == 270:
                            desmosshenanigans = 0-((((((xnum/windowres[0])-1))**sounddataspeed_intensity_quads)))-1
                            colordesmos = 1-((((xnum/windowres[0]))-1)**2)




            if sounddataspeednum != 0:
                if sounddataspeednum in range(1,3):
                    effectrange = ((((windowres[0])*64))*devisionby)
                if sounddataspeednum in range(3,5):
                    effectrange = ((((windowres[0])*64)*(sounddataspeed_intensity_quads-2))*devisionby)
                
                rendering_formulas = [
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                                                                        
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(0-(desmosshenanigans))))//devisionby),
                                        (int(lastsounddata+(effectrange*(  (desmosshenanigans))))//devisionby),
                                     ]

                if sounddata_fadeout:
                    colortransition = []
                    for i in linecolor:
                        colortransition.append(int(i/2)+int((i/2)*colordesmos))
                    colortransition = tuple(colortransition)
            

            linesrender_formula = rendering_formulas[cl_renderingmode_num]

                
            if linesrender_formula < 0:
                xnum += 1
                continue
            



            if wf_mono:
                if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    pygame.draw.line(surface,colortransition,
                             tuple(var(((int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength)))),
                             tuple(var(((int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))
                    pygame.draw.line(surface,colortransition,
                             tuple(var(((windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength)))),
                             tuple(var(((windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))
                        
                    xnum += 1

                    continue

                pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength)))),
                                 tuple(var(((int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))
                    
            else:
                if wf_split:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                        #1st channel
                        pygame.draw.line(surface,colortransition,
                                tuple(var(((int(xnum)//2,  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength))))),
                                tuple(var(((int(xnum)//2+1,((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                tuple(var(((windowres[0]-int(xnum)//2,  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength))))),
                                tuple(var(((windowres[0]-int(xnum)//2-1,((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))))
                                    
                        #2nd channel
                        pygame.draw.line(surface,colortransition,
                                tuple(var(((int(xnum)//2,  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength))))),
                                tuple(var(((int(xnum)//2+1,((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                tuple(var(((windowres[0]-int(xnum)//2,  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength))))),
                                tuple(var(((windowres[0]-int(xnum)//2-1,((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))))
                                    
                        xnum += 1

                        continue

                    pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength))))),
                                 tuple(var(((int(xnum+1),((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))))
                    pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength))))),
                                 tuple(var(((int(xnum+1),((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))))

                    pygame.draw.line(surface,windowbordercolor,(0,windowres[1]//2),(windowres[0],windowres[1]//2))

                elif wf_merge:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum)//2,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][prevlinesrender_formula][0]/32767)*cl_linelength))))),
                                 tuple(var(((int(xnum)//2,(windowres[1]/2)-(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((windowres[0]-int(xnum)//2,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula][0]/32767)*cl_linelength)))),
                                 tuple(var(((windowres[0]-int(xnum)//2,(windowres[1]/2)-(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)))))

                        xnum += 1

                        continue

                    pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula][0]/32767)*cl_linelength)))),
                                 tuple(var(((int(xnum),(windowres[1]/2)-(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)))))
                else:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        #1st channel
                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength))))),
                                 tuple(var(((int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength)))),
                                 tuple(var(((windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))
                                
                        #2nd channel
                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength))))),
                                 tuple(var(((int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))))
                        pygame.draw.line(surface,colortransition,
                                 tuple(var(((windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength)))),
                                 tuple(var(((windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)))))
                            
                        xnum += 1

                        continue

                    pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [0]/32767)*cl_linelength)))),
                                 tuple(var(((int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))))
                    pygame.draw.line(surface,colortransition,
                                 tuple(var(((int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][prevlinesrender_formula]  [1]/32767)*cl_linelength)))),
                                 tuple(var(((int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength)))))


            xnum += 1

        except IndexError:
            xnum += 1
        except ZeroDivisionError:
            xnum += 1

    if cl_rotate == 180 or cl_rotate == 90:
        surface = pygame.transform.rotozoom(surface,180,1)
        
    if cl_renderingmode_num < 4:
        pygame.draw.line(surface,windowbordercolor,tuple(var((((windowres[0]/2)-1,10)))),
                                           tuple(var((((windowres[0]/2)-1,windowres[1]-10)))))
        pygame.draw.line(surface,windowbordercolor,tuple(var((((windowres[0]/2),10)))),
                                           tuple(var((((windowres[0]/2),  windowres[1]-10)))))


    return surface



max_magnitude_strength = (2**16)

b_graphshow = False

def bars_renderer(windowres: tuple,
                  linecolor: tuple,

                  lastsounddata: int,

                  songsamplerate: float,

                  cl_onedimensional: bool,
                  cl_mirrored: bool,
                  cl_line_space: int,
                  cl_rotate: int,

                  cl_linelength: int,


                  b_renderingmode_num: int,

                  b_boostfreq: bool,
                  b_boostfreq_num: int, #index
                  b_boostfreq_graph: int, #index

                  b_boostfreq_intensity_quad: int, 
                  b_boostfreq_intensity_sqrt: int, 
                  b_boostfreq_mult: float,

                  b_adaptive_linelen: bool,
                  ):
    
    #i have no idea why the FUCK does it become weird with highload

    global b_graphshow

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)

    slightlygray_linecolor = []
    for i in range(3):
        slightlygray_linecolor.append(linecolor[i]//4)
    slightlygray_linecolor.append(linecolor[3])
    slightlygray_linecolor = tuple(slightlygray_linecolor)
    
    try:

        m_magnitude_strength = (2**16)

        chunk1ch = []
        chunk2ch = []
        num = int(windowres[0]*2)
        for i in range(num):
            chunk1ch.append(soundrawdata[int(i)+((lastsounddata))][0])
            chunk2ch.append(soundrawdata[int(i)+((lastsounddata))][1])
        bothch = [chunk1ch,chunk2ch]

        for ch in range(2):
            
            chunkdata = bytes(numpy.array(bothch[ch]))
            chunkdata = numpy.frombuffer(bytes(chunkdata), dtype=numpy.int16)
            fft_spectrum = numpy.fft.rfft(chunkdata)

            if ch == 0:
                frequencies = numpy.fft.rfftfreq(len(chunkdata), d=1/songsamplerate)
            magnitudes = numpy.abs(fft_spectrum)
            if b_adaptive_linelen:
                m_magnitude_strength = max(magnitudes)/num
                cl_linelength = 1
            if m_magnitude_strength == 0:
                m_magnitude_strength = (2**16)




            if b_renderingmode_num == 0 or b_renderingmode_num == 2:    
                magnitudes = magnitudes
            if b_renderingmode_num == 1 or b_renderingmode_num == 3:    
                magnitudes = numpy.flip(magnitudes)

            renderhowmanytimes = 1
            if b_renderingmode_num in range(2,4):
                renderhowmanytimes = 2



            for times in range(renderhowmanytimes):
                if b_renderingmode_num in range(2,4):
                    if times == 0:
                        magnitudes = magnitudes[::2]
                if times == 1:
                    magnitudes = numpy.flip(magnitudes)

                linespacenum = 0

                freqtomag_zip = zip(frequencies, magnitudes)
                for freq, mag in freqtomag_zip:
                    if cl_line_space != 0:
                        if linespacenum != 1+cl_line_space:
                            freq = 0.0
                            linespacenum = linespacenum % (1+cl_line_space)

                    if float(freq) != 0.0:
                        
                        if b_boostfreq:
                            

                            if b_boostfreq_num == 0:
                                if b_renderingmode_num == 1 or b_renderingmode_num == 3:
                                    xoffset = 1
                                else:
                                    xoffset = 0
                                    
                                if times == 1:
                                    if xoffset == 0:
                                        xoffset = 1
                                    elif xoffset == 1:
                                        xoffset = 0

                            if b_boostfreq_num == 1:
                                xoffset = 0.5
                            if b_boostfreq_num == 2:
                                if b_renderingmode_num == 1 or b_renderingmode_num == 3:
                                    xoffset = 0
                                else:
                                    xoffset = 1

                                if times == 1:
                                    if xoffset == 0:
                                        xoffset = 1
                                    elif xoffset == 1:
                                        xoffset = 0

                            x = (freq/frequencies[-1])
                            if b_renderingmode_num == 2 or b_renderingmode_num == 3:
                                x = ((freq*2)/frequencies[-1])

                            

                            if b_boostfreq_graph == 0: #straight
                                if xoffset == 0.5:
                                    graph = 1-abs(x-xoffset)*2*b_boostfreq_mult+(b_boostfreq_mult-1)
                                else:
                                    graph = abs(x-xoffset)*b_boostfreq_mult

                            if b_boostfreq_graph == 1: #quadratic
                                if xoffset == 0.5:
                                    graph = 1-abs(((x-xoffset)**(b_boostfreq_intensity_quad*2)))*b_boostfreq_mult*(2**(b_boostfreq_intensity_quad*2))+(b_boostfreq_mult-1)
                                else:
                                    graph = abs(((x-xoffset)**(b_boostfreq_intensity_quad*2)))*b_boostfreq_mult

                            if b_boostfreq_graph == 2: #sqrt
                                if xoffset == 0.5:
                                    graph = 1-(abs(x-xoffset)**abs(1-(b_boostfreq_intensity_sqrt/80)))*b_boostfreq_mult*(2**abs(1-(b_boostfreq_intensity_sqrt/80)))+(b_boostfreq_mult-1)
                                else:
                                    graph = (abs(x-xoffset)**abs(1-(b_boostfreq_intensity_sqrt/80)))*b_boostfreq_mult
                        

                        else:
                            graph = 0
                            

                        
                        #round func eats half of our fps
                        xrounded = (times*((windowres[0]//2)-1))+((((freq/frequencies[1])-cl_line_space)))
                        if xrounded - int(xrounded) >= 0.5:
                            xrounded = int(xrounded)+1
                        else:
                            xrounded = int(xrounded)

                        
                        if cl_onedimensional:
                            
                            if cl_mirrored:

                                if b_graphshow:
                                    if graph < 0:
                                        pygame.draw.line(surface,slightlygray_linecolor,(xrounded,(windowres[1]*(1+graph))*0.5),(xrounded,(windowres[1]*(1+graph))*0.5))
                                        pygame.draw.line(surface,slightlygray_linecolor,(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5),(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5))
                                                                    
                                    else:
                                        pygame.draw.line(surface,linecolor,(xrounded,(windowres[1]*(1+graph))*0.5),(xrounded,(windowres[1]*(1+graph))*0.5))
                                        pygame.draw.line(surface,linecolor,(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5),(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5))
                                

                                pygame.draw.line(surface,linecolor,(xrounded,windowres[1]//2-(((abs(mag)*(1+graph)))/((num*m_magnitude_strength)/(windowres[1])))*cl_linelength),
                                                                    (xrounded,windowres[1]//2))
                                pygame.draw.line(surface,linecolor,(xrounded,windowres[1]//2+(((abs(mag)*(1+graph)))/((num*m_magnitude_strength)/(windowres[1])))*cl_linelength),
                                                                                                    (xrounded,windowres[1]//2))
                            else:

                                if b_graphshow:
                                    if graph < 0:
                                        pygame.draw.line(surface,slightlygray_linecolor,(xrounded,(windowres[1]*(1-graph))),(xrounded,(windowres[1]*(1-graph))))
                                    else:
                                        pygame.draw.line(surface,linecolor,(xrounded,(windowres[1]*(1-graph))),(xrounded,(windowres[1]*(1-graph))))
                                


                                pygame.draw.line(surface,linecolor,(xrounded,(windowres[1]-(((abs(mag)*(1+graph)))/((num*m_magnitude_strength)/(windowres[1])))*cl_linelength)-1),
                                                                                                  (xrounded,windowres[1]-1))

                        else:
                            if b_graphshow:
                                if graph < 0:
                                    pygame.draw.line(surface,slightlygray_linecolor,(xrounded,(windowres[1]*(1+graph))*0.5),(xrounded,(windowres[1]*(1+graph))*0.5))
                                    pygame.draw.line(surface,slightlygray_linecolor,(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5),(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5))
                                    
                                else:
                                    pygame.draw.line(surface,linecolor,(xrounded,(windowres[1]*(1+graph))*0.5),(xrounded,(windowres[1]*(1+graph))*0.5))
                                    pygame.draw.line(surface,linecolor,(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5),(xrounded,windowres[1]-(windowres[1]*(1+graph))*0.5))

                            if ch == 0:
                                pygame.draw.line(surface,linecolor,(xrounded,windowres[1]//2-(((abs(mag)*(1+graph)))/((num*m_magnitude_strength)/(windowres[1])))*cl_linelength),
                                                                   (xrounded,windowres[1]//2))
                            if ch == 1:
                                pygame.draw.line(surface,linecolor,(xrounded,windowres[1]//2+(((abs(mag)*(1+graph)))/((num*m_magnitude_strength)/(windowres[1])))*cl_linelength),
                                                                   (xrounded,windowres[1]//2))

                    linespacenum += 1
                    
                if cl_onedimensional:
                    ch += 1

    except IndexError:
        pass

    return surface


def oscilloscope_renderer(windowres: tuple,
                          linecolor: tuple,

                          lastsounddata: int,

                          osc_linesperframe: int,
                          osc_fadeout: bool,

                          ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)

    tempnum = 0
    while tempnum < osc_linesperframe:

        if osc_fadeout:
            color = list(linecolor)
            color.pop(-1)
            color.append(int(tempnum/(osc_linesperframe/255)))
            color = tuple(color)

        else:
            color = linecolor

        pygame.draw.line(surface,color,
                         ((windowres[0]//2)+((windowres[0]//2)*(soundrawdata[lastsounddata+tempnum-osc_linesperframe][0]/32767))  ,(windowres[1]//2)+((windowres[1]//2)*(soundrawdata[lastsounddata+tempnum-osc_linesperframe][1]/32767))),
                         ((windowres[0]//2)+((windowres[0]//2)*(soundrawdata[lastsounddata+tempnum+1-osc_linesperframe][0]/32767)),(windowres[1]//2)+((windowres[1]//2)*(soundrawdata[lastsounddata+tempnum+1-osc_linesperframe][1]/32767))))
        
        tempnum += 1
    return surface





if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)