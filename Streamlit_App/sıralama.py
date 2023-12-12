import pandas as pd

# Verilen liste
Isletim_Sistemleri = [
    "Chrome OS", "Free Dos", "Linux", "Mac Os", "Ubuntu", "Windows", "Windows 11"
]

# Liste verilerini içeren bir DataFrame oluştur
df_os = pd.DataFrame({'Isletim_Sistemleri': Isletim_Sistemleri})

# DataFrame'i alfabetik sıraya göre sırala
df_sorted_os = df_os.sort_values(by='Isletim_Sistemleri')

# Sıralı DataFrame'i CSV dosyasına yazdır
df_sorted_os.to_csv('Isletim_Sistemleri_Sirali.csv', index=False)

print("CSV dosyası oluşturuldu: Isletim_Sistemleri_Sirali.csv")
