from typing import Any, Dict, List, Optional, Union
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from fastapi import Depends, FastAPI
from langserve import add_routes
from app.connection import get_database_connection
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentType, create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from pinecone import Pinecone, ServerlessSpec
import os

app = FastAPI()
conn = get_database_connection()
db = SQLDatabase(conn)
#### Pinecone Vector DB ####
pc_api_key = 'eda2322b-adfc-4196-885b-9b8bbae38717'
pc = Pinecone(api_key=pc_api_key)
# cloud = 'aws'
# region = 'us-east-1'
# spec = ServerlessSpec(cloud=cloud, region=region)
index_name = 'medical-mind'
index = pc.Index(index_name)
embeddings = OpenAIEmbeddings()
def get_context(query: str):
    res=index.query(vector=embeddings.embed_query(query),top_k=3,include_metadata=True)
    docs = {x["metadata"]['text']: i for i, x in enumerate(res["matches"])}
    return docs

from langchain.agents.agent_toolkits import create_retriever_tool

tool_description = """
Use it to give second opinion and diagnosis.
Input to this tool should be the current condition/diagnosis.
"""
retriever_tool = create_retriever_tool(
    get_context, name="biomedical_similar_examples", description=tool_description
)
custom_tool_list = [retriever_tool]

model = ChatOpenAI(
    model = 'gpt-3.5-turbo',
    temperature=0
)
custom_prefix = """
Always first get biomedical_similar_examples. 
If the user doesn't state current condition ask for the current diagnosis to get a relevant biomedical_similar_examples based on the diagnosis. Otherwise don't give any diagnosis. /
In case of any query other than health just say I'm not designed for that.

To get User info always keep into consideration:
Tables are linked by identifiers which usually have the suffix ‘ID’. For example, SUBJECT_ID refers to a unique patient, HADM_ID refers to a unique admission to the hospital, and ICUSTAY_ID refers to a unique admission to an intensive care unit.

Charted events such as notes, laboratory tests, and fluid balance are stored in a series of ‘events’ tables. For example the OUTPUTEVENTS table contains all measurements related to output for a given patient, while the LABEVENTS table contains laboratory test results for a patient.

Tables prefixed with ‘D_’ are dictionary tables and provide definitions for identifiers. For example, every row of CHARTEVENTS is associated with a single ITEMID which represents the concept measured, but it does not contain the actual name of the measurement. By joining CHARTEVENTS and D_ITEMS on ITEMID, it is possible to identify the concept represented by a given ITEMID.

Broadly speaking, five tables are used to define and track patient stays: ADMISSIONS; PATIENTS; ICUSTAYS; SERVICES; and TRANSFERS. Another five tables are dictionaries for cross-referencing codes against their respective definitions: D_CPT; D_ICD_DIAGNOSES; D_ICD_PROCEDURES; D_ITEMS; and D_LABITEMS. The remaining tables contain data associated with patient care, such as physiological measurements, caregiver observations, and billing information.

In some cases it would be possible to merge tables—for example, the D_ICD_PROCEDURES and CPTEVENTS tables both contain detail relating to procedures and could be combined—but our approach is to keep the tables independent for clarity, since the data sources are significantly different. Rather than combining the tables within MIMIC data model, we suggest researchers develop database views and transforms as appropriate.

Make sure to use tables prefixed with ‘D_’ as much as possible.

Always be specific. Only mention the deatil asked along with the second opinion or diagnosis.
"""
prompt = PromptTemplate.from_template(
    """
    Assist by providing the relevant information about patient with respect to their id.
    Patient_id: {patient_id}
    Question: {question}
    """
)

toolkit = SQLDatabaseToolkit(db=db, llm=model)

agent = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    extra_tools=custom_tool_list,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    prefix=custom_prefix,
)

chain = prompt | agent.run | StrOutputParser()

add_routes(
    app,
    chain,
    path="/medmind",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)