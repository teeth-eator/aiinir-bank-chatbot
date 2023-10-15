# aiinir-bank-chatbot

Build: `docker build -t llm_username:v1 .`  
Run: `docker run -p 8080:8080 llm_username:v1`

По умолчанию запускается с ChatGPT.  
Чтобы запустить с Llama, поместите файл модели в `/data/llm/`  
и укажите её название в `/app/llm.py`.

Модель можно взять [отсюда](https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF)
