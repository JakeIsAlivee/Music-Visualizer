

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import requests
def update_check(VERSION,REPONAME,REPOAUTHORNAME):
    try:
        if VERSION[0:1] == 'v': #not checking if the version is WIP
            json = requests.get(f'https://api.github.com/repos/{REPOAUTHORNAME}/{REPONAME}/releases/latest').json()
            if str(json['tag_name']) != str(VERSION):
                yes = messagebox.askyesno('AutoUpdater',"New version available!\nWould you like to download it?",
                                          icon=['info'])
                
                if yes:
                    savingfile = filedialog.asksaveasfile('wb',title='Choose a path where the new version would save',
                                                          filetypes=[('All','*.*')],initialfile=str(json['name'])+'.exe')
                    if savingfile != None:
                        savingfile.write(requests.get(json['assets'][0]['browser_download_url']).content)
                        return True
                else:
                    pass

    except Exception:
        #ignoring any exceptions that rise from network errors (or, maybe, github rate limiting your ip)
        pass 











if __name__ == '__main__':
    import time
    print('Thats not how that works')
    time.sleep(10)