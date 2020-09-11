from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect

from logic import FileInformation

app =  Flask(__name__)

def allowed_filetype(filename):
    if not '.' in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    return ext.upper() == 'CSV'

@app.route("/")
@app.route("/home", methods = ["GET", "POST"])
def home():
    try:
        if request.method == "POST":

            if request.files:
                file = request.files["file"]

                if file.filename == "":
                    print("No filename")

                if allowed_filetype(file.filename):
                    filename = secure_filename(file.filename)
                    print("File saved")

                return redirect(request.url)

        return render_template('home.html')

    except Exception as e:
        return str(e)

@app.route("/results", methods=['POST'])
def results():
    file = request.files['inputFile']
    file_info = FileInformation(file, 'calibration.txt')
    return render_template('results.html', title = 'results', data = file_info.get_info())

if __name__ == '__main__':
    app.run(debug=True)
