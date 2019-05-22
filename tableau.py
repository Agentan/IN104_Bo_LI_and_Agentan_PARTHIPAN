import os
import math
import sys
import pickle
from nltk.tokenize import word_tokenize

class Tableau:
    ID_docs = {}
    INDEX = {}
    mots_dejavus = []

    def save(self, save_path):  #sauvgarde les 2 dictionaires du tableau
        article = open(save_path, 'wb')
        pickle.dump(self.INDEX, article)
        pickle.dump(self.ID_docs, article)
        article.close()

    def initialisation(self, bdd_path, id):
        for element in os.listdir(bdd_path):
            if element.endswith('.txt'):
                element_path = bdd_path + '/' + element
                self.ID_docs[id] = element_path
                article = open(element_path, encoding='utf-8', errors='ignore') #parametres optionnels utilises pour eviter des erreurs d'encodage
                article_content = article.read()
                transf_article_content = word_tokenize(article_content)
                mots_dejavus_ici = []

                for word in transf_article_content:
                    if word not in mots_dejavus_ici:
                        nb_occ = transf_article_content.count(word)
                        if word not in self.mots_dejavus:
                            self.INDEX[word] = {}
                            self.mots_dejavus.append(word)
                        self.INDEX[word][id] = nb_occ
                        mots_dejavus_ici.append(word)
                article.close()
                id += 1

            elif os.path.isdir(bdd_path + '/' + element):
                id = self.initialisation(bdd_path + '/' + element, id)
        return id  # pour continuer a numeroter les documents

    def partie_log(self, document, word):
        # la partie log(N/dfi) ne change pas pour w_ij et w_iq, on definit cette fonction pour eviter de la calculer deux fois
        try:
            df = len(self.INDEX[word])
            N = len(self.ID_docs)
            return math.log(N / df)
        except(KeyError):
            print("the word '" + word + "' doesn't exist in the database")
            sys.exit()

    def tf(self, document, word):  ##retourne le nombre d'occurences tf_ij
        if word in self.INDEX:
            if document in self.INDEX[word]:
                return self.INDEX[word][document]
            else:
                return 0
        else:
            print("the word '" + word + "' doesn't exist in the article")
            return 0

    def similarity(self, document, transf_query):  ##calculer la similarite entre un document et la requete
        A = 0;  # w_ij * w_iq
        B = 0;  # w_ij * w_ij
        for word in transf_query:
            log = self.partie_log(document, word)
            w_ij = self.tf(document, word) * log
            tf_iq = transf_query.count(word)
            w_iq = tf_iq * log
            A += w_ij * w_iq
            B += w_ij * w_ij
        if B == 0:
            return 0
        else:
            return (A / math.sqrt(B))

    def search(self):
        query = input('enter your query :') # demande de la requete
        transf_query = word_tokenize(query)
        reunion = set(range(len(self.ID_docs)));
        result = {};
        for word in transf_query:
            if word in self.INDEX:
                containing = set(self.INDEX[word].keys());
                reunion = reunion & containing
        for document in reunion:
            result[document] = self.similarity(document, transf_query)  #calcule la similarite entre la requete et chaque document ou appara?t un mot de la requ¨ºte
            sorted_result = sorted(result.items(), key=lambda kv: kv[1], reverse=True) # trie les documents selon la valeur de leurs similarit¨¦s avec la requ¨ºte
        for couple in sorted_result:
            print(self.ID_docs[couple[0]]) #affiche les resultats de la recherche


def load(save_path): #charger l'index precedemment enregistre
    f = open(save_path, 'rb')
    D = Tableau()
    D.INDEX = pickle.load(f)
    D.ID_docs = pickle.load(f)
    f.close()
    return D
