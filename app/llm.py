def load_llm():
    if 1:
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(
            model_name='gpt-3.5-turbo' ,
            openai_api_key='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',
        )
    else:
        from langchain.llms import LlamaCpp
        llm = LlamaCpp(
            model_path='./data/llm/llama-2-7b-chat.Q4_K_M.gguf',
            temperature=0.2,
            n_ctx=4096,
            max_tokens=600,
            repeat_penalty=1.13,
        )
    return llm