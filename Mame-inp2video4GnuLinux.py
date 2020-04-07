#!/usr/bin/env python3.6.8
# coding: utf-8
#####################################################################
################## Mame inp to video for GNU/Linux ##################
# Convertir les parties de jeux enregistrée par mame (inp) en vidéo #
#####################################################################
#http://burogu.makotoworkshop.org/#
# QFTIF :
#ok- Demander le chemin des roms, des inp, le nom de l'inp
#ok- Un mode aviwrite et un mode mngwrite
#ok- rejouer l'inp en mode fenétré pour générer ou l'avi ou bien le mng (+wav)
#ok- soit à partir du avi compresser la vidéo en x264 ou x265, 
#ok- soit à partir du mgg, génerer les png et le wav, puis compresser la vidéo en x264 ou x265.
#ok- Demander le ratio du jeu pour l'encodage vidéo 4/3 ou 3/4 (Tate ou Yoko)
#ok- Check si Arborescence existe au démarrage
        # Arborescence :
        # Mame-inp2video4GnuLinux/softs/mame/  -> pgm mame64_0208
        # Mame-inp2video4GnuLinux/MediaTMP/  ->  fichier avi et mng + wav
        # Mame-inp2video4GnuLinux/MediaTMP/PngTMP -> fichiers png
        # Mame-inp2video4GnuLinux/Videos -> fichiers x264 ou x265
#ok- lancer mame en petite fenetre
#ok- indiquer le poid des fichiers temps et proposer la suppression avec un bouton
#ok- Coche pour compression vidéo automatique
#ok- réinitialiser tout
#ok- Alerter si l'inp ne correspond pas à la rom et réinitialiser.
#ok- cheminSNAP à revoir ?
#ok- tkinter récuperer position de la fenétre, pour que le popup apparaisse tjrs à sa place, même après avoir déplacer la fenétre du pgm
#ok- différentier un dossier png par nom de jeu
#ok- changer bouton et message popup en cas de mauvais inp/rom
#- sablier progression % de l'extraction png, avec nombre de frames extraites indiquée par mame en fin de playback
#- tester la présence d'advmng    /usr/bin/advmng  echo $PATH   dpkg --status advancecomp
#- incruster le terminal dans l'ui ?
#- coller des try partout…


# https://python.doctor/page-tkinter-interface-graphique-python-tutoriel
# https://docs.python.org/3.9/library/dialog.html
# https://docs.python.org/fr/3/library/re.html
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, re, getpass, time, shutil, glob
from threading import Thread

### Fichier Log
#log = open('log', 'w') 
#sys.stdout = log


# fenêtre principale de l'application
fenetre = Tk()
fenetre.title('Mame inp to video for GNU/Linux')
#fenetre.geometry('1300x450+300+300')
# Placement de la fenêtre du pgm
width = 1300
height = 450
offsetX = 0
offsetY = 600
fenetre.geometry('%dx%d+%d+%d' % (width, height, offsetX, offsetY))
fenetre['bg']='slate gray'

USER = getpass.getuser()
MessageTexte = StringVar()
cheminROM = ''
cheminRomsForder = ''
cheminINP = ''
cheminInpFolder = ''
nomJEU = ''
FichierINP = ''
cheminSNAP = os.path.dirname(os.path.abspath('MediaTMP'))+'/MediaTMP'
Aspect = StringVar()
poidTMP = StringVar()
Resolution ='320x240'
MarqueurChoix = 0
EtatCheck_Box = IntVar ()
LogfileName = 'inp2video.log'
ligneLOG = ''
NBimages = ''
#NumberOfLine = IntVar()

def ArborescenceExisteTelle():
    now = time.localtime(time.time())
    print('[LOG] : '+ time.strftime("%Y-%m-%d %H:%M:%S"+' | Fonction ArborescenceExisteTelle :', now))
#    os.system('pwd')
    if not os.path.isfile('softs/mame/mame64_0208'):
        print('[LOG] : emulateur introuvable')
        message06()
        os.makedirs('softs/mame', exist_ok=True)
    os.makedirs('MediaTMP', exist_ok=True)
    os.makedirs('Videos', exist_ok=True)

 
# Récupére la taille des fichiers temporaires
def getTotalSizeTEMP(): 
    print('[LOG] : Fonction getTotalSizeTEMP :')
#    os.system('pwd')
    print ("")
    print ("[LOG] : Listage des fichiers temporaire en cours :")
    print ("")
  #  global poidTMP
    poidfiles = 0
 #   print ("recurssif SIZE")
    for root, dirs, files in os.walk('MediaTMP/'):	# liste les fichiers récursivement
        for filename in files:
         #   print(filename)
            poidfiles += os.path.getsize(os.path.join(root, filename))
       #     print (poidfiles)

    if poidfiles > 1073741824:   # Gio
        poid = str(round((poidfiles/1024/1024/1024),2)) + ' Gio'
        print("[LOG] : poid %s" %poid)
    elif poidfiles > 1048576:    # Mio
        poid = str(round((poidfiles/1024/1024),2)) + ' Mio'
        print("[LOG] : poid %s" %poid)
    elif poidfiles > 1024:       # Kio
        poid = str(round((poidfiles/1024),2)) + ' kio'
        print("[LOG] : poid %s" %poid)
    else:
        poid = str(poidfiles) + ' io'
        print("[LOG] : poid %s" %poid)
 #   return poidTMP
    poidTMP.set(poid)


def SupprimerTMP():
    print('[LOG] : Fonction SupprimerTMP :')
#    os.system('pwd')
    shutil.rmtree('MediaTMP')
    ArborescenceExisteTelle()
    getTotalSizeTEMP()
    TestpoidTMP()

def TestpoidTMP():
    print(poidTMP.get())
    if poidTMP.get() == '0 io':
        Bouton_SupprimerTMP.configure(state='disabled')

####
def RomsFile(): # récupére le chemin des roms et le nom du jeu
    global cheminROM
    global cheminRomsForder
    global nomJEU
    cheminROM = filedialog.askopenfilename(initialdir='/home/'+USER, title="Ouvrir un fichier rom mame",filetypes=[('zip files','.zip'),('all files','.*')])
    if len(cheminROM) > 0:
        print ("[LOG] : vous avez choisi la rom: %s" % cheminROM)
        RomLabel02.configure(text='-> '+cheminROM,font='Monospace 12 bold',borderwidth=3,bg='slate gray')

        var1 = re.split(r'\W+',cheminROM)
        nomJEU = var1[len(var1)-2]
        print ('[LOG] : nomJEU: ',nomJEU)

        var2 = re.search(nomJEU+'.zip',cheminROM)
        cheminRomsForder = cheminROM[:var2.start()] + cheminROM[var2.end():]
        print ('[LOG] : cheminRomsForder: ',cheminRomsForder)

        Bouton_InpPath.configure(state='normal')
        message01()


def InpFile():  # récupére le chemin des inp et le nom de l'inp
    global cheminINP
    global cheminInpFolder
    global FichierINP
    cheminINP = filedialog.askopenfilename(initialdir='.',title="Ouvrir un fichier d'input mame",filetypes=[('inp files','.inp'),('all files','.*')])
    if len(cheminINP) > 0:
        print ("[LOG] : vous avez choisi le fichier: %s" % cheminINP)
        InpLabel02.configure(text='-> '+cheminINP,font='Monospace 12 bold',borderwidth=3,bg='slate gray')

        var1 = re.split(r'\W+',cheminINP)
        FichierINP = var1[len(var1)-2] + '.inp'
        print ('[LOG] : FichierINP: ',FichierINP)

        var2 = re.search(FichierINP,cheminINP)
        cheminInpFolder = cheminINP[:var2.start()] + cheminINP[var2.end():]
        print ('[LOG] : cheminInpFolder: ',cheminInpFolder)

        Bouton_playbackMNG.configure(state='normal')
        Bouton_playbackAVI.configure(state='normal')
        message02()

#################
# Commande MAME #
#################

def playbackAVI():
    global MarqueurChoix
    print ('[LOG] Resolution : ',Resolution)
    Bouton_RomPath.configure(state='disabled')
    Bouton_InpPath.configure(state='disabled')
    Bouton_playbackMNG.configure(state='disabled')
    Bouton_SupprimerTMP.configure(state='disabled')
    message03a()
    fenetre.update()
    os.chdir('softs/mame/')
    print('[LOG] : Fonction playbackAVI :')
#    os.system('pwd')
    print('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -aviwrite '+nomJEU+'.avi -resolution '+Resolution+' -exit_after_playback -skip_gameinfo -window')
    os.system('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -aviwrite '+nomJEU+'.avi -resolution '+Resolution+' -exit_after_playback -skip_gameinfo -window  > ../../playback.log')
#softs/mame/mame64_0208 -rompath $HOME/.advance/roms -input_directory /home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/softs -snapshot_directory /home/makoto/Documents/Python/Dev_Python/Mame-inp2video4GnuLinux/MediaTMP espgal -playback test.inp -aviwrite ma_partie.avi -exit_after_playback -skip_gameinfo -window
    os.chdir('../../')
    print('[LOG] : Fonction playbackAVI FIN :')
#    os.system('pwd')
    message04a()
    Bouton_playbackAVI.configure(state='disabled')
    Bouton_EncodageX264.configure(state='normal')
    getTotalSizeTEMP()
    MarqueurChoix = 1   # pour le bouton encodage manuel
    if rapport() != 'ERROR':
        EncodageAuto('AVI')


def playbackMNG():
    global NBimages
    Bouton_RomPath.configure(state='disabled')
    Bouton_InpPath.configure(state='disabled')
    Bouton_playbackAVI.configure(state='disabled')
    Bouton_SupprimerTMP.configure(state='disabled')
    message03b()
    fenetre.update()
 #   time.sleep(3)
    os.chdir('softs/mame/')
    print('[LOG] : Fonction playbackMNG :')
#    os.system('pwd')
    print('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -wavwrite '+cheminSNAP+'/'+nomJEU+'.wav -mngwrite '+nomJEU+'.mng -resolution '+Resolution+' -exit_after_playback -skip_gameinfo -window')
    os.system('./mame64_0208 -rompath '+cheminRomsForder+' -input_directory '+cheminInpFolder+' -snapshot_directory '+cheminSNAP+' '+nomJEU+' -playback '+FichierINP+' -wavwrite '+cheminSNAP+'/'+nomJEU+'.wav -mngwrite '+nomJEU+'.mng -resolution '+Resolution+' -exit_after_playback -skip_gameinfo -window > ../../playback.log')
# 1>/dev/pts/1
# mame nom_de_la_rom -playback ma_partie.inp -wavwrite ~/.mame/snap/ma_partie.wav -mngwrite ma_partie.mng -exit_after_playback
    os.chdir('../../')
    print('[LOG] : Fonction playbackMNG FIN :')
#    os.system('pwd')
    Bouton_playbackMNG.configure(state='disabled')
    getTotalSizeTEMP()
    if rapport() != 'ERROR':
        NBimages = rapport()
        print('NBimages : ',NBimages)
        png()
# afficher status et sablier

def rapport():	# Analyse playbackMNG.log pour réccupérer le nombre de frame jouées
    global ligneLOG
#    fichierlog = open('playback.log', 'r', encoding='iso-8859-15')  # ouvre le fichier en lecture
    playbacklog = open('playback.log', 'r', encoding='utf-8')  # ouvre le fichier en lecture
    ligneLOG=playbacklog.readline()       # lit la première ligne du fichier tempolog et stocke dans la variable ligne
    ligneLOG=playbacklog.readline()   # lit la deuxième ligne
    ligneLOG=playbacklog.readline()   # lit la troisième ligne
    ligneLOG=playbacklog.readline()   # lit la quatrième ligne
    ligneLOG=playbacklog.readline()   # lit la cinquième ligne
    ligneLOG=playbacklog.readline()   # lit la sixième ligne
    playbacklog.close()              # ferme le fichier

    nbFrames=ligneLOG.split()
    nbFrames.append('x')    # ajout arbitraire pour ralonger la phrase et permettre le prochain test if sur le 6 ième emplacement du tableau
    nbFrames.append('x')
    nbFrames.append('x')
    if nbFrames[6] == 'not':    # Input file is for machine 'espgal', not for current machine 'agallet'
        print('[LOG] : ERROR = ',ligneLOG)
        message07()
        PopupERREUR() # Reinit
        return 'ERROR'
    else:
#        print('[LOG] : Nombre de frames jouées = ', nbFrames[3])    # Total playback frames: 223
        return nbFrames[3]




###########################
# Commande encodage Vidéo #
###########################

def png():
    message03c()
    fenetre.update()
    print('[LOG] : Fonction png :')
    try:
        os.mkdir('MediaTMP/'+nomJEU)
    except FileExistsError:
        for filename in glob.glob(r'MediaTMP/'+nomJEU+'/*.png'):
            os.remove(filename) 

    os.chdir('MediaTMP/'+nomJEU)
    print('pwd png advmng :')
#    os.system('pwd')
    TailThread.start()  ####
    os.system('advmng -xn ../'+nomJEU+'.mng >> advmngLOG') #  1>/dev/pts/1
    os.chdir('../../')
#    os.system('pwd')
    Bouton_EncodageX264.configure(state='normal')
    message04a()
    getTotalSizeTEMP()
    EncodageAuto('PNG')


def x264FromPNG():
    print('[LOG] : Fonction x264FromPNG :')
#    os.system('pwd')
    message04b()
    fenetre.update()
    os.system('mencoder mf://MediaTMP/'+nomJEU+'/*.png -mf type=png:fps=60 -ovc lavc -lavcopts vcodec=mpeg4:aspect='+Aspect.get()+':vqscale=2 -oac mp3lame -lameopts cbr:br=128 -audiofile MediaTMP/'+nomJEU+'.wav -o Videos/'+nomJEU+'.mp4') # 1>/dev/pts/1
# mencoder mf://*.png -mf type=png:fps=60 -ovc lavc -lavcopts vcodec=mpeg4:aspect=3/4:vqscale=2 -oac mp3lame -lameopts cbr:br=128 -audiofile ma_partie.wav -o ma_partie.mp4
    Bouton_EncodageX264.configure(state='disabled')
    PopupFIN() # Reinit


def x264FromAVI():
    message04b()
    fenetre.update()
    print('[LOG] : Fonction x264FromAVI :')
#    os.system('pwd')
    os.system('mencoder MediaTMP/'+nomJEU+'.avi -ovc lavc -lavcopts vcodec=mpeg4:aspect='+Aspect.get()+':vqscale=2 -oac mp3lame -lameopts cbr:br=128 -o Videos/'+nomJEU+'.mp4') #  1>/dev/pts/1
# mencoder mf://*.png -mf type=png:fps=60 -ovc lavc -lavcopts vcodec=mpeg4:aspect=3/4:vqscale=2 -oac mp3lame -lameopts cbr:br=128 -audiofile ma_partie.wav -o ma_partie.mp4
    Bouton_EncodageX264.configure(state='disabled')
    PopupFIN() # Reinit


def Encodagex264():
    global MarqueurChoix
    if MarqueurChoix == 1:
        print('[LOG] : MarqueurChoix = ', MarqueurChoix)
        x264FromAVI()
        MarqueurChoix = 0
    else:
        x264FromPNG()
    getTotalSizeTEMP()
    Bouton_SupprimerTMP.configure(state='normal')
    message05()

def EncodageAuto(param):
    if EtatCheck_Box.get() == 1:
        print('[LOG] : EtatCheck_Box =',EtatCheck_Box.get())
        if param == 'AVI':
            x264FromAVI()
        elif param == 'PNG':
            x264FromPNG()
    getTotalSizeTEMP()
    Bouton_SupprimerTMP.configure(state='normal')
    message05()

#####################
# Boutons d'actions #
#####################
# Boutons Radio #
#################
#def callbackRadio1(event):
def callbackRadio1():
    global Resolution
#    print ("clicked at", event.x, event.y)
    Resolution = '320x240'
    print ('[LOG] : Resolution = ',Resolution)

Radio1 = Radiobutton(fenetre, text='Yoko 4/3',font='Monospace 16 bold',variable=Aspect,value='4/3',command=callbackRadio1,borderwidth=1,background='slate gray',activebackground='lime green',selectcolor='lime green',highlightthickness=0,indicatoron=0) 
#Radio1.bind("<Button-1>", callbackRadio1)
Radio1.pack()
Radio1.select()    # Valeur par défaut
Radio1.place(x=655, y=225)

#def callbackRadio2(event):
def callbackRadio2():
    global Resolution
#    print ("clicked at", event.x, event.y)
    Resolution = '240x320'
    print ('[LOG] : Resolution = ',Resolution)

Radio2 = Radiobutton(fenetre, text='Tate 3/4',font='Monospace 16 bold',variable=Aspect, value='3/4',command=callbackRadio2,borderwidth=1,background='slate gray',activebackground='lime green',selectcolor='lime green',highlightthickness=0,indicatoron=0) 
#Radio2.bind("<Button-1>", callbackRadio2)
Radio2.pack()
Radio2.place(x=780, y=225)
#labelValue = Label(fenetre, textvariable=Aspect)
#labelValue.pack()


# Check Box #
#############

Check_Box = Checkbutton(fenetre, variable = EtatCheck_Box, text='Encodage Vidéo automatique ',font='Monospace 12 bold',bg='slate gray',activebackground='slate gray',activeforeground='lime green',highlightbackground='lime green',highlightthickness=2)
Check_Box.pack(anchor='w', padx=10)
Check_Box.place(x=600, y=328)
Check_Box.select()


# Boutons #
###########
Bouton_RomPath = Button(fenetre,text="Choisir une ROM",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=RomsFile)
Bouton_RomPath.pack()
Bouton_RomPath.place(x=90, y=120)
#Bouton_RomPath.configure(state='disabled')
Bouton_RomPath.configure(state='normal')

Bouton_InpPath = Button(fenetre,text="Choisir un inp",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=InpFile)
Bouton_InpPath.pack()
Bouton_InpPath.place(x=90, y=170)
Bouton_InpPath.configure(state='disabled')
#Bouton_InpPath.configure(state='normal')

Bouton_playbackAVI = Button(fenetre,text="Rejouer vers AVI",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=playbackAVI)
Bouton_playbackAVI.pack()
Bouton_playbackAVI.place(x=90, y=320)
Bouton_playbackAVI.configure(state='disabled')
#Bouton_playbackAVI.configure(state='normal')

Bouton_playbackMNG = Button(fenetre,text="Rejouer vers MNG",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=playbackMNG)
Bouton_playbackMNG.pack()
Bouton_playbackMNG.place(x=350, y=320)
Bouton_playbackMNG.configure(state='disabled')
#Bouton_playbackMNG.configure(state='normal')

#Bouton_PngConvert = Button(fenetre,text="Conversion PNG",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=png)
#Bouton_PngConvert.pack()
#Bouton_PngConvert.place(x=80, y=165)
#Bouton_PngConvert.configure(state='disabled')
#Bouton_PngConvert.configure(state='normal')

Bouton_EncodageX264 = Button(fenetre,text="EncodageX264",font='Monospace 16 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=Encodagex264)
Bouton_EncodageX264.pack()
Bouton_EncodageX264.place(x=90, y=370)
Bouton_EncodageX264.configure(state='disabled')
#Bouton_EncodageX264.configure(state='normal')

Bouton_SupprimerTMP = Button(fenetre,text="SupprimerTMP",font='Monospace 12 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=SupprimerTMP)
Bouton_SupprimerTMP.pack()
Bouton_SupprimerTMP.place(x=1100, y=400)
#Bouton_SupprimerTMP.configure(state='disabled')
Bouton_SupprimerTMP.configure(state='normal')


##########
# Labels #
##########
def ChangeText(DeQui):
   DeQui.config(text = '')

Titre01 = Label(fenetre, text='Prérequis:',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Titre01.pack()
Titre01.place(x=5, y=80)

Label01_01 = Label(fenetre, text='01 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label01_01.pack()
Label01_01.place(x=20, y=125)

RomLabel02 = Label(fenetre, text='',font='Monospace 12 bold',borderwidth=3,bg='slate gray')
RomLabel02.pack()
RomLabel02.place(x=320, y=125)

Label01_02 = Label(fenetre, text='02 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label01_02.pack()
Label01_02.place(x=20, y=175) 

InpLabel02 = Label(fenetre, text='',font='Monospace 12 bold',borderwidth=3,bg='slate gray')
InpLabel02.pack()
InpLabel02.place(x=320, y=175)

Label01_03 = Label(fenetre, text="03 - S'agit'il d'un jeu Horizontal ou Vertical :",font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label01_03.pack()
Label01_03.place(x=20, y=225) 

Titre02 = Label(fenetre, text='Préférences:',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Titre02.pack()
Titre02.place(x=5, y=275)

Label02_01 = Label(fenetre, text='04 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label02_01.pack()
Label02_01.place(x=20, y=325) 

Label02_02 = Label(fenetre, text='05 -',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label02_02.pack()
Label02_02.place(x=20, y=375) 

Label02_03 = Label(fenetre, text='Les fichiers temporaires occupent :',font='Monospace 16 bold',borderwidth=3,bg='slate gray')
Label02_03.pack()
Label02_03.place(x=500, y=400) 

TEMPFilesLabel = Label(fenetre, textvariable=poidTMP)
TEMPFilesLabel.pack()
TEMPFilesLabel.place(x=1000, y=400)

SablierLabel = Label(fenetre, textvariable=NBimages)
SablierLabel.pack()
SablierLabel.place(x=1000, y=360)

################
# Zone Message #
################
ZoneMessage = PanedWindow(fenetre, orient=HORIZONTAL, bg="light gray")
#ZoneMessage.pack(expand=YES, fill=X, padx=20, pady=306)
ZoneMessage.pack(fill=X,padx=20)

#def message():    # zone de texte
msg = Label(ZoneMessage, textvariable=MessageTexte, font=('Arial Bold',25), bg='gray')
MessageTexte.set("Choisissez un jeux Mame\n")
msg.pack(fill=BOTH)

def message00():
    MessageTexte.set("Choisissez un jeux Mame\n")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message01():
    MessageTexte.set("Choisissez maintenant le fichier,\nde la partie sauvegardée")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message02():
    MessageTexte.set("Lancer maintenant la capture de la vidéo\nAVI (rapide/très gros fichier) ou MNG (très lent/fichier léger)")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03a():
    MessageTexte.set("Ouverture de la fenêtre Mame, validez si besoin…\nCapture AVI en cours, Veuillez patienter !")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03b():
    MessageTexte.set("Ouverture de la fenêtre Mame, validez si besoin…\nCapture MNG+WAV en cours, Veuillez patienter !")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message03c():
    MessageTexte.set("Capture terminée,\nConversion MNG vers PNG en cours, Veuillez patienter !")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message04a():
    MessageTexte.set("Capture terminée ! Prêt pour la compression vidéo,\nOu disposez dés maintenant des fichiers bruts dans le dossier temporaire")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message04b():
    MessageTexte.set("Compression vidéo en cours…\n")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message05():
    MessageTexte.set("Opérations terminées !\nLe fichier est dans le dossier Videos")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message06():
    MessageTexte.set("! EMULATEUR INTROUVABLE !\n")
    msg.configure(font=('Arial Bold',25), bg='gray')

def message07():
    MessageTexte.set(ligneLOG)
    msg.configure(font=('Arial Bold',25), bg='red')


#################################
# Popup de fin d'erreur/relance #
#################################
class PopupERREUR(Canvas):
    def __init__(self):
        Canvas.__init__(self)
        self.popup = Tk()
     
        # Placement du popup par rapport à la fenêtre du pgm
        width = 265 # width for the Tk popup
        height = 100 # height for the Tk popup
        self.popup.geometry('%dx%d+%d+%d' % (width, height, fenetre.winfo_x()+500, fenetre.winfo_y()+140))  # winfo récupére la position actuelle
        self.popup['bg']='slate gray'
        self.popup.title("Fin…")
        self.popup.wm_attributes('-topmost', 1) # garde le popup au dessus
        self.grab_set() # empéche d'interragir avec la fenetre mére

        #texte
        self.label = Label(self.popup, text='''Erreur !''',font='Monospace 16 bold', fg="lime green", bg='slate gray')
        self.label.pack(side=TOP, padx=40,pady=5)

        #bouttons
        self.Bouton_Reinitialiser = Button(self.popup,text="Recommencer",font='Monospace 20 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=self.REstart)
        self.Bouton_Reinitialiser.pack(side=LEFT, padx=40, pady=10)

    def REstart(self):  # pour fermer le popup
        print('[LOG] : Popup Fonction RElance')
        Bouton_RomPath.configure(state='normal')
        Bouton_InpPath.configure(state='disabled')
        Bouton_playbackMNG.configure(state='disabled')
        Bouton_playbackMNG.configure(state='disabled')
        Bouton_EncodageX264.configure(state='disabled')
        ChangeText(RomLabel02)
        ChangeText(InpLabel02)
        message00()
        self.popup.destroy()
        self.grab_release() # redonne l'interraction avec la fenétre mère


#############################
# Popup de fin d'opérations #
#############################
class PopupFIN(Canvas):
    def __init__(self):
        Canvas.__init__(self)
        self.popup = Tk()
     
        # Placement du popup par rapport à la fenêtre du pgm
        width = 250 # width for the Tk popup
        height = 100 # height for the Tk popup
        self.popup.geometry('%dx%d+%d+%d' % (width, height, fenetre.winfo_x()+500, fenetre.winfo_y()+140))  # winfo récupére la position actuelle
        self.popup['bg']='slate gray'
        self.popup.title("Fin…")
        self.popup.wm_attributes('-topmost', 1) # garde le popup au dessus
        self.grab_set() # empéche d'interragir avec la fenetre mére

        #texte
        self.label = Label(self.popup, text='''C'est fini !''',font='Monospace 16 bold', fg="lime green", bg='slate gray')
        self.label.pack(side=TOP, padx=40,pady=5)

        #bouttons
        self.Bouton_Reinitialiser = Button(self.popup,text="Terminer",font='Monospace 20 bold',borderwidth=3,bg='light gray',activeforeground='lime green',command=self.REstart)
        self.Bouton_Reinitialiser.pack(side=LEFT, padx=40, pady=10)

    def REstart(self):  # pour fermer le popup
        print('[LOG] : Popup Fonction REstart')
        Bouton_RomPath.configure(state='normal')
        Bouton_InpPath.configure(state='disabled')
        Bouton_playbackMNG.configure(state='disabled')
        Bouton_playbackMNG.configure(state='disabled')
        Bouton_EncodageX264.configure(state='disabled')
        ChangeText(RomLabel02)
        ChangeText(InpLabel02)
        message00()
        self.popup.destroy()
        self.grab_release() # redonne l'interraction avec la fenétre mère


def Tail(): # appellé via le thread par la fonction png() (attention, elle impose son chemin)
    print('[LOG] : Tail :')
    try:
        os.chdir('MediaTMP/'+nomJEU)
 #       os.system('pwd')
        os.remove('advmngLOG')
    except:
        pass

    fichier= open('advmngLOG',"w")  # création du fichier vide
    fichier.close()
    NumberOfLine = 0
#    os.system('pwd')

    try :
        while True:
#            print('pwd while tail :')
#            os.system('pwd')
            with open('advmngLOG', 'r') as f:
#                os.system('pwd')
                for line in f:
                    NumberOfLine += 1
                print ('Nombre de lignes: ',NumberOfLine)
                if NumberOfLine >= int(NBimages):   # Condition d'arrêt de la boucle
                    break
            NumberOfLine = 0
            time.sleep(0.1) # Pour éviter au processeur de bosser comme un dingo
    except FileNotFoundError:   # Si la boucle dépasse la condition d'arrêt, elle se relance, mais le chemin ayant changé car png() ne s'exécute pas, le fichier n'est pas trouvé, car au passage de «pwd while tail» on est descendu de deux dossiers.
        pass

#######################
# Classe : ThreadTail #
#######################
class ThreadTail(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("init du thread Tail")
    def run (self):
        Tail()
#### fin de la Classe : Threadtail

#############################################################
# Affichage de la sortie de clamav dans le terminal intégré #
#############################################################

#termf = Frame(fenetre, width=990, height=435)
#termf.pack(fill=BOTH, expand=YES)
#termf.place(x=15, y=450)
#wid = termf.winfo_id()
#os.system('xterm -into %d -geometry 400x200 -sb &' % wid)


#############
# Programme #
#############
ArborescenceExisteTelle()
getTotalSizeTEMP()
TestpoidTMP()
#log.close()
TailThread = ThreadTail()


fenetre.mainloop()
