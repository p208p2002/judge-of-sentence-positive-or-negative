import jieba
from gensim.models import word2vec
from gensim import models


class JOSPON():
    def __init__(self):
        #
        self.stopword_set = self.__loadStopWord()
        self.model = models.Word2Vec.load('w2vmodel/word2vec.model')
        self.middleOfPostive, self.middleOfNegative = self.__loadRegulateFiles()
        self.postiveData, self.negativeData = self.__loadPNWords()
        #
        self.__initJieba()

    def compareSimilar(self, str_a, str_b):
        try:
            val = self.model.wv.similarity(str_a,str_b)
        except:
            val = 0.0
        return val
    
    def test(self):
        with open('testcases/test.txt','r',encoding='utf-8') as f:
            testCases = f.read()
        testCases = testCases.split('\n')
        testCasesCount = len(testCases)
        passCount = 0
        for tc in testCases:
            tc = tc.split(' ')
            try:
                ans = int(tc[1])
            except:
                ans = 0
            tc = tc[0]
            words = jieba.cut(tc, cut_all=False)
            splitData = []
            splitDataVal_postive = []
            splitDataVal_negative = []
            for word in words:
                if not word in self.stopword_set:
                    splitData.append(word)
                    pVal = self.compareSimilar(self.middleOfPostive,word)                
                    nVal = self.compareSimilar(self.middleOfNegative,word)
                    
                    # 加權
                    if word in self.postiveData:
                        pVal = pVal*1.5
                    elif word in self.negativeData:
                        nVal = nVal*1.5

                    splitDataVal_postive.append(pVal)
                    splitDataVal_negative.append(nVal)
            
            print(tc,ans)
            print(splitData)
            pSum = sum(splitDataVal_postive)*100
            nSum = sum(splitDataVal_negative)*100
            print("P:",pSum)
            print(splitDataVal_postive)
            print("N:",nSum)
            print(splitDataVal_negative)
            if((pSum+nSum)*0.07 >= abs(pSum-nSum)): #差距小於總分的8%
                print("中立",pSum-nSum)
                if(ans == 0):
                    passCount += 1
                    print("**pass**")
            elif(pSum>nSum):
                print("正面",pSum-nSum)
                if(ans == 1):
                    passCount += 1
                    print("**pass**")
            else:
                print("反面",pSum-nSum)
                if(ans == -1):
                    passCount += 1
                    print("**pass**")
            print("\n")
        #
        print('正確率',passCount,'/',testCasesCount,passCount/testCasesCount)
        
        
    def __initJieba(self):
        # jieba字典
        jieba.set_dictionary('dict/dict.txt.big')
        jieba.initialize()
    
    def __loadStopWord(self):
        stopword_set = set()
        with open('blacklists/words.txt','r', encoding='utf-8') as stopwords:
            for stopword in stopwords:
                stopword_set.add(stopword.strip('\n'))
        return stopword_set
    
    def __loadRegulateFiles(self):
        with open('regulatefiles/regulate.txt','r',encoding='utf-8') as f:
            middleWord = f.read()
        middleWord = middleWord.split()
        middleOfPostive = middleWord[0]
        middleOfNegative = middleWord[1]
        return (middleOfPostive,middleOfNegative)

    def __loadPNWords(self):
        # 正面詞集
        with open('dict/positive_words.txt','r',encoding='utf-8') as f:
            data = f.read()
        postiveData = data.split()
        # 反面詞集
        with open('dict/negative_words.txt','r',encoding='utf-8') as f:
            data = f.read()
        negativeData = data.split()
        return (postiveData,negativeData)
    

if __name__ == "__main__":    
    jospon = JOSPON()
    jospon.test()