#from dbconnect import connection
from flask import Flask, render_template

import MySQLdb

app = Flask(__name__)

def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db = "eBusinessCard")
    c = conn.cursor()

    return c, conn
@app.route('/dashboard/')
def display_deals():

    c, conn = connection()

    query = "SELECT device,timevisited,ipaddress,datevisited from visitor_records"
    c.execute(query)

    data = c.fetchall()

    conn.close()



    return render_template("indexto.html", data=data)

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5200,debug=True)

