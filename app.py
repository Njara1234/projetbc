from flask import Flask, request ,render_template,send_file,redirect,make_response,flash,send_from_directory,url_for,session
import qrcode
import shutil
from barcode.writer import ImageWriter
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from io import BytesIO
import pdfkit
import os
from flask_bootstrap import Bootstrap
#from models import User
from flask_login import LoginManager,current_user,login_required,login_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from flask_session import Session
from flask_bcrypt import Bcrypt
app=Flask(__name__)


app.config.from_object(Config)
app.config['SECRET_KEY'] = '3ce9e1822fa6e31907ea65f6'
#app.config["SECRET_KEY"]='65b0b774279de460f1cc5c92'
#app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ums.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]='filesystem'
UPLOAD_FOLDER = 'static/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_DIR'] = 'static/Uploads'
root_dir = 'static/Uploads'

#from database import db
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
db = SQLAlchemy(app)
ma = Marshmallow(app)
#db.init_app(app)
bcrypt=Bcrypt(app)
Session(app)

from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager,current_user,login_required,login_user
from werkzeug.utils import secure_filename


from datetime import date, datetime
migrate = Migrate(app, db)



login_manager = LoginManager()
login_manager.login_view = 'user/index.html'
login_manager.init_app(app)
from models import  User,Admin,Superadmin


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# main index 
@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))


app.secret_key = "your-secret-key"


@app.route('/')
def index():

    
    return render_template('index.html', title="")




def data_entry():
    codique = int(input("Codique:"))
    annee = int(input("Annee:"))
    mois = int(input("Mois:"))
    return [codique, annee, mois]


def add_header_text(canvas, text):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawCentredString(595/2, 810, text)
    canvas.restoreState()

"""def generate_pdf_qr(filename, header, content_list):
    print("generate pdf")
    # Create a canvas object
    filename = os.path.join('documents', filename)
    c = canvas.Canvas(filename + ".pdf", pagesize=letter)
    # Set the canvas size to A4
    c.setPageSize((595, 842))

    # Function to generate QRCode image and return its filename
    def generate_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"qr_code_{data}.png"
        qr_img.save(qr_filename)
        return qr_filename

    col = content_list[0]
    if col > 0:
        li = content_list[4] - content_list[3] + 1
        barcode_data_list = [0] * col * li
        count = 0
        mois = content_list[3]
        for j in range(li):
            mois_txt = "{:02d}".format(mois)
            for i in range(col):
                if i == 0:
                    Partie_txt = "PA"
                elif i == 1:
                    Partie_txt = "PB"
                else:
                    Partie_txt = "PC"
                barcode_data_list[count] = Partie_txt + str(content_list[1]) + str(content_list[2]) + mois_txt
                count += 1
            mois += 1

        # Text
        add_header_text(c, header)

        # QRCode drawing
        originX = 50
        originY = 720
        qr_size = 100
        new_x = originX
        new_y = originY

        barcode_counter = 0
        for k in range(1, 2):
            for i in range(li):
                if i == 6:  # lignes per page
                    c.showPage()
                    # Text
                    add_header_text(c, header)
                    new_y = originY
                for j in range(col):
                    # Draw the QRCode on the PDF
                    barcode_data = barcode_data_list[barcode_counter]
                    qr_filename = generate_qr_code(barcode_data)
                    c.drawImage(qr_filename, new_x, new_y, width=qr_size, height=qr_size)

                    barcode_counter += 1

                    # calculate new coordinates
                    new_x = new_x + qr_size + 75
                new_x = originX
                new_y = new_y - 130

        # Save the PDF
        c.showPage()
        c.save()

        # Delete the temporary QRCode images
        for i in range(barcode_counter):
            qr_filename = f"qr_code_{barcode_data_list[i]}.png"
            os.remove(qr_filename)

        return 1
    else:
        return 0"""


def generate_pdf_qr(filename, header, content_list):
    print("generate pdf")
    # Create a canvas object
    filename = os.path.join('documents', filename)
    c = canvas.Canvas(filename + ".pdf", pagesize=letter)
    # Set the canvas size to A4
    c.setPageSize((595, 842))

    # Function to generate QRCode image and return its filename
    def generate_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"qr_code_{data}.png"
        qr_img.save(qr_filename)
        return qr_filename

    col = content_list[0]
    if col > 0:
        li = content_list[4] - content_list[3] + 1
        barcode_data_list = [0] * col * li
        count = 0
        mois = content_list[3]
        for j in range(li):
            mois_txt = "{:02d}".format(mois)
            for i in range(col):
                if i == 0:
                    Partie_txt = "PA"
                elif i == 1:
                    Partie_txt = "PB"
                else:
                    Partie_txt = "PC"
                barcode_data_list[count] = Partie_txt + str(content_list[1]) + str(content_list[2]) + mois_txt
                count += 1
            mois += 1

        # Text
        add_header_text(c, header)

        # QRCode drawing
        originX = 50
        originY = 720
        qr_size = 100
        new_x = originX
        new_y = originY

        barcode_counter = 0
        for k in range(1, 2):
            for i in range(li):
                if i == 6:  # lignes per page
                    c.showPage()
                    # Text
                    add_header_text(c, header)
                    new_y = originY
                for j in range(col):
                    # Draw the QRCode on the PDF
                    barcode_data = barcode_data_list[barcode_counter]
                    qr_filename = generate_qr_code(barcode_data)
                    c.drawImage(qr_filename, new_x, new_y, width=qr_size, height=qr_size)

                    # Draw the number of months under the QR code
                    c.drawString(new_x + 20, new_y - 20, f"Mois: {mois_txt}")

                    # Draw the QR code data (Partie + codique + annee + mois) next to the QR code
                    c.drawString(new_x, new_y - 30, barcode_data)

                    barcode_counter += 1

                    # calculate new coordinates
                    new_x = new_x + qr_size + 75
                new_x = originX
                new_y = new_y - 130

        # Save the PDF
        c.showPage()
        c.save()

        # Delete the temporary QRCode images
        for i in range(barcode_counter):
            qr_filename = f"qr_code_{barcode_data_list[i]}.png"
            os.remove(qr_filename)

        return 1
    else:
        return 0


    

def generate_pdf(filename, header, content_list):#[3(parties),10103(codique),23(annee),1(mois_debut), 2(mois_fin)]   
    print("generate pdf")
    # Create a canvas object
    filename = os.path.join('documents', filename)
    c = canvas.Canvas(filename+".pdf", pagesize=letter)
    # Set the canvas size to A4
    c.setPageSize((595, 842))
    
    # Generate a QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("Hello")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    #qr_img = qr_img.convert("RGB")

    #todo validation content_list
    #...]) + str(content_list[2]) + "{:02d}".format(content_list[3]), "PC"+str(content_list[1]) + str(content_list[2]) + "{:02d}".format(content_list[3])]
    
    #barcodes depend on col number

    col = content_list[0] # récupérer la valeur de col depuis l'entrée utilisateur
    if col > 0: # s'assurer que la valeur de col est positive
    #if content_list[0] == 3:           
       # col = content_list[0]
        li = content_list[4] - content_list[3] + 1 #=>nombres de mois
        barcode_data_list = [0]*col*li
        count = 0
        mois = content_list[3]
        for j in range(li): 
            mois_txt = "{:02d}".format(mois)
            for i in range(col):
                if i == 0:
                    Partie_txt = "PA"
                elif i == 1:
                    Partie_txt = "PB"
                else:
                    Partie_txt = "PC"
                barcode_data_list[count] = Partie_txt + str(content_list[1]) + str(content_list[2]) + mois_txt
                count += 1
            mois += 1
    
        '''
                                Draw the image on the canvas
        '''
        #Text
        add_header_text(c, header)
        
        #Barcode drawing
        originX = 50
        originY = 720
        new_width = 100
        #new_height = 50
        new_x = originX
        new_y = originY

        barcode_counter=0
        for k in range(1,2):
            for i in range(li):
                if i==6:#lignes per page
                    c.showPage()
                    #Text
                    add_header_text(c, header)
                    new_y = originY
                for j in range(col):

                    #c.drawImage("image_bytes.jpg", new_x, new_y, width=new_width, height=new_height)
                    # Draw the QR code and barcode on the PDF
                    #c.drawInlineImage(qr_img, 200, 200)

                    barcode = code39.Standard39(barcode_data_list[barcode_counter], barHeight=50, wide=2, humanReadable=True, checksum=False)
                    barcode.drawOn(c, new_x, new_y)

                    barcode_counter += 1

                    #calculate new coordonates
                    #print(new_x, new_width)
                    new_x = new_x + new_width + 75
                new_x = originX    
                new_y = new_y - 130


        # Save the PDF
        c.showPage()
        c.save()
        

    
        return 1
    else:
        return 0

@app.route('/home')
def home(): 

    return render_template('home.html')

"""@app.route('/pdf',methods=['POST','GET'])
def pdf(): 

     if not session.get('user_id'):
        return redirect('/user/')
     if session.get('user_id'):
        id=session.get('user_id')
        users=User().query.filter_by(id=id).first()
    
 
        if request.method=='POST':

            #filename=request.form.get('filename')
            filename = secure_filename(request.form.get('filename'))
            header=request.form.get('header')
            col=int(request.form['col'])
            #col_input = int(input("Entrez le nombre de colonnes : "))
            codique=int(request.form['codique'])
            annee=int(request.form['annee'])
            debut_mois=int(request.form['debut_mois'])
            fin_mois=int(request.form['fin_mois'])
            
            if filename =="" or header=="" or col=="" or codique==""or annee=="" or debut_mois=="" or fin_mois=="" :
                flash('Veuillez remplir tous les champs','danger')

            else:
                pdf_filename = filename + '.pdf'
                pdf_path = os.path.join('documents', pdf_filename)
                if os.path.exists(pdf_path):
                    flash('Un fichier avec ce nom existe déjà', 'danger')
                
                else:
                    #col = int(request.form.get('col'))
                    success = generate_pdf(filename, header, [col, codique, annee, debut_mois, fin_mois])


                    if success:  
                        #filename = os.path.join('documents', filename)
                        os.startfile(pdf_path)
                        #os.startfile(os.path.join('documents', filename + '.pdf'))

                        #os.startfile(filename + ".pdf")
                        flash('Le PDF a été généré avec succès', 'success')
                    
                    else:
                        flash('Erreur lors de la génération du PDF', 'danger')

        return render_template("/user/home.html",users=users)"""


@app.route('/pdf', methods=['POST', 'GET'])
def pdf():
    if not session.get('user_id'):
        return redirect('/user/')

    if session.get('user_id'):
        id = session.get('user_id')
        users = User().query.filter_by(id=id).first()

        if request.method == 'POST':
            # ... Votre code pour récupérer les données du formulaire ...
            #filename=request.form.get('filename')
            filename = secure_filename(request.form.get('filename'))
            header=request.form.get('header')
            col=int(request.form['col'])
            #col_input = int(input("Entrez le nombre de colonnes : "))
            codique=int(request.form['codique'])
            annee=int(request.form['annee'])
            debut_mois=int(request.form['debut_mois'])
            fin_mois=int(request.form['fin_mois'])
            # Vérifier que tous les champs sont remplis
            if not filename or not header or not col or not codique or not annee or not debut_mois or not fin_mois:
                flash('Veuillez remplir tous les champs', 'danger')
            else:
                pdf_filename = filename + '.pdf'
                pdf_path = os.path.join('documents', pdf_filename)

                # Vérifier si le fichier PDF existe déjà
                if os.path.exists(pdf_path):
                    flash('Un fichier avec ce nom existe déjà', 'danger')
                else:
                    # Générer le PDF
                    success = generate_pdf(filename, header, [col, codique, annee, debut_mois, fin_mois])

                    if success:
                        # Déplacer le fichier PDF vers le répertoire "code a barre" sur le bureau
                        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                        code_a_barre_path = os.path.join(desktop_path, 'code a barre')

                        # Créez le répertoire "code a barre" s'il n'existe pas
                        if not os.path.exists(code_a_barre_path):
                            os.makedirs(code_a_barre_path)

                        # Chemin complet du fichier PDF dans le répertoire "code a barre" sur le bureau
                        new_pdf_path = os.path.join(code_a_barre_path, pdf_filename)

                        # Déplacez le fichier PDF vers le répertoire "code a barre" sur le bureau
                        shutil.move(pdf_path, new_pdf_path)

                        # Envoyer le fichier PDF en réponse pour le téléchargement
                        return send_file(new_pdf_path, as_attachment=True)
                    else:
                        flash('Erreur lors de la génération du PDF', 'danger')

        return render_template("/user/home.html", users=users)
#------------------------------------------------------------------

# admin loign
@app.route('/admin/',methods=["POST","GET"])
def adminIndex():
    # chect the request is post or not
    if request.method == 'POST':
        # get the value of field
        username = request.form.get('username')
        password = request.form.get('password')
        # check the value is not empty
        if username=="" and password=="":
            flash('Please fill all the field','danger')
            return redirect('/admin/')
        else:
            # login admin by username 
            admins=Admin().query.filter_by(username=username).first()
            if admins and admins.password:
                session['admin_id']=admins.id
                session['admin_name']=admins.username
                flash('Login Successfully','success')
                return redirect('/admin/dashboard')
            else:
                flash('Invalid Email and Password','danger')
                return redirect('/admin/')
    else:
        return render_template('admin/index.html',title="Admin Login")

# admin Dashboard
@app.route('/admin/dashboard')
def adminDashboard():
    if not session.get('admin_id'):
        return redirect('/admin/')
    totalUser=User.query.count()
    totalApprove=User.query.filter_by(status=1).count()
    NotTotalApprove=User.query.filter_by(status=0).count()
    return render_template('admin/dashboard.html',title="Admin Dashboard",totalUser=totalUser,totalApprove=totalApprove,NotTotalApprove=NotTotalApprove)

# admin get all user 
@app.route('/admin/get-all-user', methods=["POST","GET"])
def adminGetAllUser():
    if not session.get('admin_id'):
        return redirect('/admin/')
    if request.method== "POST":
        search=request.form.get('search')
        users=User.query.filter(User.username.like('%'+search+'%')).all()
        
        return render_template('admin/all-user.html',title='Approve User',users=users)
    else:
        users=User.query.all()
        
        return render_template('admin/all-user.html',title='Approve User',users=users)


#--------------------

@app.route('/admin/approve-user/<int:id>')
def adminApprove(id):
    if not session.get('admin_id'):
        return redirect('/admin/')
        
    User().query.filter_by(id=id).update(dict(status=1))
    db.session.commit()
    flash('Approve Successfully','success')
    return redirect('/admin/get-all-user')

# change admin password
@app.route('/admin/change-admin-password',methods=["POST","GET"])
def adminChangePassword():
    admin=Admin.query.get(1)
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username == "" or password=="":
            flash('Please fill the field','danger')
            return redirect('/admin/change-admin-password')
        else:
            Admin().query.filter_by(username=username).update(dict(password=bcrypt.generate_password_hash(password,10)))
            db.session.commit()
            flash('Admin Password update successfully','success')
            return redirect('/admin/change-admin-password')
    else:
        return render_template('admin/admin-change-password.html',title='Admin Change Password',admin=admin)

# admin logout
@app.route('/admin/logout')
def adminLogout():
    if not session.get('admin_id'):
        return redirect('/admin/')
    if session.get('admin_id'):
        session['admin_id']=None
        session['admin_name']=None
        return redirect('/')

# User login
@app.route('/user/',methods=["POST","GET"])
def userIndex():
    if  session.get('user_id'):
        return redirect('/user/dashboard')
    if request.method=="POST":
        # get the name of the field
        email=request.form.get('email')
        password=request.form.get('password')
        # check user exist in this email or not
        users=User().query.filter_by(email=email).first()
        if users and users.password:
            # check the admin approve your account are not
            is_approve=User.query.filter_by(id=users.id).first()
            # first return the is_approve:
            if is_approve.status == 0:
                flash('Your Account is not approved by Admin','danger')
                return redirect('/user/')
            else:
                session['user_id']=users.id
                session['username']=users.username
                flash('Login Successfully','success')
                return redirect('/user/dashboard')
        else:
            #flash('Invalid Email and Password','danger')
            return redirect('/user/')
    else:
        return render_template('user/index.html',title="User Login")

# User Register
@app.route('/user/signup',methods=['POST','GET'])
def userSignup():
    if  session.get('user_id'):
        return redirect('/user/dashboard')
    if request.method=='POST':
        # get all input field name
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        username=request.form.get('username')
        
        password=request.form.get('password')
        #image_file=request.files.get('image_file')
        
       
       
        # check all the field is filled are not
        if fname =="" or lname=="" or email=="" or password=="" or username==""  :
            flash('Veuillez remplir tous les champs','danger')
            return redirect('/user/signup')      
 
        else:
            is_email=User().query.filter_by(email=email).first()            
            if is_email:
                
                flash('Email exisete deja','danger')
                return redirect('/user/signup')
            else:
                
                hash_password=bcrypt.generate_password_hash(password,10)
                user=User(fname=fname,lname=lname,email=email,password=hash_password,username=username)
                db.session.add(user)
                db.session.commit()
                
                flash('Le compte est créé avec succès L administrateur approuvera ','success')
                return redirect('/user/')
    else:
        return render_template('user/signup.html',title="User Signup")
    

    # Admin Register
@app.route('/admin/signup',methods=['POST','GET'])
def adminSignup():
    if  session.get('admin_id'):
        return redirect('/admin/dashboard')
    if request.method=='POST':
             
        username=request.form.get('username')        
        password=request.form.get('password')
             
              
        if password=="" or username==""  :
            flash('Veuillez remplir tous les champs','danger')
            return redirect('/admin/signup')      
 
        else:
            is_username=Admin().query.filter_by(username=username).first()            
            if is_username:
                
                flash('username exisete deja','danger')
                return redirect('/admin/signup')
            else:
                
                hash_password=bcrypt.generate_password_hash(password,10)
                admin=Admin(password=hash_password,username=username)
                db.session.add(admin)
                db.session.commit()
                
                flash('Le compte est créé avec succès  ','success')
                return redirect('/admin/')
    else:
        return render_template('admin/signup.html',title="Admin Signup")


# user dashboard
@app.route('/user/dashboard')
def userDashboard():
    if not session.get('user_id'):
        return redirect('/user/')
    if session.get('user_id'):
        id=session.get('user_id')
        users=User().query.filter_by(id=id).first()
    return render_template('user/dashboard.html',title="User Dashboard",users=users)

# user logout
@app.route('/user/logout')
def userLogout():
    if not session.get('user_id'):
        return redirect('/user/')

    if session.get('user_id'):
        session['user_id'] = None
        session['username'] = None
        #return redirect('/user/')
        return redirect('/')


@app.route('/user/change-password',methods=["POST","GET"])
def userChangePassword():
    if not session.get('user_id'):
        return redirect('/user/')
    if session.get('user_id'):
        id=session.get('user_id')
        users=User.query.get(id)
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        if email == "" or password == "":
            flash('Please fill the field','danger')
            return redirect('/user/change-password')
        else:
            users=User.query.filter_by(email=email).first()
            if users:
               hash_password=bcrypt.generate_password_hash(password,10)
               User.query.filter_by(email=email).update(dict(password=hash_password))
               db.session.commit()
               flash('Password Change Successfully','success')
               return redirect('/user/change-password')
            else:
                flash('Invalid Email','danger')
                return redirect('/user/change-password')

    else:
        return render_template('user/change-password.html',title="Change Password",users=users)

# user update profile
@app.route('/user/update-profile', methods=["POST","GET"])
def userUpdateProfile():
    if not session.get('user_id'):
        return redirect('/user/')
    if session.get('user_id'):
        id=session.get('user_id')
    users=User.query.get(id)
    if request.method == 'POST':
        # get all input field name
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        email=request.form.get('email')
        username=request.form.get('username')
        telephone=request.form.get('telephone')
        if fname =="" or lname=="" or email=="" or username=="" or telephone=="":
            flash('Please fill all the field','danger')
            return redirect('/user/update-profile')
        else:
            session['username']=None
            User.query.filter_by(id=id).update(dict(fname=fname,lname=lname,email=email,telephone=telephone,username=username))
            db.session.commit()
            session['username']=username
            flash('Profile update Successfully','success')
            return redirect('/user/dashboard')
    else:
        return render_template('user/update-profile.html',title="Update Profile",users=users)

    
@app.route('/superadmin',methods=["POST","GET"])
def SuperadminIndex():
    # check the request is post or not
    if request.method == 'POST':
        # get the value of fields
        username = request.form.get('username')
        password = request.form.get('password')
        # check the values are not empty
        if username=="" and password=="":
            flash('Please fill all the fields','danger')
            return redirect('/superadmin')
        else:
            # login superadmin by username 
            superadmin = Superadmin.query.filter_by(username=username).first()
            if superadmin and superadmin.password:
                session['superadmin_id'] = superadmin.id
                session['superadmin_name'] = superadmin.username
                flash('Login Successfully','success')
                return redirect('/admin/signup')
            else:
                flash('Invalid Email and Password','danger')
                return redirect('/superadmin')
    else:
        return render_template('admin/loginsuperadmin.html', title="Superadmin Login")
    
@app.route('/mode_demploi')
def mode_demploi():
    return render_template('mode_demploi.html')


if __name__ == '__main__':
    app.run(debug=True)