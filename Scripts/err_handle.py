import pygame
import sys

#pygame should be initialized already if you import this

def handled_error(title,VERSION,exc_traceback):

    problematicline = sys.exc_info()[2]
    while problematicline.tb_next != None:
        problematicline = problematicline.tb_next
            
    buttonindex = pygame.display.message_box(title=title,
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

    return buttonindex


def LOWLEVEL_err(traceback):

    buttonindex = pygame.display.message_box(title="CRITICAL ERROR",
                                             message="A LOW-LEVEL ERROR OCCURED\n"+
                                             "You can try to ignore it but that will definitely NOT work and you'll crash miserably\n\n"+
                                             'Traceback: '+str(traceback)+'\n',
                                             
                                             message_type='error',
                                             buttons=('Ignore','Save traceback','Close'),
                                             )

    return buttonindex


