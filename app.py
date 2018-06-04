from flask import Flask, request, render_template,json
import MySQLdb
import config


app = Flask(__name__)



def connection():
    # Edited out actual values

    conn = MySQLdb.connect(host=config.CONFIG['host'],
                           user= config.CONFIG['user'],
                           passwd=config.CONFIG['passwd'],
                           db = config.CONFIG['db'])
    c = conn.cursor()

    return c, conn


@app.route('/loginhome')
def index():
   return render_template('login.html')


@app.route("/login", methods=['POST'])
def sample():
    phone = str(request.form['phone'])  # Parameter which is used for getting customer id
    email = str(request.form['email'])  # Parameter


    try:
        c, conn = connection() # MySQL DB Connection OPEN
        c.execute("SELECT cid FROM registration where phone = '{0}'".format(phone))
        get_id = c.fetchone() # Getting ID from database using the phone number
        id = str(get_id).replace('(','').replace(',','').replace(')','')[1:37]

        c.execute("SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}'".format(id))
        data = c.fetchall() # Getting all defined details using the cid which is customer ID

        if data == ():
           data = (('', '', '', ''),)
           device = "----"
           latestip = "----"
           datetime = "----"
           totalviews = "0"


        else:
            c.execute('''SELECT device,timevisited,ipaddress,datevisited FROM visitor_records where cid = '{0}' ORDER BY visitor_records.created_at DESC LIMIT 1;'''.format(id))
            latestdata =str(c.fetchall()) # Getting the latest inserted details
            filter_latestdata = str(latestdata).replace('(','').replace(')','').replace('/','').replace(')','').replace(',','').replace('"','')
            filter_latestdatalist = filter_latestdata.split()
            c.execute("SELECT Count(*) AS NumberOfOrders FROM visitor_records where cid = '{0}'".format(id))
            countdata = c.fetchall()
            c.close()

            totalviews = str(countdata).replace('(','').replace(')',''.replace('L','').replace(',','')).replace('L','').replace(',','')
            device_type = filter_latestdatalist[0]
            device = device_type[1:len(device_type)-1]

            latestip_type = filter_latestdatalist[2]
            latestip = latestip_type[1:len(latestip_type)-1]

            time_string = str(filter_latestdatalist[1])
            time = (time_string[1:6])

            data_string = str(filter_latestdatalist[3])
            date = (data_string[6:11])

            datetime = date+" "+time

    except Exception, e:
        print 'Error ', e

    finally:
        c.close()


    return render_template("index.html", data=data,totalviews=totalviews,device=device,latestip=latestip,datetime=datetime)








if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5200,debug=True)
