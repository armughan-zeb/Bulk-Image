import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import zipfile
import os

st.set_page_config(page_title="Bulk AI Image Generator", layout="wide")
st.title("🖼️ Bulk AI Image Generator")

prompt = st.text_area("Enter a prompt:", "A futuristic cyberpunk city with neon lights", height=100)
num_images = st.slider("Number of images", 1, 10, 5)

api_url = "https://stablediffusionapi.com/api/v3/text2img"

if st.button("Generate Images"):
    with st.spinner("Generating images..."):
        os.makedirs("outputs", exist_ok=True)
        for i in range(num_images):
            response = requests.post(api_url, json={
                "key": "Qm9xcyW9TMIF5BdxtqkEJJbtoMNyBfPZbjdRJmxO5PDExjwUtLSfR9EkLtqh",  # 👈 REPLACE THIS
                "prompt": prompt,
                "width": "512",
                "height": "512",
                "samples": "1",
                "num_inference_steps": "20",
                "guidance_scale": 7.5,
                "safety_checker": "yes",
                "enhance_prompt": "yes",
                "seed": None
            })

            data = response.json()
            img_url = data["output"][0]
            img_data = requests.get(img_url).content
            img = Image.open(BytesIO(img_data))
            img.save(f"outputs/image_{i+1}.png")
            st.image(img, caption=f"Image {i+1}", use_column_width=True)

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename in os.listdir("outputs"):
                zip_file.write(f"outputs/{filename}", arcname=filename)
        zip_buffer.seek(0)

        st.success("✅ All images generated!")
        st.download_button("Download All as ZIP", zip_buffer, file_name="bulk_images.zip", mime="application/zip")
