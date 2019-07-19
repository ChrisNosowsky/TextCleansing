#dictionary.py
#
#Module used to cleanse text data
#
#Created by Matt Lauer (5/22/2018)

import collections
import re
from collections import OrderedDict
from operator import itemgetter
import os

class Dictionary(object):
    #might have to change for specific version
    _original_correct_dict       = "C:\\Development\\SVN\\Amerisure\\Analytics\\trunk\\TextAnalytics\\common\\f_workers_comp_dictionary.txt"
    _dictionary_to_add = "C:\\Development\\SVN\\Amerisure\\Analytics\\trunk\\TextAnalytics\\common\\dictionary_words_no_dups.txt"
    _notes_to_add = "C:\\Development\\SVN\\Amerisure\\Analytics\\trunk\\TextAnalytics\\common\\workers_comp_dictionary_freq_p9.txt"
    _alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    #Constructor
    def __init__(self):
        self._original_correct_dict = self.open_sesame(self._original_correct_dict)
        
        '''
        #If you are just wanting to add two dictionaries together. Existing and one you want to add on:
        #1) Train
        #2) Call add function on this in main()
        '''
        
        self._add_me_to_final = self.train(self.find_words(open(self._dictionary_to_add,'r').read()))
        
        '''
        #Notes that may have mispelled words:
        #1)Train to get dictionary mapping w/freq.
        #2)Compare to a correct dictionary(original_correct_dict)
        #3)Add _notes_correct_dict by call in main()
        '''
        #self._notes_to_add = self.train(self.find_words(open(self._notes_to_add,'r').read())) 
        #self._notes_correct_dict = self.compare(self.original_correct_dict, self._notes_to_add)
        
    #Accessors
    def get_words(self):
        return self._original_correct_dict
    @staticmethod
    def find_words(text):
        return re.findall("[a-z/-]+", text.lower())
    
    def word_probability(self,word,N=0):
        N=sum(self._original_correct_dict.values())
        return self._original_correct_dict[word] / N
    @staticmethod
    def open_sesame(filename):
        model = collections.defaultdict(lambda: 0)
        with open(filename) as f:
            for line in f:
                (key, val) = line.split(":")
                model[key] = int(val) #all unique words so all 1
        return model
    
    def edits(self,word):
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in s if b for c in self._alphabet]
        inserts    = [a + c + b     for a, b in s for c in self._alphabet]
        return set(deletes + transposes + replaces + inserts)
        
    def edits2(self, word):
        return (e2 for e1 in self.edits(word) for e2 in self.edits(e1))
        
    def known(self,words):
        return set(w for w in words if w in self._original_correct_dict)   

    def correct(self,word):
        candidates = self.known([word]) or self.known(self.edits(word)) or self.known(self.edits2(word)) or [word]
        return max(candidates, key=self.word_probability)
  
    #########################################  FUNCTIONS BELOW USED FOR TRANSFORM TXT                               #########################################
    #########################################  TO DICTIONARY FORMAT THEN ADDING THAT DICTIONARY TO FINAL DICTIONARY #########################################
    @staticmethod
    def train(features):
        '''
        Function just allows to convert notes/text file to a frequency dictionary
        Train function meant for NOTES/TEXT FILE WORD FREQUENCY! NOT 1 FOR ALL
        Unless you are training a unique word dictionary(no duplicates)
        '''
        model = collections.defaultdict(lambda: 0)
        for f in features:
            if f in model:
                model[f] += 1
            else:
                model[f] = 1
        return model
            
    def add(self, dictionary, update=0): #Update = do you want to update the already existing dictionary words?
        b = True
        for w in dictionary:
            if w in self._original_correct_dict:
                if update == 1:
                    self._original_correct_dict[w] += dictionary[w]
            else: #If word doesn't exist
                self._original_correct_dict[w] += 1
        while b:
            do = input("Do you wish to rewrite dictionary?")
            if do.lower() == "yes":
                self.writes(self._original_correct_dict)
                b = False
            elif do.lower() == "no":
                b = False
            elif do.lower() == "exit":
                b = False
            else:
                print("Incorrect statement. Try again.")
            
    ############################################################################################################################################################
    ############################################################################################################################################################
    @staticmethod
    def compare(words, medwords):
        '''
        Compares two dictionaries and writes the new model. Do this first before adding if you have notes.
        '''
        model = collections.defaultdict(lambda: 0)
        for w in words:
            for mw in medwords:
                if w == mw:
                    val = int(words[w]) + int(medwords[mw])
                    model[w] += val
                val = 0
        return model
    @staticmethod
    def writes(model): #write function doesn't overwrite dictionaries for version/history retention.
        for i in range(10):
            filename = 'C:\\Development\\SVN\\Amerisure\\Analytics\\trunk\\TextAnalytics\\translation\\f_workers_comp_dictionary{}.txt'.format(str(i))
            exists = os.path.isfile(filename)
            if exists:
                continue
            else:
                model_sorted = OrderedDict(sorted(model.items(), key=itemgetter(1), reverse = True))
                with open('f_workers_comp_dictionary' + str(i) + '.txt', 'w') as f:
                    for key, value in model_sorted.items():
                        f.write('%s:%s\n' % (key, value))
                f.close()
            break
        
def main():
    #add function:
    #1 = update existing dict words
    #0 = don't update any existing words
    d = Dictionary()
    #d.add(d._add_me_to_final,1
    

if __name__ == '__main__':
    main()
