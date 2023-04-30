from flask import Flask, request, render_template, url_for, redirect
import os, sqlite3, base64
from io import BytesIO
from PIL import Image

conn = sqlite3.connect('database.db')
cur = conn.cursor()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/display')
def display():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT img FROM image')

    rows = c.fetchall()
    conn.close()
    
    images = []
    for row in rows:
        image_bytes = row[0]
        # Decompress the image bytes into a Pillow Image object
        img = Image.open(BytesIO(image_bytes))
        # Resize the image to a smaller size (e.g. 640x480)
        img = img.resize((500, 600))
        # Compress the image and encode it as a base64-encoded string
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=60)
        base64_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
        images.append(base64_encoded)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()    
    c.execute('SELECT id, bn, fl, hdate, r FROM data')

    rowss = c.fetchall()
    conn.close()

    data = []
    for row in rowss:
        row_dict = {
            'id': row[0],
            'bn': row[1],
            'fl': row[2],
            'hdate': row[3],
            'r': row[4]
        }
        data.append(row_dict)
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()    
    c.execute('SELECT t, k, tc, kc, q FROM quality')
    
    rows2 = c.fetchall()
    conn.close()

    quality = []
    for row in rows2:
        row_dict2 = {
            't': row[0],
            'k': row[1],
            'tc': row[2],
            'kc': row[3],
            'q': row[4]
        }
        quality.append(row_dict2)
    print(rows2)
    return render_template('display.html', images=images, data=data, quality=quality)

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        File = request.form['file']
        from detect import Start
        Start('static/'+File)
        
        # Store the image in the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        with open('static/result.jpg', 'rb') as f:
            img_data = BytesIO(f.read())
        c.execute('create table if not exists image(img BLOB)')
        c.execute("INSERT INTO image (img) VALUES (?)", (img_data.read(),))
        conn.commit()
        conn.close()

        return render_template('check.html', image1='static/'+File, image2='static/result.jpg')
    return render_template('check.html')

@app.route('/submit', methods=['POST'])
def submit():
    id = request.form['id']
    bn = request.form['bn']
    fl = request.form['fl']
    hdate = request.form['hdate']
    r = request.form['r']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO data (id, bn, fl, hdate, r) VALUES (?, ?, ?, ?, ?)", (id, bn, fl, hdate, r))
    
    conn.commit()
    conn.close()

    return redirect(url_for('display'))

@app.route('/select', methods=['POST','GET'])
def select():
    return render_template('select.html')

@app.route('/soln')
def soln():
    return render_template('soln.html')

@app.route('/adul')
def adul():
    return render_template('adul.html')

@app.route('/siu')
def siu():
    return render_template('siu.html')

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    if request.method == 'POST':
        File = request.form['file']
        File = File.replace('http://127.0.0.1:5000/', '')
        print(File)
        from detect import Start
        Start(File)
        
        return render_template('select.html', output_image="http://127.0.0.1:5000/static/result.jpg", inputImage='http://127.0.0.1:5000/'+File)

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    return render_template('select2.html')

conn.commit()
conn.close()

if __name__ == "__main__":
    app.run(debug=True)