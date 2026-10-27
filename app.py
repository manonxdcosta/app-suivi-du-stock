import streamlit as st
import pandas as pd
EXCEL_PATH = r"C:/Scolarité/vas/Stage en entreprise agro-industrielle/stock_sisley.xlsx"
st.set_page_config(page_title="Suivi du stock", page_icon="📦")
st.title("📦 Suivi et actualisation du stock")

stock = pd.read_excel(EXCEL_PATH)

st.subheader("Actualisation du stock")

col1, col2 = st.columns(2)
with col1:

    liste_boites = stock["type de boîte"].dropna().unique().tolist()
    typedeboite = st.selectbox("Type de boîte :", options=["(Aucune sélection)"] + liste_boites)

with col2:
    quantite = st.number_input(
        "Nouveau stock (quantité à ajouter ou soustraire) :",
        value=0,
        step=1,
        help="Mettre un nombre positif pour ajouter, ou négatif pour retirer"
    )

st.subheader("Attribution des priorités")
saisie_personne = st.text_input("Nombre de personne(s) disponible(s) :", placeholder="Laisser vide si simple mise à jour")


if st.button("Valider"):

    if quantite != 0 and typedeboite != "(Aucune sélection)":
        if typedeboite in stock['type de boîte'].values:
            i = stock[stock['type de boîte'] == typedeboite].index[0]
            actuel = int(stock.at[i, 'stock actuel '])
            voulu = int(stock.at[i, 'stock voulu'])

            nouveau_stock = actuel + quantite
            nouveau_manquant = voulu - nouveau_stock

            stock.at[i, 'stock actuel '] = nouveau_stock
            stock.at[i, 'stock manquant'] = nouveau_manquant
            stock.to_excel(EXCEL_PATH, index=False)
            st.success(f"Modifications enregistrées : stock de « {typedeboite} » mis à jour.")
        else:
            st.error("Type de boîte non reconnu dans le fichier Excel.")


    saisie_propre = saisie_personne.strip()

    if saisie_propre == "":
        st.info("Stock mis à jour avec succès.")
    else:
        try:
            personne = int(saisie_propre)
            if personne <= 0:
                st.warning("Veuillez saisir un nombre de personnes supérieur à 0.")
            else:
                stock = pd.read_excel(EXCEL_PATH)


                min_stock = stock['stock manquant'].nlargest(personne).index
                valeur_boite = stock.loc[min_stock, 'type de boîte'].tolist()

                attributions = []
                for numero_personne, boite in enumerate(valeur_boite, 1):
                    texte_boite = str(boite).strip()

                    if texte_boite == 'maquillage':
                        objectif = "360 boîtes soit environ 2 palettes"
                    elif texte_boite in ('petite éco', 'petite eco'):
                        objectif = "396 boîtes soit environ 2 palettes"
                    elif texte_boite in ('grande éco', 'grande eco'):
                        objectif = "n boîtes soit environ n palettes"
                    elif texte_boite in ('petite GIF', 'petite gif'):
                        objectif = "n boîtes soit environ n palettes"
                    elif texte_boite in ('grande GIF', 'grande gif'):
                        objectif = "n boîtes soit environ n palettes"
                    elif texte_boite in ('grande boîte grise', 'grande boite grise'):
                        objectif = "n boîtes soit environ n palettes"
                    else:
                        objectif = "Objectif non défini"

                    attributions.append(f"- Personne {numero_personne} : les boîtes **{boite}** *(objectif : {objectif})*")

                details = "\n".join(attributions)
                st.markdown(f"### Avec {personne} disponible(s), il faut prioriser :\n{details}")

        except ValueError:
            st.error("Veuillez entrer un nombre entier valide pour le nombre de personnes.")


st.divider()
st.subheader("📋 Tableau récapitulatif du stock")
st.dataframe(stock, use_container_width=True)