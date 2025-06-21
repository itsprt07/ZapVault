import pytz
IST = pytz.timezone('Asia/Kolkata')

def render_home(message='', form='login'):
    password_hint = '''
        <small style="color: #ddd; font-size: 12px;">
            Password must be at least 8 characters, lowercase letters (a-z), and digits (0–9) only.
        </small><br>
    ''' if form == 'signup' else ''

    token_input = '''
        <input type="text" name="token" placeholder="6-digit Token" required><br>
    ''' if form == 'login' else ''

    return f'''
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <title>ZapVault 🔐</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <h1>ZapVault 🔐</h1>
        <p class="subtitle">Secure. Self-destructing. Hassle-free file sharing ⚡</p>

        <div class="form-container">
            <div class="msg">{message}</div>
            <h2>{'🔓 Login' if form == 'login' else '📝 Signup'}</h2>
            <form method="POST">
                <input type="email" name="email" placeholder="Email" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                {token_input}
                {password_hint}
                <button type="submit" name="{form}">{'Login' if form == 'login' else 'Signup'}</button>
            </form>

            <div class="toggle">
                {("Don't have an account? <a href='/?form=signup'>Sign up</a>" 
                if form == 'login' else "Already have an account? <a href='/?form=login'>Log in</a>")}
            </div>
        </div>
    </body>
    </html>
    '''
