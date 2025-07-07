# simple_user_app/app.py
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple User App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background-color: #e0f7fa; text-align: center; }
            h1 { color: #007bb6; }
            p { color: #333; }
            .container { max-width: 600px; margin: auto; padding: 30px; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            a { color: #007bb6; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗂️ File Manager</h1>
            <p>Welcome to the Simple User Application!</p>
            <p>This is content visible to general users with the <strong>user</strong> role.</p>
            <p>Here you could manage your files, view documents, and perform user-level operations.</p>
            <hr>
            <p>You can go back to the <a href="http://localhost:8000/portal">Portal</a>.</p>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
