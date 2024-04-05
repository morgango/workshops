from datasets import Dataset 
import os
from ragas import evaluate
from datetime import datetime

from ragas.metrics import (
    answer_correctness,
    answer_relevancy,
    answer_similarity,
    faithfulness,
    context_recall,
    context_precision,
    context_relevancy,
    context_entity_recall,
    )

import decouple
from decouple import config
import pandas as pd
from common import create_es_client, df_to_es

# import configuration settings
elastic_cloud_id = config("ELASTIC_CLOUD_ID")
elastic_api_key = config("ELASTIC_API_KEY")

openai_api_key = config('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

# Create an Elasticsearch client
client = create_es_client(elastic_cloud_id, elastic_api_key)


from langchain.document_loaders import DirectoryLoader
loader = DirectoryLoader("/Users/morgan/dev/workshops/prompting/generate_site/site/")
documents = loader.load()

for document in documents:
    document.metadata['filename'] = document.metadata['source']
    
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


# generator with openai models
generator_llm = ChatOpenAI(model="gpt-3.5-turbo", base_url="http://localhost:1234/v1")
critic_llm = ChatOpenAI(model="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings()

generator = TestsetGenerator.from_langchain(
    generator_llm,
    critic_llm,
    embeddings
)

# generate testset
testset = generator.generate_with_langchain_docs(documents, 
                                                 test_size=10, 
                                                 distributions={simple: 0.5, 
                                                                reasoning: 0.25, 
                                                                multi_context: 0.25}
)

df = testset.to_pandas()
# store a local copy of the data
df.to_csv('questions.csv')


# data_samples = {
#     'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
#     'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
#     'contexts' : [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'], 
#     ['The Green Bay Packers play in Green Bay, Wisconsin.','The Packers compete in the National Football Conference']],
#     'ground_truth': ['The first superbowl was held on January 15, 1967', 'The New England Patriots have won the Super Bowl a record six times']
# }

# dataset = Dataset.from_dict(data_samples)

# score = evaluate(dataset,metrics=[
#     answer_correctness, 
#     answer_relevancy, 
#     answer_similarity, 
#     faithfulness, 
#     context_recall, 
#     context_precision, 
#     context_relevancy, 
#     context_entity_recall
#     ]
# )
# # create a dataframe
# df = score.to_pandas()

# # make the dataframe more human readable
# df['run_date'] = datetime.now()
# df['uid'] = df['run_date'].apply(lambda x: x.strftime('%Y%m%d%H%M%S%f'))

# visual_fields = ['uid', 'run_date', 'question', 'answer', 'contexts', 'ground_truth']
# df = df[visual_fields + [col for col in df.columns if col not in visual_fields]]

# # store a local copy of the data
# df.to_csv('data.csv')

# # load the data to Elasticsearch
# df_to_es(df, 
#          client, 
#          "ragas_metrics",
#          if_exists="replace",)




