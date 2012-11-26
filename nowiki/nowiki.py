import sys, os, os.path
if __name__ == '__main__':
    #TODO: better option handling
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="config_file",
            help="Path to config file", metavar="FILE", default="nowiki.cfg")
    parser.add_option("-v", "--virtual-env", dest="virtualenv_path",
            help="Path to your virtualenv", metavar="DIR")
    (options, args) = parser.parse_args()
    if options.virtualenv_path:
        print 'entering ve'
        activate = os.path.join(options.virtualenv_path, 'bin/activate_this.py')
        execfile(activate, dict(__file__=activate))


from ConfigParser import SafeConfigParser
from StringIO import StringIO

from flask import Flask, abort, jsonify, render_template, request, Response
from nowikilib.page import Page
#from nowikilib import page
app = Flask(__name__, template_folder='views')
config = SafeConfigParser()
#set default configuration
config.readfp(StringIO('''
[nowiki]
datapath=data

[daemon]
debug=0
port=5000
host=127.0.0.1
page_get=1
    '''))

@app.route("/")
def get_home_html():
    #TODO: cache
    return render_template('index.src.htm', allpages = Page.get_all())


#TODO: move to a blueprint
@app.route("/page/")
def get_pages():
    return jsonify(Page.get_all())

@app.route("/page/<name>")
def get_page(name):
    if not config.getboolean('daemon', 'page_get'):
        abort(405)
    try:
        return Response(Page.get(name), mimetype='text/plain')
    except ValueError:
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


if __name__ == '__main__':
    import os
    ownpath = os.path.abspath(os.path.join(os.getcwd(),\
            os.path.dirname(sys.argv[0])))
    print 'chdirring to', ownpath
    os.chdir(ownpath)
    print os.listdir(os.getcwd())
    sys.argv[0] = 'nowiki.py'
    config.read(options.config_file)
    Page.config(config.get('nowiki', 'datapath'))
    app.debug = config.get('daemon', 'debug')
    app.run(port=config.getint('daemon', 'port'),\
            host=config.get('daemon', 'host'))

