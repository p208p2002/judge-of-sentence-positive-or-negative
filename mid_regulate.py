# -*- coding: utf-8 -*-
# 找出字典相似度中心
from gensim.models import word2vec
from gensim import models
import pickle

def compareSimilar(str_a,str_b):
    try:
        val = model.wv.similarity(str_a,str_b)
    except:
        val = 0.0
    return val

def avg(lst): 
    return sum(lst) / len(lst)

def regulate(data):
    similarValRec = {}
    for wordA in data:
        similarVals = []
        for wordB in data:
            if wordA == wordB:
                continue
            similarVal = compareSimilar(wordA,wordB)
            similarVals.append(similarVal)
        #
        similarValRec[wordA] = avg(similarVals)
    
    sortDic = sorted(similarValRec.items(), key=lambda kv: kv[1], reverse=True)    
    for i in range(10):
        print(i,sortDic[i])
    bestFitKey,val = sortDic[0]
    return bestFitKey

if __name__ == "__main__":
    # load model
    model = models.Word2Vec.load('w2vmodel/word2vec.model')

    # 正面詞集
    with open('dict/positive_words.txt','r',encoding='utf-8') as f:
        data = f.read()
    data = data.split()

    # 反面詞集
    with open('dict/negative_words.txt','r',encoding='utf-8') as f:
        data2 = f.read()
    data2 = data2.split()

    keys = []
    print("正面詞校正...")
    key = regulate(data)
    keys.append(key)
    print("反面詞校正...")
    key = regulate(data2)
    keys.append(key)

    # 儲存校正
    save = ''
    for k in keys :
        save = save + k + '\n'
    with open('regulatefiles/regulate.txt','w',encoding='utf-8') as f:
        f.write(save)

