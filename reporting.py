"""Separate STP results; database credentials must be configured as Streamlit secrets."""
import json
import uuid
import streamlit as st

def configured():
    try:
        return all(st.secrets['database'][k] for k in ('host','user','password'))
    except Exception:
        return False

def connect():
    import psycopg
    db=st.secrets['database']
    return psycopg.connect(host=db['host'],port=6543,user=db['user'],password=db['password'],dbname='postgres',sslmode='require',connect_timeout=10,prepare_threshold=None)

def submit(names, payload):
    names=names.strip()
    if not names or len(names)>160:
        raise ValueError('Enter pair names or an identifier (up to 160 characters).')
    submission_id=str(uuid.uuid4())
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO stp_pair_results (submission_id, pair_names, payload) VALUES (%s,%s,%s::jsonb)', (submission_id,names,json.dumps(payload)))
