import streamlit as st
import pandas as pd 
import numpy as np
import joblib
from PIL import Image,ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns



def main():
    
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..',["-","Tahmin Yap","Hakkında"])

    if selected_page == "-":
        image = Image.open('laptop.jpg')
        st.image(image, use_column_width=True)
        st.title('Streamlit Uygulamasına Hoşgeldiniz 👋')

        st.markdown(
            """
            Bu proje makine öğrenmesi uygulamalarının web ortamında streamlit
            kullanılarak yayınlanmasına örnek olarak geliştirilmiştir. Bir e-ticaret sitesi üzerinden 1776 adet laptop verileri çekilmiş
            ve incelenmiştir. Bu veriler kullanılarak makine öğrenmesi modelleri eğitilmiş ve en iyi sonuc veren 3 algoritma kullanılmıştır.
            
            """)
        st.info("Tahmin yapmak ve proje hakkında daha fazla bilgi edinmek için sol tarafta bulunan menüyü kullanınız.")
        


    if selected_page == "Tahmin Yap":
        predict()
    
    
    if selected_page == "Hakkında":
        about() 
    

def about():
    image = Image.open('tf.jpg')
    st.image(image, use_column_width=True)

    st.title('Geliştirici Bilgileri')
    st.subheader('Github Adresi : [Veli Yarar](https://github.com/VeliYarar/)')
    st.subheader('Mail Adresi : veli1133yarar@gmail.com')


def predict():

    # Markalar ve Modellerin yüklenmesi
    markalar = load_data_marka()
    ekran_kartlari = load_data_ekran_karti()
    islemci_tipleri = load_data_islemci_tipi()
    isletim_sistemleri = load_data_isletim_sistemi()

    # Kullanıcı arayüzü ve değer alma
    st.title('Merhaba, *Streamlit!* 👨‍💻')

    #ekran boyutu secimi
    selected_ekran_boyutu = st.number_input('Ekran Boyutu',min_value=0.0, max_value=30.0, step=0.10)
    #st.write("Ekran Boyutu :"+str(selected_ekran_boyutu)+" İNÇ")

    # ekran kartı secimi
    selected_ekran_karti = ekran_karti_index(ekran_kartlari,st.selectbox('Ekran Kartı Seçiniz..',ekran_kartlari))

    # Ekran_Yenileme_Hizi secimi
    selected_Ekran_Yenileme_Hizi = st.number_input('Ekran tazeleme hızı',min_value=0,max_value=300)
    # st.write("Ekran tazeleme hızı :"+str(selected_Ekran_Yenileme_Hizi)+" HZ")

    # Hard_Disk_Kapasitesi secimi 
    selected_Hard_Disk_Kapasitesi = st.number_input('Hard disk Kabasitesi',min_value=0,max_value=2000)
    # st.write("Hard disk Kabasitesi :"+str(selected_Hard_Disk_Kapasitesi)+" GB")
    
    # ram secimi
    selected_ram = st.number_input('RAM Kabasitesi',min_value=0,max_value=100)
    # st.write("Ram Kapasitesi :"+str(selected_ram)+" GB")

    # ssd secimi
    selected_ssd = st.number_input('SSD Kabasitesi',min_value=0,max_value=2000)
    # st.write("SSD Kabasitesi :"+str(selected_ssd)+" GB")

    # Islemci_Nesli secimi
    selected_Islemci_Nesli = st.number_input('Islemci Nesil',min_value=0,max_value=100)
    # st.write("Islemci Nesli :"+str(selected_Islemci_Nesli)+" Nesil")
    
    # Islemci_Tipi secimi
    selected_Islemci_Tipi = islemci_tipi_index(islemci_tipleri,st.selectbox('İşlemci Tipi Seçiniz..',islemci_tipleri))

    # Isletim_Sistemi secimi
    selected_Isletim_Sistemi = isletim_sistemi_index(isletim_sistemleri,st.selectbox('İşletim Sistemi Seçiniz..',isletim_sistemleri))

    # marka secimi
    selected_marka = marka_index(markalar,st.selectbox('Marka Seçiniz..',markalar))


    # model secimi

    selected_model = st.selectbox('Tahmin Modeli Seçiniz..',["Random Forest","KNN(k-Nearest Neighbors)","Decision Tree"])

    prediction_value = create_prediction_value(selected_ekran_boyutu,selected_ekran_karti,selected_Ekran_Yenileme_Hizi,
                                               selected_Hard_Disk_Kapasitesi,selected_ram,selected_ssd,selected_Islemci_Nesli,
                                               selected_Islemci_Tipi,selected_Isletim_Sistemi,selected_marka)
    
    prediction_model = load_models(selected_model)


    if st.button("Tahmin Yap"):
            result = predict_models(prediction_model,prediction_value)
            if result != None:
                st.success('Tahmin Başarılı')
                st.balloons()
                st.write("Tahmin Edilen Fiyat: "+ result + "TL")
            else:
                st.error('Tahmin yaparken hata meydana geldi..!')




def load_data_marka():
    markalar = pd.read_csv("markalar.csv")
    return markalar

def load_data_ekran_karti():
    ekran_kartlari= pd.read_csv("Ekran_Karti_Sirali.csv")
    return ekran_kartlari

def load_data_islemci_tipi():
    islemci_Tipi= pd.read_csv("Islemci_Tipi_Sirali.csv")
    return islemci_Tipi

def load_data_isletim_sistemi():
    isletim_sistemi= pd.read_csv("Isletim_Sistemleri_Sirali.csv")
    return isletim_sistemi




def load_models(modelName):
    if modelName == "Random Forest":
        dt_model = joblib.load("laptop_random_forest_model.pkl")
        return dt_model

    elif modelName == "KNN(k-Nearest Neighbors)":
        mlinear_model = joblib.load("KNN_model.pkl")
        return mlinear_model

    elif modelName == "Decision Tree":  
        rf_model = joblib.load("laptop_decision_tree_model.pkl")
        return rf_model

    else:
        st.write("Model yüklenirken hata meydana geldi..!")
        return 0


def marka_index(markalar,marka):
    index = int(markalar[markalar["Markalar"]==marka].index.values)
    return index

def ekran_karti_index(ekran_kartlari,ekran_karti):
    index1 = int(ekran_kartlari[ekran_kartlari["Ekran_Karti"]==ekran_karti].index.values)
    return index1

def islemci_tipi_index(islemci_tipleri,islemci_tipi):
    index2 = int(islemci_tipleri[islemci_tipleri["Islemci_Tipi"]==islemci_tipi].index.values)
    return index2

def isletim_sistemi_index(isletim_sistemleri,isletim_sistemi):
    index3 = int(isletim_sistemleri[isletim_sistemleri["Isletim_Sistemleri"]==isletim_sistemi].index.values)
    return index3





def create_prediction_value(selected_ekran_boyutu,selected_ekran_karti,selected_Ekran_Yenileme_Hizi,
                            selected_Hard_Disk_Kapasitesi,selected_ram,selected_ssd,selected_Islemci_Nesli,
                            selected_Islemci_Tipi,selected_Isletim_Sistemi,selected_marka):
    
    res = pd.DataFrame(data = 
            {'Ekran_Boyutu':[selected_ekran_boyutu],'Ekran_Karti':[selected_ekran_karti],'Ekran_Yenileme_Hizi':[selected_Ekran_Yenileme_Hizi],'Hard_Disk_Kapasitesi':[selected_Hard_Disk_Kapasitesi],
             'Ram':[selected_ram],'SSD_Kapasitesi':[selected_ssd],'Islemci_Nesli':[selected_Islemci_Nesli],'Islemci_Tipi':[selected_Islemci_Tipi],'Isletim_Sistemi':[selected_Isletim_Sistemi],
             'Marka':[selected_marka]})
   
    return res


def predict_models(model,res):
    result = str(int(model.predict(res)*1000)).strip('[]')
    return result



if __name__ == "__main__":
    main()


# streamlit run "c:\Users\veli1\Desktop\End To End Machine Learning Laptops Price Prediction\Streamlit_App\laptop.py"
