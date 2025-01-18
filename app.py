import streamlit as st
from streamlit_option_menu import option_menu
import home
import question
import exercice  # Assurez-vous que ce module est bien importé
import resaka  # Assurez-vous que le module resaka est bien importé

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Gestion du menu latéral
        with st.sidebar:
            app = option_menu(
                menu_title='Pondering',
                options=['Générer des QCM', 'Générer des question', 'Demande'],
                icons=['house-fill', 'person-circle', 'trophy-fill', 'chat-fill', 'info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=0,  # Page d'accueil par défaut
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # En fonction de la sélection, appeler la fonction appropriée
        if app == "Home":
            home.app()  # Assurez-vous que home.app() existe dans le module home.py
        elif app == "Générer des QCM":
            question.app()  # Assurez-vous que question.app() existe dans le module question.py
        elif app == "Générer des question":
            exercice.app()  # Assurez-vous que exercice.app() existe dans le module exercice.py
        elif app == "Demande":
            resaka.app()  # Assurez-vous que resaka.app() existe dans le module resaka.py

# Lancer l'application
if __name__ == "__main__":
    app = MultiApp()
    app.run()
