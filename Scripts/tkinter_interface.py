import tkinter

class interface:
    def __init__(self,icondir,title,
                 windowsize: tuple = (250,24),
                 ):
        root = tkinter.Tk()
        root.withdraw()
        root.iconbitmap(icondir) #for filedialog icon to show
        root.attributes("-topmost", True)
            
        root.title(title)
        root.geometry(str(windowsize[0])+'x'+str(windowsize[1])) 
        root.geometry('+'+str((root.winfo_screenwidth()//2)-(windowsize[0]//2))+
                      '+'+str((root.winfo_screenheight()//2)-(windowsize[1]//2)))
        self.root = root
    

    def show(self):
        self.root.deiconify()
    def hide(self):
        self.root.withdraw()



    def choosefromlist_loop(self,list1: list) -> str:

        listbox = tkinter.Listbox(self.root, selectmode=tkinter.SINGLE, height=len(list1),width=1000)
        listbox.pack(pady=0)
        for i in list1:
            listbox.insert(tkinter.END, i)

        confirm_button = tkinter.Button(self.root, text="Confirm", command=self.root.quit,width=1000)
        confirm_button.pack(pady=0)

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        self.root.mainloop()

        try:
            string = listbox.get((listbox.curselection()))
        except Exception:
            self.root.destroy()
            return None

        self.root.destroy()

        if len(string) > 0:
            return string
        else:
            return None

        