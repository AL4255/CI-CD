

# Vulnerbale-web app 
from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# Create vulnerable database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'user', 'userpass', 'user@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'guest', 'guest123', 'guest@example.com')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <html>
    <head><title>Vulnerable Security Testing App</title></head>
    <body>
        <h1>🔓 Vulnerable Web Application</h1>
        <p>This application contains intentional security vulnerabilities for testing purposes.</p>
        <h2>Test Areas:</h2>
        <ul>
            <li><a href="/login">🔑 Login (SQL Injection)</a></li>
            <li><a href="/search">🔍 Search (XSS Vulnerability)</a></li>
            <li><a href="/file?file=default.txt">📁 File Access (Path Traversal)</a></li>
        </ul>
        <hr>
        <p><strong>Security Scanner Target:</strong> This app is designed to be scanned by OWASP ZAP</p>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABILITY: SQL Injection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Executing query: {query}")  # For demonstration
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return f'''
            <h1>✅ Login Successful!</h1>
            <p>Welcome {user[1]}!</p>
            <p>Email: {user[3]}</p>
            <a href="/">← Back to Home</a>
            '''
        else:
            return '''
            <h1>❌ Login Failed</h1>
            <p>Invalid credentials</p>
            <a href="/login">← Try Again</a>
            '''
    
    return '''
    <html>
    <head><title>Login</title></head>
    <body>
        <h1>🔑 Login Form</h1>
        <form method="post">
            <p><input type="text" name="username" placeholder="Username" required></p>
            <p><input type="password" name="password" placeholder="Password" required></p>
            <p><button type="submit">Login</button></p>
        </form>
        <hr>
        <h3>💡 Test SQL Injection:</h3>
        <p>Try username: <code>admin' OR '1'='1' --</code></p>
        <p>Try password: <code>anything</code></p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    if query:
        # VULNERABILITY: XSS (Cross-Site Scripting)
        return f'''
        <html>
        <head><title>Search Results</title></head>
        <body>
            <h1>🔍 Search Results</h1>
            <p>You searched for: {query}</p>
            <p>No users found matching your search.</p>
            <hr>
            <a href="/search">← New Search</a> | <a href="/">← Home</a>
        </body>
        </html>
        '''
    
    return '''
    <html>
    <head><title>User Search</title></head>
    <body>
        <h1>🔍 User Search</h1>
        <form method="get">
            <p><input type="text" name="q" placeholder="Search users..."></p>
            <p><button type="submit">Search</button></p>
        </form>
        <hr>
        <h3>💡 Test XSS Attack:</h3>
        <p>Try searching: <code>&lt;script&gt;alert('XSS Attack!')&lt;/script&gt;</code></p>
        <p>Try searching: <code>&lt;img src=x onerror=alert('XSS')&gt;</code></p>
        <a href="/">← Back to Home</a>
    </body>
    </html>
    '''

@app.route('/file')
def file_read():
    filename = request.args.get('file', 'default.txt')
    
    try:
        # VULNERABILITY: Path Traversal
        with open(filename, 'r') as f:
            content = f.read()
        return f'''
        <html>
        <head><title>File Viewer</title></head>
        <body>
            <h1>📁 File: {filename}</h1>
            <pre>{content}</pre>
            <hr>
            <a href="/file?file=default.txt">← Default File</a> | <a href="/">← Home</a>
        </body>
        </html>
        '''
    except Exception as e:
        return f'''
        <html>
        <head><title>File Error</title></head>
        <body>
            <h1>❌ File Error</h1>
            <p>Could not read file: {filename}</p>
            <p>Error: {str(e)}</p>
            <hr>
            <h3>💡 Test Path Traversal:</h3>
            <p>Try: <code>/file?file=../../../etc/passwd</code></p>
            <p>Try: <code>/file?file=../../../../etc/hosts</code></p>
            <a href="/">← Back to Home</a>
        </body>
        </html>
        '''

@app.route('/health')
def health():
    return {'status': 'healthy', 'vulnerabilities': ['sql_injection', 'xss', 'path_traversal']}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
