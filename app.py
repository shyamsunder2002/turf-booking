from flask import Flask, render_template, request, redirect, session, flash
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

@app.route('/')
def index():
    db = get_db()
    turfs = db.execute("SELECT * FROM turfs WHERE available=1").fetchall()
    db.close()
    return render_template('index.html', turfs=turfs)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            flash('Registered! Please login.', 'success')
            return redirect('/login')
        except:
            flash('Username already exists.', 'danger')
        finally:
            db.close()
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        # INTENTIONALLY VULNERABLE - SQL Injection possible here
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user = db.execute(query).fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/dashboard')
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    bookings = db.execute('''
        SELECT b.*, t.name, t.location FROM bookings b
        JOIN turfs t ON b.turf_id = t.id
        WHERE b.user_id = ?
    ''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('dashboard.html', bookings=bookings)

@app.route('/book/<int:turf_id>', methods=['GET','POST'])
def book(turf_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    turf = db.execute("SELECT * FROM turfs WHERE id=?", (turf_id,)).fetchone()
    if request.method == 'POST':
        date = request.form['date']
        start = request.form['start_time']
        end = request.form['end_time']
        db.execute("INSERT INTO bookings (user_id, turf_id, date, start_time, end_time) VALUES (?,?,?,?,?)",
                   (session['user_id'], turf_id, date, start, end))
        db.commit()
        db.close()
        flash('Booking confirmed!', 'success')
        return redirect('/dashboard')
    db.close()
    return render_template('book.html', turf=turf)

@app.route('/cancel/<int:booking_id>')
def cancel(booking_id):
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    db.execute("DELETE FROM bookings WHERE id=? AND user_id=?", (booking_id, session['user_id']))
    db.commit()
    db.close()
    flash('Booking cancelled.', 'info')
    return redirect('/dashboard')

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect('/')
    db = get_db()
    turfs = db.execute("SELECT * FROM turfs").fetchall()
    bookings = db.execute('''
        SELECT b.*, t.name AS turf_name, u.username FROM bookings b
        JOIN turfs t ON b.turf_id = t.id
        JOIN users u ON b.user_id = u.id
    ''').fetchall()
    db.close()
    return render_template('admin.html', turfs=turfs, bookings=bookings)

@app.route('/admin/add-turf', methods=['POST'])
def add_turf():
    if session.get('role') != 'admin':
        return redirect('/')
    name = request.form['name']
    location = request.form['location']
    price = request.form['price']
    db = get_db()
    db.execute("INSERT INTO turfs (name, location, price_per_hour) VALUES (?,?,?)", (name, location, price))
    db.commit()
    db.close()
    return redirect('/admin')

@app.route('/admin/delete-turf/<int:turf_id>')
def delete_turf(turf_id):
    if session.get('role') != 'admin':
        return redirect('/')
    db = get_db()
    db.execute("DELETE FROM turfs WHERE id=?", (turf_id,))
    db.commit()
    db.close()
    return redirect('/admin')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)