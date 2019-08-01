from JOSPON import JOSPON
if __name__ == "__main__":
    jospon = JOSPON()
    jospon.disableStopwords()
    jospon.test('testcases/test.txt')