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
        # Get form data safely using .get() method
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        storage_location = request.form.get('storage_location')
        location = request.form.get('location', 'default_value')  # Default value if location is missing

        # Debug: Print form data
        print(f"Received data - Name: {name}, Description: {description}, Status: {status}, Storage Location: {storage_location}, Location: {location}")

        # Validate required fields
        if not name or not description or not status or not storage_location:
            return "Missing required field", 400  # Return a response indicating the issue

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects(name, description, status, storage_location, location) VALUES (%s, %s, %s, %s, %s)",
                    (name, description, status, storage_location, location))
        mysql.connection.commit()

        return redirect('/')  # Redirect to home page after adding the project
    
    return render_template('add_proj.html')

#added the delete functionality
@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    # Use the MySQL connection from Flask-MySQLdb
    cur = mysql.connection.cursor()
    
    # Execute the delete query
    cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
    
    # Commit the changes and close the cursor
    mysql.connection.commit()
    cur.close()
    
    # Redirect to the home page after deleting
    return redirect('/')

# Edit project route (optional, based on your app's requirement)
@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    cur = mysql.connection.cursor()

    # Handle GET request to fetch project details
    if request.method == 'GET':
        cur.execute("SELECT * FROM projects WHERE id = %s", (id,))
        project = cur.fetchone()
        return render_template('edit_proj.html', project=project)

    # Handle POST request to update project details
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        status = request.form.get('status')
        storage_location = request.form.get('storage_location')
        location = request.form.get('location', 'default_value')  # Default value if location is missing

        cur.execute("UPDATE projects SET name = %s, description = %s, status = %s, storage_location = %s, location = %s WHERE id = %s",
                    (name, description, status, storage_location, location, id))
        mysql.connection.commit()

        return redirect('/')  # Redirect to home page after editing the project

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
