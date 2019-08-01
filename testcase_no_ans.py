from JOSPON import JOSPON
if __name__ == "__main__":
    jospon = JOSPON(stopword_dict_path = 'blacklists/words_b.txt')
    # jospon.disableStopwords()
    jospon.test('testcases/test3.txt', hasAns = False)