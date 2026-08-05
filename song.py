import pygame
import soundfile
import os

musicformats = {
    '.flac',
    '.mp3',
    '.mp2',
    '.ogg',
    '.wav',
}

filetypes = [('MP3', '*.mp3'),
             ('WAV', '*.wav'),
             ('OGG', '*.ogg'),
             ('FLAC','*.flac'),
             ('mp2', '*.mp2')
             ]


class Song:
    def __init__(self, songdir: str):
        self.songdir = songdir
        self.rawfile = open(songdir,'r') #so the user could not delete the song file while it is imported in the program #should ALWAYS get closed when deleted from the program
        self.songlength = pygame.Sound(self.songdir).get_length()*1000 #this one takes too much time to get length

    def load(self, musicvolume: int):
        songformat = os.path.splitext(self.songdir)[1]
        pygame.mixer_music.load(self.songdir)
        pygame.mixer_music.set_volume(musicvolume/100)
        pygame.mixer_music.play()   
        pygame.mixer_music.pause()
        
        soundrawdata, rate = soundfile.read(self.songdir, dtype='int16', always_2d=True)

        return soundrawdata, rate, songformat

def songreset():
    pygame.mixer_music.unload()

    return 0,0,0

songformat = ''

songnum = 0

musicvolume_percent = 50


songpos = 0
songpos_sync = 0

lastsounddata = 0


playing = False

songqueue = []

soundrate = 0


if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)