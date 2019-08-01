import jieba
from gensim.models import word2vec
from gensim import models


class JOSPON():
    def __init__(self,stopword_dict_path ='blacklists/words.txt'):
        #
        self.stopword_set = self.__loadStopWord(stopword_dict_path)
        self.model = models.Word2Vec.load('w2vmodel/word2vec.model')
        self.middleOfPostive, self.middleOfNegative = self.__loadRegulateFiles()
        self.postiveData, self.negativeData = self.__loadPNWords()
        self.weightingWords = self.__loadWeightingWords()
        self.opsiteWords = self.__loadOpsiteWords()
        self.__weightingFlag = False
        self.__opsiteFlag = False
        #
        self.__initJieba()

    def disableStopwords(self):
        self.stopword_set = set()

    def compareSimilar(self, str_a, str_b):
        try:
            val = self.model.wv.similarity(str_a,str_b)
            if(val < 0.0):
                val = 0.0
        except:
            val = 0.0
        return val
    
    def test(self, testFilePath = 'testcases/test.txt', hasAns=True):
        with open(testFilePath,'r',encoding='utf-8') as f:
            testCases = f.read()
        testCases = testCases.split('\n')
        testCasesCount = len(testCases)
        passCount = 0
        if(hasAns):
            for tc in testCases:
                tc = tc.split(' ')
                casePass = self.eval(tc[0],tc[1])
                print('=>',casePass)
                if(casePass == 'PASS'):
                    passCount += 1
                print()
            print('正確率',passCount,'/',testCasesCount,passCount/testCasesCount)
        else:
            for tc in testCases:
                tc = tc.split('\n')
                casePass = self.eval(tc[0])
                print()

    def eval(self,targetSentence,ans=None):
        if(ans != None):
            ans = int(ans)
        words = jieba.cut(targetSentence, cut_all=False)
        splitData = []
        splitDataVal_postive = []
        splitDataVal_negative = []
        for word in words:
            if not word in self.stopword_set:
                splitData.append(word)
                pVal = self.compareSimilar(self.middleOfPostive,word)                
                nVal = self.compareSimilar(self.middleOfNegative,word)
                
                # 語氣字FLAG                
                if(self.__weightingFlag == True and (pVal != 0.0 or nVal != 0.0)):
                    self.__weightingFlag = False
                    weightVal = 2.0
                elif(self.__weightingFlag == False):
                    weightVal = 1.5

                    
                # 關鍵字加權
                if word in self.postiveData:
                    if(pVal == 0.0):
                        pVal = 0.5
                    else:
                        pVal = pVal*weightVal
                elif word in self.negativeData:
                    if(nVal == 0.0):
                        nVal = 0.5
                    else:
                        nVal = nVal*weightVal

                # 反面字FLAG，交換分數
                if(self.__opsiteFlag == False):
                    pass
                elif(self.__opsiteFlag == True and (pVal != 0.0 or nVal != 0.0)):
                    self.__opsiteFlag == False
                    tmp = pVal
                    pVal = nVal
                    nVal = tmp
                
                # 語氣字加權
                if word in self.weightingWords:
                    self.__weightingFlag = True
                
                # 反面字
                if word in self.opsiteWords:
                    self.__opsiteFlag = True

                splitDataVal_postive.append(pVal)
                splitDataVal_negative.append(nVal)
        
        # flag 復位
        self.__opsiteFlag = False
        self.__weightingFlag = False
        
        if(ans != None):
            print(targetSentence,ans)
        else:
            print(targetSentence)
        print(splitData)
        pSum = sum(splitDataVal_postive)*100
        nSum = sum(splitDataVal_negative)*100
        print("P:",pSum)
        print(splitDataVal_postive)
        print("N:",nSum)
        print(splitDataVal_negative)
        if((pSum+nSum)*0.06 >= abs(pSum-nSum)): #差距小於總分的8%
            print("=> 中立",pSum-nSum)
            if(ans == 0):
                return 'PASS'
        elif(pSum>nSum):
            print("=> 正面",pSum-nSum)
            if(ans == 1):
                return 'PASS'
        else:
            print("=> 反面",pSum-nSum)
            if(ans == -1):                
                return 'PASS'
        return 'NO_PASS'
        
        
    def __initJieba(self, dictPath = 'dict/dict.txt.big', userDictPath = 'dict/my_dict'):
        # jieba字典
        jieba.set_dictionary(dictPath)
        jieba.load_userdict(userDictPath)
        jieba.initialize()
    
    def __loadStopWord(self, stopWordDictPath):
        stopword_set = set()
        with open(stopWordDictPath ,'r', encoding='utf-8') as stopwords:
            for stopword in stopwords:
                stopword_set.add(stopword.strip('\n'))
        return stopword_set
    
    def __loadOpsiteWords(self, opsiteWordsPath = 'dict/opsitewords.txt'):
        with open(opsiteWordsPath ,'r', encoding='utf-8') as f:
            opsiteWords = f.read()
        opsiteWords = opsiteWords.split()
        return opsiteWords
    
    def __loadWeightingWords(self, weightingWordsPath = 'dict/weightingwords.txt'):
        with open(weightingWordsPath ,'r', encoding='utf-8') as f:
            weightingWords = f.read()
        weightingWords = weightingWords.split()
        return weightingWords
        
    def __loadRegulateFiles(self, reuglateFilesPath = 'regulatefiles/regulate.txt'):
        with open(reuglateFilesPath ,'r',encoding='utf-8') as f:
            middleWord = f.read()
        middleWord = middleWord.split()
        middleOfPostive = middleWord[0]
        middleOfNegative = middleWord[1]
        return (middleOfPostive,middleOfNegative)

    def __loadPNWords(self, positiveWordsDictPath = 'dict/positive_words.txt', negativeWordsDictPath = 'dict/negative_words.txt'):
        # 正面詞集
        with open(positiveWordsDictPath ,'r',encoding='utf-8') as f:
            data = f.read()
        postiveData = data.split()
        # 反面詞集
        with open(negativeWordsDictPath ,'r',encoding='utf-8') as f:
            data = f.read()
        negativeData = data.split()
        return (postiveData,negativeData)