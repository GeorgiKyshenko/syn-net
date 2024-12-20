from flask import Flask, redirect, render_template_string, render_template, url_for, abort
import nbformat
from nbconvert import HTMLExporter

app = Flask(__name__)

class Notebook:
    def __init__(self, title, file):
        self.title = title
        self.file = file
        self.is_open = "opened"
        
notebooks = [Notebook("Simple Neural Network", "Simple-Neural-Network.ipynb")]
    
    
def render_notebook(file_name):
    notebook_path = "./notebooks/" + file_name
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)
            
        html_exporter = HTMLExporter()
        html_exporter.exclude_input = False 
        html_exporter.exclude_output = False 
        body, _ = html_exporter.from_notebook_node(notebook_content)
        return render_template_string(body)
    except:
        return ""

@app.route("/")
def default_route():
  return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/math")
def math():
    return render_template("math.html")

@app.route("/ai")
def ai():
    return render_template("ai.html", notebooks=notebooks)

@app.route("/notebook/<file>/<open>")
def notebook(file, open):
    notebook_content = render_notebook(file)
    if notebook_content:
         return render_template("notebook.html", notebook_content=notebook_content, open=open)
    else:
        abort(404)

@app.route("/close")
def close_dialog():
    return redirect(url_for("ai"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run() 
  

