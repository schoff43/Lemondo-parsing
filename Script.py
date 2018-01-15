#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals   
from __future__ import division
from nltk.corpus.reader import CategorizedTaggedCorpusReader
from nltk.corpus import stopwords
from nltk import precision
from nltk import precision
from nltk import recall
from bs4 import BeautifulSoup
from nltk.classify import NaiveBayesClassifier
from os import path, makedirs
import time
import treetaggerwrapper
import urllib2
import codecs
import re
import os
import random
import bs4
import collections
import nltk

#nltk.download('all', halt_on_error=False)
def get_word_features(all_words,stop_words,n):
    word_features=[]
    for w in all_words.keys()[:n]:
        if(not(w in stop_words)):
            word_features.append(w)
    return word_features
def sent_features(sent):
    sent_words=set(sent)
    features={}
    for word in word_features:
        features['contains(%s)'%word]=(word in sent_words)
    return features
def precision_recall (classifier, test_set):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (sent, category) in enumerate(test_set):
        refsets[category].add(i)
        observed=classifier.classify(sent)
        testsets[observed].add(i)
    prec ={}
    rec = {}
    for category in leMonde.categories():
        prec[category] = nltk.precision(refsets[category], testsets[category])
        rec[category] = nltk.recall(refsets[category], testsets[category])
    return prec, rec
def fmesure(category):
    precc = float(PREC[category])
    rapp  = float(RAPP[category])
    fm = (2*precc*rapp)/(precc+rapp)
    return category, fm
def nettoyaEspace(texte):
        print "effacer les espaces "
        pattern1=re.compile(r'[ \t\n\r\f\v]+',re.UNICODE)  
        match=re.search(pattern1,texte)
        if match:
                texte=re.sub(pattern1,' ',texte)
        pattern2=re.compile(r'^()+')
        match2=re.search(pattern2,texte)
        if match2:
                texte=re.sub(pattern2,' ',texte)
        return texte
def netroyaHTML(texte):
        print "effacer Lire et Lire aussi "
        pattern=re.compile(r'<p class="lire.*">\s+Lire.*:\s+\xa0\s+<a href=".*">[\s\S]+<\/a>\s+<\/p>',re.UNICODE)
        match=re.search(pattern,texte)
        if match:
                texte=re.sub(pattern,'',texte)
        print "effacer Script parties du scripts "       
        pattern1=re.compile(r'<script>.*<\/script>',re.UNICODE)
        match1=re.search(pattern1,texte)
        if match1:
                texte=re.sub(pattern1,'',texte)
        print "effacer twitter parties "
        pattern2=re.compile(r'<blockquote class="twitter.*>[\s\S]+<\/blockquote>')
        match2=re.search(pattern2,texte)
        if match2:
                texte=re.sub(pattern2,'',texte)
        return texte
print "oukeey"
compteur=0;
tagger=treetaggerwrapper.TreeTagger(TAGLANG='fr')
print "creat les reportoires"
outDir= "/home/schoff43/Py/jour1"
outDirtag="/home/schoff43/Py/Jour1dir"
if not path.exists(outDir):
        makedirs(outDir)
if not path.exists(outDirtag):
        makedirs(outDirtag)
print "creer une liste "
listeCat = ["politique" , "culture" , "economie" , "sport" , "sciences" ]
for cat in listeCat:
    print "la verification"
    sousDir=outDir+'/'+cat
    if not path.exists(sousDir):
            makedirs(sousDir)   
    sousDir1=outDirtag
    if not path.exists(sousDir1):
            makedirs(sousDir1)
    nomFichier = "articles_" + cat +"_" + "tagged"
    with codecs.open(os.path.join(sousDir1,nomFichier+".txt"), "w", encoding="utf-8") as foutt:
        for i in range (0,2):
            url="http://www.lemonde.fr/{}/{}.html".format(cat,unicode(i));
            fichier=urllib2.urlopen(url)
            Soup=BeautifulSoup(fichier,"html5lib");
            blocURL=Soup.findAll(href=re.compile(r'\/\S+\/article\/\S+.html'))
            for e in blocURL :
                    url=e["href"]
                    url="http://www.lemonde.fr"+url
                    fichie=urllib2.urlopen(url)
                    Soup=BeautifulSoup(fichie,"html5lib")
                    nomFichier1="article_"+cat+'_'+unicode(compteur)
                    compteur+=1;
                    article=unicode(Soup.find(id=re.compile("articleBody")))
                    article=netroyaHTML(article)
                    article=BeautifulSoup( article,"html5lib");
                    article=article.get_text()
                    article=nettoyaEspace(article)
                    with codecs.open(os.path.join(sousDir,nomFichier1+".txt"),"w",encoding="utf-8") as fout:
                        fout.write(article)
                    fout.close()
                    tags=tagger.tag_text(article)
                    for tag in tags:
                        foutt.write(tag+"\n")
        compteur=0;        
foutt.close()

leMonde=CategorizedTaggedCorpusReader(outDirtag,r'\S+_tagged\.txt',cat_pattern='articles_(\w+)_tagged\.txt')
nb_c=0
nb_m=0
nb_p=0
nb_v=0
t_c=0;
for category in leMonde.categories():
    print "comptage des mots, des caracteres, des phrases"    
    print ("ok")
    nb_caracteres=len(leMonde.raw(categories=category))
    nb_mots=len(leMonde.words(categories=category))
    nb_phrases=len(leMonde.sents(categories=category))
    nb_vocab=len(set([w.lower() for w in leMonde.words(categories=category)]))
    print ("nombre ce caracters dans" + category+ ":" +str(nb_caracteres)+"\n"
           +"nombre de mots  dans" + category+ ":" +str(nb_mots)+"\n"
           +"nombre de phrases dans" + category+ ":" +str(nb_phrases)+"\n"
           +"nombre de vocabulaire dans" + category+ ":" +str(nb_vocab)+"\n")
    nb_c=nb_c+nb_caracteres
    nb_m=nb_mots+nb_m
    nb_p=nb_p+nb_phrases
    nb_v=nb_v+nb_vocab
print ("nombre ce caracters dans" +  ":" +str(nb_c)+"\n"
           +"nombre de mots  dans" + ":" +str(nb_m)+"\n"
           +"nombre de phrases dans" +  ":" +str(nb_p)+"\n"
           +"nombre de vocabulaire dans" +  ":" +str(nb_v)+"\n")
t_c=nb_c+nb_m+nb_p+nb_v
documents=[(sent,category)for category in leMonde.categories()for sent in leMonde.sents(categories=category)]
random.shuffle(documents)
all_words=nltk.FreqDist(w.lower()for w in leMonde.words())
stop_words = ["!", "\"", "(", ")", ",", "-elle", "-il", ".", "/", ":", ";", "?", "a", "absolument", "actuellement", 
"ainsi","alors", "ans", "apparemment", "approximativement", "après", "après demain", "assez", "assurément", "au",
"aucun", "aucunement", "aucuns","aujourd'hui", "auparavant", "aussi", "aussitôt", "autant", "autre", "autrefois",
"autrement", "aux", "avait","avant", "avant hier", "avec", "avoir", "beaucoup", "bien", "bientôt", "bon", "c'", "car",
"carrément", "ce", "cela", "cependant", "certainement", "certes", "ces", "cette", "ceux","chaque", "ci", "comme", 
"comment", "complètement", "d'", "d'abord", "dans", "davantage", "de", "dedans", "dehors", "demain", "depuis",
"derechef", "des", "deux", "devrait", "diablement", "divinement", "doit", "donc",
"dorénavant", "dos", "droite", "drôlement", "du", "début","déjà", "désormais", "elle", "elles", "en", "en vérité", "encore",
"enfin", "ensuite", "entièrement", "entre temps", "environ", "essai","est", "et", "eu", "extrêmement", "fait", "faites", "fois",
"font","force", "grandement", "guère", "habituellement", "haut", "hier","hors","ici", "il", "ils", "infiniment", "insuffisamment",
"jadis", "jamais", "je", "joliment", "l'", "la", "le", "les", "leur", "leurs", "longtemps", "lors", "là", "ma", "maintenant", "mais",
 "mes", "moins","mon", "mot", "même", "n'", "naguère", "ne", "ni", "nommés","non", "notre", "nous", "nouveaux", "nullement",
  "on", "ont", "ou", "oui", "où","par", "parce que", "parfois", "pas", "pas mal", "passablement", "personne", "personnes", "peu",
"peut", "peut-être", "pièce", "plupart", "plus", "plutôt", "point", "pour","pourquoi", "premièrement", "presque", "probablement",
 "prou", "précisément", "puis","qu'", "quand", "quasi", "quasiment", "que", "quel", "quelle", "quelles", 
"quelque", "quelquefois", "quels","qui", "quotidiennement", "resume", "rien","rudement", "s'", "sa", "sans", "sans doute", "se",
"selon", "ses", "seulement", "si", "sien", "sitôt", "soit", "son","sont", "soudain", "sous", "souvent", "soyez", "subitement", "suffisamment", "sur",
 "t'", "ta", "tandis", "tant", "tantôt", "tard", "tellement", "tel", "tels","terriblement", "tes", "ton", "totalement", "toujours", "tous", "tout", 
"tout à fait", "toutefois", "trop", "très", "tu", "tôt", "un", "une", "valeur", "vers", "voie", "voient", "volontiers", 
"vont", "votre", "vous", "vraiment", "vraisemblablement", "y'", "y", "à", "à demi", "à peine", "à peu près", "ça","étaient", "état", "étions", "été", "être"]
t_c2=t_c*0.3
t_c1=t_c*0.7

word_features=get_word_features(all_words,stop_words,200)
featuresets=[(sent_features(d), c) for (d, c) in documents]
train_set=featuresets[140:]
test_set=featuresets[:60]
classifier = nltk.NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)

PresRap=precision_recall(classifier,test_set)

PresRap=precision_recall(classifier,test_set)
PREC = PresRap[0]
RAPP = PresRap[1]
print"::::::PREP RAPP ::::"
print PREC
print RAPP

for category in leMonde.categories():
    try :
        print(fmesure(category))
    except :
        print ("(" + "'" + category + "'" + ", pas de valeur pour cette categorie" + ")")
