# -*- coding: UTF-8 -*-
from flask import (Flask, flash, logging, redirect, render_template, request,
                   session, url_for)
from flask_mysql_connector import MySQL

from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, TextAreaField, validators

app =Flask(__name__)

app.secret_key="dehatek"
app.config["MYSQL_HOST"] = "sql7.freemysqlhosting.net"
app.config["MYSQL_PORT"] = "3306"
app.config["MYSQL_USER"] = "sql7387757"
app.config["MYSQL_PASSWORD"] = "JcN5a17QBK"
app.config["MYSQL_DATABASE"] = "sql7387757"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/layout")
def layout():
    return render_template("layout.html")
class fRegisterform(Form):
    fname = StringField("Yetkili adı  :")
    fsurname = StringField("Yetkili Soyad  :")
    tic = StringField("Firma adı  :")
    adres = StringField("Adress  :")
    telefon = StringField("Firma Telefon  :")
    yetkili = StringField("Sektör adı  :")
    yetkilitel = StringField("Firma Kuruluş  tarihi :")
    yetkilimail = StringField("Yetkili Telefon  :")
    yetkiliadres = StringField("Yetkili MailAdresi  :")
    password = PasswordField("Parola Oluştur")
class loginform(Form):
    mail = StringField("Firma mail/Kullanıcı Adı :")

    password = PasswordField("Parola :")

class RegisterForm(Form):
    name = StringField("adınız  :")
    surname = StringField("soyadınız :")
    point = StringField("Ofis Programı ")
    point1 = StringField("Tekonolojik Donanım ")
    point2 = StringField("Muhasebe programları")




@app.route( "/register" , methods=["GET","POST"])


#personel Kayıt 
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        point = form.point.data
        point1 = form.point1.data
        point2 = form.point2.data
        a = 6

        if int(point) < a and int(point1) < a:
            if int(point2) < a :
                cursor = mysql.connection.cursor()
                sorgu = "INSERT INTO homework(name,surname,point,point1,point2) Values (%s,%s,%s,%s,%s)"
                values=(name,surname,point,point1,point2)
                cursor.execute(sorgu,values)
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for("index"))

            
          


        
    else:
        return render_template("register.html",form = form)

@app.route( "/fregister" , methods=["GET","POST"])

#Firma Kayıt
def fregister():
    form = fRegisterform(request.form)

    if request.method == "POST" and form.validate():
        fname = form.fname.data
        fsurname = form.fsurname.data
        tic = form.tic.data
        adres = form.adres.data
        telefon = form.telefon.data
        yetkili = form.yetkili.data
        yetkilitel = form.yetkilitel.data
        yetkilimail = form.yetkilimail.data
        yetkiliadres = form.yetkiliadres.data
        password = sha256_crypt.encrypt(form.password.data)
        

        cursor = mysql.new_cursor()
        sorgu = "Insert into Fhome(fname,fsurname,tic,adres,telefon,yetkili,yetkilitel,yetkilimail,yetkiliadres,password) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(fname,fsurname,tic,adres,telefon,yetkili,yetkilitel,yetkilimail,yetkiliadres,password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("index"))
    else:
        return render_template("fregister.html",form = form)


@app.route("/dashboard")
def dashboard():
    cursor = mysql.connection.cursor()

    sorgu = "Select * From homework"

    result  = cursor.execute(sorgu)

    
    articles = cursor.fetchall()
    ada = ""
    return render_template("dashboard.html" , articles = articles , ada = ada)


@app.route("/search" , methods = ["GET","POST"])
def search():

   if request.method == "GET":
       return render_template("search.html")

   else:
       
       select = request.form.get('select1')
       cursor = mysql.connection.cursor()
       
       sorgu = "SELECT * FROM homework WHERE point =  " + select
       result = cursor.execute(sorgu)
       if result == 0 :
           return redirect(url_for("index.html"))
       asd = cursor.fetchall()
       adaa = ""
       return render_template("search.html" , adaa = adaa , asd = asd)

    
@app.route("/login" , methods = ["GET","POST"] )
def login():
   form = loginform(request.form)
   if request.method == "POST":
    mail = form.mail.data
    password = form.password.data

    cursor = mysql.connection.cursor()

    sorgu= "Select * from Fhome where yetkilimail = %s"

    result = cursor.execute(sorgu,(mail,))
    sonuc = cursor.fetchall()
    app.logger.info(sonuc)
    if not result:
        app.logger.info('Yanlış şifre')

        pass
    else:
        data = cursor.fetchone()
        real_password = data["password"]

        
            
        if sha256_crypt.verify(password_entered,real_password):
            flash("başarılı giriş","success")
            session["logged_in"]= True
            session["username"] = username
            app.logger.info("parola giriş başarılı")
            return redirect(url_for("index"))
        else:
            flash("yanlış parola")
            return redirect(url_for("login"))
            app.logger.info("parola yanlış")

        """else:

              flash("Hatalı Kullanıcı Adı","danger")
            return redirect(url_for("login"))
"""
   return render_template("login.html" , form = form )

if __name__ == "__main__":
    app.run(debug=True)
