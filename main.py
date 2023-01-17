from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# Create Flask app and set secret key, should be hidden in production
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
  

# MySQL configuration, pass in your data
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'crud_web_app_db'

# Initialize MySQL connection
mysql = MySQL(app)  

def get_db_cursor():
    return mysql.connection.cursor()


# Render template for the main page and fetch all data from 'users' table
@app.route("/")
def index():
    cur = get_db_cursor()
    cur.execute("SELECT*FROM users")
    data = cur.fetchall()
    return render_template('index.html', students = data)


# Insert new record into `users` table
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = get_db_cursor()
        cur.execute("INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('index'))


# Delete a record from `users` table
@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = get_db_cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))


# Update existing record in `users` table
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = get_db_cursor()
        cur.execute("""
               UPDATE users
               SET name=%s, email=%s, phone=%s
               WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
