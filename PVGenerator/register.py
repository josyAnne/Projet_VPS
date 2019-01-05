import os
from xml.dom import minidom
import imgkit
import random
config="config.xml"


def getFolderPath():
    mydoc = minidom.parse(config)
    items = mydoc.getElementsByTagName("config")
    folder=""
    for elem in items:
        print(elem)
        if elem.attributes['name'].value=="folderPath":
            folder=elem.firstChild.data
            break
    return folder

def register_pv(pv, idBureau, idScrutateur):

    directory=getFolderPath()+os.path.sep+"Bureau_"+str(idBureau)
    if not os.path.exists(directory):
        os.makedirs(directory)
    directory+=os.path.sep+"Scrutateur_"+str(idScrutateur)+".jpg"
    nbCandidat= len(pv[0]) - 1
    nbScrutateur= nbCandidat

    htmlCandidat=''
    css='css.css'
    html='<!DOCTYPE html>'
    html+='<html lang="en">'
    html+='<head></head>'
    html='<table style="width: 100%;">'
    html+='<tbody>'
    html+='<tr style="width: 100%;">'
    html+='<td style="width: 50%"><b>Bureau</b></td>'
    html+='<td style="width: 50%">Bureau_'+str(idBureau)+'</td>'
    html+='</tr>'
    html += '<tr style="width: 100%;">'
    html += '<td style="width: 50%"><b>#Electeur</b></td>'
    html += '<td style="width: 50%">'+str(pv[1])+'</td>'
    html += '</tr>'
    html += '<tr>'
    html += '<td colspan="2"><pre></pre></td>'
    html += '</tr>'
    html+='<tr style="width: 100%;"></tr>'
    html += '<tr style="width: 100%;">'
    html += '<td style="width: 50%"><b>NomsCandidats</b></td>'
    html += '<td style="width: 50%"><b>#Voies</b></td>'
    html += '</tr>'
    i = 0
    for elt in pv[0]:   
        if i== len(pv[0])-1:
            html += '<tr style="width: 100%;">'
            html += '<td style="width: 50%">BulletinNul</td>'
            html += '<td style="width: 50%">'+str(elt)+'</td>'
            html += '</tr>'
            html += '<tr>'
            html += '<td colspan="2"><pre></pre></td>'
            html += '</tr>'
            html += '<tr style="width: 100%;">'
            html += '<td style="width: 50%"><b>NomsScrutateurs</b></td>'
            html += '<td style="width: 50%"><b>Signatures</b></td>'
            html += '</tr>'
        else:
            html+='<tr style="width: 100%;border:1px solid #000;">'
            html+='<td style="width: 50%">Candidat'+str(i+1)+'</td>'
            html += '<td style="width: 50%">'+str(elt) + '</td>'
            html += '</tr>'
        i+=1

    i=0
    while (i < nbScrutateur):
        i = i + 1
        signature=''
        j=0
        while(j<random.randint(3, 10)):
            j+=1
            signature+=random.choice('abcdefghijklmnopqrstuvwz')
        html += '<tr style="width: 100%;border:1px solid #000;">'
        html += '<td style="width: 50%">Scrutateur' + str(i) + '</td>'
        html += '<td style="width: 50%">' + signature + '</td>'
        html += '</tr>'

    html+='</tbody>'
    html+='</table>'
    print(directory)
    imgkit.from_string(html, directory,css=css)


