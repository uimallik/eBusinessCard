from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from flask import Flask, request, render_template

app = Flask(__name__)


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
    url.svg('uca-url.svg', scale=8)  #Saving as SVG file
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
    return render_template('idcard.html', value=filename, value2=filename2)



@app.route('/home')
def index():
   return render_template('index.html')


# Return Existing file
@app.route("/file/<id>", methods=['GET'])
def fil(id):
    print id
    filename = "/static/"+str(id)
    return render_template('download.html', value=filename)

    '''
    
    with open(filename, 'rb') as bites:

        return send_file(io.BytesIO(bites.read()),
                     attachment_filename=filename,
                     mimetype='image/png',as_attachment=True)

    '''









if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
















