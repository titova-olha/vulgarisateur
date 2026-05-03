import streamlit as st
from openai import OpenAI
import json

# Настройка внешнего вида страницы
st.set_page_config(page_title="Le Vulgarisateur", page_icon="🧬")

st.title("🧬 Le Vulgarisateur Scientifique")
st.write("Transformez des articles complexes en explications simples avec des illustrations !")

# Подключение к OpenAI (ключ будет браться из секретных настроек Streamlit)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("La clé API est manquante. Veuillez la configurer.")
    st.stop()

# Поле для ввода текста
abstract = st.text_area("Collez l'abstract de l'article scientifique ici :", height=200)

# Кнопка запуска
if st.button("Simplifier & Illustrer ✨"):
    if not abstract:
        st.warning("Veuillez entrer un texte avant de cliquer.")
    else:
        with st.spinner("Analyse et simplification en cours..."):
            try:
                # Шаг 1: Просим GPT упростить текст и придумать промпт для картинки
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": "Tu es un expert en vulgarisation scientifique. Prends le texte fourni et fais deux choses : 1) Réécris-le pour un enfant de 10-12 ans en français simple et engageant. 2) Crée un prompt détaillé en anglais pour DALL-E 3 afin d'illustrer ce texte. Renvoie UNIQUEMENT un objet JSON avec les clés exactes : 'u_text' (pour le texte simplifié) et 'dalle_prompt' (pour le prompt de l'image)."},
                        {"role": "user", "content": abstract}
                    ]
                )
                
                result = json.loads(response.choices[0].message.content)
                simplified_text = result["u_text"]
                image_prompt = result["dalle_prompt"]

                st.subheader("Explication simple :")
                st.write(simplified_text)

                # Шаг 2: Просим DALL-E нарисовать картинку по промпту
                with st.spinner("Génération de l'illustration (cela peut prendre 10-15 secondes)..."):
                    image_response = client.images.generate(
                        model="dall-e-3",
                        prompt=image_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    image_url = image_response.data[0].url
                    
                    st.subheader("Illustration :")
                    st.image(image_url)

            except Exception as e:
                st.error(f"Une erreur s'est produite : {e}")
