import os
from flask import Flask, render_template, request, send_file
from azure.identity import DefaultAzureCredential
from azure.ai.generative import AIGenerativeClient
from azure.ai.generative.models import ImageGenerationOptions
import io
from PIL import Image
import requests

app = Flask(__name__)

# Initialize Azure client
def get_azure_client():
    endpoint = "https://project20aug2025.openai.azure.com/"
    key = "CXHLwVOtogrGhr5jv2hztjoLY1f0Tlytl0Auidf27tgSYtOU9UCPJQQJ99BHACYeBjFXJ3w3AAAAACOGA2cm"
    
    if not endpoint or not key:
        raise ValueError("Azure Gen AI endpoint and key must be configured")
    
    credential = DefaultAzureCredential()
    return AIGenerativeClient(
        endpoint=endpoint,
        credential=credential,
        api_key=key
    )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        size = request.form.get("size", "1024x1024")
        
        try:
            client = get_azure_client()
            response = client.images.generate(
                deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME", "dall-e-3"),
                prompt=prompt,
                size=size,
                n=1,
                quality="standard"
            )
            
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            img = Image.open(io.BytesIO(img_data))
            
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            return send_file(img_io, mimetype='image/png')
            
        except Exception as e:
            app.logger.error(f"Error generating image: {str(e)}")
            return render_template("index.html", error=str(e))
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
