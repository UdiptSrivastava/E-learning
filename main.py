from flask import Flask, render_template, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename, redirect
import os
import random
import json

app = Flask(__name__)

with open('config.json') as c:
    params = json.load(c)["params"]
app.secret_key = "super-secret-key"
app.config['cv_path'] = params['cv_path']
app.config['dp_path'] = params['dp_path']
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['email'],
    MAIL_PASSWORD=params['password']
)
mail = Mail(app)
db = SQLAlchemy(app)


class Feedback(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    Email_Id = db.Column(db.String(40), unique=False, nullable=False)
    Contact_no = db.Column(db.String(40), unique=False, nullable=False)
    Feedback = db.Column(db.String(40), unique=False, nullable=False)
    Date = db.Column(db.String(40), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(40), unique=False, nullable=False, default='N')


class Enquiry(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    cno = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    gen = db.Column(db.String(6), unique=False, nullable=False)
    city = db.Column(db.String(30), unique=False, nullable=False)
    enquiry = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(1), unique=False, nullable=False, default='N')


class Career(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(8), unique=False, nullable=False)
    address = db.Column(db.String(40), unique=False, nullable=False)
    cv = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(8), unique=False, nullable=False)
    date = db.Column(db.String(40), unique=False, nullable=True, default=datetime.now())
    status = db.Column(db.String(40), unique=False, nullable=False, default='N')


class Course(db.Model):
    course_code = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(40), unique=False, nullable=False)
    fees = db.Column(db.String(40), unique=False, nullable=False)
    duration = db.Column(db.String(40), unique=False, nullable=False)
    career = db.Column(db.String(40), unique=False, nullable=False)
    module = db.Column(db.String(40), unique=False, nullable=False)

class Stu_course(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    ccode = db.Column(db.String(40), unique=False, nullable=False)
    cname = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    fee = db.Column(db.String(40), unique=False, nullable=False)
    duration = db.Column(db.String(40), unique=False, nullable=False)
    career = db.Column(db.String(40), unique=False, nullable=False)
    module = db.Column(db.String(40), unique=False, nullable=False)


class Application(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(8), unique=False, nullable=False)
    course = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(8), unique=False, nullable=False)
    bank = db.Column(db.String(40), unique=False, nullable=False)
    ddno = db.Column(db.String(40), unique=False, nullable=False)


class Member(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(8), unique=False, nullable=False)
    course = db.Column(db.String(40), unique=False, nullable=False)
    date = db.Column(db.String(8), unique=False, nullable=False)
    bank = db.Column(db.String(40), unique=False, nullable=False)
    ddno = db.Column(db.String(40), unique=False, nullable=False)
    image = db.Column(db.String(40), unique=False, nullable=True)
    address = db.Column(db.String(100), unique=False, nullable=True)
    status = db.Column(db.String(40), unique=False, nullable=False, default='active')


class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    user_id = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40), unique=False, nullable=False)
    status = db.Column(db.String(8), unique=False, nullable=False, default='S')

class Profile(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    contact = db.Column(db.String(40), unique=False, nullable=False)
    address = db.Column(db.String(40), unique=False, nullable=False)
    image= db.Column(db.String(40), unique=False, nullable=False)

class Questions(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    ques = db.Column(db.String(1000), unique=False, nullable=False)
    option1 = db.Column(db.String(20), unique=False, nullable=False)
    option2 = db.Column(db.String(20), unique=False, nullable=False)
    option3 = db.Column(db.String(6), unique=False, nullable=False)
    option4 = db.Column(db.String(30), unique=False, nullable=False)
    correct = db.Column(db.String(100), unique=False, nullable=False)
    course = db.Column(db.String(30), unique=False, nullable=False)


class Result(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=False, nullable=False)
    attempted = db.Column(db.String(200), unique=False, nullable=False)
    total = db.Column(db.String(20), unique=False, nullable=False)
    correct = db.Column(db.String(20), unique=False, nullable=False)
    wrong = db.Column(db.String(6), unique=False, nullable=False)
    unanswered = db.Column(db.String(30), unique=False, nullable=False)
    grade = db.Column(db.String(100), unique=False, nullable=False)
    percent = db.Column(db.String(30), unique=False, nullable=False)
    result = db.Column(db.String(30), unique=False, nullable=False)
    course_code = db.Column(db.String(20), unique=False, nullable=False)
    course_name = db.Column(db.String(30), unique=False, nullable=False)

def get_password(n):
    s = "qwertyupkjhgfdsazxcvbnmQWERTYUPLKJHGFDSAZXCVBNM23456789"
    str = ''
    for i in range(0, n):
        a = random.randint(0, len(s))
        str += s[a]
    return str

@app.route('/')
def home():
    pid = 0
    data = Course.query.all()
    return render_template('index.html',data=data,pid=pid)

@app.route('/about')
def about():
    msg = ''
    pid = 3;
    return render_template('about.html', pid=pid)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    pid = 4
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('cno')
        feed = request.form.get('fb')

        sql = Feedback(name=name, Email_Id=email, Contact_no=contact, Feedback=feed)
        db.session.add(sql)
        db.session.commit()
        msg = 'Feedback saved successfully'
    return render_template('contact.html', pid=pid)




@app.route('/profile', methods=['GET', 'POST'])
def profile():
    name = ""
    email = ""
    cno = ""
    add=""
    img=""
    msg=""
    fname=""
    if request.method == 'POST':

        sno=session['id']
        print(sno)
        data=Member.query.filter_by(sno=sno).first()
        name = request.form.get('name')
        email = request.form.get('email')
        cno = request.form.get('contact')
        add = request.form.get('add')

        file = request.files['image']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]

        if ext == ".png" or ext == ".jpeg" or ext == ".jpg":


                fname = secure_filename(str(int(data.sno) + 1) + ext)

                data.image=fname
                db.session.commit()

                file.save(os.path.join(app.config['dp_path'], fname))


        else:
            msg = "Please upload a valid image"

        data.name=name
        data.email=email
        data.contact=cno
        data.address=add
        data.image=fname
        db.session.commit()
        msg="Profile Updated successfully"

    else:
        sno = session['id']
        data = Member.query.filter_by(sno=sno).first()
        name = data.name
        email = data.email
        cno = data.contact
        add = data.address
        fname=data.image



    li=[sno,name,email,cno,add,fname]

    return render_template('user/admin/profile.html',li=li)

@app.route('/courses')
def courses():
    pid = 7
    data = Course.query.all()
    return render_template('course.html', pid=pid, data=data)


@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    msg = ''
    pid = 5;
    if request.method == 'POST':
        name = request.form.get('name')
        contact = request.form.get('cno')
        email = request.form.get('email')
        gender = request.form.get('gen')
        city = request.form.get('city')
        enq = request.form.get('enquiry')

        sql = Enquiry(name=name, cno=contact, gen=gender, city=city, enquiry=enq, email=email)
        db.session.add(sql)
        db.session.commit()
        msg = 'Enquiry saved successfully'

    return render_template('enquiry.html', pid=pid)


@app.route('/career', methods=['GET', 'POST'])
def career():
    name = ""
    email = ""
    cno = ""
    gen = ""
    msg = ""
    pid = 6
    if request.method == 'POST':
        msg = "Your career details saved"
        name = request.form.get('name')
        cno = request.form.get('cno')
        gender = request.form.get('gen')
        email = request.form.get('email')
        add = request.form.get('add')
        city = request.form.get('city')
        file = request.files['cv']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]
        if ext == ".pdf" or ext == ".doc" or ext == ".docx":
            data = Career.query.filter_by(email=email).first()
            if not data:
                data = Career.query.order_by(Career.sno.desc()).first()
                if not data:
                    fname = secure_filename("1" + ext)
                else:
                    fname = secure_filename(str(int(data.sno) + 1) + ext)
                entry = Career(name=name, email=email, contact=cno, gender=gender, address=add, city=city,
                               cv=fname)
                db.session.add(entry)
                db.session.commit()
                print(fname)
                file.save(os.path.join(app.config['cv_path'], fname))
                name = ""
                email = ""
                cno = ""
                gen = ""
                msg = "Career Detail Successfully Saved"
            else:
                msg = 'Email-Id already exist'
        else:
            msg = "Please upload a valid CV File"

    li1 = [name, email, cno, gen, msg]
    return render_template('career.html', li=li1, pid=pid)


@app.route('/login', methods=['GET', 'POST'])
def login():
    name = ""
    email = ""
    cno = ""
    gen = ""
    msg = ""
    pid = 0;
    if request.method == 'POST' and 'RegSubmit' in request.form:

        name = request.form.get('name')
        cno = request.form.get('cno')
        gender = request.form.get('gen')
        email = request.form.get('email')
        course = request.form.get('course')
        bank = request.form.get('bank')
        dd = request.form.get('dd')
        date = request.form.get('date')
        pid = 0
        data = Application.query.filter_by(email=email).first()
        if not data:
            entry = Application(name=name, email=email, contact=cno, gender=gender, course=course, date=date, bank=bank,
                                ddno=dd)

            db.session.add(entry)

            db.session.commit()
            mail.send_message('Message from ' + "eLearning",
                              sender=params['email'],
                              recipients=[email],
                              body="Hello " + name + "\nYour details are received. We contact you soon ")
            msg = "Your details saved"
        else:
            msg = "Already Registered"
            pid = 1
    elif request.method == 'POST' and 'Login' in request.form:
        email = request.form.get('email')
        password = request.form.get('pass')

        data = Login.query.filter_by(user_id=email).first()
        if not data:
            msg = "Email does not exist"
            pid = 2
        else:
            if data.password == password:
                session['name'] = data.name
                session['uid'] = data.user_id
                session['id'] = data.sno
                status=data.status
                data = Member.query.filter_by(email=email).first()
                session['img'] = data.image
                if status=='A':
                    return render_template('user/admin/index.html')
                else :
                    return render_template('user/student/index.html')

            else:
                msg = "Invalid password"
                pid = 2
    data = Course.query.all()
    return render_template('index.html', msg=msg, pid=pid, data=data)


# admin
@app.route('/admin')
def admin():
    msg = ''
    return render_template('user/admin/index.html')


@app.route('/course/<string:code>,<string:cmd>', methods=['GET', 'POST'])
def course(code, cmd):
    cc = ''
    cn = ''
    mod = ''
    fee = ''
    dur = ''
    car = ''
    msg = ''
    if request.method == 'POST':
        cc = request.form.get('cc')
        cn = request.form.get('cn')
        fee = request.form.get('fee')
        dur = request.form.get('dur')
        car = request.form.get('car')
        mod = request.form.get('mod')

        if cmd == '1':
            data = Course.query.filter_by(course_code=cc).first()
            if not data:
                data = Course.query.filter_by(course_name=cn).first()
                if not data:
                    sql = Course(course_code=cc, course_name=cn, fees=fee, duration=dur, career=car, module=mod)
                    db.session.add(sql)
                    db.session.commit()
                    msg = 'Course Added suceesfully'
                    cc = ''
                    cn = ''
                    mod = ''
                    fee = ''
                    dur = ''
                    car = ''
                else:
                    msg = 'Course Name already exist'
            else:
                msg = 'Course Code already exist'
        elif cmd == '3':
            flag = 1
            if session['cc'] != cc:
                find = Course.query.filter_by(course_code=cc).first()
                if find:
                    flag = 0
                    msg = "Course Code already exist"
            elif session['cn'] != cn:
                find = Course.query.filter_by(course_name=cn).first()
                if find:
                    flag = 0
                    msg = "Course Name already exist"

            if flag == 1:
                # code = session['cc']
                data = Course.query.filter_by(course_code=code).first()
                data.course_code = cc
                data.course_name = cn
                data.duration = dur
                data.fees = fee
                data.module = mod
                data.career = car
                db.session.commit()
                session.pop("cc")
                session.pop("cn")
                cmd = '0'
                code = '0'
        elif cmd == '4':
            rs = Course.query.filter_by(course_code=code).first()
            db.session.delete(rs)
            db.session.commit()
            cmd = '0'
            code = '0'
    if code != '':
        if cmd == '2' or cmd == '3' or cmd == '4':
            code = code
            val = Course.query.filter_by(course_code=code).first()
            cc = val.course_code
            cn = val.course_name
            fee = val.fees
            dur = val.duration
            mod = val.module
            car = val.career
            session['cc'] = cc
            session['cn'] = cn

    data = Course.query.all()
    li = [cc, cn, fee, dur, mod, car, code, cmd, msg]
    return render_template('user/admin/course.html', data=data, li=li)


@app.route('/application/<string:sno>', methods=["GET", "POST"])
def application(sno):
    name = ''
    email = ''
    contact = ''
    gender = ''
    course = ''
    date = ''
    bank = ''
    ddno = ''
    img=''
    add=''
    msg = ''
    sn = 0
    if request.method == 'POST' and 'Confirm' in request.form:

        data = Login.query.order_by(Login.sno.desc()).first()
        if not data:
            sn = 1
        else:
            sn = int(data.sno) + 1
        upass = get_password(6)
        data = Application.query.filter_by(sno=sno).first()
        entry = Login(sno=sn, name=data.name, user_id=data.email, password=upass, status='S')
        db.session.add(entry)
        db.session.commit()

        data = Member.query.filter_by(email=email).first()
        if not data:
            data = Application.query.filter_by(sno=sno).first()
            cc=data.course
            email = data.email
            entry = Member(sno=sn,name=data.name, email=data.email, contact=data.contact, gender=data.gender,
                           course=data.course, date=data.date, bank=data.bank, ddno=data.ddno,image=img,address=add)
            db.session.add(entry)
            db.session.commit()

            db.session.delete(data)
            db.session.commit()


            data = Course.query.filter_by(course_code=cc).first()

            entry = Stu_course(sno=sn,ccode=cc,email=email,cname=data.course_name,fee=data.fees,duration=data.duration,module=data.module,career=data.career)
            db.session.add(entry)
            db.session.commit()

            # mail.send_message('Message from ' + "eLearning",
            #                   sender=params['email'],
            #                   recipients=[data.email_id],
            #                   body="Hello " + data.name + "\nYour details are received. We contact you soon ")



            sno = '0'
    elif request.method == 'POST' and 'Delete' in request.form:
        data = Application.query.filter_by(sno=sno).first()
        db.session.delete(data)
        db.session.commit()
        sno = '0'
    elif sno != '0':
        data = Application.query.filter_by(sno=sno).first()
        sno = data.sno
        name = data.name
        email = data.email
        contact = data.contact
        gender = data.gender
        course = data.course
        date = data.date
        bank = data.bank
        ddno = data.ddno
    data = Application.query.all()
    li = [sno, name, email, contact, gender, course, date, bank, ddno]
    return render_template('user/admin/application.html', data=data, li=li)


@app.route('/status/<string:sno>,<string:cmd>', methods=["GET", "POST"])
def status(cmd, sno):
    name = ''
    email = ''
    contact = ''
    gender = ''
    course = ''
    date = ''
    bank = ''
    ddno = ''
    msg = ''

    if request.method == 'POST':
        if 'Inactive' in request.form:
            data = Member.query.filter_by(sno=sno).first()
            data.status = 'inactive'
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[data.email],
                              body="Hello " + data.name + "\nYour User Id " + data.email + " deactivated.")
            cmd = '0'
        elif 'Active' in request.form:
            data = Member.query.filter_by(sno=sno).first()
            data.status = 'active'
            db.session.commit()
            mail.send_message('Message from ' + 'eLearning',
                              sender=params['email'],
                              recipients=[data.email],
                              body="Hello " + data.name + "\nYour User Id " + data.email + " activated.")
            sno = '0'
            cmd = '0'
        elif 'Delete' in request.form:
            data = Member.query.filter_by(sno=sno).first()
            db.session.delete(data)
            db.session.commit()
            sno = '0'
            cmd = '0'

    if cmd == '2' or cmd == '3':
        data = Member.query.filter_by(sno=sno).first()
        sno = data.sno
        name = data.name
        email = data.email
        contact = data.contact
        gender = data.gender
        course = data.course
        date = data.date
        bank = data.bank
        ddno = data.ddno
        status = data.status

    if cmd == '0':
        data = Member.query.filter_by(status='active').all()

    elif cmd == '1':
        data = Member.query.filter_by(status='inactive').all()

    li = [cmd, name, email, contact, gender, course, date, bank, ddno, sno]
    return render_template('user/admin/statuss.html', data=data, li=li)


@app.route('/display/<string:cmd>,<string:sno>', methods=["GET", "POST"])
def display(cmd, sno):
    name = ''
    email = ''
    contact = ''
    gender = ''
    course = ''
    date = ''
    feedback = ''
    enquiry = ''
    city = ''
    address = ''
    cv = ''
    msg = ''
    status = ''

    if request.method == 'POST' and 'Reply' in request.form:
        if session['cmd'] == '7':
            data = Feedback.query.filter_by(sno=sno).first()
            cmd = '1'
        elif session['cmd'] == '8':
            data = Enquiry.query.filter_by(sno=sno).first()
            cmd = '2'
        elif session['cmd'] == '9':
            data = Career.query.filter_by(sno=sno).first()
            cmd = '3'
        email = request.form.get('email')
        name = request.form.get('name')
        reply = request.form.get('reply')

        mail.send_message('Message from ' + "eLearning",
                          sender=params['email'],
                          recipients=[email],
                          body="Hello " + name + "\n " + reply)

        data.status = 'Y'
        db.session.commit()
        sno = '0'

    if sno == '0':
        if cmd == '1':
            data = Feedback.query.all()
        elif cmd == '2':
            data = Enquiry.query.all()
        else:
            data = Career.query.all()

    else:
        if cmd == '4' or cmd == '7':
            data = Feedback.query.filter_by(sno=sno).first()
            sno = data.sno
            name = data.name
            email = data.Email_Id
            contact = data.Contact_no
            feedback = data.Feedback
            date = data.Date
            status = data.status

            if cmd == '7':
                session['cmd'] = '7'

        elif cmd == '5' or cmd == '8':
            data = Enquiry.query.filter_by(sno=sno).first()
            sno = data.sno
            name = data.name
            email = data.email
            contact = data.cno
            enquiry = data.enquiry
            date = data.date
            city = data.city
            gender = data.gen
            status = data.status

            if cmd == '8':
                session['cmd'] = '8'

        elif cmd == '6' or cmd == '9':
            data = Career.query.filter_by(sno=sno).first()
            sno = data.sno
            name = data.name
            email = data.email
            contact = data.contact
            address = data.address
            date = data.date
            city = data.city
            gender = data.gender
            cv=data.cv
            status = data.status

            if cmd == '9':
                session['cmd'] = '9'

    li = [cmd, sno, name, email, contact, gender, feedback, city, enquiry, address, cv, date, status]
    return render_template('user/admin/display.html', data=data, li=li)


@app.route('/ques/<string:code>', methods=['GET', 'POST'])
def ques(code):
    session['code']=code
    return redirect('/question/+0+,0')

@app.route('/question/<string:sno>,<string:cmd>', methods=['GET', 'POST'])
def question(sno, cmd):
    ques = ''
    opt1 = ''
    opt2 = ''
    opt3 = ''
    opt4 = ''
    ans = ''
    cc=''
    msg = ''
    code=session['code']
    if request.method == 'POST':
        sno = request.form.get('sno')
        ques = request.form.get('ques')
        opt1 = request.form.get('o1')
        opt2 = request.form.get('o2')
        opt3 = request.form.get('o3')
        opt4 = request.form.get('o4')
        ans = request.form.get('ans')
        cc = request.form.get('course')
        if cmd == '1':
                data = Questions.query.filter_by(course=code).first()
                sql = Questions(ques=ques, option1=opt1, option2=opt2, option3=opt3, option4=opt4,correct=ans,course=code)
                db.session.add(sql)
                db.session.commit()
                msg = 'Question Added suceesfully'
                ques = ''
                opt1 = ''
                opt2 = ''
                opt3 = ''
                opt4 = ''
                ans = ''

        elif cmd == '3':
                sno=session['sno']
                cmd = session['cmd']
                data = Questions.query.filter_by(sno=sno).first()
                print(sno)
                data.ques = ques
                data.option1 = opt1
                data.option2 = opt2
                data.option3 = opt3
                data.option4 = opt4
                data.correct = ans
                db.session.commit()

                cmd = '0'
                # return redirect('/question/'+session['code']+',0')
        elif cmd == '4':
            sno = session['sno']
            cmd = session['cmd']
            rs = Questions.query.filter_by(sno=sno).first()
            db.session.delete(rs)
            db.session.commit()
            cmd = '0'


    elif cmd == '2' or cmd == '3' or cmd == '4':
                data =  Questions.query.filter_by(sno=sno).first()

                sno=data.sno
                code=data.course
                ques=data.ques
                opt1=data.option1
                opt2=data.option2
                opt3=data.option3
                opt4=data.option4
                ans=data.correct
                cc=data.course
                session['cmd']=cmd
                session['sno']=sno


    data = Questions.query.filter_by(course=code).all()
    print(data)
    li = [ques, opt1, opt2, opt3, opt4, ans, cmd, msg, cc, code]
    return render_template('user/admin/question.html', data=data, li=li)


@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():

    password=''
    cpass=''
    npass=''
    msg=''
    if request.method == 'POST':
        sno=session['id']
        data=Login.query.filter_by(sno=sno).first()
        password=request.form.get('pass')
        npass=request.form.get('npass')
        cpass=request.form.get('cpass')
        if password!=data.password:
            msg="Invalid password"
        elif cpass!=npass:
            msg="Password do not match"
        else:
            data.password=npass
            db.session.commit()
            password = ''
            cpass = ''
            npass = ''
            msg="Password changed successfully"


    li=[password,npass,cpass,msg]
    return render_template('user/admin/change_pass.html',li=li)

@app.route('/student')
def student():

    return render_template('user/student/index.html')


@app.route('/stu_profile', methods=['GET', 'POST'])
def stu_profile():
    name = ""
    email = ""
    cno = ""
    add=""
    img=""
    msg=""
    fname=""
    if request.method == 'POST':

        sno=session['id']
        print(sno)
        data=Member.query.filter_by(sno=sno).first()
        name = request.form.get('name')
        email = request.form.get('email')
        cno = request.form.get('contact')
        add = request.form.get('add')

        file = request.files['image']
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1]

        if ext == ".png" or ext == ".jpeg" or ext == ".jpg":


                fname = secure_filename(str(int(data.sno) + 1) + ext)

                data.image=fname
                db.session.commit()

                file.save(os.path.join(app.config['dp_path'], fname))


        else:
            msg = "Please upload a valid image"

        data.name=name
        data.email=email
        data.contact=cno
        data.address=add
        data.image=fname
        db.session.commit()
        msg="Profile Updated successfully"

    else:
        sno = session['id']

        data = Member.query.filter_by(sno=sno).first()
        print(sno)
        name = data.name
        email = data.email
        cno = data.contact
        add = data.address
        fname=data.image



    li=[sno,name,email,cno,add,fname]

    return render_template('user/student/stu_profile.html',li=li)


@app.route('/stu_change_pass', methods=['GET', 'POST'])
def stu_change_pass():

    password=''
    cpass=''
    npass=''
    msg=''
    if request.method == 'POST':
        sno=session['id']
        data=Login.query.filter_by(sno=sno).first()
        password=request.form.get('pass')
        npass=request.form.get('npass')
        cpass=request.form.get('cpass')
        if password!=data.password:
            msg="Invalid password"
        elif cpass!=npass:
            msg="Password do not match"
        else:
            data.password=npass
            db.session.commit()
            password = ''
            cpass = ''
            npass = ''
            msg="Password changed successfully"


    li=[password,npass,cpass,msg]
    return render_template('user/student/change_pass.html',li=li)



@app.route('/stu_course/<string:cmd>,<string:code>', methods=['GET', 'POST'])
def stu_course(cmd,code):

    sno=session['id']
    cc = ''
    cn = ''
    mod = ''
    fee = ''
    dur = ''
    car = ''
    msg = ''
    if cmd=='0':
        data = Stu_course.query.filter_by(sno=sno).all()


    elif cmd=='1':
        data = Stu_course.query.filter_by(sno=sno,ccode=code).first()
        cc=code
        cn=data.cname
        fee=data.fee
        dur=data.duration
        car=data.career
        mod=data.module

    li=[cc,cn,fee,dur,mod,car,cmd]
    return render_template('user/student/course.html', li=li,data=data)

@app.route('/study/<string:code>', methods=['GET', 'POST'])
def study(code):
    session['code']=code
    if code=='OJ':
        return redirect('/java/0')
    elif code=='DBMS':
        return redirect('/dbms/0')

@app.route('/java/<string:cmd>', methods=['GET', 'POST'])
def java(cmd):
    if cmd=='0':
        return render_template('user/student/course/java/index.html')
    elif cmd=='1':
        return render_template('user/student/course/java/intro.html')
    elif cmd=='2':
        return render_template('user/student/course/java/syntax.html')
    elif cmd == '3':
        return render_template('user/student/course/java/variable.html')
    elif cmd == '4':
        return render_template('user/student/course/java/datatype.html')


@app.route('/dbms/<string:cmd>', methods=['GET', 'POST'])
def dbms(cmd):
    if cmd=='0':
        return render_template('user/student/course/java/index.html')

@app.route('/test/<string:code>', methods=['GET', 'POST'])
def test(code):

    if request.method == 'POST':
        ql = list(request.form.keys())
        questions = Questions.query.filter(Questions.sno.in_(ql)).all()
        print(questions)
        ca = 0
        wa = 0
        ua = 0
        for q in questions:
            if q.correct == request.form.get(str(q.sno)):
                ca = ca + 1
            elif request.form.get(str(q.sno)) == 'nil':
                ua = ua + 1
            else:
                wa = wa + 1
        result = ""
        total = 10 - ua - wa * .25
        percent = total * 10

        result = ""
        grade = ""
        attempted=ca+wa
        total = ca-wa*.25
        percent = total * 10
        if percent >= 90:
            grade = 'A'
        elif percent >= 80:
            grade = 'B'
        elif percent >= 70:
            grade = 'C'
        elif percent >= 60:
            grade = 'D'
        elif percent >= 50:
            grade = 'E'
        else:
            grade = 'F'

        if grade == 'F':
            result = 'FAIL'
        else:
            result = 'PASS'
        data = Course.query.filter_by(course_code=code).first();
        sql = Result(id=session['id'],attempted=attempted,total=total,correct=ca,wrong=wa,unanswered=ua,grade=grade,percent=percent,result=result,course_code=code,course_name=data.course_name)
        db.session.add(sql)
        db.session.commit()
        li = [ca, wa, ua, total, percent, grade, result]

        return render_template('user/student/result.html', li=li)




    elif code=='OJ':
        questions = Questions.query.filter_by(course=code).all()
        questions = random.sample(questions, k=10)

        return render_template('user/student/test.html',data=questions)

@app.route('/result/<string:cmd>,<string:sno>', methods=['GET', 'POST'])
def result(cmd,sno):
    id=session['id']
    code=''
    course=''
    total=''
    percent=''
    correct=''
    wrong=''
    res=''
    grade=''
    if cmd=='0':
        data = Result.query.filter_by(id=id).all()
    else:
        data = Result.query.filter_by(sno=sno).first()
        print(data)
        code=data.course_code
        course=data.course_name
        correct=data.correct
        wrong=data.wrong
        res=data.result
        grade=data.grade
        total=data.total

    li=[cmd,code,course,total,correct,wrong,res,grade]
    return render_template('user/student/test_results.html',data=data,li=li)

@app.route('/video/<string:code>', methods=['GET', 'POST'])
def video(code):
    session['code']=code
    if code=='OJ':
        return render_template('user/student/course/java/video.html')
    elif code=='c':
        return redirect ('c/0')


if __name__ == '__main__':
    app.run(debug=True)
