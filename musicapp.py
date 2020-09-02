from tkinter import *
import pygame
from tkinter import filedialog
import os
from mutagen.mp3 import MP3 # for finding total length of song
import time
from tkinter import ttk as ttk
root = Tk()
root.title("Music App")
root.geometry("600x400")
#initialising pygame mixer
pygame.mixer.init()
di = {}# to store directory of songs
totallen = 0
#FUnctions
def addsong():
    song = filedialog.askopenfilename(title = "Choose a song", initialdir = r" C:\Users\Jay Shah\Desktop\python\mp3")
    global di
    di = {}
    #print(directory,song)
    directory,songname = os.path.split(song)
    di[songname] = directory
    playlist.insert(END, songname)
    #print(song)

def addmultiple():
    songs = filedialog.askopenfilenames(title = "Choose multiple songs")
    global di
    for song in songs:
        directory,songname = os.path.split(song)
        di[songname] = directory
        playlist.insert(END, songname)
def playedlen():
    if stopped:
        return
    plen = pygame.mixer.music.get_pos()//1000
    #plen = int(slider.get())
    global di
    global paused
    convertedplen = time.strftime("%M:%S", time.gmtime(plen))
    cursong = playlist.curselection()
    song = playlist.get(ACTIVE)
    songname = di[song] + "/"+ song
    global totallen
    mutagensong = MP3(songname)
    totallen =  mutagensong.info.length
    convertedtotal = time.strftime("%M:%S", time.gmtime(totallen))

    #plen += 1
    if int(slider.get()) == totallen:
        statusbar.config(text=f"Time Elapsed: {convertedtotal}   of   {convertedtotal}  ")
    elif paused:
        pass
    elif plen == int(slider.get()):
        sliderpos = int(totallen)
        slider.config(to=sliderpos, value=int(slider.get()))
        convertedplen = time.strftime("%M:%S", time.gmtime(int(slider.get())))
        statusbar.config(text=f"Time Elapsed: {convertedplen}   of   {convertedtotal}  ")
    else:
        sliderpos = int(totallen)
        slider.config(to=sliderpos, value= int(slider.get()))
        convertedplen = time.strftime("%M:%S", time.gmtime(int(slider.get())))
        statusbar.config(text=f"Time Elapsed: {convertedplen}   of   {convertedtotal}  ")
        nextsec = int(slider.get()) + 1
        slider.config(value = nextsec)
    #slider.config(value = plen)
    #sliderlabel.config(text = plen)
    statusbar.after(1000,playedlen)

def play():
    global stopped
    stopped = False
    song = playlist.get(ACTIVE)
    global di
    global totallen
    songname = di[song] + "/" + song
    #print(songname)
    pygame.mixer.music.load(songname)
    pygame.mixer.music.play(loops = 0)#defines the number of times the song will play

    playedlen()
    #Updating the slider length and value
    slider.config(to=totallen, value=0)
global stopped
stopped = False
def stop():
    statusbar.config(text="Stopped Music")
    slider.config(value = 0)
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    statusbar.config(text = "Stopped Music")
    global stopped
    stopped = True
def forward():
    global di
    try:
        nextone = playlist.curselection()[0] + 1
        print(nextone)
        songname = playlist.get(nextone)
        songname = di[songname] + "/" + songname
        pygame.mixer.music.load(songname)
        pygame.mixer.music.play(loops=0)
        slider.config(value=0)
        playlist.selection_clear(0, END)
        playlist.activate(nextone)
        playlist.selection_set(nextone, last =None)
    except:
        pass

def back():
    global di
    try:
        prevone = playlist.curselection()[0] - 1
        #print(prevone)
        songname = playlist.get(prevone)
        songname = di[songname] + "/" + songname
        pygame.mixer.music.load(songname)
        pygame.mixer.music.play(loops=0)
        slider.config(value = 0)
        playlist.selection_clear(0, END)
        playlist.activate(prevone)
        playlist.selection_set(prevone, last =None)
    except:
        pass

def slide(x):
    #sliderlabel.config(text = f'{int(slider.get())} of {int(totallen)}')
    song = playlist.get(ACTIVE)
    global di
    songname = di[song] + "/" + song
    #print(songname)
    pygame.mixer.music.load(songname)
    pygame.mixer.music.play(loops=0, start = int(slider.get()))

def delete():
    stop()
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()
def deleteall():
    stop()
    playlist.delete(0, END)
    pygame.mixer.music.stop()
global paused
paused = False
def pause(ispaused):
    global paused
    global stopped
    stopped = False
    paused =  not ispaused
    if paused:
        pygame.mixer.music.pause()
        paused = True
    else:
        pygame.mixer.music.unpause()
        paused = False

#Listbox showcasing songs present
playlistl = Label(root, text = "Your Playlist")
playlistl.pack(pady=10)
playlist = Listbox(root, bg = "black", fg = "white", width = 100)
playlist.pack(pady=20)

#Song Slider displaying position of song played
slider = ttk.Scale(root,from_ = 0, to=100,orient = HORIZONTAL, value = 0,command = slide,length = 360)
slider.pack()
#sliderlabel = Label(root,text="0")
#sliderlabel.pack()


#Status Bar for song played and length
statusbar = Label(root, text= "", bd = 1, relief = GROOVE)
statusbar.pack(fill = X,pady = 5)

#Images for buttons
backbtnimg = PhotoImage(file = "previous.png")
playbtnimg = PhotoImage(file = "play.png")
pausebtnimg = PhotoImage(file = "pause.png")
stopbtnimg = PhotoImage(file = "stop.png")
forwardbtnimg = PhotoImage(file = "next.png")

#Frame for packing images
controlframe= Frame(root)
controlframe.pack()

#Making buttons for the images
backbtn = Button(controlframe, image =backbtnimg, borderwidth = 0, command = back)
playbtn = Button(controlframe, image =playbtnimg, borderwidth = 0, command = play)
pausebtn = Button(controlframe, image =pausebtnimg, borderwidth = 0, command = lambda: pause(paused))
stopbtn = Button(controlframe, image =stopbtnimg, borderwidth = 0, command = stop)
forwardbtn = Button(controlframe, image =forwardbtnimg, borderwidth = 0, command = forward)

#Packing the images in the control frame
backbtn.grid(row = 0, column = 1 )
playbtn.grid(row = 0, column = 2)
pausebtn.grid(row = 0, column = 3)
stopbtn.grid(row = 0, column = 4)
forwardbtn.grid(row = 0, column = 5)

#Creating a Menu
mainmenu = Menu(root)
root.config(menu = mainmenu)

addsongmenu = Menu(mainmenu)
mainmenu.add_cascade(label = "Add songs", menu = addsongmenu)
addsongmenu.add_command(label = "Add one song", command = addsong)
addsongmenu.add_command(label="Add multiple songs", command = addmultiple)

deletesongmenu = Menu(mainmenu)
mainmenu.add_cascade(label = "Delete Songs", menu = deletesongmenu)
deletesongmenu.add_command(label="Delete One Song", command = delete)
deletesongmenu.add_command(label = "Delete All songs", command = deleteall)

root.mainloop()