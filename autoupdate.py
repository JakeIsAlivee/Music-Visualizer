import time

import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
import requests

import subprocess
import threading
import sys

def update_check_logic(interface_class: interface, VERSION,REPONAME,REPOAUTHORNAME):
    try:

        if VERSION[0:1] == 'v': #not checking if the version is WIP

            json = requests.get(f'https://api.github.com/repos/{REPOAUTHORNAME}/{REPONAME}/releases/latest').json()
            if str(json['tag_name']) != str(VERSION):
                yes = messagebox.askyesno('AutoUpdater',"New version is available! ("+str(json['tag_name'])+")\nWould you like to download it?",
                                          icon=['info'])
                
                if yes:
                    filedir = filedialog.asksaveasfilename(
                                                            title="Choose a path where the new version would save",
                                                            filetypes=[("All", "*.*")],
                                                            initialfile=str(json["name"]) + ".exe",
                                                            )
                    
                    interface_class.show()
                    interface_class.downloading()
                    interface_class.root.update()
                    interface_class.root.attributes("-topmost", False)

                    if filedir:
                        
                        try:
                            filebytes = requests.get(json['assets'][0]['browser_download_url'])
                            filebytes.raise_for_status()
                            interface_class.root.update()
                        except requests.HTTPError as traceback:
                            messagebox.showerror('Uh oh',
                                                 'Networking error\n'+
                                                 'Response: '+str(traceback.response))
                            sys.exit()

                        with open(filedir, "wb") as f:
                            f.write(filebytes.content)

                        subprocess.Popen([filedir])
                        interface_class.root.update()
                        sys.exit()

                else:
                    pass

    except Exception:
        #ignoring any exceptions that rise from network errors (or, maybe, github rate limiting your ip)
        pass



class interface:
    def __init__(self,icondir,
                 windowsize: tuple = (250,24),
                 ):
        root = tk.Tk()
        root.withdraw()
        root.iconbitmap(icondir) #for filedialog icon to show
        root.attributes("-topmost", True)
            
        root.title("AutoUpdater")
        root.geometry(str(windowsize[0])+'x'+str(windowsize[1])) 
        root.geometry('+'+str((root.winfo_screenwidth()//2)-(windowsize[0]//2))+
                      '+'+str((root.winfo_screenheight()//2)-(windowsize[1]//2)))
        self.root = root

    def downloading(self):
        label = tk.Label(self.root, text="Downloading...", font=("Arial", 14))
        label.pack(pady=0)
    

    def show(self):
        self.root.deiconify()
    def hide(self):
        self.root.withdraw()

    



def update_check_start(icondir,VERSION,REPONAME,REPOAUTHORNAME):
    #i tried to make the interface and update logic work in seperate threads but failed

    root = interface(icondir)

    update_check_logic(root,VERSION,REPONAME,REPOAUTHORNAME)

    root.root.destroy()

        


    




if __name__ == '__main__':
    
    print('Thats not how that works')
    time.sleep(10)