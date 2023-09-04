#!/usr/bin/python

import psycopg2
import json
from pgvector.psycopg2 import register_vector

DB_HOST = "<YOUR DB HOST NAME>"
DB_NAME = "<YOUR DB NAME>"
USER = "<DB USERNAME>"
PASSWORD = "<DB PASSWORD>"

def insert_embedding_json(pdf_json_file_name):
    with open(pdf_json_file_name, 'r') as f:
        data = json.load(f)

    sql = """INSERT INTO docembedding (page_number, content, pdf_file_path, embedding) 
             VALUES (%s, %s, %s, %s);"""

    conn = None
    vendor_id = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host=DB_HOST, 
                                database=DB_NAME,
                                user=USER,
                                password=PASSWORD)
        # create a new cursor
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        register_vector(conn)
        # create table if not exist
        cur.execute("DROP TABLE IF EXISTS docembedding;")
        cur.execute("CREATE TABLE IF NOT EXISTS docembedding(id bigserial PRIMARY KEY, page_number text, content text, pdf_file_path text, embedding vector(1024));")
        # execute the INSERT statement
        for page_index, page in enumerate(data):
            record_to_insert = (data[page_index]["page_number"], data[page_index]["content"], data[page_index]["pdf_file_path"], data[page_index]["embedding"])
            cur.execute(sql, record_to_insert)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

