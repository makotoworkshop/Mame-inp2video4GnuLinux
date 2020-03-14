#!/usr/bin/env python3.6.8
# coding: utf-8
#####################################################################
################## Mame inp to video for GNU/Linux ##################
# Convertir les parties de jeux enregistrée par mame (inp) en vidéo #
#####################################################################
#http://burogu.makotoworkshop.org/#
# QFTIF :
#ok- Demander le chemin des roms, des inp, le nom de l'inp
# Un mode aviwrite et un mode mngwrite
#ok- rejouer l'inp en mode fenétré pour générer ou l'avi ou bien le mng (+wav)
#ok- soit à partir du avi compresser la vidéo en x264 ou x265, 
#ok- soit à partir du mgg, génerer les png et le wav, puis compresser la vidéo en x264 ou x265.
#- Demander la résolution et-ou le ratio du jeu pour l'encodage
#- Demander pour suppression des temporaires avant de quitter et au démarrage si détecté.
#- Check si Arborescence existe au démarrage
        # Arborescence :
        # Mame-inp2video4GnuLinux/softs/mame/  -> pgm mame64_0208
        # Mame-inp2video4GnuLinux/MediaTMP/  ->  fichier avi et mng + wav
        # Mame-inp2video4GnuLinux/MediaTMP/PngTMP -> fichiers png
        # Mame-inp2video4GnuLinux/Videos -> fichiers x264 ou x265
#- Alerter si l'inp ne correspond pas à la rom
#- incruster mame dans l'UI

# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://docs.python.org/3.9/library/dialog.html
# https://docs.python.org/fr/3/library/re.html
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, re, getpass, time

# fenêtre principale de l'application
fenetre = Tk()
fenetre.title('Mame inp to video for GNU/Linux')
fenetre.geometry('1365x700')
fenetre['bg']='slate gray'

USER = getpass.getuser()
MessageTexte = StringVar()
cheminROM = ''
cheminRomsForder = ''
cheminINP = ''
cheminInpFolder = ''
nomJEU = ''
FichierINP = ''
cheminSNAP = '/home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/MediaTMP'    # fixe
#cheminROMS = '$HOME/.advance/roms'
#cheminINP = '/home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/softs' # déduire le nom de l'inp avec le chemin
#file_path = os.path.join(current_directory,file_name)

####
#def RomsFolder():
#    global cheminROM
#    cheminROM = filedialog.askdirectory(initialdir='/home/'+USER, title='Choisissez un repertoire')
#    if len(cheminROM) > 0:
#        print ("vous avez choisi le repertoire %s" % cheminROM)
#        RomLabel = Label(fenetre, text=cheminROM)
#        RomLabel.pack()
#        RomLabel.place(x=150, y=25)

def RomsFile(): # récupére le chemin des roms et le nom du jeu
    global cheminROM
    global cheminRomsForder
    global nomJEU
    cheminROM = filedialog.askopenfilename(initialdir='/home/'+USER, title="Ouvrir un fichier rom mame",filetypes=[('zip files','.zip'),('all files','.*')])
    if len(cheminROM) > 0:
        print ("vous avez choisi la rom: %s" % cheminROM)
        RomLabel02 = Label(fenetre, text='-> '+cheminROM,font='Monospace 16 bold',borderwidth=3,bg='slate gray')
        RomLabel02.pack()
        RomLabel02.place(x=320, y=55)

        var1 = re.split(r'\W+',cheminROM)
        nomJEU = var1[len(var1)-2]
        print ('nomJEU: ',nomJEU)

        var2 = re.search(nomJEU+'.zip',cheminROM)
        cheminRomsForder = cheminROM[:var2.start()] + cheminROM[var2.end():]
        print ('cheminRomsForder: ',cheminRomsForder)

        Bouton_InpPath.configure(state='normal')
        message01()


def InpFile():  # récupére le chemin des inp et le nom de l'inp
    global cheminINP
    global cheminInpFolder
    global FichierINP
    cheminINP = filedialog.askopenfilename(initialdir='.',title="Ouvrir un fichier d'input mame",filetypes=[('inp files','.inp'),('all files','.*')])
    if len(cheminINP) > 0:
        print ("vous avez choisi le fichier: %s" % cheminINP)
        InpLabel02 = Label(fenetre, text='-> '+cheminINP,font='Monospace 16 bold',borderwidth=3,bg='slate gray')
        InpLabel02.pack()
        InpLabel02.place(x=320, y=105)

        var1 = re.split(r'\W+',cheminINP)
        FichierINP = var1[len(var1)-2] + '.inp'
        print ('FichierINP: ',FichierINP)

        var2 = re.search(FichierINP,cheminINP)
        cheminInpFolder = cheminINP[:var2.start()] + cheminINP[var2.end():]
        print ('cheminInpFolder: ',cheminInpFolder)

        Bouton_playbackMNG.configure(state='normal')
        Bouton_playbackAVI.configure(state='normal')
        message02()

#################
# Commande MAME #
#################
def playback():
    os.chdir('softs/mame/')
    os.system('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' '+nomJEU+' -playback '+FichierINP)
#softs/mame/mame64_0208 -rompath $HOME/.advance/roms -input_directory /home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/softs espgal -playback test.inp


def playbackAVI():
    Bouton_RomPath.configure(state='disabled')
    Bouton_InpPath.configure(state='disabled')
    Bouton_playbackMNG.configure(state='disabled')
    message03a()
    fenetre.update()
    os.chdir('softs/mame/')
    os.system('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -aviwrite '+nomJEU+'.avi -exit_after_playback -skip_gameinfo -window')
    print('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -aviwrite '+nomJEU+'.avi -exit_after_playback -skip_gameinfo -window')
#softs/mame/mame64_0208 -rompath $HOME/.advance/roms -input_directory /home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/softs -snapshot_directory /home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/MediaTMP espgal -playback test.inp -aviwrite ma_partie.avi -exit_after_playback -skip_gameinfo -window
    Bouton_playbackAVI.configure(state='disabled')

def playbackMNG():
    Bouton_RomPath.configure(state='disabled')
    Bouton_InpPath.configure(state='disabled')
    Bouton_playbackAVI.configure(state='disabled')
    message03b()
    fenetre.update()
 #   time.sleep(3)
    os.chdir('softs/mame/')
    os.system('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -wavwrite '+cheminSNAP+'/'+nomJEU+'.wav -mngwrite '+nomJEU+'.mng -exit_after_playback -skip_gameinfo -window')
    print('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -wavwrite '+cheminSNAP+'/'+nomJEU+'.wav -mngwrite '+nomJEU+'.mng -exit_after_playback -skip_gameinfo -window')
# mame nom_de_la_rom -playback ma_partie.inp -wavwrite ~/.mame/snap/ma_partie.wav -mngwrite ma_partie.mng -exit_after_playback
    Bouton_playbackMNG.configure(state='disabled')
    png()
# afficher status et sablier

###########################
# Commande encodage Vidéo #
###########################

def png():
    message03c()
    fenetre.update()
    os.chdir('../../MediaTMP/PngTMP')
    os.system('advmng -xn ../'+nomJEU+'.mng')
# advmng -xn ../$partie.mng
    Bouton_EncodageX264.configure(state='normal')
    message04a()

def x264():
    message04b()
    fenetre.update()
    os.system('mencoder mf://*.png -mf type=png:fps=60 -ovc lavc -lavcopts vcodec=mpeg4:aspect=3/4:vqscale=2 -oac mp3lame -lameopts cbr:br=128 -audiofile ../'+nomJEU+'.wav -o ../../Videos/'+nomJEU+'.mp4')
# mencoder mf://*.png -mf type=png:fps=60 -ovc lavc -lavcopts vcodec=mpeg4:aspect=3/4:vqscale=2 -oac mp3lame -lameopts cbr:br=128 -audiofile ma_partie.wav -o ma_partie.mp4
    Bouton_EncodageX264.configure(state='disabled')
    message05()


#####################
# Boutons d'actions #
#####################

Bouton_RomPath = Button(fenetre,text="Choisir une ROM",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=RomsFile)
Bouton_RomPath.pack()
Bouton_RomPath.place(x=90, y=50)
#Bouton_RomPath.configure(state='disabled')
Bouton_RomPath.configure(state='normal')

Bouton_InpPath = Button(fenetre,text="Choisir un inp",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=InpFile)
Bouton_InpPath.pack()
Bouton_InpPath.place(x=90, y=100)
Bouton_InpPath.configure(state='disabled')
#Bouton_InpPath.configure(state='normal')

Bouton_playbackAVI = Button(fenetre,text="Rejouer vers AVI",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=playbackAVI)
Bouton_playbackAVI.pack()
Bouton_playbackAVI.place(x=90, y=200)
Bouton_playbackAVI.configure(state='disabled')
#Bouton_playbackAVI.configure(state='normal')

Bouton_playbackMNG = Button(fenetre,text="Rejouer vers MNG",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=playbackMNG)
Bouton_playbackMNG.pack()
Bouton_playbackMNG.place(x=450, y=200)
Bouton_playbackMNG.configure(state='disabled')
#Bouton_playbackMNG.configure(state='normal')

#Bouton_PngConvert = Button(fenetre,text="Conversion PNG",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=png)
#Bouton_PngConvert.pack()
#Bouton_PngConvert.place(x=80, y=165)
#Bouton_PngConvert.configure(state='disabled')
#Bouton_PngConvert.configure(state='normal')

Bouton_EncodageX264 = Button(fenetre,text="EncodageX264",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=x264)
Bouton_EncodageX264.pack()
Bouton_EncodageX264.place(x=90, y=250)
Bouton_EncodageX264.configure(state='disabled')
#Bouton_EncodageX264.configure(state='normal')

##########
# Labels #
##########
Titre01 = Label(fenetre, text='Prérequis:',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Titre01.pack()
Titre01.place(x=5, y=10)

Label01 = Label(fenetre, text='01 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label01.pack()
Label01.place(x=20, y=55)

Label02 = Label(fenetre, text='02 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label02.pack()
Label02.place(x=20, y=105) 

Titre02 = Label(fenetre, text='Préférences:',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Titre02.pack()
Titre02.place(x=5, y=155)

Label03 = Label(fenetre, text='03 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label03.pack()
Label03.place(x=20, y=205) 

Label04 = Label(fenetre, text='04 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label04.pack()
Label04.place(x=20, y=255) 

################
# Zone Message #
################
ZoneMessage = PanedWindow(fenetre, orient=HORIZONTAL, bg="light gray")
ZoneMessage.pack(expand=NO, fill=X, padx=20, pady=306)

#def message():    # zone de texte
msg = Label(ZoneMessage, textvariable=MessageTexte, font=('Arial Bold',25), bg='gray')
MessageTexte.set("Choisissez un jeux Mame\n")
msg.pack(fill=BOTH)

def message01():
    MessageTexte.set("Choisissez maintenant le fichier,\nde la partie sauvegardée")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message02():
    MessageTexte.set("Lancer maintenant la capture de la vidéo\nAVI (rapide/très gros fichier) ou MNG (très lent/fichier léger)")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03a():
    MessageTexte.set("Ouverture de la fenêtre Mame, validez si besoin…\nCapture AVI en cours, Veuillez patienter")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03b():
    MessageTexte.set("Ouverture de la fenêtre Mame, validez si besoin…\nCapture MNG+WAV en cours, Veuillez patienter")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03c():
    MessageTexte.set("Capture terminée,\nConversion MNG vers PNG en cours, Veuillez patienter")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message04a():
    MessageTexte.set("Choisissez le type de compression vidéo\nOu disposez dés maintenant des fichiers brut dans le dossier temporaire")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message04b():
    MessageTexte.set("Compression vidéo en cours…\n")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message05():
    MessageTexte.set("Opérations terminées !\n")
    msg.configure(font=('Arial Bold',25), bg='gray')

fenetre.mainloop()
