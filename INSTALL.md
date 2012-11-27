# Install

## Debian

    apt-get install python python-pip python-virtualenv
    adduser nowiki
    cd /opt
    git clone git://github.com/boyska/nowiki.git
    mv nowiki/nowiki/data /var/nowiki
    chown root:root nowiki -R
    chown root:nowiki nowiki
    chmod ugo-w nowiki -R
    chmod go-rwx nowiki -R
    chmod g+rwx nowiki
    chown nowiki:www-data /var/nowiki -R
    chmod g-w /var/nowiki -R
    chmod g+rX /var/nowiki -R
    chmod o-rwx /var/nowiki -R
    cp nowiki/nowiki/nowiki.example.cfg /etc/nowiki.cfg
    chown root. /etc/nowiki.cfg
    chmod go-wx /etc/nowiki.cfg

    cd nowiki
    sudo -u nowiki bash
    virtualenv nowiki_ve
    source nowiki_ve/bin/activate
    pip bundle nowiki.pybundle -r requirements.txt
    pip install nowiki.pybundle
    deactivate
    exit

    cp /opt/nowiki/contrib/debian.nowiki.init /etc/init.d/nowiki
    chmod +x /etc/init.d/nowiki

    # edit /etc/init.d/nowiki and /etc/nowiki.cfg as needed

	service nowiki start
