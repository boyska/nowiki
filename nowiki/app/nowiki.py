import sys

from flask import Flask, abort, jsonify, render_template, request
sys.path.append('..')
from nowikilib.page import Page
#from nowikilib import page
app = Flask(__name__, template_folder='../views')

@app.route("/")
def get_home_html():
    #TODO: cache
    return render_template('index.src.htm', allpages = Page.get_all())


#TODO: move to Pluggable Views (http://flask.pocoo.org/docs/views/ )
@app.route("/page/")
def get_pages():
    return jsonify(Page.get_all())
@app.route("/page/<name>")
def get_page(name):
    try:
        return Page.get(name)
    except:
        abort(404)

@app.route("/page/<name>", methods=['DELETE'])
def delete_page(name):
    if not Page.exists(name):
        abort(404)
    Page.delete(name)
    return 'ok'
    
@app.route("/page/<name>", methods=['PUT'])
def set_page(name):
    if not Page.exists(name):
        abort(404)
    content = request.form['content']
    #TODO: sanitize!
    Page.set(name, content)
    return 'ok'


@app.route("/page/", methods=['POST'])
def new_page():
    name = request.form['slug']
    if Page.exists(name):
        abort(405) #method not allowed
    content = request.form['content']
    page = Page(name, content)
    page.save()
    return 'ok'


Page.config('../data/') #TODO: fix this uglyness
if __name__ == '__main__':
    app.debug = True
    app.run()

