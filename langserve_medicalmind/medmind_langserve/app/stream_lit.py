import streamlit as st
import json
import requests

st.title("MedicalMind - Personalized Medical Decision Support System")

def generate_response(patient_id,question):
  inputs = {
    "input": {
      'patient_id':patient_id,
      'question':question
    }
  }
  res = requests.post(url = 'http://127.0.0.1:8000/medmind/invoke',json = inputs)
  response_json = res.json()
  output_text = response_json['output']
  st.info(output_text)

with st.form('my_form'):
  patient_id = st.sidebar.text_input('Patient ID')
  question = st.text_area('Question:')
  submitted = st.form_submit_button('Submit')
  if not patient_id:
    st.warning('Please enter Patient ID!', icon='⚠')
  if submitted and patient_id:
    generate_response(patient_id,question)