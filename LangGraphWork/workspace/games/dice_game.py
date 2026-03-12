# Basit bir zar oyunu
import random

def roll_dice():
    return random.randint(1, 6)

if __name__ == "__main__":
    print("Zar atılıyor...")
    result = roll_dice()
    print(f"Sonuç: {result}")