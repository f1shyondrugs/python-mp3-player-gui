import customtkinter as tk
import pygame
import random
import os
from customtkinter import filedialog
from functools import partial
import tkinter as ltk
from PIL import Image, ImageTk
from mutagen.mp3 import MP3

mp3_folder = "null"
paused = False

with open("config.txt", "r") as w:
    a = w.readlines()
    try:
        mp3_folder = a[0]
    except:
        mp3_folder = "null"



def start_and_change_color(song, button):
    start(song)
    
    for key, other_button in d.items():
        if key == song:
            other_button.configure(fg_color="#242424")  
        elif f'"{mp3_folder}/{key}"' == f'"{song}"':
            other_button.configure(fg_color="#242424")

        elif key == song:
            other_button.configure(fg_color="#242424")

        else:
            other_button.configure(fg_color="#1f6aa5")



def choose_folder():
    global mp3_folder
    global scrollable_frame
    mp3_folder = filedialog.askdirectory()
    pygame.init()
    pygame.mixer.music.stop()  


    scrollable_frame.destroy()

    scrollable_frame = tk.CTkFrame(master=root, width=770, height=660)
    scrollable_frame.place(x=200,y=20)

    folder_label = tk.CTkLabel(scrollable_frame, text="No Folder Selected.")
    folder_label.place(x=10,y=5)

    with open("config.txt", "w") as w:
        w.write(mp3_folder)


    global d
    global frame
    global command

    d = {}
    if mp3_folder != "null":
        folder_label.configure(text=f"{mp3_folder}")
        files = os.listdir(mp3_folder)
        mp3_files = [f for f in files if f.endswith('.mp3')]
        mp3_files.sort()
        y1=40

        for file in mp3_files:
            
            command = lambda f=file: start(f)
            frame = tk.CTkButton(scrollable_frame, anchor="w", width=720, height=35, text=f"{file}", command=command)
            frame.place(x=20,y=y1)

            frame.configure(command=partial(start_and_change_color, file, frame))
            frame.place(x=20, y=y1)
            d[str(file)] = frame
            y1 = y1 + 40   
    

def start(song):
    global playlist
    global current_song
    if not mp3_folder:
        folder_label.configure(text="Bitte wähle einen Ordner aus.")
        return

    playlist = [os.path.join(mp3_folder, mp3_file) for mp3_file in mp3_files]

    
    if song != "None":
        pygame.init()
        pygame.mixer.music.stop()
        if song[0] == "/":
            pygame.mixer.music.load(song)
            current_song = playlist.index(song)

        else:
            pygame.mixer.music.load(mp3_folder + "/" + song)
            current_song = playlist.index(mp3_folder + "/" + song)


        pygame.mixer.music.play()
        playbtn.configure(text="Stop", command=stop)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        

    else:
        if paused == True:
            pygame.mixer.music.unpause()
            playbtn.configure(text="Stop", command=stop)
            start_and_change_color(str(playlist[current_song]), playlist[current_song])


        else:
            pygame.init()
            current_song = 0
            pygame.mixer.music.load(playlist.pop(0))
            pygame.mixer.music.play()
            playbtn.configure(text="Stop", command=stop)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            start_and_change_color(str(playlist[current_song]), playlist[current_song])


def skip_song():
    global current_song
    pygame.mixer.music.stop()  
    current_song = (current_song + 1) % len(playlist)
    start_and_change_color(str(playlist[current_song]), playlist[current_song])
    pygame.mixer.music.load(playlist[current_song])  
    pygame.mixer.music.play()  


def previous_song():
    global current_song
    pygame.mixer.music.stop()  
    current_song = (current_song - 1) % len(playlist)
    start_and_change_color(str(playlist[current_song]), playlist[current_song])
    pygame.mixer.music.load(playlist[current_song]) 
    pygame.mixer.music.play()


def stop():
    global paused
    paused=True
    pygame.mixer.music.pause()
    playbtn.configure(text="Start", command=lambda: start("None"))


def slider_callback(value):
    pygame.init()
    pygame.mixer.music.set_volume(value)
    v = str(value)
    durlbl.configure(text=f"Volume: {v[:4]}/1")

def shuffle():
    global playlist
    random.shuffle(playlist)

root = tk.CTk()
root.minsize(1000,700)
root.maxsize(1000,1200)
root.title("MP3 Player")
image_icon = ltk.PhotoImage(file="img/musik-alt.png")
root.iconphoto(False, image_icon)

selectbtn = tk.CTkButton(root, text="Select MP3 Folder", command=choose_folder)
selectbtn.place(x=20, y=20)

selectbtn = tk.CTkButton(root, text="Shuffle deez songs", command=shuffle)
selectbtn.place(x=20, y=60)

slider_1 = tk.CTkSlider(master=root, command=slider_callback, from_=0, to=1, width=150)
slider_1.place(x=15, y=180)
slider_1.set(1)

durlbl = tk.CTkLabel(root, text="Volume: 1/1")
durlbl.place(x=20, y=200)

left = tk.CTkImage(Image.open("img/winkel-links.png"), size=(26, 26))
previousbtn = tk.CTkButton(master=root,image=left, width=65, text="", command=previous_song)
previousbtn.place(x=20, y=100)

right = tk.CTkImage(Image.open("img/winkel-rechts.png"), size=(26, 26))
skipbtn = tk.CTkButton(master=root, image=right, text="", width=65, command=skip_song)
skipbtn.place(x=95, y=100)

playbtn = tk.CTkButton(root, text="Start", command=lambda: start("None"))
playbtn.place(x=20, y=140)

scrollable_frame = tk.CTkFrame(master=root, width=770, height=1200)
scrollable_frame.place(x=200,y=20)

folder_label = tk.CTkLabel(scrollable_frame, text="No Folder Selected.")
folder_label.place(x=10,y=5)




d = {}
if mp3_folder != "null":
    folder_label.configure(text=f"{mp3_folder}")
    files = os.listdir(mp3_folder)
    mp3_files = [f for f in files if f.endswith('.mp3')]
    mp3_files.sort()
    y1=40
    playlist = [os.path.join(mp3_folder, mp3_file) for mp3_file in mp3_files]
    playlist.sort()


    for file in mp3_files:
        
        command = lambda f=file: start(f)
        frame = tk.CTkButton(scrollable_frame, anchor="w", width=720, height=35, text=f"{file}", command=command)
        frame.place(x=20,y=y1)

        frame.configure(command=partial(start_and_change_color, file, frame))
        frame.place(x=20, y=y1)
        d[str(file)] = frame
        y1 = y1 + 40   

root.mainloop()