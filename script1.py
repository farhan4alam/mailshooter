import os
import secrets
import pandas as pd
import smtplib
import random
import time
from flask import Flask, render_template,url_for,flash,redirect,request
from forms import mailingform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_wtf.csrf import CsrfProtect

app=Flask(__name__)
CsrfProtect(app)

title_detail=[
        {'main_title':'Enter From Here!!'},
        {'main_title':'An Efficient Mail App'}
]
app.config['SECRET_KEY']='TArgeting BOOming ACQUIring'

@app.route("/")
def home():
    return render_template("home.html",title_detail=title_detail,main_title='Enter From Here')

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/mail_files',file_fn)
    form_file.save(file_path)
    return file_path

@app.route("/dash", methods=['GET','POST'])
def dash():
    form=mailingform()
    if form.validate_on_submit():
        if request.method == 'POST'  and form.file.data:
            file_p = save_file(form.file.data)
            result = request.form
            final_mail = MIMEMultipart('alternative')
            e=pd.read_excel(file_p)
            emails=e['Email_Ids'].values
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(result['mail'],result['password'])
            msg1 = MIMEText(result['content'], 'html')
            su = result['subject']
            final_mail['Subject'] = su
            final_mail.attach(msg1)
            count = 0
            a=len(emails)
            b=str(a)
            #body = "Subject: {}\n\n{}".format(subject,msg1)
            delay=[5, 7, 10, 12, 11, 4, 21, 3, 9, 13, 17,18,23,25,8,6,14,16,15];
            for email in emails:
                server.sendmail(result['mail'], email, final_mail.as_string())
                random.shuffle(delay)
                delay_suffle1 = delay[1]
                de = int(delay_suffle1)
                count = count + 1


                time.sleep(delay_suffle1)


        server.quit()
        flash ('Out of '+b+' ,All '+b+ ' mails have been fired sucessfully...Congratulations!!' ,'success')
        return render_template("sending.html",result = result,file_p = file_p,emails=emails)
    return render_template("dash.html",title_detail=title_detail,main_title='MailShooter Dashboard',form=form)



@app.route("/sending",methods=['GET','POST'])
def sending():
    return render_template("sending.html",title_detail=title_detail,main_title='An Efficient Mailing App!!')



@app.errorhandler(405)
def server_error(e):
    flash ('You are not allowed to access this page !!','danger')
    return render_template('home.html'), 405

@app.errorhandler(404)
def notfound_server_error(e):
    flash ('Page is not found or valid!!','danger')
    return render_template('home.html'), 404


if __name__=="__main__":
    app.run(debug=True)
