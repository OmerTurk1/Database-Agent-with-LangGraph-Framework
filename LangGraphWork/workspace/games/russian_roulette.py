# Basit bir Rus ruleti oyunu
import random

def russian_roulette():
    # 6 odacıklı bir silah
    chambers = [0, 0, 0, 0, 0, 1]
    random.shuffle(chambers)
    return chambers[0] == 1

if __name__ == "__main__":
    print("Rus ruleti oynanıyor...")
    if russian_roulette():
        print("Patlama! Kaybettiniz.")
    else:
        print("Şanslısınız! Hayatta kaldınız.")