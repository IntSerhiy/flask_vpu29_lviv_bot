from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

CLIENT = OpenAI(api_key="sk-proj-mmRKHjeDcfL9vQxDezi4T3BlbkFJKXL7oAEiuxFsU8ZC9xVs")
pc = Pinecone(api_key="30f3efb4-4c57-40c4-bdfc-c2b6a4f52635")
index = pc.Index('lvivcroissant')


def split(text: str):
    return text.split('\n')


def get_embedding(text: str):
    embedding = CLIENT.embeddings.create(input=text, model="text-embedding-3-small")
    return embedding.data[0].embedding

def save_embedding(embedding, text):
    index.upsert(
        vectors = [
            {
                #f'id': str(uuid.uuid4()),
                'values': embedding,
                'metadata': {'text': text}
            }
        ]
    )

def save_text(text: str):
    """Зберігання вектора та тексту."""
    chunks = split(text)
    for chunk in chunks:
        embedding = get_embedding(chunk)
        save_embedding(embedding=embedding, text=chunk)

def search(query: str, top_k):
    """Пошук векторів."""
    embedding = get_embedding(query)
    result = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )
    return list(map(lambda x: x.metadata['text'], result.matches))



# save_text('Степа́н Андрі́йович Банде́ра — український політичний діяч, революціонер, \n'
#           'один із радикальних та чільних ідеологів, практиків і теоретиків українського націоналістичного руху XX століття, \nпісля розколу Організації українських націоналістів — голова Проводу')
