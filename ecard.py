from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
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

# New Registrations
@app.route("/", methods=['POST'])
def sample():

    name = str(request.form['name'])
    address1 = str(request.form['address1'])
    address2 = str(request.form['address2'])
    phone = str(request.form['phone'])
    email = str(request.form['email'])




    test = "/home/default/Desktop/eBusinessCard/static"

    '''
    import shutil

    shutil.rmtree(test,ignore_errors=True)
    os.makedirs(test,0755)
    #print(filelist)
    '''
    ################## Choosing Template ################################################################################
    img = Image.open("input.png")
    print("Input taken")


    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/default/Downloads/Postman/resources/app/assets/fonts/OpenSans/AbhayaLibre-ExtraBold.ttf", 60)
    draw.text((550, 150),name,(26,176,74),font=font)

    #Address line 1
    font = ImageFont.truetype("/home/default/Downloads/Postman/resources/app/assets/fonts/OpenSans/OpenSans-Bold.ttf", 36)
    draw.text((550, 210),address1,(123,124,117),font=font)
    eachone = name+'.png'
    #img.save('imgoutput.png')
    img.save(eachone)


    #Address line 2
    font = ImageFont.truetype("/home/default/Downloads/Postman/resources/app/assets/fonts/OpenSans/OpenSans-Bold.ttf", 36)
    draw.text((550, 250),address2,(123,124,117),font=font)
    #img.save('imgoutput.png')
    img.save(eachone)
    #Phone
    font = ImageFont.truetype("/home/default/Downloads/Postman/resources/app/assets/fonts/OpenSans/OpenSans-Bold.ttf", 36)
    draw.text((550, 290),"P: "+phone,(123,124,117),font=font)
    #img.save('imgoutput.png')
    img.save(eachone)
    #Email
    font = ImageFont.truetype("/home/default/Downloads/Postman/resources/app/assets/fonts/OpenSans/OpenSans-Bold.ttf", 30)
    draw.text((550, 330),"Email: "+email,(123,124,117),font=font)
    #img.save('imgoutput.png') # added static
    img.save(eachone)
    print('output done')

    ################ End of Choosing Template ##########################################################################

    ################ Move file to static folder ########################################################################
    import shutil
    shutil.copy('/home/default/Desktop/eBusinessCard/'+eachone,'/home/default/Desktop/eBusinessCard/static/')
    ##############End Move file to static folder #######################################################################


    ############ QR Code generation ####################################################################################

    import pyqrcode
    url = pyqrcode.create('http://192.168.1.10:5000/file/'+eachone)
    url.svg('uca-url.svg', scale=8, background="white")  # Saving as SVG file
    url.eps('uca-url.eps', scale=2)

    ########### End of QR code generation ##############################################################################

    ########### Convert SVG to PNG #####################################################################################
    import cairosvg
    eachoneQR = 'QR'+name+'.png'
    cairosvg.svg2png(url='uca-url.svg', write_to=eachoneQR)
    ########### End Convert SVG to PNG #################################################################################

    ################ Move file to static folder ########################################################################
    import shutil
    shutil.copy('/home/default/Desktop/eBusinessCard/'+eachoneQR,'/home/default/Desktop/eBusinessCard/static/')
    ##############End Move file to static folder #######################################################################



    filename = 'static/'+eachoneQR
    filename2 = 'static/'+eachone
    #return render_template('download.html')
    # return render_template('idcard.html', value=filename, value2=filename2)
    return render_template('carddownload.html', value=filename, value2=filename2)



@app.route('/home')
def index():
   return render_template('index.html')


# Return Existing file
@app.route("/file/<id>", methods=['GET'])
def fil(id):
    print id
    filename = "/static/"+str(id)
    req_data = {}
    req_data['headers'] = dict(request.headers)
    # IP Address capturing
    ipaddress = request.remote_addr
    rs =  json.dumps(req_data['headers'])
    rt = json.loads(rs)
    # Device Capturing
    st = json.dumps(rt['User-Agent'])
    device = st.split()

    #ls_alpha = [i for i in device if not i.isdigit()]
    ls_alpha = str(device).replace('(','').replace(')','')
    ls_alpha = str(ls_alpha).replace('/','').replace(')','')
    final = ls_alpha.split()
    ls_alpha = str(final).replace('"','').replace(';','')

    final = ls_alpha.split()
    xt = final[1:3]
    l_out = [''.join(e for e in string if e.isalnum()) for string in xt]
    known_sysdevices = ['Linux','Windows']
    known_mobdevices = ['Andriod','iPhone',]
    set1 = set(l_out)
    set2 = set(l)
    set(l_out)&


    import datetime
    import time
    ts = time.time()
    sts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    r = sts.split()
    date = str(r[0])
    tim = str(r[1])







    c, conn = connection()

    #('''INSERT INTO prescription (prescriptionId,patientId,fileName,patientName,timeStamp,penName,patientEmail,penId,doctorName) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(userid, patientid, filename, patient_name, timestamp, prescription, email,prescriptionid,doctorname))

    #query = "SELECT device,timevisited,ipaddress,datevisited from visitor_records"
    #query = "INSERT INTO visitor_records ipaddress,"

    #c.execute(query)

    #data = c.fetchall()

    conn.close()






    return render_template('download.html', value=filename)











if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















