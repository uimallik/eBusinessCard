from flask import Flask, request, render_template,json

app = Flask(__name__)

import MySQLdb

def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db = "eBusinessCard")
    c = conn.cursor()

    return c, conn


@app.route("/dashboard/<id>", methods=['GET'])
def display_deals(id):

    c, conn = connection()

    #query = "SELECT device,timevisited,ipaddress,datevisited from visitor_records where cid=%s",id

    #query_string = "SELECT device,timevisited,ipaddress,datevisited FROM visitor_records WHERE cid = '{id}'".format(username=username)
    c.execute("SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}'".format(id))
    #c.execute(query)

    data = c.fetchall()
    c.execute('''SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}' ORDER BY visitor_records.created_at DESC LIMIT 1;'''.format(id))
    latestdata =c.fetchall()
    ls = str(latestdata)
    ls_alpha = str(ls).replace('(','').replace(')','')
    ls_alpha = str(ls_alpha).replace('/','').replace(')','')
    lst = ls_alpha.split()
    ls_a = str(ls_alpha).replace(',','').replace('"','')
    lss = ls_a.split()

    c.execute("SELECT Count(*) AS NumberOfOrders FROM visitor_records where cid = '{0}'".format(id))
    countdata = c.fetchall()
    ls_atr = str(countdata).replace('(','').replace(')',''.replace('L','').replace(',',''))
    ls_aaatr = str(ls_atr).replace('L','').replace(',','')

    conn.close()
    totalviews = ls_aaatr
    device = lss[0]
    #str(lss[0]).replace(''','').replace(',','')
    latestip = lss[2]
    datetime = lss[1]+" "+lss[3]

    tm = str(lss[1])
    tms = (tm[1:6])

    dt = str(lss[3])
    dts = (dt[6:11])

    datetime = dts+" "+tms

    return render_template("index.html", data=data,totalviews=totalviews,device=device,latestip=latestip,datetime=datetime)

@app.route('/loginhome')
def index():
   return render_template('login.html')


@app.route("/login", methods=['POST'])
def sample():
    phone = str(request.form['phone'])
    email = str(request.form['email'])
    c, conn = connection()

    c.execute("SELECT cid FROM registration where phone = '{0}'".format(phone))
    details = c.fetchone()
    print details
    idstdsed = str(details).replace('(','').replace(',','').replace(')','')
    id = idstdsed[1:37]
    print(id)

    c.execute("SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}'".format(id))
    #c.execute(query)

    data = c.fetchall()
    c.execute('''SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}' ORDER BY visitor_records.created_at DESC LIMIT 1;'''.format(id))
    latestdata =c.fetchall()
    ls = str(latestdata)
    ls_alpha = str(ls).replace('(','').replace(')','')
    ls_alpha = str(ls_alpha).replace('/','').replace(')','')
    lst = ls_alpha.split()
    ls_a = str(ls_alpha).replace(',','').replace('"','')
    lss = ls_a.split()

    c.execute("SELECT Count(*) AS NumberOfOrders FROM visitor_records where cid = '{0}'".format(id))
    countdata = c.fetchall()
    ls_atr = str(countdata).replace('(','').replace(')',''.replace('L','').replace(',',''))
    ls_aaatr = str(ls_atr).replace('L','').replace(',','')

    conn.close()
    totalviews = ls_aaatr
    device = lss[0]
    #str(lss[0]).replace(''','').replace(',','')
    latestip = lss[2]
    datetime = lss[1]+" "+lss[3]

    tm = str(lss[1])
    tms = (tm[1:6])

    dt = str(lss[3])
    dts = (dt[6:11])

    datetime = dts+" "+tms

    return render_template("index.html", data=data,totalviews=totalviews,device=device,latestip=latestip,datetime=datetime)








if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5200,debug=True)
