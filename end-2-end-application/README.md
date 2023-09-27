### Prerequisits:
1. Clone the code into Ubuntu Linux
2. Install python packages PyPDF2, textract: https://textract.readthedocs.io/en/stable/
3. Install langchain

### Step by step to build the solution:
1. Create emebdding model SageMaker endpoint. Go to SageMaker jumpstart to create an embedding model. In our testing, we used "jumpstart-dft-mx-tcembedding-robertafin-large-uncased" as the SageMaker endpoint.

2. Put your PDF file in data folder

3. Create RDS PostgreSQL, make sure the machine which is running your code is able to connect to the RDS PostgreSQL DB. Write down the connection information of DB. Update the information in create_embedding.py and query_embedding.py

4. Go to utilities folder, run "python3 main.py". This script will chunk the PDF file by page and extract the text from PDF file. Create embeddings based on the extracted text and save into PostgreSQL DB

5. Make sure you have Bedrock access, prepare your aws credential profile which is able to access Bedrock. Update the profile name in question_answering_bedrock.py

6. go to langchain folder, run streamlit run app.py bedrock

7. Then you can access the app and ask your question
