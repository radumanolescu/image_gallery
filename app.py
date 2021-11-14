# docs @ http://flask.pocoo.org/docs/1.0/quickstart/

from flask import Flask, jsonify, redirect, request, render_template
import image_list
import txt_db

app = Flask(__name__)


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

