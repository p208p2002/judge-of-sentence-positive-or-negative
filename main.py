from JOSPON import JOSPON
if __name__ == "__main__":
    jospon = JOSPON()
    while(True):
        sentense = input('輸入句子: ')
        jospon.eval(sentense)
