from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pm_user'
app.config['MYSQL_PASSWORD'] = 'your_password'  # Replace with your password
app.config['MYSQL_DB'] = 'project_management'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    cur.close()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        percentage = request.form['percentage']
        storage = request.form['storage']

        if not name:
            flash('Project name is required!', 'error')
            return redirect(url_for('add_project'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects (name, percentage_completed, storage_location) VALUES (%s, %s, %s)", (name, percentage, storage))
        mysql.connection.commit()
        cur.close()
        flash('Project added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_project.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
    project = cur.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        percentage = request.form['percentage']
        storage = request.form['storage']

        if not name:
            flash('Project name is required!', 'error')
            return redirect(url_for('edit_project', id=id))

        cur.execute("UPDATE projects SET name=%s, percentage_completed=%s, storage_location=%s WHERE id=%s", (name, percentage, storage, id))
        mysql.connection.commit()
        cur.close()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('index'))

    cur.close()
    return render_template('edit_project.html', project=project)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_project(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
