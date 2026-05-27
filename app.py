import streamlit as st
from openai import OpenAI

# --- Настройка интерфейса ---
st.title("🧬 Le Vulgarisateur Scientifique")
st.write("Transformez un texte académique complexe en une explication simple pour un enfant de 10-12 ans.")

# Подключение клиента OpenAI для текста (использует твой ключ OPENAI_API_KEY из Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Инициализация памяти (Session State) ---
if "texte_simplifie" not in st.session_state:
    st.session_state.texte_simplifie = None

# --- Шаг 1: Ввод текста ---
texte_original = st.text_area("Collez votre abstract scientifique ici :", height=200)

# Кнопка для генерации текста
if st.button("📝 Simplifier le texte"):
    if texte_original:
        with st.spinner("Analyse et simplification en cours..."):
            try:
                # Генерация текста (gpt-4o-mini работает идеально и он точно активен)
                reponse_texte = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Tu es un expert en vulgarisation scientifique. Prends le texte fourni et réécris-le pour un enfant de 10-12 ans en français, en utilisant une métaphore filée."},
                        {"role": "user", "content": texte_original}
                    ]
                )
                st.session_state.texte_simplifie = reponse_texte.choices[0].message.content
            except Exception as e:
                st.error(f"Erreur lors de la génération du texte : {e}")
    else:
        st.warning("Veuillez entrer un texte d'abord.")

# --- Шаг 2: Отображение текста и кнопка для бесплатной картинки ---
if st.session_state.texte_simplifie:
    st.markdown("### Explication simple :")
    st.write(st.session_state.texte_simplifie)
    
    st.divider() # Красивая линия-разделитель
    st.write("Voulez-vous ajouter une métaphore visuelle ?")
    
    # Кнопка для генерации бесплатной картинки (работает без ключей OpenAI)
    if st.button("🎨 Générer une illustration"):
        with st.spinner("Création de l'image en cours..."):
            try:
                # Составляем промпт для детской книжной иллюстрации на основе упрощенного текста
                prompt_image = f"Children book style illustration, colorful, metaphorical, simple shapes, clear background, related to: {st.session_state.texte_simplifie[:300]}"
                
                # Подготавливаем текст для ссылки (заменяем пробелы на безопасный код %20)
                prompt_safe = prompt_image.replace(" ", "%20").replace("\n", "%20")
                
                # Обращаемся к независимому бесплатному генератору изображений
                image_url = f"https://image.pollinations.ai/prompt/{prompt_safe}?width=1024&height=1024&nologo=true"
                
                st.markdown("### Illustration :")
                st.image(image_url)
                
            except Exception as e:
                st.error(f"⚠️ Erreur lors de la création de l'image : {e}")