"""
The "Module" class represents a collection of intents
"""

import pkgutil
import inspect
import traceback

import settings, log

#container to hold a list of modules loaded
module_lib = None


class Module(object):

    def __init__(self,
                 name,
                 intent=[],
                 user=[],
                 enabled=True):

        # Make a unique module name
        self.name = name

        # intent objects that perform an action
        self.intents = intent

        # the user with permission to use intent
        self.user = user

        # True if the mod is enabled
        self.enabled = enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True





def find_mods():
    """ Find and import modules from the module directories """
    global mod_lib
    mod_lib = []
    log.debug('Looking for modules in: '+str(settings.MOD_DIRS))
    for finder, name, _ in pkgutil.iter_modules(settings.MOD_DIRS):
        try:
            mod = finder.find_module(name).load_module(name)
            for member in dir(mod):
                obj = getattr(mod, member)
                if inspect.isclass(obj):
                    for parent in obj.__bases__:
                        if 'Module' is parent.__name__:
                            mod_lib.append(obj())
        except Exception as e:
            print(traceback.format_exc())
            log.error('Error loading \''+name+'\' '+str(e))


def list_mods():
    """ Print modules in order """
    global mod_lib
    log.info('Module List: '+str([mod.name for mod in mod_lib])[1:-1])

def list_enabled_mods():
    """ Print modules in order that are enabled and active """
    global mod_lib
    log.info('Enabled Modules: '+str([mod.name for mod in mod_lib if mod.enabled])[1:-1])


def get_mod(name):
    """ Attempts to disable the specified mod """
    global mod_lib
    for mod in mod_lib:
        if name in mod.name:
            return mod
    return None


def disable_mod(name):
    """ Attempts to disable the specified mod """
    global mod_lib
    for mod in mod_lib:
        if name in mod.name:
            log.info('Disabling: '+name+'\n')
            mod.enabled = False


def enable_mod(name):
    """ Attempts to enable the specified mod """
    global mod_lib
    for mod in mod_lib:
        if name in mod.name:
            log.info('Enabling: '+name+'\n')
            mod.enabled = True
