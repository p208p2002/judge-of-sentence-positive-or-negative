from JOSPON import JOSPON
if __name__ == "__main__":
    jospon = JOSPON(stopword_dict_path = 'dict/stopwords')
    # jospon.disableStopwords()
    jospon.test('testcases/test4.txt', hasAns = False)