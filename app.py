# docs @ http://flask.pocoo.org/docs/1.0/quickstart/

from flask import Flask, jsonify, redirect, request, render_template
import image_list
import txt_db

app = Flask(__name__)


# ---------- ---------- ---------- ---------- ---------- ----------

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # POST request
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json())  # parse as JSON
        return 'OK', 200

    # GET request (http://localhost:5000/hello)
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers


# ---------- ---------- ---------- ---------- ---------- ----------

@app.route('/r1106a_01', methods=['GET', 'POST'])
def m1106a_01():
    # GET request (http://localhost:5000/r1106a)
    return render_template('1106a.html', name=image_list.all_meta())
    # temporary code, obsolete


# ---------- ---------- ---------- ---------- ---------- ----------
@app.route('/r1106a', methods=['GET', 'POST'])
def m1106a():
    # GET request (http://localhost:5000/r1106a)
    items_list = [{'1': 'Hello', '2': 'World', '3': {'link': '#', 'text': 'Open'}},
                  {'1': 'World', '2': 'Hello', '3': {'link': '#', 'text': 'Open'}}]
    return render_template('1106a.html', columns=['1', '2', '3'], items=items_list)
    # temporary code, obsolete


# ---------- ---------- ---------- ---------- ---------- ----------
@app.route('/r1107a', methods=['GET', 'POST'])
def m1107a():
    # GET request (http://localhost:5000/r1107a)
    cols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
            '19',
            '20', '21', '22']
    metadata = image_list.all_meta()
    return render_template('1107a.html', columns=cols, items=metadata)
    # temporary code, obsolete


# ---------- ---------- ---------- ---------- ---------- ----------
@app.route('/index', methods=['GET', 'POST'])
def show_index():
    # GET request (http://localhost:5000/index)
    flt_srt = request.form
    # ImmutableMultiDict([('filter1', 'Medium'), ('fv1', 'watercolor/liquid watercolor'), ('filter2', ''), ('sort1', ''), ('sort2', '')])
    filterby = {}
    for k, v in flt_srt.items():
        if k.startswith("filter") or k.startswith("fv"):
            filterby[k] = v
    sortby = []
    for k, v in flt_srt.items():
        if k.startswith("sort"):
            sortby.append(v)
    headings = image_list.read_headings("MetadataTemplate.txt")
    cols = [str(i) for i in range(len(headings))]
    metadata = image_list.selected_meta(filterby, sortby) # all_meta()
    flt = txt_db.all_filter_col_names
    srt = txt_db.all_sort_col_names
    rng=txt_db.ranges()
    return render_template('index.html', columns=cols, headings=headings, items=metadata,
                           filter=flt, sort=srt, ranges=rng)


# ---------- ---------- ---------- ---------- ---------- ----------
@app.route('/edit_metadata', methods=['GET', 'POST'])
def edit_metadata():
    # GET request (http://localhost:5000/edit_metadata?image=IMG_7493.JPG)
    image_file = "static/images/" + request.args.get('image', type=str)
    meta_file = txt_db.meta_for(image_file)
    headings = image_list.metadata_headings(meta_file)
    metadata = image_list.metadata_indexed_values(meta_file)
    return render_template('edit_metadata.html', headings=headings, items=metadata)


# ---------- ---------- ---------- ---------- ---------- ----------
@app.route('/save_metadata', methods=['GET', 'POST'])
def save_metadata():
    # GET request (http://localhost:5000/save_metadata?image=IMG_7493.JPG)
    if request.method == 'POST':
        image_list.save_meta(request.form)
    return redirect('/index')


# ---------- ---------- ---------- ---------- ---------- ----------
# Code:
# C:\Users\Radu\-\projects\Python\image_gallery\*.py
# Templates:
# C:\Users\Radu\-\projects\Python\image_gallery\templates\*.html
# ---------- ---------- ---------- ---------- ---------- ----------
# conda activate web
# cd C:\Users\Radu\-\projects\Python\image_gallery
# (web) C:\Users\Radu\-\projects\Python\image_gallery>flask run

