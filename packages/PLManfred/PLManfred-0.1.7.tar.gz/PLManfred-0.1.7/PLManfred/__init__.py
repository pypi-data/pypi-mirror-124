from PLManfred.audio import *
import os
import playsound
from PLManfred.say import  *
from PLManfred.logo import *
from PLManfred.czy import *
from PLManfred.pogoda import *
from PLManfred.skript import *

def Manfred():
    logo()
    say("Witaj, Jestem Manfred")
    while True:
        print(" ")
        audio = get_audio()
        if len(czy(audio, ADMIN_COMMADN)):
            if len(czy(audio, PA_ADMIN)):
                say("pa")
                quit()
                exit()
################
            if len(czy(audio, setupup)):
                say("ok")
                setupadd()
        if len(czy(audio, wyszukaj)):
            if len(czy(audio, z)):
                if len(czy(audio, pamieci)):
                    say("ok")
################################################################################
        if len(czy(audio, KLUCZ_COMMAND)):
################
            if len(czy(audio, zart)):
                lossay(zartycommand)
################
            if len(czy(audio, jaka)):
################
                if len(czy(audio, jest)):
################
                    if len(czy(audio, temperatura)):
################
                        if len(czy(audio, w)):
################
                            if len(czy(audio, BIAŁYSTOK)):
                                temp("Białystok")

################
                            if len(czy(audio, WARSZAWA)):
                                temp("Warszawa")

################
                            if len(czy(audio, bielskbiałej)):
                                pogo("Bielsko Biała")

################
                            if len(czy(audio, BIELSK)):
################
                                if len(czy(audio, BIAŁE)):
                                    temp("Bielsko Biała")

################
                            if len(czy(audio, Chojnice)):
                                temp("Chojnice")

################
                            if len(czy(audio, czestochowa)):
                                temp("Częstochowa")

################
            if len(czy(audio, wyszukaj)):
                g = audio.lower().split(' ' + czy(audio, wyszukaj)[0] + ' ')[1]
                say("Oto co mi się udało znaleść.")
                googleurl = "https://www.google.com/search?q=" + g.replace(" ", "+").replace("?", "%3F")
                webbrowser.open(googleurl)
                command()

################
            if len(czy(audio, odpal)):
################
                if len(czy(audio, spotif)):
                    say("ok")
                    webbrowser.open("https://open.spotify.com/")

################
                if len(czy(audio, netflix)):
                    say("ok")
                    webbrowser.open("https://www.netflix.com/")

################
                if len(czy(audio, instagram)):
                    say("ok")
                    webbrowser.open("https://www.instagram.com/")

################
                if len(czy(audio, facebook)):
                    say("ok")
                    webbrowser.open("https://www.facebook.com/")

################
                if len(czy(audio, gmail)):
                    say("ok")
                    webbrowser.open("https://mail.google.com/")

################
                if len(czy(audio, PROSZE)):
################
                    if len(czy(audio, yt)):
                        ytw = audio.lower().split(' ' + czy(audio, yt)[0] + ' ')[1]
                        youtubeopen(ytw)







#############################komendy############################################
KLUCZ_COMMAND = ["ok", "manfred", "bot", "okej", "żulu",  "manfredi"]


################################################################################

yt = ["youtube", "youtubie", "film"]
ADMIN_COMMADN = ["admin"]
PA_ADMIN = ["pa", "pa pa", "papa"]
RESTART_ADMIN = ["restart"]
KLUCZ_COMMAND = ["ok", "manfred", "bot", "okej", "żulu",  "manfredi"]
PROSZE = ["prosze", "proszę"]
odpal = ["odpal"]
google = ["google"]
jaka = ["jaka"]
jest = ["jest"]
setupup = ["setup", "set up"]
temperatura = ["temperatura"]
w = ["w"]
z = ["z"]
czestochowa = ["częstochowa", "częstochowie"]

BIAŁYSTOK = ["białyestoku", "białymstoku"]
Chojnice = ["chojnice"]
BIELSK = ["bielsk", "bielsko"]
bielskbiałej = ["bielsk-białej", "bielsku-białej"]
BIAŁE = ["białe", "biała"]
WARSZAWA = ["warszawie"]

wyszukaj = ["wyszukaj"]
zart = ["żart"]
zartycommand = ["nauczyciel języka polskiego pyta się uczniów jak brzmi liczba mnoga do rzeczownika niedziela? Wakacje proszę pani", "Jak się nazywa lekarz, który leczy pandy? Pandoktor", "Dlaczego duchy nie kłamią? Bo wiedzą, że możesz je przejrzeć na wylot", " koniec roku szkolnego. tato, ty to masz szczęście do pieniędzy, Dlaczego? nie  musisz kupować książek na przyszły rok zostaje w tej samej klasie", "panie doktoże wczyscy mnie ignowują. Następny proczę"]

spotif = ["spotify"]
instagram = ["instagram"]
netflix = ["netflix"]
facebook = ["facebook", "facebooka"]
gmail = ["gmail"]

wyszukaj = ["wyszukaj"]
pamieci = ["pamięci5"]
