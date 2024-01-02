from flask import Flask, jsonify, render_template, request, redirect, url_for, g
import pandas as pd
from flask_cors import CORS
import io
import config
import numpy as np

app = Flask(__name__)
CORS(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = config.database_connection()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

logged_in = False
logged_in_user = ''

@app.route('/')
def home():
    return render_template('main.html', logged_in=logged_in, logged_in_user=logged_in_user)

@app.route('/nightly', methods=['GET'])
def get_nightly_data():
    box_client = config.configure_box_auth()

    if box_client:
        folder_id = '235564814351'
        items = box_client.folder(folder_id).get_items()
        csv_file = next((item for item in items if item.name.endswith('.csv')), None)
        
        if csv_file:
            csv_content = csv_file.content()
            content_string_buffer = io.StringIO(csv_content.decode('utf-8'))
            df = pd.read_csv(content_string_buffer)
            first_two_columns = df.iloc[:, :2]
            filtered_data = first_two_columns[~first_two_columns.iloc[:, 1].isin(['NA', 'UNSTABLE'])]

            # Replace NaN values with None (which is JSON serializable)
            filtered_data.replace({np.nan: None}, inplace=True)

            # Transform the filtered data into a list of dictionaries
            service_data = []
            for index, row in filtered_data.iterrows():
                service_data.append({
                    'Service Name': row.iloc[0],  # Assuming the first column is Service Name
                    'Passed Tests %': row.iloc[1]  # Assuming the second column is Passed Tests %
                })

            return jsonify(service_data)  # Return the transformed data
        else:
            return jsonify([])  # If no CSV data found, return an empty array
    else:
        return jsonify({'error': 'INFO Unable to fetch data!'})

@app.route('/rel', methods=['GET'])
def get_rel_data():
    box_client = config.configure_box_auth()

    if box_client:
        folder_id = '235765926614'
        items = box_client.folder(folder_id).get_items()
        csv_file = next((item for item in items if item.name.endswith('.csv')), None)
        
        if csv_file:
            csv_content = csv_file.content()
            content_string_buffer = io.StringIO(csv_content.decode('utf-8'))
            df = pd.read_csv(content_string_buffer)
            first_two_columns = df.iloc[:, :2]
            filtered_data = first_two_columns[~first_two_columns.iloc[:, 1].isin(['NA', 'UNSTABLE'])]

            # Replace NaN values with None (which is JSON serializable)
            filtered_data.replace({np.nan: None}, inplace=True)

            # Transform the filtered data into a list of dictionaries
            service_data = []
            for index, row in filtered_data.iterrows():
                service_data.append({
                    'Service Name': row.iloc[0],  # Assuming the first column is Service Name
                    'Passed Tests %': row.iloc[1]  # Assuming the second column is Passed Tests %
                })

            return jsonify(service_data)  # Return the transformed data
        else:
            return jsonify([])  # If no CSV data found, return an empty array
    else:
        return jsonify({'error': 'INFO Unable to fetch data!'})

@app.route('/dev', methods=['GET'])
def get_dev_data():
    box_client = config.configure_box_auth()

    if box_client:
        folder_id = '235765206622'
        items = box_client.folder(folder_id).get_items()
        csv_file = next((item for item in items if item.name.endswith('.csv')), None)
        
        if csv_file:
            csv_content = csv_file.content()
            content_string_buffer = io.StringIO(csv_content.decode('utf-8'))
            df = pd.read_csv(content_string_buffer)
            first_two_columns = df.iloc[:, :2]
            filtered_data = first_two_columns[~first_two_columns.iloc[:, 1].isin(['NA', 'UNSTABLE'])]

            # Replace NaN values with None (which is JSON serializable)
            filtered_data.replace({np.nan: None}, inplace=True)

            # Transform the filtered data into a list of dictionaries
            service_data = []
            for index, row in filtered_data.iterrows():
                service_data.append({
                    'Service Name': row.iloc[0],  # Assuming the first column is Service Name
                    'Passed Tests %': row.iloc[1]  # Assuming the second column is Passed Tests %
                })

            return jsonify(service_data)  # Return the transformed data
        else:
            return jsonify([])  # If no CSV data found, return an empty array
    else:
        return jsonify({'error': 'INFO Unable to fetch data!'})
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged_in, logged_in_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cur = db.cursor()

        # Check user credentials against the database
        cur.execute("SELECT username FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        
        if user:
            logged_in = True
            logged_in_user = user[0]
            cur.close()  # Close the cursor
            return redirect(url_for('home'))
        else:
            cur.close()  # Close the cursor
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    global logged_in, logged_in_user
    logged_in = False
    logged_in_user = ''
    return redirect(url_for('login'))

if __name__ == '__main__':
    # app.run(host='sec-isc-infra-jenkins.swg-devops.com',debug=True)
    app.run(host='0.0.0.0',port=80,debug=True)
