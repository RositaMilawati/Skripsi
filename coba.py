import streamlit as st
import requests 
import pandas as pd
import matplotlib.pyplot as plt
import time

hide_st_style = """
<style>
footer {visibility: hidden;}
[data-testid="column"] {
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 3%;
    border-radius: 5px;
    
    border-left: 0.5rem solid #CCCCCC !important;
    border-right: 0.5rem solid #CCCCCC !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
    }
[data-testid="stMarkdownContainer"]{
    font-weight: 700 !important;
    text-transform: uppercase !important;
}

</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

def load(data):
    res = requests.get(f'https://blynk.cloud/external/api/get?token=c7eJuI9iMv7A8vhDEY_VpQj8BIWCqr5n&{data}')
    return res.text

def app():
    st.header("Monitoring & Sensor Data")
    st.header("SISTEM PENDETEKSI KEBAKARAN")

    data = {
        'Timestamp': [],
        'Suhu (°C)': [],
        'Kelembaban (%Rh)': [],
        'Asap': [],
        'Api': []
    }

    placeholder = st.empty()

    for seconds in range(10):
        with placeholder.container():
            col1, col2, col3, col4 = st.columns(4)

            suhu = load("V0")
            kelembaban = load("V1")
            asap = load("V2")
            api = load("V3")

            col1.metric("Suhu", suhu + "°C")
            col2.metric("Kelembaban", kelembaban + "%Rh")
            col3.metric("Asap", asap)
            col4.metric("Api", api)

            # suhu='40'     
            data['Timestamp'].append(pd.Timestamp.now())
            data['Suhu (°C)'].append(float(suhu))  # Convert to float
            data['Kelembaban (%Rh)'].append(float(kelembaban))  # Convert to float
            data['Asap'].append(int(asap))  # Convert to integer
            data['Api'].append(int(api))  # Convert to integer

            time.sleep(1)

    df = pd.DataFrame(data)

    # if st.button("Show Data Sensors"):
    st.dataframe(df)
    # Simpan DataFrame ke file CSV
    df.to_csv('data_sensor.csv', index=False)
    st.success("Data berhasil disimpan ke file CSV.")

    # if st.button("Plot Data"):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Timestamp'], df['Suhu (°C)'], label='Suhu (°C)')
    plt.plot(df['Timestamp'], df['Kelembaban (%Rh)'], label='Kelembaban (%Rh)')
    plt.plot(df['Timestamp'], df['Asap'], label='Asap')
    plt.plot(df['Timestamp'], df['Api'], label='Api')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.title('Sensor Data Over Time')
    plt.legend()
    st.pyplot(plt)

    # Analisa outlier dengan metode  interquartile range (IQR)
    st.header("Analisa Outlier Data SUHU dengan metode  interquartile range (IQR)")
    q1 = df['Suhu (°C)'].quantile(0.25)
    q3 = df['Suhu (°C)'].quantile(0.75)
    inner_fence = q1 - 1.5 * (q3 - q1)
    outer_fence = q3 + 1.5 * (q3 - q1)
    outer_fence=32
    #  outliers_suhu = df['Suhu (°C)'][df['Suhu (°C)'] < inner_fence] | df['Suhu (°C)'][df['Suhu (°C)'] > outer_fence]
    outliers_suhu = df['Suhu (°C)'][df['Suhu (°C)'] > outer_fence]
    st.write("Batas Suhu Kuartil 3 /  q3 : ",q3)
    st.write("Deteksi Outlier Suhu Yang Menyimpang : ",outliers_suhu)

    if outliers_suhu.empty :
        st.warning("Suhu dalam keadaan normal")
    else:
        st.warning("AWASI SUHU MULAI TIDAK NORMAL")

    if 'Api' in df and df['Api'].any() == '1':
        st.warning("Awas ada tanda Terjadi KEBAKARAN")
    else:
        st.warning("Kondisi AMAN tidak ada tanda TERJADI KEBAKARAN")

    
app_mode = st.sidebar.selectbox('MENU', ['Dashboard', 'Monitoring & Sensor Data'])

if app_mode == 'Dashboard':
    st.header('Perancangan Sistem Pendeteksi Kebakaran Terkontrol Telegram Untuk Sistem Keamanan Laboratorium Komputer Pada SMKN 13 Kota Bekasi')
    st.image('logo_unsada.png')
    st.markdown('Dibuat Oleh :')
    st.subheader('Rosita Milawati - 2019230038')    

elif app_mode == 'Monitoring & Sensor Data':
    app()