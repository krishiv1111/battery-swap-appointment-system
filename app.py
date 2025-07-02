from flask import Flask, render_template, request, redirect, session
import mysql.connector


app = Flask(__name__)
app.secret_key='1234'

# database connection

conn = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '1339',
    database = 'battery_swap'
)

cursor = conn.cursor(dictionary=True)

# homepage route
@app.route('/')
def home(): return render_template ('index.html')
 
# create user registration
@app.route('/register', methods = ['GET', 'POST'])
def register (): 
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password)
        )
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

# create login page
@app.route('/login', methods = ['GET', 'POST'])
def login () :
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s", (username, password)
        )
        user = cursor.fetchone()
        if user :
            session['user_id']=user['id']
            session['username']=user['username']
            return redirect('/dashboard')
        else :
            return "Invalid Credentials"
    return render_template('login.html')

# create logout page
@app.route('/logout')
def logout () :
    session.clear()
    return redirect('/')

# create dashboard
@app.route('/dashboard')
def dashboard () :
    if 'user_id' in session :
        return render_template ('dashboard.html', username = session['username'])
    else : return redirect('/login')

# appointment booking
@app.route('/book', methods = ['GET', 'POST'])
def book () :
    if 'user_id' not in session :
        return redirect ('/login')
    if request.method=='POST' :
        station = request.form['station']
        date = request.form['date']
        time = request.form['time']
        cursor.execute("INSERT INTO appointments (user_id, station, date, time, status) VALUES (%s, %s, %s, %s, %s)", (session['user_id'], station, date, time, 'booked'))
        conn.commit()
        return redirect ('/myappointments')  
    return render_template ('book.html')

# my appointments
@app.route('/myappointments')
def myappointments() :
    if 'user_id' not in session :
        return redirect ('/login')
    cursor.execute("SELECT * FROM appointments WHERE user_id = %s", (session['user_id'],))
    appointments = cursor.fetchall()
    return render_template ('myappointments.html', appointments= appointments, username = session['username'])

# admin 
@app.route('/admin')
def admin() :
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    return render_template('admin.html', appointments=appointments)

# admin status update
@app.route('/update_status/<int:appointment_id>', methods = ['GET', 'POST'])
def update_status(appointment_id):
    new_status= request.form['status']
    cursor.execute("UPDATE appointments SET status=%s WHERE booking_id=%s", (new_status, appointment_id))
    conn.commit()
    return redirect('/admin')

# admin login
@app.route('/adminlogin', methods=['GET', 'POST']) 
def adminlogin():
    if request.method=='POST' :
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s ", (username, password))
        admin=cursor.fetchone()
        if admin :
            session['admin_id'] = admin['admin_id']
            session['admin_username'] = admin['username']
            return redirect ('/admin')
        else :
            return "Invalid Credentials"
    return render_template ('adminlogin.html')

if __name__ == '__main__':
    app.run(debug=True)