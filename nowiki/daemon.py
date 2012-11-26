import sys, os
from optparse import OptionParser

if __name__ == '__main__':
    #TODO: better option handling
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

    ownpath = os.path.abspath(os.path.join(os.getcwd(),\
            os.path.dirname(sys.argv[0])))
    print 'chdirring to', ownpath
    os.chdir(ownpath)
    sys.argv[0] = os.path.basename(sys.argv[0])
    from nowiki import app, config, Page
    config.read(options.config_file)
    app.config.config = config
    Page.config(config)
    app.debug = config.get('daemon', 'debug')
    app.run(port=config.getint('daemon', 'port'),\
            host=config.get('daemon', 'host'))

