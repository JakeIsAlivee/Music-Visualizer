import pygame
import time
import os


anim_transparency = 0
anim_ontop = 0

anim_volume = 0

anim_song = 0

anim_nowplaying = 0


def surface_static_new_visualizer(windowres: tuple,
                                  callable_font,
                                  bgcolor: tuple,
                                  windowbordercolor: tuple,

                                  transparent: bool,
                                  transparencycolor: tuple, #with alpha channel
                                  visualizergeneral_mode: int,
                                  programnotifscolor: tuple,
                                  songplaying: bool,
                                  musicvolume_percent: int,
                                  songnum: int,
                                  songqueue: list,

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
                                  ):

    curtime = time.perf_counter()

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    if transparent == False:
        surface.fill(bgcolor)
    if transparent == True:
        surface.fill(transparencycolor)

    if visualizergeneral_mode == 1:
        surface.blit(classic_renderer(windowres,
                                      linecolor,

                                      lastsounddata,
                                      devisionby,

                                      cl_line_space,
                                      cl_linelength,
                                      cl_renderingmode_num,

                                      cl_onedimensional,
                                      cl_mirrored,
                                      ))

    if visualizergeneral_mode == 2:
        surface.blit(waveform_renderer(windowres,
                                       linecolor,
                                       windowbordercolor,

                                       lastsounddata,
                                       devisionby,

                                       cl_renderingmode_num,

                                       wf_mono,
                                       wf_merge,
                                       wf_split,
                                       ))
    if visualizergeneral_mode == 3:
        surface.blit(bars_renderer(windowres,
                                   linecolor,
                                   ))
    if visualizergeneral_mode == 4:
        surface.blit(oscilloscope_renderer(windowres,
                                           linecolor,

                                           lastsounddata,

                                           osc_linesperframe,
                                           osc_fadeout,
                                           ))
    
        
    

    if anim_nowplaying+3 > curtime:
        #really big fps drops
        #should optimize this later
        songname = os.path.splitext(os.path.split(songqueue[songnum].songdir)[1])[0]
        fontsize = 16

        
        nowplayingstr = 'Now playing: "'+songname+'"'
        nowplaying_text = callable_font(fontsize).render(nowplayingstr,False,programnotifscolor)

        pixelspersymbol = nowplaying_text.get_width()/len(nowplayingstr)
        sizemult = (len(nowplayingstr)*(pixelspersymbol))/(len(nowplayingstr)*fontsize)

        while len(nowplayingstr)*fontsize*sizemult > windowres[0] and fontsize != 1:
            fontsize -= 1

        nowplaying_text = callable_font(fontsize-1).render(nowplayingstr,False,programnotifscolor)


        nowplaying_surfacexy = [nowplaying_text.get_width()+4,nowplaying_text.get_height()+4]
        nowplaying_surface = pygame.Surface((nowplaying_surfacexy[0],nowplaying_surfacexy[1]))
        if transparent:
            nowplaying_surface.fill(transparencycolor)
        else:
            nowplaying_surface.fill(bgcolor)
        nowplaying_surface.blit(nowplaying_text, (2,2))
        pygame.draw.lines(nowplaying_surface,(0,0,255),False,
                          [(0,0),(nowplaying_surfacexy[0]-1,0),
                           (nowplaying_surfacexy[0]-1,nowplaying_surfacexy[1]-1),(0,nowplaying_surfacexy[1]-1),
                           (0,0)])
        
        #this was hell
        match int(((anim_nowplaying+3)-curtime)*1000):
            case range(2500,3000): #roll out animation
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

            case range(500,2500): #staying still
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
                
            case range(0,500): #roll in animation
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
                
    surface = pygame.transform.rotate(surface,cl_rotate)

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

    if songplaying == False:
        pygame.draw.line(surface,programnotifscolor,((windowres[0]/2)-(windowres[0]/12),(windowres[1]/2)+(windowres[1]/3)),((windowres[0]/2)-(windowres[0]/12),(windowres[1]/2)-(windowres[1]/3)),10)
        pygame.draw.line(surface,programnotifscolor,((windowres[0]/2)+(windowres[0]/12),(windowres[1]/2)+(windowres[1]/3)),((windowres[0]/2)+(windowres[0]/12),(windowres[1]/2)-(windowres[1]/3)),10)

    pygame.draw.lines(surface,(0,0,255,255),False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)])

    
    return surface


#im so fucking braindead i cant
soundrawdata = None
def classic_renderer(windowres: tuple,
                     linecolor: tuple,

                     lastsounddata: int,
                     devisionby: int,

                     cl_line_space: int,
                     cl_linelength: int,
                     cl_renderingmode_num: int,

                     cl_onedimensional: bool,
                     cl_mirrored: bool,
                     
                     ):


    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)

    

    #if else hell but works pretty fineee, no masive fps drops

    #if cl_rotate == 0 or cl_rotate == 180:
    xnum = cl_line_space

    while xnum < windowres[0]:
        try:
            rendering_formulas = [
              int(xnum)-(windowres[0]//2)+((lastsounddata)//devisionby),
            0-int(xnum)+(windowres[0]//2)+((lastsounddata)//devisionby),
            0-int(xnum//2)+(windowres[0]//2)+   ((lastsounddata)//devisionby),
              int(xnum//2)-(windowres[0]//2)+   ((lastsounddata)//devisionby),
              int(xnum)+                   ((lastsounddata)//devisionby),
            0-int(xnum)+                   ((lastsounddata)//devisionby),
            0-int(xnum)+(windowres[0])+   ((lastsounddata)//devisionby),
              int(xnum)-(windowres[0])+   ((lastsounddata)//devisionby),
            ]

            linesrender_formula = rendering_formulas[cl_renderingmode_num]
               
            if linesrender_formula < 0:
                xnum = xnum+1+cl_line_space
                continue
            



            if cl_onedimensional:
                if cl_mirrored:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                 (int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                 (windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                        xnum = xnum+1+cl_line_space
                                
                        continue


                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                 (int(xnum),(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                else:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,(windowres[1]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))),
                                 (int(xnum)//2,windowres[1])) 
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,(windowres[1])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                 (windowres[0]-int(xnum)//2,windowres[1]))

                        xnum = xnum+1+cl_line_space
                        continue

                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),windowres[1]-(windowres[1]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))),
                                 (int(xnum),windowres[1]))



            else:
                if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    pygame.draw.line(surface,linecolor,
                             (int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength))),
                             (int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                    pygame.draw.line(surface,linecolor,
                             (windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))),
                             (windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))))
                        
                    xnum = xnum+1+cl_line_space

                    continue


                pygame.draw.line(surface,linecolor,
                                 (int(xnum),(windowres[1]//2)+(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)),
                                 (int(xnum),(windowres[1]//2)-(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))
                

                """if cl_rotate == 180:
                    if cl_onedimensional:
                        if cl_mirrored:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,linecolor,
                                         (windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))
                                pygame.draw.line(surface,linecolor,
                                         (int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                                xnum = xnum+1+cl_line_space

                                continue


                            pygame.draw.line(surface,linecolor,
                                         (windowres[0]-int(xnum),(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (windowres[0]-int(xnum),(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))))

                        else:
                            if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                                pygame.draw.line(surface,linecolor,
                                         (windowres[0]-int(xnum)//2,(windowres[1]*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)))),
                                         (windowres[0]-int(xnum)//2,0)) 
                                pygame.draw.line(surface,linecolor,
                                         (int(xnum)//2,(windowres[1])*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                         (int(xnum)//2,0))

                                xnum = xnum+1+cl_line_space
                                continue

                            pygame.draw.line(surface,linecolor,
                                         (windowres[0]-int(xnum),0+(windowres[1]*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength)))),
                                         (windowres[0]-int(xnum),0))



                    else:
                        if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                            pygame.draw.line(surface,linecolor,
                                     (windowres[0]-int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength))),
                                     (windowres[0]-int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength))))
                            pygame.draw.line(surface,linecolor,
                                     (int(xnum)//2,(windowres[1]//2)+(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][0]/32767)*cl_linelength))),
                                     (int(xnum)//2,(windowres[1]//2)-(windowres[1]//2)*(abs((soundrawdata[::devisionby][linesrender_formula][1]/32767)*cl_linelength))))
                        
                            xnum = xnum+1+cl_line_space

                            continue


                        pygame.draw.line(surface,linecolor,
                                         (windowres[0]-int(xnum),(windowres[1]//2)+(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][0])/32767)*cl_linelength)),
                                         (windowres[0]-int(xnum),(windowres[1]//2)-(windowres[1]//2)*abs(((soundrawdata[::devisionby][linesrender_formula][1])/32767)*cl_linelength)))
                """


            xnum = xnum+1+cl_line_space

        except IndexError:
            xnum = xnum+1+cl_line_space

        
        if cl_renderingmode_num < 4:
            pygame.draw.line(surface,(0,0,128),((windowres[0]/2)-1,10),((windowres[0]/2)-1,windowres[1]-10))
            pygame.draw.line(surface,(0,0,128),((windowres[0]/2),10)  ,((windowres[0]/2),  windowres[1]-10))
    

    """if cl_rotate == 90 or cl_rotate == 270:
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
                             (10,(windowres[1]/2)-1),
                             (windowres[0]-10,(windowres[1]/2)-1))
            pygame.draw.line(surface,(0,0,128),
                             (10,(windowres[1]/2))  ,
                             (windowres[0]-10,(windowres[1]/2)  ))"""

    
    return surface


#waveform drops the fps MASSIVELY rn
def waveform_renderer(windowres: tuple,
                      linecolor: tuple,
                      windowbordercolor: tuple,

                      lastsounddata: int,
                      devisionby: int,

                      cl_renderingmode_num: int,

                      wf_mono: bool,
                      wf_merge: bool,
                      wf_split: bool,
                      ):


    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)

    xnum = 0

    while xnum < windowres[0]:
        try:
            rendering_formulas = [
              int(xnum)-(windowres[0]//2)+((lastsounddata)//devisionby),
            0-int(xnum)+(windowres[0]//2)+((lastsounddata)//devisionby),
            0-int(xnum//2)+(windowres[0]//2)+   ((lastsounddata)//devisionby),
              int(xnum//2)-(windowres[0]//2)+   ((lastsounddata)//devisionby),
              int(xnum)+                   ((lastsounddata)//devisionby),
            0-int(xnum)+                   ((lastsounddata)//devisionby),
            0-int(xnum)+(windowres[0])+   ((lastsounddata)//devisionby),
              int(xnum)-(windowres[0])+   ((lastsounddata)//devisionby),
            ]

            linesrender_formula = rendering_formulas[cl_renderingmode_num]
                
            if cl_renderingmode_num in range(1,3) or cl_renderingmode_num in range(5,7):
                formula_num = -1
            else:
                formula_num = 1

            if linesrender_formula < 0:
                xnum += 1
                continue
            



            if wf_mono:
                if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                    pygame.draw.line(surface,linecolor,
                             (int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                             (int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                    pygame.draw.line(surface,linecolor,
                             (windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                             (windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                        
                    xnum += 1

                    continue

                pygame.draw.line(surface,linecolor,
                                 (int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767),
                                 (int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767))
                    
            else:
                if wf_split:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        #1st channel
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767))),
                                 (int(xnum)//2+1,((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767))))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767))),
                                 (windowres[0]-int(xnum)//2-1,((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767))))
                                
                        #2nd channel
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767))),
                                 (int(xnum)//2+1,((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767))))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767))),
                                 (windowres[0]-int(xnum)//2-1,((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767))))
                                
                        xnum += 1

                        continue

                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),  ((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [1])/32767)),
                                 (int(xnum+1),((windowres[1]/2)+(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767)))
                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),  ((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767)),
                                 (int(xnum+1),((windowres[1]/2)-(windowres[1]/2/2))+((windowres[1]/2/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767)))

                    pygame.draw.line(surface,windowbordercolor,(0,windowres[1]//2),(windowres[0],windowres[1]//2))

                elif wf_merge:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly

                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][0])/32767)),
                                 (int(xnum)//2,(windowres[1]/2)-(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula][1])/32767)))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)),
                                 (windowres[0]-int(xnum)//2,(windowres[1]/2)-(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)))

                        xnum += 1

                        continue

                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][0]/32767)),
                                 (int(xnum),(windowres[1]/2)-(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula][1]/32767)))
                else:
                    if cl_renderingmode_num == 2 or cl_renderingmode_num == 3: #mirroring the wave in the middle of the screen #causes to drop half of the fps sadly
                        #1st channel
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula]  [0])/32767)),
                                 (int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767)))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0]/32767)),
                                 (windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0]/32767)))
                                
                        #2nd channel
                        pygame.draw.line(surface,linecolor,
                                 (int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula]  [1])/32767)),
                                 (int(xnum)//2+1,(windowres[1]/2)+(windowres[1]/2)*((soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767)))
                        pygame.draw.line(surface,linecolor,
                                 (windowres[0]-int(xnum)//2,  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [1]/32767)),
                                 (windowres[0]-int(xnum)//2-1,(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1]/32767)))
                            
                        xnum += 1

                        continue

                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [0])/32767),
                                 (int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][0])/32767))
                    pygame.draw.line(surface,linecolor,
                                 (int(xnum),  (windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula]  [1])/32767),
                                 (int(xnum+1),(windowres[1]/2)+(windowres[1]/2)*(soundrawdata[::devisionby][linesrender_formula+formula_num][1])/32767))


            xnum += 1

        except IndexError:
            xnum += 1

        
    if cl_renderingmode_num < 4:
        pygame.draw.line(surface,(0,0,128),((windowres[0]/2)-1,10),((windowres[0]/2)-1,windowres[1]-10))
        pygame.draw.line(surface,(0,0,128),((windowres[0]/2),10)  ,((windowres[0]/2),  windowres[1]-10))


    return surface


def bars_renderer(windowres: tuple,
                  linecolor: tuple,):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)

    #do that later

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






gpu_threadsperblock = 32
gpu_blockspergrid = 512



if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)