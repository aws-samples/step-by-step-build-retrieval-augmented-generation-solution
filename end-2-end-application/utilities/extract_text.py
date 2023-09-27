from PyPDF2 import PdfWriter, PdfReader
import textract


def chunk(inputpdf, dst_path):
	for i in range(len(inputpdf.pages)):
	    page = i + 1
	    output = PdfWriter()
	    output.add_page(inputpdf.pages[i])
	    with open(dst_path + "document-page%s.pdf" % page, "wb") as outputStream:
	        output.write(outputStream)

def extract(src_pathlist, dst_path):
	for path in src_pathlist:
	     path_in_str = str(path)  
	     byte_text = textract.process(path_in_str)
	     text = byte_text.decode('utf-8')
	     text_path = dst_path + path_in_str.split('/')[3] + ".txt"
	     with open(text_path, 'w') as f:
	        f.write(text)

