# Setting up
## Table of Contents
- [Setting up](#setting-up)
  - [1. Get Patient Database](#1-get-patient-database)
  - [2. Configure Vector Database](#2-configure-vector-database)
- [Starting the Server](#starting-the-server)
  - [Backend Server](#backend-server)
  - [Frontend Interface](#frontend-interface)

---

## Setting up

### 1. Get Patient Database
To set up the patient database, download the MIMIC-III demo dataset:
- Visit [PhysioNet's MIMIC-III Demo page](https://physionet.org/content/mimiciii-demo/1.4/).
- Follow their instructions to obtain access and download the dataset.
  
Once downloaded, ensure that the data is available in the environment where you'll run Medical Mind.

### 2. Configure Vector Database (RAG Setup)
This project uses a vector database to enhance retrieval capabilities.
- Follow the **Pinecone setup** instructions in `langserve_medicalmind/Medical_Mind_For_Patients.ipynb`.
- This notebook contains all steps required to configure the vector database, which is essential for the RAG functionality.

---

## Starting the Server

### Backend Server
To start the backend server, use the following command:
```bash
python langserve_medicalmind/medmind_langserve/app/server.py
```
### Frontend Server
For interacting with the server, use the Streamlit-based frontend:
```bash
streamlit run langserve_medicalmind/medmind_langserve/app/stream_lit.py
```

# MedicalMind
Using LLMs in the healthcare 

![Screenshot 2024-02-05 153308](https://github.com/talha-0/MedicalMind/assets/92780334/84302ab8-6dfd-4a62-8e7d-bfbfdf0f3fdc)


![image](https://github.com/talha-0/MedicalMind/assets/92780334/b5670f8b-495b-49ae-8b52-18652077381e)
