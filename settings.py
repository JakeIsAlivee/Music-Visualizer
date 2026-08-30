import pygame
import os

from functools import lru_cache

def init(VER: str,jia_icon_surface):
    global VERSION
    global icon_jakeisalivee
    VERSION = VER
    icon_jakeisalivee = jia_icon_surface



scriptdirfolder = os.path.dirname(os.path.realpath(__file__))
slash = os.sep


icon_telegram =  pygame.transform.scale(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Telegram.png'),(64,64))

icon_keyboard = pygame.transform.rotate(pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'Keyboard.png'),-15)

icon_brush = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'draw.png')
icon_visualizer = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'visualizer icon.png')
icon_songqueue =  pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'music.png')
icon_program = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'program.png')

icon_folder = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'folder icon.png')
icon_shuffle = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'shuffle.png')
icon_reverse = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'reverse.png')

icon_moveup = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'moveup icon.png')
icon_movedown = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'movedown icon.png')
icon_delete = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'delete icon.png')
icon_view = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'songqueue'+slash+'view file.png')

contacts = {
    'GitHub':   'https://github.com/JakeIsAlivee',
    'Telegram': 'https://t.me/JakeCreations',
    'Tiktok': 'https://www.tiktok.com/@jake0078700',
    'Itch.io': 'https://jakeisalivee.itch.io/',
    'Twitter': 'https://x.com/JakeIsAlivee',
    'Donations': 'https://dalink.to/jakeisalivee',
    'Youtube': 'https://www.youtube.com/@Jake07870',
    'Twitch': 'https://www.twitch.tv/jakeisaliveerrr',
    'Steam': 'https://steamcommunity.com/id/JakeIsAlivee/',
    'Osu': 'https://osu.ppy.sh/users/21369159',
}





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


@lru_cache(1)
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
    for i in range(3):
        slightlygraycolor.append(textcolor[i]//2)
    slightlygraycolor.append(textcolor[3])
    slightlygraycolor = tuple(slightlygraycolor)

    controls_text = callable_font(24).render('Controls',False,textcolor)
    surface.blit(pygame.transform.invert(icon_keyboard),(0,36))
    surface.blit(controls_text,(38,44))   
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,44),(36+controls_text.get_width()+4,44),
                                                       (36+controls_text.get_width()+4,68),(36,68),
                                                       (36,44)])
    
    
    surface.blit(pygame.transform.invert(icon_brush),(2,68))
    customize_text = callable_font(24).render('Customize',False,textcolor)
    surface.blit(customize_text,(38,76))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,76),  (36+customize_text.get_width()+4,76),
                                                       (36+customize_text.get_width()+4,100),(36,100),
                                                       (36,76)])

    surface.blit(icon_program,(2,104))
    program_text = callable_font(24).render('Program',False,textcolor)
    surface.blit(program_text,(38,107))
    pygame.draw.lines(surface,slightlygraycolor,False,[(36,108) ,(36+program_text.get_width()+4,108),
                                                       (36+program_text.get_width()+4,132),(36,132), 
                                                       (36,108)
                                                       ])



    visualizer_text = callable_font(24).render('Visualizer',False,textcolor)
    surface.blit(icon_visualizer, (windowres[0]-4-visualizer_text.get_width()-2-icon_visualizer.get_width(),
                                       
                                       38))
    surface.blit(visualizer_text, (windowres[0]-4-visualizer_text.get_width(),
                                   
                                   44))
    pygame.draw.lines(surface,slightlygraycolor,False,[(windowres[0]-(2+visualizer_text.get_width()+4),68),(windowres[0]-(2+visualizer_text.get_width()+4),44),
                                                       (windowres[0]-2,44),(windowres[0]-2,68),   (windowres[0]-(2+visualizer_text.get_width()+4),68)])

    

    songsqueue_text = callable_font(24).render('Song Queue',False,textcolor)
    surface.blit(icon_songqueue,(windowres[0]-36-songsqueue_text.get_width(),
                                     
                                     72))
    surface.blit(songsqueue_text, (windowres[0]-4-songsqueue_text.get_width(),
                                   
                                    74))
    pygame.draw.lines(surface,slightlygraycolor,False,[(windowres[0]-(2+songsqueue_text.get_width()+4),76),(windowres[0]-2,76),
                                                       (windowres[0]-2,100),(windowres[0]-(2+songsqueue_text.get_width()+4),100),   (windowres[0]-(2+songsqueue_text.get_width()+4),76)])



    
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




@lru_cache(1)
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

    fontsize = 12
    
    t_transparent_text = callable_font(fontsize).render('T: Transparent window switch',False,textcolor)
    surface.blit(t_transparent_text,((4),((1*(fontsize+1))+buttons_text.get_height())))

    o_ontop_text =       callable_font(fontsize).render('O: Always on top window switch',False,textcolor)
    surface.blit(o_ontop_text,      ((4),((2*(fontsize+1))+buttons_text.get_height())))

    uad_volup_text =        callable_font(fontsize).render('Up/Down arrow: Volume control',False,textcolor)
    surface.blit(uad_volup_text,      ((4),((3*(fontsize+1))+buttons_text.get_height())))

    ra_nextsong_text =   callable_font(fontsize).render('Right/Left arrow: Next/Previous song',False,textcolor)
    surface.blit(ra_nextsong_text,   ((4),((4*(fontsize+1))+buttons_text.get_height())))

    movewin_text =           callable_font(fontsize).render('Move window: Hold any mouse button and drag',False,textcolor)
    surface.blit(movewin_text,      ((4),((5*(fontsize+1))+buttons_text.get_height())))

    r_random_text =       callable_font(fontsize).render('R: Load random song',False,textcolor)
    surface.blit(r_random_text,      ((4),((6*(fontsize+1))+buttons_text.get_height()))) 
    

    c_close_text =       callable_font(fontsize).render('C/Del: Close the window',False,textcolor)
    surface.blit(c_close_text,      ((4),((7*(fontsize+1))+buttons_text.get_height()))) 

    changeresolution1_text = callable_font(fontsize).render('Change resolution: Hold RMB or LMB',False,textcolor)
    surface.blit(changeresolution1_text,      ((windowres[0]//2)+(4),((1*(fontsize+1))+buttons_text.get_height())))
    changeresolution2_text = callable_font(fontsize).render('and scroll mouse wheel up or down',False,textcolor)
    surface.blit(changeresolution2_text,      ((windowres[0]//2)+(4),((2*(fontsize+1))+buttons_text.get_height())))

    songrewinging_text = callable_font(fontsize).render('Shift+Right/Left arrow: song rewinding',False,textcolor)
    surface.blit(songrewinging_text,      ((windowres[0]//2)+(4),((3*(fontsize+1))+buttons_text.get_height())))

    

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    return surface

color_num = 0 #dict index

colors_RGBA_typing = [False,False,False,False]

colors_RGBA_typing_list = [list(str(0)+' '),
                           list(str(0)+' '),
                           list(str(0)+' '),
                           list(str(0)+' ')]


#unhashable arg - dict, cant cache
@lru_cache(1)
def surface_static_new_customize(windowres: tuple,
                                 callable_font,
                                 bgcolor: tuple,
                                 textcolor: tuple,
                                 windowbordercolor: tuple,

                                 allcolorkeys: tuple,
                                 allcolorvars: tuple,
                                ):


    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    customize_text = callable_font(32).render('Customize',False,textcolor)

    surface.blit(customize_text,((windowres[0]//2)-(customize_text.get_width() //2),
                                 2))

    colors_text = callable_font(24).render('Colors ',False,textcolor)
    R_text = callable_font(24).render('R',False,(128,0,0,textcolor[3]))
    G_text = callable_font(24).render('G',False,(0,128,0,textcolor[3]))
    B_text = callable_font(24).render('B',False,(0,0,128,textcolor[3]))
    alpha_text = callable_font(24).render('A',False,textcolor)
    surface.blit(colors_text,(4,
                              36))
    surface.blit(R_text,(220,
                         36))
    surface.blit(G_text,(268,
                         36))
    surface.blit(B_text,(315,
                         36))
    surface.blit(alpha_text,(364,
                             36))

    startingy = 64
    colorkeyslist = list(allcolorkeys)
    colorvarslist = list(allcolorvars)

    #transparent_chromakey_win remove
    colorkeyslist.pop(-1)
    colorvarslist.pop(-1)

    typing_bool = False
    for e in range(4):
        if colors_RGBA_typing[e] == True:
            typing_bool = True

    for i in range(len(colorkeyslist)):
        key = colorkeyslist[i]
        if typing_bool and i == color_num:
            var = colors_RGBA_typing_list
        else:
            var = colorvarslist[i]
        key_text = callable_font(16).render(str(str(key).capitalize()+': ').ljust(25),False,textcolor)

        str_var_RGBA = '('
        for a in range(4):
            try:
                if typing_bool and i == color_num:
                    varlist_tostr = str()
                    for s in var[a]:
                        varlist_tostr = varlist_tostr+str(s)
                    str_var_RGBA = str_var_RGBA+str(varlist_tostr).ljust(4)+', '
                else:
                    str_var_RGBA = str_var_RGBA+str(var[a]).ljust(4)+', '
            except IndexError:
                pass
        str_var_RGBA = str_var_RGBA[0:len(str_var_RGBA)-2]+')'

        var_text = callable_font(16).render(str_var_RGBA,False,textcolor)
        surface.blit(key_text,(4,startingy+(i*16)))
        surface.blit(var_text,(4+key_text.get_width(),startingy+(i*16)))


    
    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))
    
    return surface




scrollwheely = 0

#func has an unhashable list arg, dont cache
def surface_static_new_songqueue(windowres: tuple,
                                 callable_font,
                                 bgcolor: tuple,
                                 textcolor: tuple,

                                 windowbordercolor: tuple,
                                 songqueue: list,
                                 ):

    bgcolorr = windowbordercolor
    windowbordercolor = bgcolor

    bgcolor = list(bgcolorr)
    bgcolor.pop(-1)
    bgcolor = tuple(bgcolor)

    textcolor = list(textcolor)
    textcolor.pop(-1)
    textcolor = tuple(textcolor)

    windowbordercolor = list(windowbordercolor)
    windowbordercolor.pop(-1)
    windowbordercolor = tuple(windowbordercolor)


    
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

devisionby = 1 #classic&waveform

cl_renderingmode_num = 0 #classic&waveform
cl_line_space = 0 #classic%bars
cl_onedimensional = False #classic%bars
cl_mirrored = False #classic%bars
cl_rotate = 0 #classic&waveform soon bars
cl_linelength = 1.0 #classic&waveform&bars


wf_mono = True
wf_split = False
wf_merge = False


osc_linesperframe = 1024
osc_fadeout = False




b_rendering_modes ={
    0: 'Low to High',
    1: 'High to Low',
    2: 'Low to High to Low',
    3: 'High to Low to High',
}
b_renderingmode_num = 0

b_boostfreq = False
b_boostfreq_num = 0
b_boostfreq_desc = ['High','Middle','Low',]

b_boostfreq_graph_num = 0
b_boostfreq_graph_desc = ['Straight','Quadratic','SquareRoot']

b_boostfreq_intensity_quad = 1
b_boostfreq_intensity_sqrt = 40


b_boostfreq_mult = 1.0
b_boostfreq_mult_typing = False
b_boostfreq_mult_typing_list = list(str(b_boostfreq_mult)+' ')


b_adaptive_linelen = False

@lru_cache(1)
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
    for i in range(3):
        slightlygreycolor.append(textcolor[i]//2)
    slightlygreycolor.append(textcolor[3])
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
            pygame.draw.lines(surface,textcolor,False,[(110,123),(120,123),
                                                                     (120,133),(110,133),
                                                                     (110,123)])
            if cl_onedimensional:
                pygame.draw.line(surface,textcolor,(110,123),(120,133))
                pygame.draw.line(surface,textcolor,(120,123),(110,133))
    
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,textcolor)
                surface.blit(cl_mirrored_text,(4,134))
                pygame.draw.lines(surface,textcolor,False,[(65,135),(75,135),
                                                           (75,145),(65,145),
                                                           (65,135)])
                if cl_mirrored:
                    pygame.draw.line(surface,textcolor,(65,135),(75,145))
                    pygame.draw.line(surface,textcolor,(75,135),(65,145))
            else:
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,slightlygreycolor)
                surface.blit(cl_mirrored_text,(4,134))
                pygame.draw.lines(surface,slightlygreycolor,False,[(65,135),(75,135),
                                                                   (75,145),(65,145),
                                                                   (65,135)])
                if cl_mirrored:
                    pygame.draw.line(surface,slightlygreycolor,(65,135),(75,145))
                    pygame.draw.line(surface,slightlygreycolor,(75,135),(65,145))


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

            cl_linelength_typing_str = ''
            for i in cl_linelength_typing_list:
                cl_linelength_typing_str += str(i)
            
            cl_linelength_text = callable_font(12).render('Line length multiplier: '+cl_linelength_typing_str,False,textcolor)
            surface.blit(cl_linelength_text,(4,158))


            cl_rotate_typing_str = ''
            for i in cl_rotate_typing_list:
                cl_rotate_typing_str += str(i)
            cl_rotate_text = callable_font(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,textcolor) #do later
            surface.blit(cl_rotate_text,(4,146))
        
        

        case 3:
            br_setting = callable_font(16).render('Bars settings:',False,textcolor)
            surface.blit(br_setting,(4,70))

            cl_mode_text = callable_font(12).render('Modes: <> "'+str(b_rendering_modes[b_renderingmode_num])+'"',False,textcolor)
            surface.blit(cl_mode_text, (4,86))


            cl_line_space_typing_str = ''
            for i in cl_line_space_typing_list:
                cl_line_space_typing_str += str(i)
            
            cl_space_between_lines_text = callable_font(12).render('Pixels between lines: '+cl_line_space_typing_str,False,textcolor)
            surface.blit(cl_space_between_lines_text,(4,98))
    
            cl_onedimensional_text = callable_font(12).render('One dimensional: ',False,textcolor)
            surface.blit(cl_onedimensional_text,(4,110))
            pygame.draw.lines(surface,textcolor,False,[(110,111),(120,111),
                                                       (120,121),(110,121),
                                                       (110,111)])
            if cl_onedimensional:
                pygame.draw.line(surface,textcolor,(110,111),(120,121))
                pygame.draw.line(surface,textcolor,(120,111),(110,121))
    
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,textcolor)
                surface.blit(cl_mirrored_text,(4,122))
                pygame.draw.lines(surface,textcolor,False,[(65,123),(75,123),
                                                           (75,133),(65,133),
                                                           (65,123)])
                if cl_mirrored:
                    pygame.draw.line(surface,textcolor,(65,123),(75,133))
                    pygame.draw.line(surface,textcolor,(75,123),(65,133))
            else:
                cl_mirrored_text = callable_font(12).render('Mirrored: ',False,slightlygreycolor)
                surface.blit(cl_mirrored_text,(4,122))
                pygame.draw.lines(surface,slightlygreycolor,False,[(65,123),(75,123),
                                                                   (75,133),(65,133),
                                                                   (65,123)])
                if cl_mirrored:
                    pygame.draw.line(surface,slightlygreycolor,(65,123),(75,133))
                    pygame.draw.line(surface,slightlygreycolor,(75,123),(65,133))



            cl_rotate_typing_str = ''
            for i in cl_rotate_typing_list:
                cl_rotate_typing_str += str(i)

            cl_rotate_text = callable_font(12).render('Rotate clockwise: '+cl_rotate_typing_str,False,slightlygreycolor)
            surface.blit(cl_rotate_text,(4,134))



            
            b_adaptivelinelen_text = callable_font(12).render('Adaptive line length: ',False,textcolor)
            surface.blit(b_adaptivelinelen_text,(4,158))

            pygame.draw.lines(surface,textcolor,False,[(135,159),(145,159),
                                                       (145,169),(135,169),
                                                       (135,159)])

            cl_linelength_typing_str = ''
            for i in cl_linelength_typing_list:
                cl_linelength_typing_str += str(i)

            if b_adaptive_linelen:
                cl_linelength_text = callable_font(12).render('Line length multiplier: '+cl_linelength_typing_str,False,slightlygreycolor)
                surface.blit(cl_linelength_text,(4,146))

                pygame.draw.line(surface,textcolor,(135,159),(145,169))
                pygame.draw.line(surface,textcolor,(145,159),(135,169))
                                
            else:
                cl_linelength_text = callable_font(12).render('Line length multiplier: '+cl_linelength_typing_str,False,textcolor)
                surface.blit(cl_linelength_text,(4,146))






            b_boostfreq_text = callable_font(12).render(' :Boost Frequencies',False,textcolor)
            surface.blit(b_boostfreq_text,(windowres[0]-4-b_boostfreq_text.get_width(),86))

            x = windowres[0]-4-b_boostfreq_text.get_width()
            pygame.draw.lines(surface,textcolor,False,[(x-10,87),(x,87),
                                                       (x,97),(x-10,97),
                                                       (x-10,87)])

            
            
            if b_boostfreq:
                pygame.draw.line(surface,textcolor,(x-10,87),(x,97))
                pygame.draw.line(surface,textcolor,(x,87),(x-10,97))
                colorrr = textcolor
            else:
                colorrr = slightlygreycolor


            b_boostwhatfreq_text = callable_font(12).render('Boost < '+str(b_boostfreq_desc[b_boostfreq_num]).center(6)+' > frequency',False,colorrr)
            surface.blit(b_boostwhatfreq_text,(windowres[0]-4-b_boostwhatfreq_text.get_width(),98))
                
            b_boostgraph_text = callable_font(12).render('< '+str(b_boostfreq_graph_desc[b_boostfreq_graph_num].center(17))+' > Boost Graph',False,colorrr)
            surface.blit(b_boostgraph_text,(windowres[0]-4-b_boostgraph_text.get_width(),110))

            if b_boostfreq_graph_num in range(0,2):
                b_boostintensity_text = callable_font(12).render('< '+str(b_boostfreq_intensity_quad).center(7)+' > Boost Intensity',False,colorrr)
                surface.blit(b_boostintensity_text,(windowres[0]-4-b_boostintensity_text.get_width(),122))
            if b_boostfreq_graph_num in range(2,3):
                b_boostintensity_text = callable_font(12).render('< '+str((b_boostfreq_intensity_sqrt/80)).center(7)+' > Boost Intensity',False,colorrr)
                surface.blit(b_boostintensity_text,(windowres[0]-4-b_boostintensity_text.get_width(),122))

            b_boostfreq_mult_typing_str = ''
            for i in b_boostfreq_mult_typing_list:
                b_boostfreq_mult_typing_str += str(i)

            b_boostfreq_mult_text = callable_font(12).render('Boost by: '+str(b_boostfreq_mult_typing_str+'x').ljust(7),False,colorrr)
            surface.blit(b_boostfreq_mult_text,(windowres[0]-4-b_boostfreq_mult_text.get_width(),134))
        



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

    if effects_workhere:
        bgslightlygrey = []
        for i in range(3):
            try:
                bgslightlygrey.append(bgcolor[i]//2)
            except ZeroDivisionError:
                bgslightlygrey.append(bgcolor[i])
        bgslightlygrey = tuple(bgslightlygrey)
        
        if effects_surface_visible: #rollin
            button_roll = pygame.Surface((32,16))
            button_roll.fill(bgslightlygrey)
            pygame.draw.lines(button_roll,windowbordercolor,False, [(0,0),(0,16-1),(32-1,16-1),(32-1,0),(0,0)])
            button_text = callable_font(8).render('^',False,textcolor)
            button_text = pygame.transform.rotate(button_text,180)
            button_text = pygame.transform.scale(button_text,(16,8))
            button_roll.blit(button_text,(8,4))
            surface.blit(button_roll,(windowres[0]-214,windowres[1]-(60*(1-(effects_anim_time)))-16))
            surface.blit(surface_movable_new_effects((214,60),callable_font,bgslightlygrey,textcolor,windowbordercolor),
                        (windowres[0]-214,windowres[1]-(60*(1-(effects_anim_time)))))
        else: #rollout
            button_roll = pygame.Surface((32,16))
            button_roll.fill(bgslightlygrey)
            pygame.draw.lines(button_roll,windowbordercolor,False, [(0,0),(0,16-1),(32-1,16-1),(32-1,0),(0,0)])
            button_text = callable_font(8).render('^',False,textcolor)
            button_text = pygame.transform.scale(button_text,(16,8))
            button_roll.blit(button_text,(8,6))
            surface.blit(button_roll,(windowres[0]-214,windowres[1]-(60*(effects_anim_time))-16))
            surface.blit(surface_movable_new_effects((214,60),callable_font,bgslightlygrey,textcolor,windowbordercolor),
                        (windowres[0]-214,windowres[1]-(60*(effects_anim_time))))

    
    
    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    del slightlygreycolor
    return surface

effects_anim_time_raw = 0
effects_anim_time = 0
effects_surface_visible = False

effects_workhere = True

sounddataspeed_num = 0
sounddatarenderspeed_desc = {
    0: 'Straight',
    1: 'SquareRoot',
    2: 'ReverseSquareRoot',
    3: 'Quadratic',
    4: 'ReverseQuadratic',
}

sounddataspeed_intensity_sqrts = 40
sounddataspeed_intensity_quads = 3

sounddataspeed_fadeout = True


def surface_movable_new_effects(      windowres: tuple,
                                      callable_font,
                                      bgcolor: tuple,
                                      textcolor: tuple,
                                      windowbordercolor: tuple
                                      ):

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    effects_text = callable_font(16).render('Effects',False,textcolor)
    surface.blit(effects_text,((windowres[0]//2)-(effects_text.get_width()//2)-2,2))

    effectgraph_text = callable_font(12).render('Effect Graph: <> '+(sounddatarenderspeed_desc[sounddataspeed_num].rjust(18)),False,textcolor)
    surface.blit(effectgraph_text,((windowres[0])-(effectgraph_text.get_width())-2,20))

    if sounddataspeed_num in range(1,3): #sqrt
        effectintensity_text = callable_font(12).render('Effect intensity: < '+(str(((sounddataspeed_intensity_sqrts)/80))).center(7)+' >',False,textcolor)
        surface.blit(effectintensity_text,((windowres[0])-(effectintensity_text.get_width())-2,34))

        fadeout_text = callable_font(12).render('Fadeout:',False,textcolor)
        surface.blit(fadeout_text,((windowres[0])-(fadeout_text.get_width())-20,48))
        pygame.draw.lines(surface,textcolor,False,[((windowres[0])-12,48)   ,((windowres[0])-2,48),
                                                   ((windowres[0])-2,58)    ,((windowres[0])-12,58),
                                                   ((windowres[0])-12       ,48)])
        if sounddataspeed_fadeout:
            pygame.draw.line(surface,textcolor,((windowres[0])-12,48),   ((windowres[0])-2,58))
            pygame.draw.line(surface,textcolor,((windowres[0])-2,48),    ((windowres[0])-12,58))

    if sounddataspeed_num in range(3,5): #quad
        effectintensity_text = callable_font(12).render('Effect intensity: < '+(str(sounddataspeed_intensity_quads-2).center(7))+' >',False,textcolor)
        surface.blit(effectintensity_text,((windowres[0])-(effectintensity_text.get_width())-2,34))

        fadeout_text = callable_font(12).render('Fadeout:',False,textcolor)
        surface.blit(fadeout_text,((windowres[0])-(fadeout_text.get_width())-20,48))
        pygame.draw.lines(surface,textcolor,False,[((windowres[0])-12,48)   ,((windowres[0])-2,48),
                                                   ((windowres[0])-2,58)    ,((windowres[0])-12,58),
                                                   ((windowres[0])-12       ,48)])
        if sounddataspeed_fadeout:
            pygame.draw.line(surface,textcolor,((windowres[0])-12,48),   ((windowres[0])-2,58))
            pygame.draw.line(surface,textcolor,((windowres[0])-2,48),    ((windowres[0])-12,58))

    pygame.draw.lines(surface,windowbordercolor,False, [(0,0),(0,windowres[1]-1),(windowres[0]-1,windowres[1]-1),(windowres[0]-1,0),(0,0)],)
    
    return surface



pr_bluetooth_output_device = False

num_cores = 2
program_numcores_typing = False
program_numcores_typing_list = list(str(num_cores)+' ')


@lru_cache(1)
def surface_static_new_program(windowres: tuple,
                               callable_font,
                               bgcolor: tuple,
                               textcolor: tuple,
                               windowbordercolor: tuple,

                               fpscap: int,
                               highload: bool,
                               ):
    

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)


    slightlygreycolor = []
    for i in range(3):
        slightlygreycolor.append(textcolor[i]//2)
    slightlygreycolor.append(textcolor[3])
    slightlygreycolor = tuple(slightlygreycolor)

    

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
    pygame.draw.lines(surface,textcolor,False,[(184,51),(198,51),
                                                             (198,65),(184,65),
                                                             (184,51)])
    if pr_bluetooth_output_device:
        pygame.draw.line(surface,textcolor,(184,51),(198,65))
        pygame.draw.line(surface,textcolor,(198,51),(184,65))

    fullyred = (255,0,0,textcolor[3])
    highload_text = callable_font(16).render('HIGHLOAD: ',False,fullyred)
    surface.blit(highload_text,(4,66))

    pygame.draw.lines(surface,fullyred,False,[(80,67),(94,67),
                                               (94,81),(80,81),
                                               (80,67)])

    program_numcores_typing_str = ''
    for i in program_numcores_typing_list:
        program_numcores_typing_str += str(i)
    
    if highload:
        pygame.draw.line(surface,fullyred,(80,67),(94,81))
        pygame.draw.line(surface,fullyred,(94,67),(80,81))

        numcores_text = callable_font(16).render('Threads: '+str(program_numcores_typing_str),False,textcolor)
        surface.blit(numcores_text,(4,82))
    else:
        numcores_text = callable_font(16).render('Threads: '+str(program_numcores_typing_str),False,slightlygreycolor)
        surface.blit(numcores_text,(4,82))



    credits_text = callable_font(12).render('Credits',False,textcolor)
    surface.blit(credits_text,(windowres[0]-credits_text.get_width()-5,windowres[1]-76-12))

    surface.blit(pygame.transform.scale(icon_jakeisalivee,(64,64)), (windowres[0]-68,windowres[1]-76))
    surface.blit(pygame.transform.scale(icon_telegram,(64,64)),(windowres[0]-136,windowres[1]-76))
    version_text = callable_font(10).render('Version: '+VERSION,False,textcolor)
    surface.blit(version_text,(windowres[0]-5-version_text.get_width(),windowres[1]-11))

    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    return surface


credits_yippee_anim = pygame.image.load_animation(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'yippee.gif')
credits_yippee_sound = pygame.Sound(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'yippee.mp3')
credits_confetti_anim = pygame.image.load_animation(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'confetti (stock).gif')
credits_confetti_sound = pygame.Sound(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'confetti (stock).mp3')
credits_fue_sound = pygame.Sound(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'фуэ.mp3')
credits_fue_photo = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'фуэ.jpg')
credits_scary_sound = pygame.Sound(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'intense scary sound.mp3')


credits_pygamece_logo = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'pygame-ce logo.png')
credits_pygamece_logo = pygame.transform.scale(credits_pygamece_logo,(128,64))

credits_python_logo = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'python_logo.png')
credits_python_logo = pygame.transform.scale(credits_python_logo,(64,64))

confetti_played = False
yippee_played = False
fue_time = 0

credits_mouseonsecret = False
credits_ihave2sides_photo = pygame.image.load(scriptdirfolder+slash+'Data'+slash+'icons'+slash+'credits'+slash+'funnies'+slash+'2sides.jpg')
credits_ihave2sides_photo = pygame.transform.scale(credits_ihave2sides_photo,(64,64))

def surface_static_new_credits(windowres: tuple,
                               callable_font,
                               bgcolor: tuple,
                               textcolor: tuple,

                               windowbordercolor: tuple,

                               timeanim_start: float,
                               timenow: float,

                               ):
    global confetti_played
    global yippee_played
    global fue_time

    surface = pygame.Surface((windowres[0],windowres[1]),pygame.SRCALPHA)
    surface.fill(bgcolor)

    nowtime_ms = int(timenow*1000)
    starttime_ms = int(timeanim_start*1000)

    text_everything_time = int(starttime_ms)
    text_animations_time = int(starttime_ms+250)
    text_design_time = int(starttime_ms+500)
    text_icons_time = int(starttime_ms+750)
    text_code_time = int(starttime_ms+1000)

    text_jakeisalivee_time = int(starttime_ms+3000)
    jakeisalivee_confetti_time = int(starttime_ms+3000)
    jakeisalivee_icon_time = int(starttime_ms+3500)

    jakeisalivee_telegram_ch_time = int(starttime_ms+4000)
    jakeisalivee_github_time = int(starttime_ms+4200)
    jakeisalivee_itchio_time = int(starttime_ms+4400)
    jakeisalivee_donation_time = int(starttime_ms+4600)
    jakeisalivee_youtube_time = int(starttime_ms+4800)
    jakeisalivee_tiktok_time = int(starttime_ms+5000)
    jakeisalivee_twitter_time = int(starttime_ms+5400)
    jakeisalivee_steam_time = int(starttime_ms+5600)

    jakeisalivee_text_telegram = callable_font(16).render('Telegram',False,textcolor)
    jakeisalivee_text_github =   callable_font(16).render('Github',False,textcolor)
    jakeisalivee_text_itchio =   callable_font(16).render('Itch.io',False,textcolor)
    jakeisalivee_text_donation = callable_font(16).render('Donate',False,textcolor)
    jakeisalivee_text_youtube =  callable_font(16).render('Youtube',False,textcolor)
    jakeisalivee_text_tiktok =   callable_font(16).render('TikTok',False,textcolor)
    jakeisalivee_text_twitter =  callable_font(16).render('Twitter',False,textcolor)
    jakeisalivee_text_steam =    callable_font(16).render('Steam',False,textcolor)
    
    yippee_time = int(starttime_ms+4000)

    confetti_anim_flip_time = int(credits_confetti_anim[0][1]*4)
    confetti_anim_frame = ((nowtime_ms-starttime_ms)//confetti_anim_flip_time) % len(credits_confetti_anim)

    yippee_anim_flip_time = int(credits_yippee_anim[0][1])
    yippee_anim_frame = ((nowtime_ms-yippee_time)//yippee_anim_flip_time) % len(credits_yippee_anim)

    text_madein_python_with_pygamece_time = int(starttime_ms+5000)

    text_specialthanks_time = int(starttime_ms+6000)
    text_you_time = text_specialthanks_time+3000
    text_thankyou_time = text_specialthanks_time+4500

    #x**0.5 = sqrt
    amazingideas_text = callable_font(16).render(' Amazing Ideas:',False,textcolor)
    anchor_middlex = 4+amazingideas_text.get_width()//2

    animations_text = callable_font(16).render('Animations:',False,textcolor)
    design_text = callable_font(16).render('Design:',False,textcolor)
    icons_text = callable_font(16).render('Icons:',False,textcolor)
    code_text = callable_font(16).render('Code:',False,textcolor)

    jakeisalivee_text = callable_font(16).render('JakeIsAlivee',False,textcolor)

    madein_and_with_text = callable_font(16).render('Made in Python with Pygame-Ce',False,textcolor)
    surface_madein_and_with = pygame.Surface((madein_and_with_text.get_width(),madein_and_with_text.get_height()+68),pygame.SRCALPHA)

    surface_madein_and_with.blit(credits_python_logo,(4,0))
    surface_madein_and_with.blit(credits_pygamece_logo,(credits_python_logo.get_width()+8,0))
    surface_madein_and_with.blit(madein_and_with_text,(0,68))
    
    if nowtime_ms in range(text_everything_time,text_everything_time+1000):
        surface.blit(amazingideas_text,(4-((anchor_middlex*2)*((((nowtime_ms-text_everything_time)/1000)-1)**2)),4+(0*16)))
    if nowtime_ms > text_everything_time+1000:
        surface.blit(amazingideas_text,(4,4+(0*16)))

    if nowtime_ms in range(text_animations_time,text_animations_time+1000):
        surface.blit(animations_text,(4+(anchor_middlex-(animations_text.get_width()//2))-((anchor_middlex*2)*((((nowtime_ms-text_animations_time)/1000)-1)**2)),
                                      4+(1*16)))
    if nowtime_ms > text_animations_time+1000:
        surface.blit(animations_text,(4+(anchor_middlex-(animations_text.get_width()//2)),4+(1*16)))

    if nowtime_ms in range(text_design_time,text_design_time+1000):
        surface.blit(design_text,(4+(anchor_middlex-(design_text.get_width()//2))-((anchor_middlex*2)*((((nowtime_ms-text_design_time)/1000)-1)**2)),4+(2*16)))
    if nowtime_ms > text_design_time+1000:
        surface.blit(design_text,(4+(anchor_middlex-(design_text.get_width()//2)),4+(2*16)))

    if nowtime_ms in range(text_icons_time,text_icons_time+1000):
        surface.blit(icons_text,(4+(anchor_middlex-(icons_text.get_width()//2))-((anchor_middlex*2)*((((nowtime_ms-text_icons_time)/1000)-1)**2)),4+(3*16)))
    if nowtime_ms > text_icons_time+1000:
        surface.blit(icons_text,(4+(anchor_middlex-(icons_text.get_width()//2)),4+(3*16)))

    if nowtime_ms in range(text_code_time,text_code_time+1000):
        surface.blit(code_text,(4+(anchor_middlex-(code_text.get_width()//2))-((anchor_middlex*2)*((((nowtime_ms-text_code_time)/1000)-1)**2)),4+(4*16)))
    if nowtime_ms > text_code_time+1000:
        surface.blit(code_text,(4+(anchor_middlex-(code_text.get_width()//2)),4+(4*16)))
    
    
    
    if nowtime_ms in range(text_jakeisalivee_time,text_jakeisalivee_time+1000):
        jakeisalivee_text.set_alpha(int((255)*(1-((((nowtime_ms-text_jakeisalivee_time)/1000)-1)**2))))
        surface.blit(jakeisalivee_text,((windowres[0]//2)-(jakeisalivee_text.get_width()//2),(4)))
    if nowtime_ms > text_jakeisalivee_time+1000:
        surface.blit(jakeisalivee_text,((windowres[0]//2)-(jakeisalivee_text.get_width()//2),(4)))

    jakeisalivee_anchorx = 32
    if nowtime_ms in range(jakeisalivee_icon_time,jakeisalivee_icon_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_icon_time)/1000)-1)**2
        if credits_mouseonsecret:
            surfacealpha = credits_ihave2sides_photo
            surfacealpha.set_alpha(255*graph)
            surface.blit(surfacealpha,(windowres[0]-(((4+(jakeisalivee_anchorx*2)))*graph),4))
        else:
            surfacealpha = icon_jakeisalivee
            surfacealpha.set_alpha(255*graph)
            surface.blit(surfacealpha,(windowres[0]-(((4+(jakeisalivee_anchorx*2)))*graph),4))
    if nowtime_ms > jakeisalivee_icon_time+1000:
        if credits_mouseonsecret:
            surface.blit(credits_ihave2sides_photo,(windowres[0]-(4+(jakeisalivee_anchorx*2)),(4)))
        else:
            surface.blit(icon_jakeisalivee,(windowres[0]-(4+(jakeisalivee_anchorx*2)),(4)))

    if nowtime_ms in range(jakeisalivee_telegram_ch_time,jakeisalivee_telegram_ch_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_telegram_ch_time)/1000)-1)**2
        jakeisalivee_text_telegram.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_telegram,(windowres[0]-((jakeisalivee_text_telegram.get_width()//2)+4+jakeisalivee_anchorx),
                                                 52+(16*graph)))
    if nowtime_ms > jakeisalivee_telegram_ch_time+1000:
        surface.blit(jakeisalivee_text_telegram,(windowres[0]-((jakeisalivee_text_telegram.get_width()//2)+4+jakeisalivee_anchorx),
                                                 68))

    if nowtime_ms in range(jakeisalivee_github_time,jakeisalivee_github_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_github_time)/1000)-1)**2
        jakeisalivee_text_github.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_github,(windowres[0]-((jakeisalivee_text_github.get_width()//2)+4+jakeisalivee_anchorx),
                                               68+(16*graph)))
    if nowtime_ms > jakeisalivee_github_time+1000:
        surface.blit(jakeisalivee_text_github,(windowres[0]-((jakeisalivee_text_github.get_width()//2)+4+jakeisalivee_anchorx),
                                               84))

    if nowtime_ms in range(jakeisalivee_itchio_time,jakeisalivee_itchio_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_itchio_time)/1000)-1)**2
        jakeisalivee_text_itchio.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_itchio,(windowres[0]-((jakeisalivee_text_itchio.get_width()//2)+4+jakeisalivee_anchorx),
                                                 84+(16*graph)))
    if nowtime_ms > jakeisalivee_itchio_time+1000:
        surface.blit(jakeisalivee_text_itchio,(windowres[0]-((jakeisalivee_text_itchio.get_width()//2)+4+jakeisalivee_anchorx),
                                               100))

    if nowtime_ms in range(jakeisalivee_donation_time,jakeisalivee_donation_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_donation_time)/1000)-1)**2
        jakeisalivee_text_donation.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_donation,(windowres[0]-((jakeisalivee_text_donation.get_width()//2)+4+jakeisalivee_anchorx),
                                                 100+(16*graph)))
    if nowtime_ms > jakeisalivee_donation_time+1000:
        surface.blit(jakeisalivee_text_donation,(windowres[0]-((jakeisalivee_text_donation.get_width()//2)+4+jakeisalivee_anchorx),
                                                 116))

    if nowtime_ms in range(jakeisalivee_youtube_time,jakeisalivee_youtube_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_youtube_time)/1000)-1)**2
        jakeisalivee_text_youtube.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_youtube,(windowres[0]-((jakeisalivee_text_youtube.get_width()//2)+4+jakeisalivee_anchorx),
                                                 116+(16*graph)))
    if nowtime_ms > jakeisalivee_youtube_time+1000:
        surface.blit(jakeisalivee_text_youtube,(windowres[0]-((jakeisalivee_text_youtube.get_width()//2)+4+jakeisalivee_anchorx),
                                                  132))

    if nowtime_ms in range(jakeisalivee_tiktok_time,jakeisalivee_tiktok_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_tiktok_time)/1000)-1)**2
        jakeisalivee_text_tiktok.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_tiktok,(windowres[0]-((jakeisalivee_text_tiktok.get_width()//2)+4+jakeisalivee_anchorx),
                                               132+(16*graph)))
    if nowtime_ms > jakeisalivee_tiktok_time+1000:
        surface.blit(jakeisalivee_text_tiktok,(windowres[0]-((jakeisalivee_text_tiktok.get_width()//2)+4+jakeisalivee_anchorx),
                                               148))
    
    if nowtime_ms in range(jakeisalivee_twitter_time,jakeisalivee_twitter_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_twitter_time)/1000)-1)**2
        jakeisalivee_text_twitter.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_twitter,(windowres[0]-((jakeisalivee_text_twitter.get_width()//2)+4+jakeisalivee_anchorx),
                                               148+(16*graph)))
    if nowtime_ms > jakeisalivee_twitter_time+1000:
        surface.blit(jakeisalivee_text_twitter,(windowres[0]-((jakeisalivee_text_twitter.get_width()//2)+4+jakeisalivee_anchorx),
                                               164))

    if nowtime_ms in range(jakeisalivee_steam_time,jakeisalivee_steam_time+1000):
        graph = 1-(((nowtime_ms-jakeisalivee_steam_time)/1000)-1)**2
        jakeisalivee_text_steam.set_alpha(255*graph)
        surface.blit(jakeisalivee_text_steam,(windowres[0]-((jakeisalivee_text_steam.get_width()//2)+4+jakeisalivee_anchorx),
                                                164+(16*graph)))
    if nowtime_ms > jakeisalivee_steam_time+1000:
        surface.blit(jakeisalivee_text_steam,(windowres[0]-((jakeisalivee_text_steam.get_width()//2)+4+jakeisalivee_anchorx),
                                                180))
                



    
    if nowtime_ms in range(jakeisalivee_confetti_time,jakeisalivee_confetti_time+1000):
        if not confetti_played:
            confetti_played = True
            credits_confetti_sound.play()
        confetti_surface = credits_confetti_anim[confetti_anim_frame][0]
        confetti_surface = pygame.transform.scale(confetti_surface,((jakeisalivee_text.get_width()+32),
                                                                    (jakeisalivee_text.get_height()+16)))
        confetti_surface.set_alpha(int((255)*(1-((((nowtime_ms-jakeisalivee_confetti_time)/1000)-1)**2))))
        surface.blit(confetti_surface,((windowres[0]//2)-(confetti_surface.get_width()//2),(0)))
    if nowtime_ms in range(jakeisalivee_confetti_time+1000,jakeisalivee_confetti_time+4000):
        confetti_surface = credits_confetti_anim[confetti_anim_frame][0]
        confetti_surface = pygame.transform.scale(confetti_surface,((jakeisalivee_text.get_width()+32),
                                                                    (jakeisalivee_text.get_height()+8)))
        surface.blit(confetti_surface,((windowres[0]//2)-(confetti_surface.get_width()//2),(0)))
    if nowtime_ms in range(jakeisalivee_confetti_time+4000,jakeisalivee_confetti_time+5000):
        confetti_surface = credits_confetti_anim[confetti_anim_frame][0]
        confetti_surface = pygame.transform.scale(confetti_surface,((jakeisalivee_text.get_width()+32),
                                                                    (jakeisalivee_text.get_height()+16)))
        confetti_surface.set_alpha(int((255)*((((nowtime_ms-(jakeisalivee_confetti_time+4000))/1000)-1)**2)))
        surface.blit(confetti_surface,((windowres[0]//2)-(confetti_surface.get_width()//2),(0)))

    if nowtime_ms in range(yippee_time,yippee_time+1000):
        if not yippee_played:
            yippee_played = True
            credits_yippee_sound.play()
        yippee_surface = credits_yippee_anim[yippee_anim_frame][0]
        yippee_surface = pygame.transform.scale_by(yippee_surface,0.25)
        surface.blit(yippee_surface,((windowres[0]//2)-(yippee_surface.get_width()//2),
                                     (windowres[1]//2)-(yippee_surface.get_height()//2)))



    if nowtime_ms in range(text_madein_python_with_pygamece_time,text_madein_python_with_pygamece_time+3000):
        surface.blit(surface_madein_and_with,(4-((8+surface_madein_and_with.get_width())*((((nowtime_ms-text_madein_python_with_pygamece_time)/3000)-1)**2)),4+(6*16)))

    if nowtime_ms > text_madein_python_with_pygamece_time+3000:
        surface.blit(surface_madein_and_with,(4,4+(6*16)))
        


    specialthanks_text = callable_font(16).render('Special Thanks',False,textcolor)
    you_text = callable_font(12).render('You.',False,textcolor)
    thankyou_text = callable_font(12).render('Thank you for using this program.',False,textcolor)

    if nowtime_ms in range(text_specialthanks_time,text_specialthanks_time+1000):
        surface.blit(specialthanks_text,((windowres[0]-specialthanks_text.get_width()-2)+((specialthanks_text.get_width()+2)*((((nowtime_ms-text_specialthanks_time)/1000)-1)**2)),
                                         windowres[1]-(16+(2*12))))
    if nowtime_ms > text_specialthanks_time+1000:
        surface.blit(specialthanks_text,(windowres[0]-specialthanks_text.get_width()-2,
                                         windowres[1]-(16+(2*12))))

    if nowtime_ms in range(text_you_time,text_you_time+1000):
        surface.blit(you_text,((windowres[0]-you_text.get_width()-2)+((you_text.get_width()+2)*((((nowtime_ms-text_you_time)/1000)-1)**2)),
                               windowres[1]-(2+(2*12))))
    if nowtime_ms > text_you_time+1000:
        surface.blit(you_text,(windowres[0]-you_text.get_width()-2,
                               windowres[1]-(2+(2*12))))
        
    if nowtime_ms in range(text_thankyou_time,text_thankyou_time+3000):
        surface.blit(thankyou_text,((windowres[0]-thankyou_text.get_width()-2)+((thankyou_text.get_width()+2)*((((nowtime_ms-text_thankyou_time)/3000)-1)**2)),
                                     windowres[1]-(2+(1*12))))
    if nowtime_ms > text_thankyou_time+3000:
        surface.blit(thankyou_text,(windowres[0]-thankyou_text.get_width()-2,
                                    windowres[1]-(2+(1*12))))


    surface.blit(surface_static_settings_decorator(windowres,
                                                   callable_font,
                                                   windowbordercolor,
                                                   textcolor))

    fue_time_ms = int(fue_time*1000)
    if nowtime_ms in range(fue_time_ms,fue_time_ms+1000):
        credits_scary_sound.set_volume(0.5*(1-((nowtime_ms-fue_time_ms)/1000)**2))
        fue_surface = credits_fue_photo
        fue_surface = pygame.transform.scale(fue_surface,(windowres[0]+((windowres[0]//2)*(1-((((nowtime_ms-fue_time_ms)/1000)-1))**2)),windowres[1]))
        fue_surface.set_alpha(int((255)*((((nowtime_ms-fue_time_ms)/1000)-1)**2)))
        surface.blit(fue_surface,((windowres[0]//2)-(fue_surface.get_width()//2),
                                  (windowres[1]//2)-(fue_surface.get_height()//2)))

    return surface

@lru_cache(1)
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




cl_zoom_typing = False
cl_zoom_typing_list = list(str(devisionby)+' ')
cl_line_space_typing = False
cl_line_space_typing_list = list(str(cl_line_space)+' ')
cl_rotate_typing = False
cl_rotate_typing_list = list(str(cl_rotate)+'° ')
cl_linelength_typing = False
cl_linelength_typing_list = list(str(cl_linelength)+' ')

osc_linesperframe_typing = False
osc_linesperframe_typing_list = list(str(osc_linesperframe)+' ')


class typing:

    def cancel_all():
        typing.cancel_clzoom()
        typing.cancel_cllinespace()
        typing.cancel_clrotate()
        typing.cancel_cllinelength()
        typing.cancel_osclinesperframe()
        typing.cancel_boostby()
        
        typing.cancel_numcores()
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
            num = int(cl_rotate_typing_str.replace('°', ''))
            if num in range(0,45):
                cl_rotate_typing_str = '0° '
            elif num in range(45,90):
                cl_rotate_typing_str = '90° '
            elif num in range(90,135):
                cl_rotate_typing_str = '90° '
            elif num in range(135,180):
                cl_rotate_typing_str = '180° '
            elif num in range(180,225):
                cl_rotate_typing_str = '180° '
            elif num in range(225,270):
                cl_rotate_typing_str = '270° '
            elif num in range(270,1000):
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

    def cancel_numcores():
        global program_numcores_typing
        global program_numcores_typing_list
        global num_cores

        program_numcores_typing_list[-1] = ' '

        program_numcores_typing = False
        program_numcores_typing_str = ''
        for i in program_numcores_typing_list:
            program_numcores_typing_str += str(i)

        try:
            num_cores = int(program_numcores_typing_str)
            if num_cores == 0:
                num_cores = 1
        except ValueError:
            num_cores = 1
        program_numcores_typing_list = list(str(num_cores)+' ')


    def cancel_boostby():
        global b_boostfreq_mult_typing
        global b_boostfreq_mult_typing_list
        global b_boostfreq_mult

        b_boostfreq_mult_typing_list[-1] = ' '
        
        b_boostfreq_mult_typing = False

        b_boostfreq_mult_typing_str = ''
        for i in b_boostfreq_mult_typing_list:
            b_boostfreq_mult_typing_str += str(i)
        
        try: 
            b_boostfreq_mult = float(b_boostfreq_mult_typing_str)
        except ValueError:
            b_boostfreq_mult = 1.0
        b_boostfreq_mult_typing_list = list(str(b_boostfreq_mult)+' ')



    def cancel_colorsRGBA(colors: dict):
        global colors_RGBA_typing
        global colors_RGBA_typing_list
        global color_num

        typingg = False
        for r in colors_RGBA_typing:
            if r == True:
                typingg = True

        for i in range(4):
            colors_RGBA_typing_list[i][-1] = ' '

        colorslistlist_toliststr = ['','','','']

        for a in range(4):
            for i in range(4):
                try:
                    colorslistlist_toliststr[a] = colorslistlist_toliststr[a]+str(colors_RGBA_typing_list[a][i])
                    int(colorslistlist_toliststr[a])
                except ValueError:
                    colorslistlist_toliststr[a] = '0'
                except IndexError:
                    pass
        newcolorsRGBA = []
        for i in colorslistlist_toliststr:
            if int(i) > 255:
                i = 255
            if int(i) < 0:
                i = 0
            newcolorsRGBA.append(int(i))
        newcolorsRGBA = tuple(newcolorsRGBA)

        colorsdict_keys = list(colors.keys())
        colorsdict_vars = list(colors.values())

        lastkey = colorsdict_keys[-1]
        colorsdict_keys.pop(-1)
        colorsdict_vars.pop(-1)
        if typingg:
            colorsdict_vars.pop(color_num)
            colorsdict_vars.insert(color_num, newcolorsRGBA)

        colorstuple_list = []
        for i in range(len(colorsdict_keys)):
            colorstuple_list.append((colorsdict_keys[i],colorsdict_vars[i]))

        #transparent_chromakey_win without alpha channel
        colorstuple_list.append((lastkey,colorsdict_vars[-1][0:3]))
        
        newdict_colors = dict(colorstuple_list)

        color_num = 0
        colors_RGBA_typing = [False,False,False,False]
        colors_RGBA_typing_list = [list(str(0)+' '),
                                   list(str(0)+' '),
                                   list(str(0)+' '),
                                   list(str(0)+' ')]

        return newdict_colors







if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(3)