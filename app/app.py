#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from fastapi import FastAPI
from langchain.chains import LLMChain
from langchain.memory import RedisChatMessageHistory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate,
)


prompt = '''
Вы консультант в банке Тинькофф. Вы консультируете клиентов,
помогаете им решать проблемы и находить информацию.
Если вы не знаете правильный ответ или смысл вопроса не понятен, 
вы сообщаете об этом и просите уточнить вопрос.
Если клиент спрашивает о стоимости какой-либо услуги, вы внимательно 
просматриваете таблицу тарифов и выделяете оттуда релевантную информацию.
Отвечайте, используя три предложения.
Отвечайте на русском языке.
Помогите клиенту решить его вопрос, пользуясь следующим контекстом:

{context}
'''

prompt_template = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(prompt),
        MessagesPlaceholder(variable_name='chat_history'),
        HumanMessagePromptTemplate.from_template('{question}')
    ],
)


import app.docs as my_docs
db = my_docs.load_documentation_db()
#db = my_docs.create_documentation_db()
import app.llm as my_llm
llm = my_llm.load_llm()


app = FastAPI()

@app.post('/message')
def message(user_id: str, message: str):
    history = RedisChatMessageHistory(user_id)
    conversation = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True,
    )
    context = my_docs.query_docs(db, message)
    ai_message = conversation.predict(
        question=message, 
        chat_history=history.messages, 
        context=context,
    )
    history.add_user_message(message)
    history.add_ai_message(ai_message)
    print('user message:', message)
    print('ai message:', ai_message)
    return {'message': ai_message,}