import json

import re

def get_nhs_number(text):
  result = re.search(r"NHS (?:ID|Number): ?(\d{4}[ -]?\d{3}[ -]?\d{3})[^0-9]", text, re.IGNORECASE)
  
  if result != None:
    return result.groups()[0]
  else:
    return None

def get_all_dates(text):
  result = re.findall(r"([0-9]{4}-[0-9]{1,2}-[0-9]{1,2}|[0-9]{1,2}/[0-9]{1,2}/[0-9]{4})", text, re.IGNORECASE)
  return result

def get_diagnoses(text):
  result = re.search(r"Diagnoses:(.+)Medications:", text, re.IGNORECASE + re.DOTALL)
  
  if result != None:
    return result.groups()[0].strip().split("\n")
  else:
    return None

def get_medications(text):
  result = re.search(r"Medications:([a-zA-Z \-\n]+)(?:,|\.)", text, re.IGNORECASE + re.DOTALL)
  
  if result != None:
    return result.groups()[0].strip().split("\n")[0:-1]
  else:
    return None

def get_patient_name(text):
  result = re.search(r"Dear ([a-zA-Z ]+),", text, re.IGNORECASE)
  
  if result != None:
    return result.groups()[0]
  else:
    return None

def get_body(text, medications):
  last_medication = medications[-1]
  pattern = last_medication + r"(.+)"
  
  result = re.search(pattern, text, re.IGNORECASE + re.DOTALL)
  
  if result != None:
    return result.groups()[0].strip()
  else:
    return None


def main(text):
  nhs_number = get_nhs_number(text)
  dates = get_all_dates(text)
  patient_name = get_patient_name(text)
  diagnosis = get_diagnoses(text)
  medications = get_medications(text)
  
  body = get_body(text, medications)
  
  return json.dumps({
    "nhs number": nhs_number,
    "dates": dates,
    "patient name": patient_name,
    "diagnosis": diagnosis,
    "medications": medications,
    "body": body,
    # "address": ""
  })
