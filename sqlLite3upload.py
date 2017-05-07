#!flask/bin/python
from flask import Flask, jsonify, Response,request, abort, render_template
from sqlalchemy import create_engine
import datetime, os, sqlite3
import pdfParser

app = Flask(__name__)


def insert_doc(contentDF):
    #conn = sqlite3.connect('example.db')
    conn = create_engine('sqlite:///example.db')
    contentDF.to_sql(name='parsedPdfs', con=conn, if_exists='append', index=False)
    # cur = conn.cursor()
    # cur.execute("INSERT INTO parsedPdfs values"+args+"")
    # conn.commit()
    # conn.close()
    return 1

def check_exists(fileName):
    query = "select distinct(FileName) from parsedPdfs where FileName=" + "'" + fileName + "'"
    conn = sqlite3.connect('example.db')
    cur = conn.cursor()
    cur.execute(query)
    retfile = cur.fetchone()
    if retfile is not None:
        return -1
    else:
        return 1
    conn.close()


@app.route('/pdfParser/v1.0/upload')
def upload_file():
    return render_template("upload.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']

        flag = check_exists(f.filename)
        if flag == 1:
            fileName = './documents/'+f.filename
            contentDF = pdfParser.parsePDF(fileName)
            flg = insert_doc(contentDF)
            if flg == 1:
                return Response(f.filename+' parsed and saved in database')
            else:
                return Response('Something has gone wrong')

        elif flag == -1:
            return Response(f.filename+' Exists in database')


if __name__ == "__main__":
    app.run(debug=True)
