import pandas as pd
import streamlit as st

# Charger le fichier CSV
uploaded_file = st.file_uploader("Télécharger le fichier CSV", type=["csv"])

if uploaded_file is not None:
    # Lire le CSV dans un DataFrame
    df = pd.read_csv(uploaded_file)

    necessary_columns = ["Date de début de l'évènement", "Heure de début de l'évènement",
                         "Date de fin de l'évènement", "Heure de fin de l'évènement",
                         "Description de l'évènement", "Catégories d'Évènement"]
    for col in necessary_columns:
        if col not in df.columns:
            df[col] = None

    st.write("Modifier les données pour chaque cours :")
    new_data = []
    for index, row in df.iterrows():
        st.write("------")  # Ajoute un séparateur visuel
        row_data = []
        for col in df.columns:
            if 'Date' in col or 'Heure' in col:
                st.markdown(f"<h6 style='color: #DD373B; margin-top: 0px;'>{col}</h6>", unsafe_allow_html=True)
                date_time_value = pd.to_datetime(row[col], errors='coerce')
                if 'Date' in col:
                    new_value = st.date_input("", value=date_time_value if pd.notna(date_time_value) else None, key=f"{col}_{index}")
                    formatted_value = new_value.strftime('%d/%m/%Y') if pd.notna(new_value) else ''
                else:
                    new_value = st.time_input("", value=date_time_value.time() if pd.notna(date_time_value) else None, key=f"{col}_{index}")
                    formatted_value = new_value.strftime('%H:%M') if new_value else ''
                row_data.append(formatted_value)
            elif col == "Description de l'évènement" or col == "Catégories d'Évènement":
                st.markdown(f"<h6 style='color: #DD373B; margin-bottom: 0px;'>{col}</h6>", unsafe_allow_html=True)
                if col == "Description de l'évènement":
                    new_value = st.text_area("", value=row[col], key=f"{col}_{index}")
                else:
                    options = ["AlphabeTICaction", "Formation", "Pratique Libre", "Programme Préparatoire à l’Emploi PPE"]
                    new_value = st.selectbox("", options, index=options.index(row[col]) if row[col] in options else 0, key=f"{col}_{index}")
                row_data.append(new_value)
            else:
                new_value = st.text_input(f"{col} pour {row['Cours']}", value=row[col], key=f"{col}_{index}")
                row_data.append(new_value)
        new_data.append(row_data)

    df = pd.DataFrame(new_data, columns=df.columns)
    st.download_button(
        label="Télécharger le CSV modifié",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="cours_modifié.csv",
        mime='text/csv',
    )
