

import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
import requests

import subprocess
import sys

def update_check(icondir,VERSION,REPONAME,REPOAUTHORNAME):
    try:

        if VERSION[0:1] == 'v': #not checking if the version is WIP
            root = tk.Tk()
            root.withdraw()
            root.iconbitmap(icondir) #for filedialog icon to show
            root.attributes("-topmost", True)
            
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
                    if filedir:
                        filebytes = requests.get(json['assets'][0]['browser_download_url'])
                        try:
                            filebytes.raise_for_status()
                            raise requests.HTTPError
                        except requests.HTTPError as traceback:
                            messagebox.showerror('Uh oh',
                                                 'Networking error\n'+
                                                 str(traceback))
                            sys.exit()

                        with open(filedir, "wb") as f:
                            f.write(filebytes.content)

                        subprocess.Popen([filedir])

                        sys.exit()
                else:
                    pass

    except Exception:
        #ignoring any exceptions that rise from network errors (or, maybe, github rate limiting your ip)
        pass 











if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)