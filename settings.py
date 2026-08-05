import pygame
import os

def init(VER: str,):
    global VERSION
    VERSION = VER

scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep

icon_telegram =  pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Telegram.png'),(64,64))
icon_keyboard = pygame.transform.rotate(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Keyboard.png'),-15)

icon_brush = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'draw.png')
icon_visualizer = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'visualizer icon.png')
icon_songqueue =  pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'music.png')
icon_program = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'program.png')

icon_folder = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'folder icon.png')
icon_shuffle = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'shuffle.png')
icon_reverse = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'reverse.png')

icon_moveup = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'moveup icon.png')
icon_movedown = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'movedown icon.png')
icon_delete = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'delete icon.png')
icon_view = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'view file.png')

contacts = {
    'GitHub':   'https://github.com/JakeIsAlivee',
    'Telegram': 'https://t.me/JakeCreations',
}

icon_jakeisalivee = pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'JakeIsAlivee coffee cup.ico'),(64,64))







general_mode_names = {
    1: 'Classic',
    2: 'Waveform',
    3: 'Bars',
    4: 'Oscilloscope'
}

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


def surface_static_new_settings(windowres: tuple,
                                callable_font,
                                bgcolor: tuple,
                                textcolor: tuple,
                                windowbordercolor: tuple,

                                ):
    
    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    settings_text =       callable_font(32).render('Settings',False,textcolor)
    surface.blit(settings_text,      ((windowres[0]//2)-(settings_text.get_width()//2),2))

    slightlygraycolor = []
    for i in textcolor:
        slightlygraycolor.append(i//2)
    slightlygraycolor = tuple(slightlygraycolor)

    surface.blit(pygame.transform.invert(icon_keyboard),(0,36))
    controls_text = callable_font(24).render('Controls',False,textcolor)
    surface.blit(controls_text,(38,44))   
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,44),(152,44),
                                                      (152,68),(36,68),    (36,44)])

    
    
    surface.blit(pygame.transform.invert(icon_brush),(2,68))
    customize_text = callable_font(24).render('Customize',False,textcolor)
    surface.blit(customize_text,(38,76))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,76),  (166,76),
                                                       (166,100),(36,100),   (36,76)])

    surface.blit(icon_program,(2,104))
    program_text = callable_font(24).render('Program',False,textcolor)
    surface.blit(program_text,(38,107))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,108) ,(138,108),
                                                       (138,132),(36,132),        (36,108)
                                                       ])



    visualizer_text = callable_font(24).render('Visualizer',False,textcolor)
    surface.blit(icon_visualizer, (windowres[0]-4-visualizer_text.get_width()-2-icon_visualizer.get_width(),
                                       
                                       38))
    surface.blit(visualizer_text, (windowres[0]-4-visualizer_text.get_width(),
                                   
                                   44))
    pygame.draw.lines(surface,slightlygraycolor,False,[(windowres[0]-146,68),(windowres[0]-146,44),
                                                       (windowres[0]-2,44),(windowres[0]-2,68),   (windowres[0]-146,68)])

    

    songsqueue_text = callable_font(24).render('Song Queue',False,textcolor)
    surface.blit(icon_songqueue,(windowres[0]-36-songsqueue_text.get_width(),
                                     
                                     72))
    surface.blit(songsqueue_text, (windowres[0]-4-songsqueue_text.get_width(),
                                   
                                    74))
    pygame.draw.lines(surface,slightlygraycolor,False,[(windowres[0]-146,76),(windowres[0]-2,76),
                                                       (windowres[0]-2,100),(windowres[0]-146,100),   (windowres[0]-146,76)])



    
    surface.blit(pygame.transform.scale(icon_jakeisalivee,(64,64)), (windowres[0]-68,windowres[1]-76))
    surface.blit(pygame.transform.scale(icon_telegram,(64,64)),(windowres[0]-136,windowres[1]-76))
    version_text = callable_font(10).render('Version: '+VERSION,False,textcolor)
    surface.blit(version_text,(windowres[0]-5-version_text.get_width(),windowres[1]-11))


    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    del slightlygraycolor
    return surface





def surface_static_new_controls(windowres: tuple,
                                callable_font,
                                bgcolor: tuple,
                                textcolor: tuple,
                                windowbordercolor: tuple,

                                ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)


    
    buttons_text =       callable_font(32).render('Controls',False,textcolor)
    surface.blit(buttons_text,      ((windowres[0]//2)-(buttons_text.get_width()//2),2))
        
    t_transparent_text = callable_font(16).render('T: Transparent window switch',False,textcolor)
    surface.blit(t_transparent_text,((4),((2*2)+buttons_text.get_height())))

    o_ontop_text =       callable_font(16).render('O: Always on top window switch',False,textcolor)
    surface.blit(o_ontop_text,      ((4),((2*3)+buttons_text.get_height() +t_transparent_text.get_height())))

    uad_volup_text =        callable_font(16).render('Up/Down arrow: Volume control',False,textcolor)
    surface.blit(uad_volup_text,      ((4),((2*4)+buttons_text.get_height() +(t_transparent_text.get_height()*2))))

    ra_nextsong_text =   callable_font(16).render('Right/Left arrow: Next/Previous song',False,textcolor)
    surface.blit(ra_nextsong_text,   ((4),((2*5)+buttons_text.get_height() +(t_transparent_text.get_height()*3))))

    movewin_text =           callable_font(16).render('Move window: Hold LMB or RMB and drag',False,textcolor)
    surface.blit(movewin_text,      ((4),((2*6)+buttons_text.get_height() +(t_transparent_text.get_height()*4))))
    changeresolution1_text = callable_font(16).render('Change resolution: Hold RMB or LMB',False,textcolor)
    surface.blit(changeresolution1_text,      ((4),((2*7)+buttons_text.get_height() +(t_transparent_text.get_height()*5))))
    changeresolution2_text = callable_font(16).render('and scroll mouse wheel up or down',False,textcolor)
    surface.blit(changeresolution2_text,      ((4),((2*8)+buttons_text.get_height() +(t_transparent_text.get_height()*6))))


    c_close_text =       callable_font(16).render('C: Close the window',False,textcolor)
    surface.blit(c_close_text,      ((4),((2*9)+buttons_text.get_height() +(t_transparent_text.get_height()*7))))
    

    wherecontrolswork_text_r1 = callable_font(16).render('Most of the controls  ',False,textcolor)
    wherecontrolswork_text_r2 = callable_font(16).render('work in the visualizer',False,textcolor)
    surface.blit(wherecontrolswork_text_r1, (windowres[0]-wherecontrolswork_text_r1.get_width(),
                                                windowres[1]-wherecontrolswork_text_r1.get_height()*2))
    surface.blit(wherecontrolswork_text_r2, (windowres[0]-wherecontrolswork_text_r2.get_width(),
                                                windowres[1]-wherecontrolswork_text_r2.get_height()))
    
    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    return surface


def surface_static_new_customize(windowres: tuple,
                                 callable_font,
                                 bgcolor: tuple,
                                 textcolor: tuple,
                                 windowbordercolor: tuple,

                                ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    return surface

scrollwheely = 0

def surface_static_new_songqueue(windowres: tuple,
                                 callable_font,
                                 bgcolor: tuple,
                                 textcolor: tuple,

                                 windowbordercolor: tuple,
                                 songqueue: list,
                                 ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    songsrendernum = 1
    while songsrendernum <= len(songqueue):

        if (4*songsrendernum)+(28*songsrendernum)+4 < scrollwheely:
            songsrendernum += 1
            continue

        songdir = os.path.split(songqueue[songsrendernum-1].songdir)[1]
        if len(songdir) > ((windowres[0]-150)/18):
            songdir = songdir[0:((windowres[0]-150)//18)]+'...'
                

        songdir_text = callable_font(18).render(' '+str(songsrendernum)+'. "'+str(songdir)+'"',False,textcolor)

        surface.blit(songdir_text,(4,(4*songsrendernum)+(28*songsrendernum)+8-scrollwheely))
        pygame.draw.line(surface,windowbordercolor,(0,(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely),(windowres[0],(4*songsrendernum)+(28*songsrendernum)+4+28-scrollwheely))

        surface.blit(icon_view,(windowres[0]-28,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icon_delete,(windowres[0]-56,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icon_movedown,(windowres[0]-84,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))
        surface.blit(icon_moveup,(windowres[0]-112,(4*songsrendernum)+(28*songsrendernum)+4-scrollwheely))

        songsrendernum += 1
        
        if (4*songsrendernum)+(28*songsrendernum)+4-scrollwheely > windowres[1]:
            break

    addsong_text = callable_font(24).render('+',False,textcolor)
    surface.blit(addsong_text,(4,(4*songsrendernum)+(28*songsrendernum)+2-scrollwheely))

    songqueuebg = pygame.Surface((windowres[0],32))
    songqueuebg.fill(bgcolor)
    surface.blit(songqueuebg,(0,0))
    songsqueue_text = callable_font(24).render('Song queue',False,textcolor)
    surface.blit(songsqueue_text,(4,2))
    pygame.draw.line(surface,windowbordercolor,(0,4+songsqueue_text.get_height()),(windowres[0],4+songsqueue_text.get_height()))
    surface.blit(icon_folder,(windowres[0]-28,4))
    surface.blit(icon_shuffle,(windowres[0]-60,4))
    surface.blit(icon_reverse,(windowres[0]-92,4))
    
    escbg = pygame.Surface((windowres[0],28))
    escbg.fill(bgcolor)
    surface.blit(escbg,(0,windowres[1]-28))
    pygame.draw.line(surface, windowbordercolor,(0,windowres[1]-25),(windowres[0],windowres[1]-25))

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    return surface

devisionby = 1

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


osc_linesperframe = 1024
osc_fadeout = False

osc_linesperframe_typing = False
osc_linesperframe_typing_list = list(str(osc_linesperframe)+' ')



b_rendering_modes ={
    0: 'Low to High',
    1: 'High to Low',
    2: 'Low to High to Low',
    3: 'High to Low to High',
}
b_renderingmode_num = 0

"""
bars modes
1 - 0 range
0 - 1 range
1 - 0 - 1 range
0 - 1 - 0 range

"""



def surface_static_new_visualmodes(windowres: tuple,
                                   callable_font,
                                   bgcolor: tuple,
                                   textcolor: tuple,
                                   windowbordercolor: tuple,

                                   visualizergeneral_mode: int,
                                   ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)
    
    visualizer_text =       callable_font(32).render('Visualizer',False,textcolor)
    surface.blit(visualizer_text,      ((windowres[0]//2)-(visualizer_text.get_width()//2),2))
    
    generalmodes_text = callable_font(26).render('Mode: <> "'+str(general_mode_names[visualizergeneral_mode])+'"',False,textcolor)
    surface.blit(generalmodes_text, (4,34))

    slightlygreycolor = []
    for i in textcolor:
        slightlygreycolor.append(i//2)
    slightlygreycolor = tuple(slightlygreycolor)

    match visualizergeneral_mode:
        case 1:
        
            cl_setting = callable_font(16).render('Classic settings:',False,textcolor)
            surface.blit(cl_setting,(4,70))

            cl_mode_text = callable_font(12).render('Modes: < "'+str(cl_rendering_modes[cl_renderingmode_num])+'" >',False,textcolor)
            surface.blit(cl_mode_text, (4,86))

            cl_zoom_typing_str = ''
            for i in cl_zoom_typing_list:
                cl_zoom_typing_str += str(i)

            cl_zoom_text = callable_font(12).render('Zoom out by: x'+cl_zoom_typing_str,False,textcolor) #user should type numbers here
            surface.blit(cl_zoom_text, (4,98))

            cl_line_space_typing_str = ''
            for i in cl_line_space_typing_list:
                cl_line_space_typing_str += str(i)

            cl_space_between_lines_text = callable_font(12).render('Pixels between lines: '+cl_line_space_typing_str,False,textcolor)
            surface.blit(cl_space_between_lines_text,(4,110))
    
            cl_onedimensional_text = callable_font(12).render('One dimensional: ',False,textcolor)
            surface.blit(cl_onedimensional_text,(4,122))
            pygame.draw.lines(surface,textcolor,False,[(120,123),(130,123),
                                                                     (130,133),(120,133),
                                                                     (120,123)])
            if cl_onedimensional:
                pygame.draw.line(surface,textcolor,(120,123),(130,133))
                pygame.draw.line(surface,textcolor,(130,123),(120,133))
    
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,textcolor)
                surface.blit(cl_mirrored_text,(4,134))
                pygame.draw.lines(surface,textcolor,False,[(70,135),(80,135),
                                                           (80,145),(70,145),
                                                           (70,135)])
                if cl_mirrored:
                    pygame.draw.line(surface,textcolor,(70,135),(80,145))
                    pygame.draw.line(surface,textcolor,(80,135),(70,145))
            else:
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,slightlygreycolor)
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

            cl_rotate_text = callable_font(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,textcolor)
            surface.blit(cl_rotate_text,(4,146))


            cl_linelength_typing_str = ''
            for i in cl_linelength_typing_list:
                cl_linelength_typing_str += str(i)

            cl_linelength_text = callable_font(12).render('Line length multiplier: '+cl_linelength_typing_str,False,textcolor)
            surface.blit(cl_linelength_text,(4,158))
    


        case 2:
            wf_setting = callable_font(16).render('Waveform settings:',False,textcolor)
            surface.blit(wf_setting,(4,70))

            cl_mode_text = callable_font(12).render('Modes: < "'+str(cl_rendering_modes[cl_renderingmode_num])+'" >',False,textcolor)
            surface.blit(cl_mode_text, (4,86))

            cl_zoom_typing_str = ''
            for i in cl_zoom_typing_list:
                cl_zoom_typing_str += str(i)

            cl_zoom_text = callable_font(12).render('Zoom out by: x'+cl_zoom_typing_str,False,textcolor) #user should type numbers here
            surface.blit(cl_zoom_text, (4,98))

            wf_mono_text = callable_font(12).render('Mono: ',False,textcolor)
            surface.blit(wf_mono_text, (4,110))
            pygame.draw.lines(surface,textcolor,False,[(41,112),(51,112),
                                                                     (51,122),(41,122),
                                                                     (41,112)])
            if wf_mono:
                pygame.draw.line(surface,textcolor,(41,112),(51,122))
                pygame.draw.line(surface,textcolor,(51,112),(41,122))



                wf_merge_text = callable_font(12).render('Merge: ',False,slightlygreycolor)
                surface.blit(wf_merge_text,(4,122))

                pygame.draw.lines(surface,slightlygreycolor,False,[(48,125),(58,125),
                                                                         (58,135),(48,135),
                                                                         (48,125)])
                if wf_merge:
                    pygame.draw.line(surface,slightlygreycolor,(48,125),(58,135))
                    pygame.draw.line(surface,slightlygreycolor,(58,125),(48,135))


                wf_split_text = callable_font(12).render('Split: ',False,slightlygreycolor)
                surface.blit(wf_split_text,(4,134))

                pygame.draw.lines(surface,slightlygreycolor,False,[(48,135),(58,135),
                                                                         (58,145),(48,145),
                                                                         (48,135)])
                if wf_split:
                    pygame.draw.line(surface,slightlygreycolor,(48,135),(58,145))
                    pygame.draw.line(surface,slightlygreycolor,(58,135),(48,145))
            else:

                wf_merge_text = callable_font(12).render('Merge: ',False,textcolor)
                surface.blit(wf_merge_text,(4,122))

                pygame.draw.lines(surface,textcolor,False,[(48,125),(58,125),
                                                           (58,135),(48,135),
                                                           (48,125)])
                if wf_merge:
                    pygame.draw.line(surface,textcolor,(48,125),(58,135))
                    pygame.draw.line(surface,textcolor,(58,125),(48,135))


                wf_split_text = callable_font(12).render('Split: ',False,textcolor)
                surface.blit(wf_split_text,(4,134))

                pygame.draw.lines(surface,textcolor,False,[(48,135),(58,135),
                                                               (58,145),(48,145),
                                                               (48,135)])
                if wf_split:
                    pygame.draw.line(surface,textcolor,(48,135),(58,145))
                    pygame.draw.line(surface,textcolor,(58,135),(48,145))



            cl_rotate_typing_str = ''
            for i in cl_rotate_typing_list:
                cl_rotate_typing_str += str(i)
            cl_rotate_text = callable_font(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,slightlygreycolor) #do later
            surface.blit(cl_rotate_text,(4,146))
        
        

        case 3:
            br_setting = callable_font(16).render('Bars settings:',False,textcolor)
            surface.blit(br_setting,(4,70))



        case 4:
            osc_setting = callable_font(16).render('Oscilloscope settings:',False,textcolor)
            surface.blit(osc_setting,(4,70))

            osc_linesperframe_typing_str = ''
            for i in osc_linesperframe_typing_list:
                osc_linesperframe_typing_str += str(i)
            osc_linesperframe_text = callable_font(12).render('Lines per frame: '+osc_linesperframe_typing_str,False,textcolor)
            surface.blit(osc_linesperframe_text,(4,86))

            osc_fadeout_text = callable_font(12).render('Fadeout: ',False,textcolor)
            surface.blit(osc_fadeout_text,(4,98))

            pygame.draw.lines(surface,textcolor,False,[(63,99),(73,99),
                                                                     (73,109),(63,109),
                                                                     (63,99)])
            if osc_fadeout:
                pygame.draw.line(surface,textcolor,(63,99),(73,109))
                pygame.draw.line(surface,textcolor,(73,99),(63,109))





    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    del slightlygreycolor
    return surface

pr_bluetooth_output_device = False
def surface_static_new_program(windowres: tuple,
                               callable_font,
                               bgcolor: tuple,
                               textcolor: tuple,
                               windowbordercolor: tuple,

                               fpscap: int
                               ):
    

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    program_text = callable_font(32).render('Program',False,textcolor)
    surface.blit(program_text,((windowres[0]//2)-(program_text.get_width()//2),2))

    if fpscap == 0:
        fpscapstr = 'Unlimited'
    else:
        fpscapstr = str(fpscap)
    fps_text = callable_font(16).render('Fps cap: <> '+fpscapstr,False,textcolor)
    surface.blit(fps_text,(4,34))
    bluetooth_latencyfix_text = callable_font(16).render('Bluetooth latency fix: ',False,textcolor)
    surface.blit(bluetooth_latencyfix_text,(4,50))
    pygame.draw.lines(surface,textcolor,False,[(228,51),(242,51),
                                                             (242,65),(228,65),
                                                             (228,51)])
    if pr_bluetooth_output_device:
        pygame.draw.line(surface,textcolor,(228,51),(242,65))
        pygame.draw.line(surface,textcolor,(242,51),(228,65))

    credits_text = callable_font(12).render('Credits',False,textcolor)
    surface.blit(credits_text,(windowres[0]-credits_text.get_width()-5,windowres[1]-76-12))

    surface.blit(pygame.transform.scale(icon_jakeisalivee,(64,64)), (windowres[0]-68,windowres[1]-76))
    surface.blit(pygame.transform.scale(icon_jakeisalivee,(64,64)),(windowres[0]-136,windowres[1]-76))
    version_text = callable_font(10).render('Version: '+VERSION,False,textcolor)
    surface.blit(version_text,(windowres[0]-5-version_text.get_width(),windowres[1]-11))

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    return surface

def surface_static_new_credits(windowres: tuple,
                               callable_font,
                               bgcolor: tuple,
                               textcolor: tuple,

                               windowbordercolor: tuple,

                               ):
    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    jakeisalivee_text = callable_font(12).render('JakeIsAlivee',False,textcolor)
    mylove_text = callable_font(14).render('M y   L o v e .',False,textcolor)

    code_text = callable_font(16).render('Code',False,textcolor)
    surface.blit(code_text,(windowres[0]//2-code_text.get_width()//2,2))
    surface.blit(jakeisalivee_text,(windowres[0]//2-jakeisalivee_text.get_width()//2,18))

    icons_text = callable_font(16).render('Icons',False,textcolor)
    surface.blit(icons_text,(windowres[0]//2-icons_text.get_width()//2,34))
    surface.blit(jakeisalivee_text,(windowres[0]//2-jakeisalivee_text.get_width()//2,50))

    animations_text = callable_font(16).render('Animations',False,textcolor)
    surface.blit(animations_text,(windowres[0]//2-animations_text.get_width()//2,66))
    surface.blit(jakeisalivee_text,(windowres[0]//2-jakeisalivee_text.get_width()//2,82))

    specialthanks_text = callable_font(16).render('Special Thanks',False,textcolor)
    surface.blit(specialthanks_text,(windowres[0]//2-specialthanks_text.get_width()//2,
                                     windowres[1]-44))
    surface.blit(mylove_text,(windowres[0]//2-mylove_text.get_width()//2,
                              windowres[1]-28))
    you_text = callable_font(12).render('You',False,textcolor)
    surface.blit(you_text,(windowres[0]//2-you_text.get_width()//2,
                           windowres[1]-14))

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    return surface


def surface_static_settings_decorator(windowres: tuple,
                                      callable_font,
                                      windowbordercolor: tuple,
                                      textcolor: tuple,

                                      ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    
    esc_back_text =      callable_font(16).render('Esc: Back',False,textcolor)
    surface.blit(esc_back_text,     ((4),(windowres[1]-2-esc_back_text.get_height())))

    pygame.draw.lines(surface,windowbordercolor,False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)])

    return surface






#only for reusability, we use this so much
class typing:

    def cancel_clzoom():
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
            if devisionby == 0:
                devisionby = 1
        except ValueError:
            devisionby = 1
        cl_zoom_typing_list = list(str(devisionby)+' ')

    def cancel_cllinespace():
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
        except ValueError:
            cl_line_space = 0
        cl_line_space_typing_list = list(str(cl_line_space)+' ')

    def cancel_clrotate():
        global cl_rotate_typing
        global cl_rotate_typing_list
        global cl_rotate

        cl_rotate_typing_list[-1] = ' '

        cl_rotate_typing = False
        cl_rotate_typing_str = ''
        for i in cl_rotate_typing_list:
            cl_rotate_typing_str += str(i)

        try: 
            match int(cl_rotate_typing_str.replace('°', '')):
                case range(0,45):
                    cl_rotate_typing_str = '0° '
                case range(45,90):
                    cl_rotate_typing_str = '90° '
                case range(90,135):
                    cl_rotate_typing_str = '90° '
                case range(135,180):
                    cl_rotate_typing_str = '180° '
                case range(180,225):
                    cl_rotate_typing_str = '180° '
                case range(225,270):
                    cl_rotate_typing_str = '270° '
                case range(270,1000):
                    cl_rotate_typing_str = '270° '
        
            cl_rotate = int(cl_rotate_typing_str.replace('°', ''))
        except ValueError:
            cl_rotate = 0
        cl_rotate_typing_list = list(str(cl_rotate)+'° ')

    def cancel_cllinelength():
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
        except ValueError:
            cl_linelength = 1.0
        cl_linelength_typing_list = list(str(cl_linelength)+' ')

    def cancel_osclinesperframe():
        global osc_linesperframe_typing
        global osc_linesperframe_typing_list
        global osc_linesperframe
        
        osc_linesperframe_typing_list[-1] = ' '

        osc_linesperframe_typing = False
        osc_linesperframe_typing_str = ''
        for i in osc_linesperframe_typing_list:
            osc_linesperframe_typing_str += str(i)
        
        try:
            osc_linesperframe = int(osc_linesperframe_typing_str)
        except ValueError:
            osc_linesperframe = 1024
        osc_linesperframe_typing_list = list(str(osc_linesperframe)+' ')

    









if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)