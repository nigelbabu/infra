'''A fabric fabfile. See available commands do::

    fab -l

You can specify host and username using --hosts and --user options
'''
from __future__ import with_statement
import os
import datetime
import urllib2

from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *

## =====================================
## AWS Specific
## =====================================

def fix_profile():
    '''(NOT WORKING) Fix up root profile on ec2 (o/w complaints about: err: stdin: is
    not a tty).
    '''
    text = '''if `tty -s`; then
    mesg n
fi
'''
    fn = '/root/.profile'
    comment(fn, '^mesg n', backup='')
    append(fn, text)


def move_directories_to_mnt():
    '''Move /var, /home to /mnt/root/XXX and fstab them in.

    NB: assume we run as root.
    
    NB: if you already have a service such as mysql of postgresql running
    you'll need to stop it.

    Inspired by http://developer.amazonwebservices.com/connect/entry.jspa?externalID=1663
    '''
    assert not exists('/mnt/root'), '/mnt/root already exists!'
    run('mkdir /mnt/root')
    dirs = [ 'var', 'home' ]
    for dir in dirs:
        # avoid possible problem with being in dir that is being moved
        with cd('/'):
            run('mv /%s /mnt/root' % dir)
            run('mkdir /%s' % dir)
            append('/mnt/root/%s /%s     none bind' % (dir, dir), '/etc/fstab',
                    use_sudo=False)
            run('mount /%s' % dir)


