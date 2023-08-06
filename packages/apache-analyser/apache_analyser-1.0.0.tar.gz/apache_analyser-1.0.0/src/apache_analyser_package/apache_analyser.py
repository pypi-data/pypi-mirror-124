
# !/usr/bin/python3 
import json
import re
import argparse
from statistics import mean
from statistics import mode
from collections import Counter
from datetime import date
from tkinter import *


# splitter :separer les textes dans une ligne afin de recuperer the time,
# ip address, request, response code, packet size, referrer,
# system agent and browser
def splitter(line_to_parse):
    line = line_to_parse.split(' ')
    get = line_to_parse.split('"')
    usr_agent = get[5]
    list1 = dict(
        time=line[3]+' '+line[4],
        remote_ip=line[0],
        request=get[1],
        path=line[6],
        response=line[8],
        size=line[9],
        referrer=get[3],
        user_agent=usr_agent,
        system_agent=lire_os(usr_agent),
        browser=lire_browser(usr_agent)
    )
    return list1

# lire_os : pour identifier et afficher la version d'OS de la machine
def lire_os(usr_agent):
    if "Windows" in usr_agent:
        sys_agent = "Windows"
    elif "Linux" in usr_agent:
        if "Android" in usr_agent:
            sys_agent = "Android"
        else:
            sys_agent = "Linux"
    elif "Mac" in usr_agent:
        if "iPhone" in usr_agent:
            sys_agent = "iPhone OS"
        else:
            sys_agent = "Mac OS"
    else:
        sys_agent = "OS unknown"
    return sys_agent

# lire_browser : pour identifier le navigateur de web
def lire_browser(usr_agent):
    if "Chrome" in usr_agent:
        browser = "Google Chrome"
    elif "Safari" in usr_agent:
        browser = "Safari"
    elif "MSIE" in usr_agent:
        browser = "MS Internet Explorer/Edge"
    elif "Firefox" in usr_agent:
        browser = "Mozilla Firefox"
    else:
        browser = "Web browser unknown or bot"
    return browser

# lire_log : fonction pour parser un document entier
# en utilisant splitter
def lire_log(nom_fic):
    f = open(nom_fic, "r")
    list2 = []
    for l in f:
        list2.append(splitter(l))
    return list2

# convert_JSON : convertir un apache log à json
def convert_json(nom_fic):
    list2 = []
    with open(nom_fic, "r") as f:
        nom_fic2 = nom_fic[:-4]+".json"
        for l in f:
            list2.append(splitter(l))
    with open(nom_fic2, "w") as f2:
        json.dump(list2, f2, indent=4)
    return list2

# count_OS : compter le nombre d'utilisateur qui utilise tel système d'exploitation pour acceder le serveur 
# afiche le nombre, le pourcentage et un diagramme circulaire
def count_os(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    result = {}
    for data in dict1:
        if data['system_agent'] not in result:
            result[data['system_agent']] = 1
        else:
            result[data['system_agent']] = result[data['system_agent']]+1
    string="\nLe nombre d'utilisateur qui utilise tel système d'exploitation pour accéder au serveur :\n\n"
    for os in result:
        string=string+"\t"+os+" : "+str(result[os])+'\n'
    string = string+stat_percentage(result)
    bar_graph(result) #afficher un graphe à barres
    return string

# average_size : donne la taille moyenne des paquets pour un enregistrement apache
def average_size(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    l_size = []
    for data in dict1:
        if data['size'] != '-':
            size_float = float(data['size'])
            l_size.append(size_float)
    avgsize = mean(l_size)
    maxsize = max(l_size)
    minsize = min(l_size)
    string = "\nLa taille moyenne de fichier demandé est égale à : "+str(round(avgsize, 4))+" octets"
    string = string + "\nLa taille max de fichier demandé est égale à : "+str(maxsize)+" octets"
    string = string + "\nLa taille min de fichier demandé est égale à : "+str(minsize)+" octets"
    return string

# trafic_du_jour : calculer le nombre total de visiteur à jour actuel
def trafic_du_jour(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    today = date.today()
    d = today.strftime("%d/%B/%Y")
    nb_visiteur = 0
    for data in dict1:
        date1 = data['time'].split(':')
        date1[0] = date1[0][1:]
        if date1[0] == d:
            nb_visiteur = nb_visiteur+1
    string = "\nLe nombre total de visiteur aujourd'hui : "+str(nb_visiteur)
    return string

# count_method : compter le nombre de méthode utilisée par le monde pour acceder le serveur
# afficher le nombre, le pourcentage et un graphe à barres
def count_method(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    result = {
        "GET":0,
        "POST":0,
        "HEAD":0,
        "PUT":0,
        "Others":0
    }
    for data in dict1:
        if "GET" in data['request']:
            result["GET"] = result["GET"]+1
        elif "POST" in data['request']:
            result["POST"] = result["POST"]+1
        elif "HEAD" in data['request']:
            result["HEAD"] = result["HEAD"]+1
        elif "PUT" in data['request']:
            result["PUT"] = result["PUT"]+1
        else:
            result["Others"] = result["Others"]+1
    string = "\nLe nombre de méthode utilisée pour acceder le serveur :\n\n"
    for method in result:
        string = string+"\t"+method+" : "+str(result[method])+'\n'
    string = string+stat_percentage(result)
    pie_chart(result)
    return string

# heure_creuse : trouver l'heure creuse
def heure_creuse(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    l_heure = []
    for data in dict1:
        heure = data['time'].split(':')
        l_heure.append(heure[1])
    heure_creuse = mode(l_heure)
    heure_creuse2 = int(heure_creuse) +1
    string="\nL'heure où il y a le plus de trafic sur le serveur : "+heure_creuse+'h00 - '+str(heure_creuse2)+'h00'
    return string

# count_response : compter le nombre de code de réponse
# afficher le nombre (eg. "200" : 100), le pourcentage, et un diagramme circulaire
def count_response(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    l_rep = []
    for data in dict1:
        l_rep.append(data['response'])
    result = Counter(l_rep)
    string = "\nLe nombre de code HTTP :\n\n"
    for response in result:
        string = string+'\t'+response+' : '+str(result[response])+'\n'
    string = string+"\nAttention : L'apparition répétitive de code d'état de famille 4xx et 5xx (403, 500, 503 etc.) peuvent potentiellement impliquer une faille de sécurité\n"+stat_percentage(result)
    pie_chart(result)
    return string

# analyse_ip_addr : trouver 10 adresse ip qui visite le serveur le plus avec la fréquence et le nombre de visiteur unique
def analyse_ip_addr(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    l_ipaddress = []
    for data in dict1:
        l_ipaddress.append(data['remote_ip'])
    ip_addr1 = Counter(l_ipaddress).most_common(10) #Les 10 clients le plus fréquentés
    ip_addr2 = Counter(l_ipaddress)
    total_session = len(l_ipaddress)
    visiteur_unique = 0
    for ip_addr in ip_addr2 : #pour calculer visiteur unique
        if ip_addr2[ip_addr] == 1:
            visiteur_unique = visiteur_unique+1
    result = dict(ip_addr1) #change to dictionary
    string = "\nLes 10 adresses IP dont la fréquence de visite est la plus élévée :\n\n"
    placement = 1 #compteur pour placement
    for ip in result:
        string = string+'\t'+str(placement)+'. '+ip+' : '+str(result[ip])+'\n'
        placement = placement+1
    string = string+'\nLe nombre de visiteur unique : '+str(visiteur_unique)
    string = string+'\nLe nombre total de sessions : '+str(total_session)
    return string

# analyse_doc_type : trouver 10 type des documents le plus demandés avec la fréquence et 
# le nombre de session qui le type est non identifiable
def analyse_doc_type(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    l_typedoc = []
    unidentified_type = 0
    for data in dict1:
        if re.match("^.*[.].*$", data['path']) != None:
            type_doc = data['path'].split('.')
            if "?" in type_doc[1]:
                type_doc1 = type_doc[1].split('?')
                l_typedoc.append(type_doc1[0])
            else:
                l_typedoc.append(type_doc[1])
        else:
            unidentified_type = unidentified_type+1
    analyse_format = Counter(l_typedoc).most_common(10)
    result = dict(analyse_format) #change to dictionary
    string='\nLes 10 types de documents le plus demandé  :\n\n'
    placement = 1
    for doc in result:
        string = string+'\t'+str(placement)+'. '+doc+' : '+str(result[doc])+'\n'
        placement = placement+1
    string = string+'\nLe nombre de session dont le type de document est non identifiable  : '+str(unidentified_type)
    return string

# count_browser : compter le navigateur utilsé pour acceder le serveur // 
# afficher le nombre, pourcentage et diagramme circulaire
def count_browser(nom_fic_json):
    with open(nom_fic_json, "r") as f:
        dict1 = json.load(f)
    result = {}
    for data in dict1:
        if data['browser'] not in result:
            result[data['browser']] = 1
        else:
            result[data['browser']] = result[data['browser']]+1
    string = '\nLes navigateurs utilisés pour acceder au serveur :\n\n'
    for browser in result:
        string = string+"\t"+browser+" : "+str(result[browser])+"\n"
    string = string+stat_percentage(result)
    pie_chart(result)
    return string

# stat_percentage : Les données en pourcentage
def stat_percentage(dict1):

    total = 0
    string = ""
    for data in dict1:
        total = total+dict1[data]
    for data in dict1:
        dict1[data] = str((round((dict1[data]/total)*100, 2)))+"%"
    string = string+'\nLes données en pourcentage :\n\n'
    for data in dict1:
        string = string+"\t"+data+" : "+dict1[data]+"\n"
    return string

#graphique en utilisant tkinter
#pie_chart : create a pie chart from a dictionary which contains a percentage as a string
def pie_chart(dict1):
    root = Tk()
    root.title("Diagramme Circulaire")
    canvas = Canvas(root, width=400, height=400)
    canvas.pack()
    colour = ["Red", "Blue", "Green", "Yellow", "Pink", "Brown", "Orange", "Grey" ]
    legend = ""
    freq = []
    i = 0 #counter for colour
    j = 0 #counter for create_arc
    angle = 0
    for data in dict1: #create legend for the data according to their colour
        legend = legend+colour[i]+" - "+data+" : "+dict1[data]+"\n"
        i = i+1
    for data in dict1:
        dict1[data] = float(dict1[data][:-1]) #somehow our dictionary returns a percentage as a string, even if we stocked the value in a temporary varibale, so we need to change it back to interger
        dict1[data] = round((dict1[data]/100)*360)
        freq.append(dict1[data])
    Label(root, text=legend, justify="left").place(x=2, y=2)
    for data in dict1:
        canvas.create_arc(110, 110, 310, 310, fill=colour[j], start=angle, extent=freq[j])
        angle = angle+freq[j]
        j = j+1
    root.mainloop()
    
#bar_graph : create a bar graph from a dictionary which contains a percentage as a string  
def bar_graph(dict1):
    root = Tk()
    root.title("Graphique à Barres")
    canvas = Canvas(root, width=600, height=600)
    canvas.pack()
    i = 0
    j = 0
    x_start = 50
    legend = ""
    colour = ["Red", "Blue", "Green", "Yellow", "Pink", "Brown", "Orange", "Grey" ]
    for data in dict1: #create legend for the data according to their colour
        legend = legend+colour[i]+" - "+data+" : "+dict1[data]+"\n"
        i = i+1
    Label(root, text=legend, justify="left").place(x=2, y=2)
    for data in dict1:
        dict1[data] = float(dict1[data][:-1])
    
    canvas.create_line(20, 500, 580, 500)
    for data in dict1:
        y_end = 500-(dict1[data]*5)
        canvas.create_rectangle(x_start, 500, x_start+70, y_end, fill=colour[j])
        Label(root, text=data).place(x=x_start+7, y=507)
        Label(root, text=str(dict1[data])+"%").place(x=x_start+20, y=y_end-25)
        x_start = x_start+80
        j = j+1
    root.mainloop()


# CLI
# nomFic=input('Nom de fichier log que vous souhaitez analyser : ')
my_parser = argparse.ArgumentParser(
description="Analyser fichier log au format apache. Attention : il faut impérativement convertir le fichier log en format json (avec l'option --a) pour pouvoir utiliser les autres options ")

my_parser.add_argument('filename', type=argparse.FileType('r'),)
my_parser.add_argument('dict1', nargs='?', type=json.loads)

# convertJSON
my_parser.add_argument('--a', action='store_true', help='changer le fichier en format JSON')

#OSAnalyser
my_parser.add_argument('--b', action='store_true', help="analyser l'OS d'utilisateur")

#AvgSize
my_parser.add_argument('--c', action='store_true', help="calculer la taille moyenne de paquets demandés")

#TraficduJour
my_parser.add_argument('--d', action='store_true', help="voir le trafic du jour sur le serveur")

#AnalyseMethode
my_parser.add_argument('--e', action='store_true', help="analyser la méthode de requête solicitée")

# HeureCreuse
my_parser.add_argument('--f', action='store_true', help="voir l'heure creuse du serveur et le trafic en fonction d'heure")

#AnalyseResponse
my_parser.add_argument('--g', action='store_true', help="analyser les réponses des requêtes")

#AnalyseIPAdd
my_parser.add_argument('--i', action='store_true', help="analyser les adresses IP de clients")

#AnalyseTypeDoc
my_parser.add_argument('--j', action='store_true', help="analyser les 10 types de documents les plus demandés par client")

#AnalyseBrowser
my_parser.add_argument('--k', action='store_true', help="analyser le navigateur utilisé par client")

__version_info__ = ('1','0','0')
__version__ = '.'.join(__version_info__)

my_parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")
args = my_parser.parse_args()

nom_fic = args.filename.name
nom_fic = nom_fic.split('.')
nom_fic = nom_fic[0]+'.json'
# print(nom_fic)
if args.a:
    convert_json(args.filename.name)
# print(args.a)
# print(args.filename.name)


if args.b:
    resultat_os = count_os(nom_fic)
    print(resultat_os)

if args.c:
    resultat_avg = average_size(nom_fic)
    print(resultat_avg)

if args.d:
    resultat_trafic = trafic_du_jour(nom_fic)
    print(resultat_trafic)

if args.e:
    resultat_methode = count_method(nom_fic)
    print(resultat_methode)

if args.f:
    resultat_heure_creuse = heure_creuse(nom_fic)
    print(resultat_heure_creuse)

if args.g:
    resultat_reponse = count_response(nom_fic)
    print(resultat_reponse)

if args.i:
    resultat_ip = analyse_ip_addr(nom_fic)
    print(resultat_ip)

if args.j:
    resultat_type_doc = analyse_doc_type(nom_fic)
    print(resultat_type_doc)

if args.k:
    resultat_count_browser = count_browser(nom_fic)
    print(resultat_count_browser)