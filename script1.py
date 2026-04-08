import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.title("Projekt - Analiza API")
st.write("Dashboard pokazujący dane z JSONPlaceholder.")

# pobieranie danych z neta
r1 = requests.get("https://jsonplaceholder.typicode.com/users")
ludzie = r1.json()

r2 = requests.get("https://jsonplaceholder.typicode.com/todos")
zadania = r2.json()

# wrzucam do dataframe zeby bylo latwiej
df_ludzie = pd.DataFrame(ludzie)
df_zadania = pd.DataFrame(zadania)

# łączenie tabel (znalazlem funkcje merge)
razem = pd.merge(df_zadania, df_ludzie[['id', 'name']], left_on='userId', right_on='id')
razem = razem.rename(columns={'name': 'user_name'})

# liczenie statystyk
wszystko = len(razem)
gotowe = len(razem[razem['completed'] == True])
procent = (gotowe / wszystko) * 100

# szukanie kto zrobil najwiecej
najlepszy = razem[razem['completed'] == True]['user_name'].value_counts().idxmax()

st.subheader("Statystyki")
c1, c2, c3 = st.columns(3)
c1.metric("Wszystkie zadania", wszystko)
c2.metric("Ukonczone (%)", str(round(procent, 1)) + "%")
c3.metric("Najlepszy pracownik", najlepszy)

st.divider()

# WYKRESY
st.subheader("Wykresy")
k1, k2 = st.columns(2)

with k1:
    st.write("Status zadań")

    # przygotowanie danych do kolowego
    zliczone = razem['completed'].value_counts().reset_index()
    zliczone.columns = ['Status', 'Ile']
    zliczone['Status'] = zliczone['Status'].map({True: 'Zrobione', False: 'Do zrobienia'})

    wykres1 = px.pie(zliczone, values='Ile', names='Status')
    st.plotly_chart(wykres1, use_container_width=True)

with k2:
    st.write("Zadania na osobe")

    # grupowanie dla slupkowego
    grupa = razem.groupby('user_name')['completed'].count().reset_index()
    grupa.columns = ['Kto', 'Ile']

    wykres2 = px.bar(grupa, x='Kto', y='Ile', text_auto=True)
    st.plotly_chart(wykres2, use_container_width=True)

# pokaz surowe dane na dole
with st.expander("Kliknij zeby zobaczyc tabele"):
    st.dataframe(razem[['user_name', 'title', 'completed']].head(10))