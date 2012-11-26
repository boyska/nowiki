def check_db(app, fix):
    if not Page.db.check_sanity(fix):
        print 'Errors detected in data dir%s' % ("...fixed" if fix else "")
        if not fix:
            return 1
    return 0

import sys, os
from optparse import OptionParser

if __name__ == '__main__':
    #TODO: better option handling
    parser = OptionParser()
    parser.add_option("-c", "--config-file", dest="config_file",
            help="Path to config file", metavar="FILE", default="nowiki.cfg")
    parser.add_option("-v", "--virtual-env", dest="virtualenv_path",
            help="Path to your virtualenv", metavar="DIR")

    parser.add_option("--check-db", action="store_true", dest="check_db",
            help="Check for permission problems on the db")
    parser.add_option("--fix", action="store_true", dest="fix",
            help="Fix the problems, not only check for them")
    (options, args) = parser.parse_args()
    if options.virtualenv_path:
        activate = os.path.join(options.virtualenv_path, 'bin/activate_this.py')
        execfile(activate, dict(__file__=activate))

    ownpath = os.path.abspath(os.path.join(os.getcwd(),\
            os.path.dirname(sys.argv[0])))
    os.chdir(ownpath)
    sys.argv[0] = os.path.basename(sys.argv[0])

    from nowiki import app, config, Page
    config.read(options.config_file)
    app.config.config = config
    Page.config(config)

    if options.check_db:
        sys.exit(check_db(app, options.fix))
