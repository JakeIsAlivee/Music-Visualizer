
# I make it works on Linux (ur version didnt works on Manjaro)
# I made code looks better and PEP8-like but it have some issues
# But i am to lazy to fix them, mb later.
# I think u should use tkinter's filedialog cause it is in py-std
# Good luck!

import soundfile
import pygame
import numpy as np
import os
import sys
import time
import gc

GUI_AVAILABLE = True
try:
    import easygui
except:
    GUI_AVAILABLE = False


try:
    import win32api
    import win32con
    import win32gui
    WINDOWS = True
except ImportError:
    WINDOWS = False
    


if getattr(sys, 'frozen', False):
    scriptdirfolder = os.path.dirname(sys.executable)
else:
    scriptdirfolder = os.path.dirname(os.path.abspath(__file__))

slash = os.sep
SUPPORTED_FORMATS = {'.flac', '.mp3', '.mp2', '.ogg', '.wav'}

class Song:
    def __init__(self, songdir):
        self.songdir = songdir
        self.songlen = 0
        self.sounddata = None
        self.rate = 0
        self.channels = 1
        self.loaded = False
        
    def load(self):
        if self.loaded: return
        
        try:
            pygame_sound = pygame.mixer.Sound(self.songdir)
            self.songlen = pygame_sound.get_length() * 1000
            self.sounddata, self.rate = soundfile.read(self.songdir)
            if len(self.sounddata.shape) == 2:
                self.channels = self.sounddata.shape[1]
            else: self.channels = 1
            self.loaded = True
            
        except Exception as e:
            print(f"Error loading song {self.songdir}: {e}")
            raise

class AudioVisualizer:
    def __init__(self):
        # RENDER THINGS
        self.running = True
        self.playing = False
        self.current_song = 0
        self.volume = 0.5
        self.zoom_level = 1
        self.render_mode = 0
        self.scene = "visualizer"  # visualizer, settings, queue
        
        # WINDOW THINGS
        self.window_width = 600
        self.window_height = 260
        self.pos_x = 0
        self.pos_y = 0
        
        # MOUSE THINGS
        self.dragging = False
        self.drag_start = (0, 0)
        
        # ANIMATIONS
        self.animations = {}
        
        # SONGS QUEUE
        self.songs = []
        
        # RENDER SETTINGS
        self.render_modes = {
            0: '<|<', 1: '>|>', 2: '>|<', 3: '<|>',
            4: '|<<', 5: '|>>', 6: '>>|', 7: '<<|'}
        
        # ZOOM LEVELS
        self.zoom_levels = {
            1: 'x1024', 2: 'x512', 4: 'x256', 8: 'x128',
            16: 'x64', 32: 'x32', 64: 'x16', 128: 'x8',
            256: 'x4', 512: 'x2', 1024: 'x1'}
        self.init_pygame()
        
    def init_pygame(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE
        )
        
        pygame.display.set_caption("Audio Visualizer")
        
        info = pygame.display.Info()
        self.pos_x = (info.current_w - self.window_width) // 2
        self.pos_y = (info.current_h - self.window_height) // 2
        
    def load_song(self, filepath):
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return False
            
        ext = os.path.splitext(filepath)[1].lower()
        if ext not in SUPPORTED_FORMATS:
            print(f"Unsupported format: {ext}")
            return False
            
        song = Song(filepath)
        try:
            song.load()
            self.songs.append(song)
            return True
        except Exception as e:
            print(f"Failed to load song: {e}")
            return False
            
    def play_current(self):
        if not self.songs: return
        pygame.mixer.music.load(self.songs[self.current_song].songdir)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        self.playing = True
        
    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False
        
    def next_song(self):
        if not self.songs: return
            
        self.stop()
        self.current_song = (self.current_song + 1) % len(self.songs)
        self.play_current()
        
    def prev_song(self):
        if not self.songs: return
            
        self.stop()
        self.current_song = (self.current_song - 1) % len(self.songs)
        self.play_current()
        
    def toggle_play(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
            else:
                self.play_current()
            self.playing = True
            
    def draw_visualizer(self):
        self.screen.fill((0, 0, 0))
        if not self.songs: return
            
        song = self.songs[self.current_song]
        if not song.loaded: return
        pos = pygame.mixer.music.get_pos()
        
        sample_rate = song.rate
        sample_index = int(pos * sample_rate / 1000)
        
        width = self.window_width
        height = self.window_height
        center_y = height // 2
        
        for x in range(width):
            try:
                idx = self.calculate_sample_index(x, sample_index, width)
                if idx < 0 or idx >= len(song.sounddata): continue

                if song.channels == 2:
                    sample = song.sounddata[idx]
                    amp_left = sample[0]
                    amp_right = sample[1]
                else:
                    amp = song.sounddata[idx]
                    amp_left = amp_right = amp
                    
                scale = height * 0.4
                y_left = center_y + int(amp_left * scale)
                y_right = center_y - int(amp_right * scale)
                
                color = (255, 255, 255)
                if self.render_mode in [2, 3]:
                    pygame.draw.line(self.screen, color,
                                   (x // 2, y_left),
                                   (x // 2, y_right))
                    pygame.draw.line(self.screen, color,
                                   (width - x // 2, y_left),
                                   (width - x // 2, y_right))
                else:
                    pygame.draw.line(self.screen, color,
                                   (x, y_left),
                                   (x, y_right))
            except (IndexError, ValueError):
                continue
                
        if self.render_mode < 4:
            pygame.draw.line(self.screen, (0, 128, 255),
                           (width // 2, 10),
                           (width // 2, height - 10), 2)

        if not self.playing:
            bar_width = 30
            bar_height = 80
            x_center = width // 2
            
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (x_center - bar_width - 10, center_y - bar_height // 2,
                            bar_width, bar_height))
            pygame.draw.rect(self.screen, (255, 255, 255),
                           (x_center + 10, center_y - bar_height // 2,
                            bar_width, bar_height))
                            
    def calculate_sample_index(self, x, base_index, width):
        zoom = self.zoom_level
        
        if self.render_mode == 0:  # <|<
            return (x - width // 2 + base_index) // zoom
        elif self.render_mode == 1:  # >|>
            return (-x + width // 2 + base_index) // zoom
        elif self.render_mode == 2:  # >|<
            return (-x + width + base_index) // zoom
        elif self.render_mode == 3:  # <|>
            return (x - width + base_index) // zoom
        elif self.render_mode == 4:  # |<<
            return (x + base_index) // zoom
        elif self.render_mode == 5:  # |>>
            return (-x + base_index) // zoom
        elif self.render_mode == 6:  # >>|
            return (-x + width + base_index) // zoom
        elif self.render_mode == 7:  # <<|
            return (x - width + base_index) // zoom
        else:
            return base_index // zoom
            
    def draw_settings(self):
        self.screen.fill((0, 0, 128))
        font = pygame.font.SysFont('Arial', 24, bold=True)
        title = font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title, (20, 20))
        
        if self.songs:
            song = self.songs[self.current_song]
            song_name = os.path.basename(song.songdir)
            if len(song_name) > 30:
                song_name = song_name[:27] + "..."
                
            info_font = pygame.font.SysFont('Arial', 16)
            song_text = info_font.render(f"Now playing: {song_name}", True, (255, 255, 255))
            self.screen.blit(song_text, (20, 60))
        vol_font = pygame.font.SysFont('Arial', 18)
        vol_text = vol_font.render(f"Volume: {int(self.volume * 100)}%", True, (255, 255, 255))
        self.screen.blit(vol_text, (20, 100))

        zoom_text = vol_font.render(f"Zoom: {self.zoom_levels.get(self.zoom_level, 'x1')}", True, (255, 255, 255))
        self.screen.blit(zoom_text, (20, 130))

        mode_text = vol_font.render(f"Mode: {self.render_modes[self.render_mode]}", True, (255, 255, 255))
        self.screen.blit(mode_text, (20, 160))
        
        controls = [
            "Space: Play/Pause",
            "Left/Right: Previous/Next song",
            "Up/Down: Volume control",
            "ESC: Back to visualizer",
            "Q: Quit"]
        
        for i, control in enumerate(controls):
            ctrl_text = info_font.render(control, True, (200, 200, 200))
            self.screen.blit(ctrl_text, (20, 200 + i * 25))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup(event)
                
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mousemotion(event)
                
            elif event.type == pygame.WINDOWRESIZED:
                self.window_width = event.x
                self.window_height = event.y
                
    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE:
            self.toggle_play()
            
        elif event.key == pygame.K_RIGHT:
            self.next_song()
            
        elif event.key == pygame.K_LEFT:
            self.prev_song()
            
        elif event.key == pygame.K_UP:
            self.volume = min(1.0, self.volume + 0.1)
            pygame.mixer.music.set_volume(self.volume)
            
        elif event.key == pygame.K_DOWN:
            self.volume = max(0.0, self.volume - 0.1)
            pygame.mixer.music.set_volume(self.volume)
            
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
            current = list(self.zoom_levels.keys())
            idx = current.index(self.zoom_level) if self.zoom_level in current else 0
            if idx > 0:
                self.zoom_level = current[idx - 1]
                
        elif event.key == pygame.K_MINUS:
            current = list(self.zoom_levels.keys())
            idx = current.index(self.zoom_level) if self.zoom_level in current else 0
            if idx < len(current) - 1:
                self.zoom_level = current[idx + 1]
                
        elif event.key == pygame.K_m:
            self.render_mode = (self.render_mode + 1) % len(self.render_modes)
            
        elif event.key == pygame.K_ESCAPE:
            if self.scene == "settings":
                self.scene = "visualizer"
            else:
                self.scene = "settings"
                
        elif event.key == pygame.K_q:
            self.running = False
            
    def handle_mousedown(self, event):
        if event.button == 1:
            self.dragging = True
            self.drag_start = event.pos
            
    def handle_mouseup(self, event):
        if event.button == 1:
            self.dragging = False
            
    def handle_mousemotion(self, event):
        if self.dragging:
            dx = event.pos[0] - self.drag_start[0]
            dy = event.pos[1] - self.drag_start[1]
            
            self.pos_x += dx
            self.pos_y += dy
            
            self.drag_start = event.pos
            
    def run(self):
        if GUI_AVAILABLE:
            filepath = easygui.fileopenbox(
                "Select audio file",
                "Audio Visualizer",
                scriptdirfolder,
                filetypes=["*.wav", "*.mp3", "*.ogg", "*.flac"]
            )
            
            if not filepath:
                print("No file selected. Exiting.")
                return
                
            if not self.load_song(filepath):
                print("Failed to load audio file.")
                return
        else:
            if len(sys.argv) > 1:
                filepath = sys.argv[1]
                if not self.load_song(filepath):
                    print(f"Failed to load: {filepath}")
                    return
            else:
                print("Usage: python visualizer.py <audio_file>")
                print("Or install easygui for file selection dialog")
                return
        self.play_current()
        clock = pygame.time.Clock()
        
        while self.running:
            self.handle_events()
            
            if self.scene == "visualizer":
                self.draw_visualizer()
            elif self.scene == "settings":
                self.draw_settings()
                
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()
        
def main():
    visualizer = AudioVisualizer()
    
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if pygame.get_init():
            pygame.quit()
            
if __name__ == "__main__":
    main()
