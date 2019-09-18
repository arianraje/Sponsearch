from nltk.tokenize import word_tokenize, sent_tokenize
import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

stop_file = open("Stop_Words.txt", "r")
stop_words = word_tokenize(stop_file.read())

class Compare():

    def find_tags(self, string):
        words = word_tokenize(string)
        words = [word for word in words if word not in stop_words]
        word_counter = {}
        for word in words:
            if word in word_counter.keys():
                word_counter[word] += 1
            else:
                word_counter[word] = 1
        sorted_words = sorted(word_counter, key = word_counter.get, reverse = True)
        tags = sorted_words[:5]
        return tags

    def compare_tags(self, tags1, tags2):
        return len(set(tags1).intersection(tags2))/len(tags1)

    def compare_summaries(self, summ1, summ2):
        sentences1 = sent_tokenize(summ1)
        sentences2 = sent_tokenize(summ2)
        sim_score = 0
        for sent1 in sentences1:
            for sent2 in sentences2:
                doc1 = nlp(u"{}".format(sent1))
                doc2 = nlp(u"{}".format(sent2))
                score = doc1.similarity(doc2)
                sim_score += score
        sim_score = sim_score/(len(summ1) + len(summ2))
        return sim_score

    def fin_score(self, account1, account2):
        return (self.compare_summaries(account1["Profile"], account2["Profile"]) + self.compare_tags(account1["Tags"], account2["Tags"]))/2
