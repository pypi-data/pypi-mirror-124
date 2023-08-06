#
import random
def rich():
    reds = ["01","02","03","04","05", "06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","33"]
    blues =["01","02","03","04","05", "06","07","08","09","10","11","12","13","14","15","16"]
    reds_you_get = []
    for i in range(6):
        x = random.choice(reds)
        reds_you_get.append(x)
        reds.remove(x)

    blue = random.choice(blues)
    blue = "['" +str(blue) +"']"
    print( sorted(reds_you_get), blue )
