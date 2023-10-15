from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.directory import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

db_path='./data/chroma'
tariffs_f = open('./docs/cards.csv', encoding='utf_8')
tariffs = tariffs_f.read()


def embedder():
    from langchain.embeddings import HuggingFaceEmbeddings
    model_name = 'Den4ikAI/rubert-tiny2-retriever'
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    cache_folder = './data/embeddings'
    embedder = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        cache_folder=cache_folder,
    )
    return embedder

def load_documentation_db() -> Chroma:
    db = Chroma(embedding_function=embedder(), persist_directory=db_path)
    return db

def create_documentation_db() -> Chroma:
    pdf = DirectoryLoader('./docs', '*.pdf', loader_cls=PyPDFLoader)
    splitter = RecursiveCharacterTextSplitter(
        separators = ['\n\n\n', '\n\n', '\n'],
        is_separator_regex = False,
        chunk_size = 1000,
        chunk_overlap = 100,
        length_function = len,
    )
    docs = pdf.load_and_split(splitter)
    db = Chroma.from_documents(docs, embedder(), persist_directory=db_path)
    return db

def query_docs(db: Chroma, query: str) -> str:
    docs = db.similarity_search(query, 2)
    ret = 'csv-таблица тарифов:\n' + tariffs + '\n\n'
    for doc in docs:
        ret += '\n' + doc.page_content
    return ret