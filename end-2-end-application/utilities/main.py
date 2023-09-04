#!/usr/bin/python
from extract_text import chunk, extract
from PyPDF2 import PdfWriter, PdfReader
from pathlib import Path
from create_embedding import create_embedding_output
from insert_embedding import insert_embedding_json

#chunk original pdf
inputpdf = PdfReader(open("../data/Selected_Document_1.pdf", "rb"))
chunked_dst_path = "../data/chunkedpages/"
chunk(inputpdf, chunked_dst_path)

#extract pdf pages to text format
src_pathlist = Path("../data/chunkedpages").glob('**/*.pdf')
extracted_dst_path = "../data/extractedpages/"
extract(src_pathlist, extracted_dst_path)

#create embedding based on the extracted pages
pdf_json_file_name = 'output.json'
output_file_name = 'embedding.json'
create_embedding_output(pdf_json_file_name, output_file_name)

#insert embedding into your vector DB
insert_embedding_json(output_file_name)
