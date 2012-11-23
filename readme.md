## RaxAuth

A simple module to authenticate against the Rackspace Cloud Identity (Keystone).

Implementation is simple but still leaves a bit to be desired at the moment:

    >>> a = raxauth.auth('<username>', '<apikey>')
    >>> print a.getToken()['id']
    asdasdw2-fdds-asda-asda-asdadasdas

There are plenty of methods to return the data you're looking from from the service catalog as dictionaries.  Future updates will return nothing but pretty data -- the current results are functional but not very Pythonic.

*This module is extremely immature.*