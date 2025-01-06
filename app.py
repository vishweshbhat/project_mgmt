from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'proj_user'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'your_password'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'proj_mgmt_db'  # Your database name

mysql = MySQL(app)

# Home route - to display the project management page
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects")
    projects = cur.fetchall()
    return render_template('index.html', projects=projects)

# Add project route
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        storage_location = request.form['storage_location']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects(name, description, status, storage_location) VALUES (%s, %s, %s, %s)",
                    (name, description, status, storage_location))
        mysql.connection.commit()
        return redirect('/')
    
    return render_template('add_proj.html')

# Edit project route (edit status)
@app.route('/update_status/<int:id>', methods=['GET', 'POST'])
def update_status(id):
    if request.method == 'POST':
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE projects SET status = %s WHERE id = %s", (status, id))
        mysql.connection.commit()
        return redirect('/')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
    project = cur.fetchone()
    return render_template('edit_proj.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
