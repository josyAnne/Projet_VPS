# This Python file uses the following encoding: utf-8

from random import randrange, choice
import sys,math
from config import min, max
from register import register_pv

class GenerateurPV:


    F_ZERO =0    
    F_SOLITAIRE = 1
    F_COALITION = 2

    def __init__(self, nbBureau, nbCandidat, niveauFraude):     
        self.nbCandidat = int(nbCandidat)
        self.niveauFraude = int(niveauFraude)
        self.nbBureau = int(nbBureau)
        if self.niveauFraude !=0 and self.niveauFraude !=1 and self.niveauFraude!=2:
            raise ValueError("niveauFraude value error")
        self.generationPV()


    def generationPV(self):
        
        #On choisit le parti au pouvoir au hasard
        pp = randrange(self.nbCandidat)

        if  self.niveauFraude == self.F_ZERO:
            self.generationPV_FZERO(pp)
        elif self.niveauFraude == self.F_SOLITAIRE:
            self.generationPV_FSOLITAIRE(pp) 
        else:
            self.generationPV_FCOALITION(pp)


    def generationPV_FZERO(self, pp):
    #methode de generation des PV dans le cas ou il n'y a pas de fraude
        #On parcourt les bureaux de vote
        for i in range(self.nbBureau):
            
            pv_vrai = self.genPV()
            
            register_pv(pv_vrai, i+1, "PV_Vrai")

            for j in range(self.nbCandidat):

                if j==pp:
                    register_pv(pv_vrai, i+1, str(pp+1)+"_PartiAuPouvoir")
                else:
                    register_pv(pv_vrai, i+1, str(j+1)+"_")
            
            register_pv(pv_vrai, i+1, "Elecam")


    #méthode de génération des PV dans le cas où il y'a des fraudes solitaires
    def generationPV_FSOLITAIRE(self, pp):

        #On parcourt les bureaux de vote
        for i in range(self.nbBureau):
            
            pv_vrai = self.genPV()
            register_pv(pv_vrai, i+1, "PV_Vrai")
            pv_parti_pouvoir = []

            for j in range(self.nbCandidat):                

                #On determine si le scrutateur va frauder
                fraude = randrange(2)

                if fraude:
                    if j==pp:
                        pv_parti_pouvoir =  self.genPVFraude(pv_vrai, j, [j])
                        register_pv(pv_parti_pouvoir, i+1, str(pp+1)+"_PartiAuPouvoir")
                    else:       
                        register_pv(self.genPVFraude(pv_vrai, j, [j]), i+1, str(j+1)+"_") 
                else:
                    if j==pp:
                        pv_parti_pouvoir =  self.genPVFraude(pv_vrai,j, [j])
                        register_pv(pv_parti_pouvoir, i+1, str(pp+1)+"_PartiAuPouvoir")
                    else:       
                        register_pv(pv_vrai, i+1, str(j+1)+"_")                          

            #Enregistrement du PV de Elecam
            register_pv(pv_parti_pouvoir, i+1, "Elecam")


    #méthode de génération des PV dans le cas où il y'a des coalitions
    def generationPV_FCOALITION(self, pp):

        nbreCoalition = randrange(self.nbCandidat)

        coalitions = self.formation_coalitions(nbreCoalition)

        for i in range(self.nbBureau):

            pv_vrai = self.genPV()
            register_pv(pv_vrai, i+1, "PV_Vrai")

            pv_parti_pouvoir = pv_vrai

            for coalition in coalitions:

                fraude = randrange(2)
                if fraude:

                    pv_fraude = self.genPVFraude(pv_vrai, coalition[1], coalition[0])

                    if pp in coalition[0]:
                        pv_parti_pouvoir = pv_fraude

                    for elt in coalition[0]:
                        if elt == pp:
                            register_pv(pv_fraude, i+1, str(pp+1)+"_PartiAuPouvoir")
                        else:
                            register_pv(pv_fraude, i+1, str(elt+1)+"_")
                else:

                    for elt in coalition[0]:
                        if elt == pp:
                            register_pv(pv_vrai, i+1, str(pp+1)+"_PartiAuPouvoir")
                        else:
                            register_pv(pv_vrai, i+1, str(elt+1)+"_")

            #Enregistrement du PV de Elecam
            register_pv(pv_parti_pouvoir, i+1, "Elecam")



    #génération d'un PV
    def genPV(self):

        list = []
        nbInscrit  = randrange(min, max)        
        reste  = nbInscrit
        for i in range(self.nbCandidat):
            if i==0:
                random = randrange(math.ceil(reste/2))
            else:
                random = randrange(reste)               
            list.append(random)
            reste -= random
        list.append(reste) 
        return (list, nbInscrit)


    #génération d'un PV fraudé par modification d'un autre passé en paramètre
    def genPVFraude(self, pv_vrai, id, liste_coalition):

        pv_fraude = list(pv_vrai[0])

        #Je vais comparer la somme des voies de la coalition avec celle du reste
        liste_reste = [elt for elt in range(len(pv_vrai[0])) if elt not in liste_coalition]
        reste = [pv_vrai[0][elt] for elt in liste_reste]        
        voies_reste = sum(reste)        
        voies_coalition = pv_vrai[1] - voies_reste
        
        retrait = []
        liste_coalition_exclu = [elt for elt in liste_coalition if elt != id]
        coalition_exclu = [pv_vrai[0][elt] for elt in liste_coalition_exclu]
        voies_coaliton_exclu = sum(coalition_exclu)        
        
        # si les voies de la coalition sont plus grandes, je vais enlever un nombre de voies à chaque membre de la coalition                
        if voies_coalition >= voies_reste and len(liste_coalition) > 1:            
            for elt in liste_coalition_exclu :
                percent = pv_vrai[0][elt]/voies_coaliton_exclu                                                              
                pv_fraude[elt] -= math.floor(pv_vrai[0][elt]*0.5*percent)
                retrait.append(math.floor(pv_vrai[0][elt]*0.5*percent))             
            pv_fraude[id] += sum(retrait)

        else :
            for elt in liste_reste:
                percent = pv_vrai[0][elt]/voies_reste       
                pv_fraude[elt] -= math.floor(pv_vrai[0][elt]*0.5*percent)
                retrait.append(math.floor(pv_vrai[0][elt]*0.5*percent))             
            if len(liste_coalition) == 1:
                pv_fraude[id] += sum(retrait)
            else :
                pv_fraude[id] += math.floor((sum(retrait) + voies_coalition)/2)
                voies_a_partager  = (sum(retrait) + voies_coalition) - math.floor((sum(retrait) + voies_coalition)/2)
                count = voies_a_partager
                for elt in liste_coalition_exclu :
                    percent = pv_vrai[0][elt]/voies_coaliton_exclu  
                    count -= math.floor(voies_a_partager*percent)       
                    pv_fraude[elt] = math.floor(voies_a_partager*percent)
                pv_fraude[id] += count              

        return (pv_fraude, pv_vrai[1])


    #Enregistrement d'un pv sur le disque sous forme d'image
    def register_pv(self, pv, id_bureau, id_scrutateur):
        return []

    # formation des coalitions
    def formation_coalitions(self, n_coalition):

        #Bon je vais d'abord mettre la liste des candidats dans une liste fictive
        liste = list(range(self.nbCandidat))
        if n_coalition == 1:
            return [(liste, choice(liste))]
        elif n_coalition == self.nbCandidat :
            return [([nb], nb) for nb in liste]
        else:
            coalitions = []
            count = n_coalition - 1
            initial = self.nbCandidat
            for i in range(n_coalition-1):
                number = randrange(1, 1+ initial -count)
                initial -= number
                count = count -1
                member_coalition = []
                for elt in range(number):
                    member = choice(liste)
                    member_coalition.append(member)
                    liste.remove(member)
                coalitions.append((member_coalition, choice(member_coalition)))
            coalitions.append((liste, choice(liste)))
            return coalitions


if __name__=="__main__":
    
    
    nbBureau = sys.argv[1]
    nbCandidat = sys.argv[2]
    niveauFraude = sys.argv[3]
    
    genPV =  GenerateurPV(nbBureau, nbCandidat, niveauFraude)



















