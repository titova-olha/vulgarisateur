import streamlit as st
from openai import OpenAI

# --- Настройка интерфейса ---
st.title("🧬 Le Vulgarisateur Scientifique")
st.write("Transformez un texte académique complexe en une explication simple pour un enfant de 10-12 ans.")

# Подключение клиента OpenAI (убедись, что ключ есть в настройках Streamlit Cloud)
client = OpenAI(api_key=st.secrets["api_key"])

# --- Инициализация памяти (Session State) ---
# Если в памяти еще нет сохраненного текста, создаем для него пустое место
if "texte_simplifie" not in st.session_state:
    st.session_state.texte_simplifie = None

# --- Шаг 1: Ввод текста ---
texte_original = st.text_area("Collez votre abstract scientifique ici :", height=200)

# Кнопка для генерации только текста
if st.button("📝 Simplifier le texte"):
    if texte_original:
        with st.spinner("Analyse et simplification en cours..."):
            try:
                # Генерация текста
                reponse_texte = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Tu es un expert en vulgarisation scientifique. Prends le texte fourni et réécris-le pour un enfant de 10-12 ans en français, en utilisant une métaphore filée."},
                        {"role": "user", "content": texte_original}
                    ]
                )
                # Сохраняем результат в ПАМЯТЬ Streamlit
                st.session_state.texte_simplifie = reponse_texte.choices[0].message.content
            except Exception as e:
                st.error(f"Erreur lors de la génération du texte : {e}")
    else:
        st.warning("Veuillez entrer un texte d'abord.")

# --- Шаг 2: Отображение текста и кнопка для картинки ---
# Если в памяти есть текст, показываем его и предлагаем сгенерировать картинку
if st.session_state.texte_simplifie:
    st.markdown("### Explication simple :")
    st.write(st.session_state.texte_simplifie)
    
    st.divider() # Горизонтальная линия для красоты
    st.write("Voulez-vous ajouter une métaphore visuelle ?")
    
    # Вторая кнопка - только по желанию!
    if st.button("🎨 Générer une illustration (DALL-E 3)"):
        with st.spinner("Création de l'image en cours... Cela peut prendre quelques secondes."):
            try:
                # Генерация промпта для картинки на основе простого текста
                prompt_image = f"Illustration de style livre pour enfants, colorée et métaphorique, basée sur ce concept : {st.session_state.texte_simplifie[:500]}"
                
                # Использование НОВОГО синтаксиса OpenAI для картинок
                reponse_image = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt_image,
                    n=1,
                    size="1024x1024"
                )
                
                image_url = reponse_image.data[0].url
                
                st.markdown("### Illustration :")
                st.image(image_url)
                
            except Exception as e:
                st.error(f"⚠️ Erreur lors de la création de l'image : {e}")