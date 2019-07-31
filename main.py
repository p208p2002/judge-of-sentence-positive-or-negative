import jieba
from gensim.models import word2vec
from gensim import models

def compareSimilar(str_a,str_b):
    try:
        val = model.wv.similarity(str_a,str_b)
    except:
        val = 0.0
    return val

if __name__ == "__main__":
    # jieba字典
    jieba.set_dictionary('dict/dict.txt.big')

    # 停用詞表
    stopword_set = set()
    with open('blacklists/words.txt','r', encoding='utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))    
    
    jieba.initialize()

    # 預訓練模型
    model = models.Word2Vec.load('w2vmodel/word2vec.model')

    # 校正中心字
    with open('regulatefiles/regulate.txt','r',encoding='utf-8') as f:
        middleWord = f.read()
    middleWord = middleWord.split()
    middleOfPostive = middleWord[0]
    middleOfNegative = middleWord[1]
    print(middleOfPostive,middleOfNegative)

    # 測試檔案
    with open('testcases/test.txt','r',encoding='utf-8') as f:
        testCases = f.read()    
    testCases = testCases.split()

    for tc in testCases:
        words = jieba.cut(tc, cut_all=False)
        splitData = []
        splitDataVal_postive = []
        splitDataVal_negative = []
        for word in words:
            if not word in stopword_set:
                splitData.append(word)
                pVal = compareSimilar(middleOfPostive,word)
                splitDataVal_postive.append(pVal)
                nVal = compareSimilar(middleOfNegative,word)
                splitDataVal_negative.append(nVal)
        
        print(tc)
        print(splitData)
        pSum = sum(splitDataVal_postive)*100
        nSum = sum(splitDataVal_negative)*100
        print("P:",pSum)
        print("N:",nSum)
        if((pSum+nSum)*0.08 >= abs(pSum-nSum)): #差距小於總分的8%
            print("中立",pSum-nSum)
        elif(pSum>nSum):
            print("正面",pSum-nSum)
        else:
            print("反面",pSum-nSum)
        print("\n")
        