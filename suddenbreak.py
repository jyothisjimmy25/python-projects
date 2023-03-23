import random

from flask import Flask, render_template, request, redirect, session
from DBConnection import Db

app = Flask(__name__)
app.secret_key="hi"
static_path="E:\\project\\dead_duck\\static\\"

@app.route('/',methods=['get','post'])
def hello():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        print(username,password)
        db=Db()
        res=db.selectOne("select * from login where username='"+username+"' and password='"+password+"'")
        if res is None:
            return "<script>alert('Invalid details');window.location='/'</script>"
        else:
            type=res['usertype']
            if type=="admin":
                return redirect('/admin_home')
            elif type=="department":
                session['lid']=res['login_id']
                return redirect("/dept_home")
            else:
                return "<script>alert('Invalid user');window.location='/'</script>"
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin/Admin_home.html')


@app.route('/dept_add',methods=['get','post'])
def dept_add():
    if request.method=="POST":
        dept_name=request.form['textfield']
        email=request.form['textfield2']
        phone=request.form['textfield3']
        password=random.randint(1000, 9999)

        db=Db()
        lid=db.insert("insert into login(username, password, usertype) values('"+email+"','"+str(password)+"','department')")
        db.insert("INSERT INTO dept(dept_id, dept_name, email, phone_no) VALUES('"+str(lid)+"','"+dept_name+"','"+email+"','"+str(phone)+"')")
        return "<script>alert('Department added');window.location='/dept_add'</script>"
    else:
        return render_template('admin/Dept_add.html')

@app.route('/dept_view')
def dept_view():
    db=Db()
    res=db.select("select * from dept")
    return render_template('admin/Dept_view.html', data=res)

@app.route('/delete_dept/<id>')
def delete_dept(id):
    db = Db()
    res = db.delete("delete from login where login_id='"+id+"'")
    res = db.delete("delete from dept where dept_id='" + id + "'")
    return "<script>alert('deleted');window.location='/dept_view'</script>"

@app.route('/dept_update/<id>')
def dept_update(id):
    db = Db()
    res = db.selectOne("select * from dept where dept_id ='"+id+"' ")
    return render_template('admin/dept_update.html', data=res)

@app.route("/dept_update_post", methods=['post'])
def dept_update_post():
    dname=request.form['textfield']
    email=request.form['textfield2']
    id=request.form['hid']
    phone=request.form['textfield3']
    db = Db()
    res = db.update("update dept set dept_name='"+dname+"',email='"+email+"',phone_no='"+phone+"'  where dept_id='"+id+"'")
    return "<script>alert('updated');window.location='/dept_view'</script>"


@app.route('/view_user')
def view_user():
    db = Db()
    res = db.select("select * from user, login where login.login_id=user.user_id and login.usertype='user'")
    return render_template('admin/view_user.html', data=res)

@app.route('/approve_user/<id>')
def approve_user(id):
    db = Db()
    res = db.update("update login set usertype='user' where login_id='"+id+"'")
    return "<script>alert('Approved');window.location='/verify_user'</script>"

@app.route('/reject_user/<id>')
def reject_user(id):
    db = Db()
    res = db.delete("delete from login  where login_id='"+id+"'")
    res = db.delete("delete from user where user_id='"+id+"'")
    return "<script>alert('Rejected');window.location='/verify_user'</script>"


@app.route('/verify_user')
def verify_user():
    db = Db()
    res = db.select("select * from user, login where login.login_id=user.user_id and login.usertype='pending'")
    return render_template('admin/verify_user.html', data=res)

@app.route('/view_notification')
def view_notification():
    db = Db()
    res = db.select("select notification.*,dept.dept_name from notification, dept where notification.department_id = dept.dept_id")
    return render_template('admin/View_notification.html',data=res)

@app.route('/view_feedback')
def view_feedback():
    db = Db()
    res = db.select("select feedback.*,user.user_name from feedback,user where feedback.user_id=user.user_id")
    return render_template('admin/view_feedback.html',data=res)

@app.route('/change_password',methods=['get','post'])
def change_password():
    if request.method=="POST":
        cur_pass=request.form['textfield']
        new_pass=request.form['textfield2']
        db=Db()
        res=db.selectOne("select * from login where password='"+cur_pass+"' and usertype='admin'")
        if res is not None:
            db.update("update login set password='"+new_pass+"' where usertype='admin'")
            return "<script>alert('Password changed successfully');window.location='/change_password'</script>"
        else:
            return "<script>alert('Incorrect password');window.location='/change_password'</script>"
    return render_template('admin/change_pass.html')



@app.route('/dept_home')
def dept_home():
    return render_template('dept/Dept_home.html')

@app.route('/authority_reg',methods=['get','post'])
def authority_reg():
    if request.method=="POST":
        name=request.form['textfield']
        email=request.form['textfield2']
        phone_no=request.form['textfield3']
        image=request.files['filefield']
        password=random.randint(1000, 9999)
        image.save(static_path+"images\\"+image.filename)
        path="/static/images/"+image.filename
        dept_id=session['lid']
        db=Db()
        lid=db.insert("insert into login(username, password, usertype) values('"+email+"','"+str(password)+"','authority')")
        db.insert("INSERT INTO service_authority(authority_id, name, email, phone_no, image, dept_id) VALUES('"+str(lid)+"','"+name+"','"+email+"','"+str(phone_no)+"','"+path+"','"+str(dept_id)+"')")
        return "<script>alert('authority added');window.location='/authority_reg'</script>"
    else:
        return render_template("dept/authority_reg.html")


@app.route('/view_authority')
def view_authority():
    dept_id = session['lid']
    db = Db()
    res = db.select("select * from service_authority where dept_id ='"+str(dept_id)+"'")
    return render_template('dept/view_authority.html',data=res)

@app.route('/upd_authority_reg/<id>')
def upd_authority_reg(id):
    db = Db()
    res = db.selectOne("select * from  service_authority where authority_id ='" + id + "' ")
    return render_template('dept/upd_authority_reg.html', data=res)

@app.route("/upd_authority_reg_post", methods=['post'])
def upd_authority_reg_post():
    name=request.form['textfield']
    id=request.form['hid']
    phone=request.form['textfield3']
    db=Db()
    if 'filefield' in request.files:
        img=request.files['filefield']
        if img.filename!="":        #   has image
            img.save(static_path + "images\\" + img.filename)
            path = "/static/images/" + img.filename
            res = db.update(
                "update service_authority set name='" + name + "',image='" + path + "',phone_no='" + phone + "'  where authority_id='" + id + "'")
        else:                       #   browser issue
            res = db.update(
                "update service_authority set name='" + name + "',phone_no='" + phone + "'  where authority_id='" + id + "'")
    else:                           #   no image
        res = db.update(
            "update service_authority set name='" + name + "',phone_no='" + phone + "'  where authority_id='" + id + "'")


    return "<script>alert('updated');window.location='/view_authority'</script>"

@app.route('/delete_authority/<id>')
def delete_authority(id):
    db = Db()
    res = db.delete("delete from login where login_id='"+id+"'")
    res = db.delete("delete from service_authority where authority_id='" + id + "'")
    return "<script>alert('deleted');window.location='/view_authority'</script>"

@app.route('/add_device/<id>')
def add_device(id):
    return render_template('dept/add_device.html', id=id)

@app.route('/add_device_post',methods=['post'])
def add_device_post():
    device_name=request.form['textfield']
    imei=request.form['textfield2']
    authority_id=request.form['hid']

    db=Db()
    db.insert("INSERT INTO device( device_name, imei, authority_id) VALUES('"+device_name+"','"+imei+"','"+authority_id+"')")
    return "<script>alert('Device added');window.location='/view_authority'</script>"


@app.route('/send_notifcation', methods=['get','post'])
def send_notifcation():
    if request.method == "POST":
    dept_name = request.form['textfield']
    email = request.form['textfield2']
    phone = request.form['textfield3']
    password = random.randint(1000, 9999)

            db = Db()
            lid = db.insert("insert into login(username, password, usertype) values('" + email + "','" + str(
                password) + "','department')")
            db.insert("INSERT INTO dept(dept_id, dept_name, email, phone_no) VALUES('" + str(
                lid) + "','" + dept_name + "','" + email + "','" + str(phone) + "')")
            return "<script>alert('Department added');window.location='/dept_add'</script>"
        else:
            return render_template('admin/Dept_add.html')

    return render_template('dept/send_notifcation.html')


@app.route('/view_post')
def view_post():
    db = Db()
    res = db.select("select post.*,user.user_name from post, user where post.user_id=user.user_id and post.status='forwarded to department'")
    return render_template('dept/view_post.html', data=res)


@app.route('/view_report')
def view_report():
    db = Db()
    res = db.select("select report.*,service_authority.name from report,service_authority where report.authority_id=service_authority.authority_id")
    return render_template('dept/view_report.html', data=res)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
