# admin_dashboard_app/app.py
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background-color: #ffebee; text-align: center; }
            h1 { color: #c62828; }
            p { color: #333; }
            .container { max-width: 600px; margin: auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .warning { background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #856404; margin: 20px 0; }
            a { color: #c62828; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Admin Dashboard</h1>
            <div class="warning">
                <strong>⚠️ RESTRICTED ACCESS</strong><br>
                This area contains sensitive administrative functions.
            </div>
            <p>Welcome to the Admin Dashboard!</p>
            <p>This is highly sensitive content for administrators only.</p>
            <p>Here you can manage users, configure system settings, and access administrative tools.</p>
            <p>Only users with the <strong>admin</strong> role can access this application.</p>
            <hr>
            <p>You can go back to the <a href="http://localhost:8000/app">Apps</a>.</p>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
