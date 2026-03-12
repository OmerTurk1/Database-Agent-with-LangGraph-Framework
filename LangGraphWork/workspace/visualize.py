import pandas as pd
import matplotlib.pyplot as plt

def visualize_data(file_path):
    # CSV dosyasını oku
    data = pd.read_csv(file_path)
    
    # Verileri görselleştir
    plt.figure(figsize=(10, 6))
    plt.plot(data['Number'], data['Square'], label='Square', marker='o')
    plt.plot(data['Number'], data['Cube'], label='Cube', marker='s')
    
    plt.title('Numbers, Squares, and Cubes')
    plt.xlabel('Number')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# CSV dosyasını görselleştir
visualize_data('numbers.csv')