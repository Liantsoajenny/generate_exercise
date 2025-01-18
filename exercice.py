import streamlit as st
import PyPDF2
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
import random
from io import BytesIO

def app():
    st.title("Génération des questions à partir de contenu")

    # Choix pour entrer le contenu : fichier PDF ou texte
    choix_entrée = st.selectbox("Choisissez la source du contenu", 
                                ["Télécharger un fichier PDF", "Saisir du texte manuellement"], 
                                key="choix_entrée")  # Ajout du key unique

    contenu = ""
    if choix_entrée == "Télécharger un fichier PDF":
        uploaded_file = st.file_uploader("Téléchargez un fichier PDF", type=["pdf"], key="file_uploader")  # key unique
        if uploaded_file is not None:
            contenu = extract_text_from_pdf(uploaded_file)
    
    elif choix_entrée == "Saisir du texte manuellement":
        contenu = st.text_area("Saisissez le texte manuellement", height=300, key="text_area")  # key unique

    # Affichage du contenu extrait ou saisi
    if contenu:
        st.subheader("Contenu extrait ou saisi :")
        st.text_area("Contenu du fichier ou du texte", contenu, height=300, key="content_display")  # key unique

        # Générer des questions à partir du texte
        num_questions = st.slider("Nombre de questions à générer", 1, 10, 5)  # Choisir le nombre de questions
        if st.button("Générer des questions", key="generate_qcm_button"):  # key unique
            with st.spinner("Génération des questions..."):
                questions = generate_questions_from_text(contenu, num_questions)
                
                if questions:
                    for idx, q in enumerate(questions):
                        st.write(f"**Question {idx + 1}:** {q['question']}")

# Fonction pour lire le texte à partir d'un fichier PDF
def extract_text_from_pdf(pdf_file):
    # Lire le contenu du fichier PDF en mémoire (pas besoin de l'enregistrer sur le disque)
    reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Fonction pour générer des questions à partir du texte
def generate_questions_from_text(text, num_questions):
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Division du texte en passages
    passages = text.split(". ")
    documents = [passage for passage in passages if len(passage.strip()) > 30]  # Filtrer les passages trop courts

    # Vérification si les documents sont suffisants
    if not documents:
        st.write("Texte trop court pour générer des questions. Veuillez fournir un texte plus long.")
        return []

    # Création de l'index FAISS
    faiss_index = FAISS.from_texts(documents, embedding)

    # Configuration de RetrievalQA avec le modèle de chat
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)  # Remplace par ta clé OpenAI si nécessaire
    retriever = faiss_index.as_retriever()
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Générer des questions

    prompt_template = """
    Based on the following text, create a clear question in the same language as the text:
    Input text:
    {text}
    """

    questions = []
    for i in range(num_questions):
        try:
            random_passage = random.choice(documents)
            response = rag_chain.run(prompt_template.format(text=random_passage))

            # Ajouter la question générée à la liste
            questions.append({
                "question": response.strip()
            })
        except Exception as e:
            st.write(f"Erreur lors de la génération de la question : {str(e)}")
    
    return questions

# Lancer l'application Streamlit
if __name__ == "__main__":
    app()
