
from os import path
import re

class aMSNLang(object):
    lang_keys = {}
    lang_dirs = []
    base_lang = 'en'
    lang_code = base_lang
    
    lineRe = re.compile('([^\s]*)\s*(.*)')  # key + whitespace + value
    langRe = re.compile('(.+)-.+')          # code or code-variant
    
    @staticmethod
    def loadLang(lang_code, force_reload=False):
        if aMSNLang.lang_code is lang_code and force_reload is False:
            # Don't reload the same lang unless forced.
            return
        
        hasVariant = bool(aMSNLang.langRe.match(lang_code) is not None)
        
        # Check for lang variants.
        if hasVariant is True:
            root = str(aMSNLang.langRe.split(lang_code)[1])
        else:
            root = str(lang_code)
        
        if lang_code is aMSNLang.base_lang:
            # Clear the keys if we're loading the base lang.
            aMSNLang.clearKeys()
        
        if root is not aMSNLang.base_lang:
            # If it's not the default lang, load the base first.
            aMSNLang.loadLang(aMSNLang.base_lang)
        
        if hasVariant is True:
            # Then we have a variant, so load the root.
            aMSNLang.loadLang(root)
        
        # Load the langfile from each langdir.
        fileWasLoaded = False
        for dir in aMSNLang.getLangDirs():
            try:
                f = file(path.join(dir, 'lang' + lang_code), 'r')
                fileWasLoaded = True
            except IOError:
                # file doesn't exist.
                continue
            
            line = f.readline()
            while line:
                if aMSNLang.lineRe.match(line) is not None:
                    components = aMSNLang.lineRe.split(line)
                    aMSNLang.setKey(str(components[1]), str(components[2]))
                
                # Get the next line...
                line = f.readline()
            
            f.close()
        
        # If we've loaded a lang file, set the new lang code.
        if fileWasLoaded is True:
            aMSNLang.lang_code = str(lang_code)
        
    @staticmethod
    def addLangDir(lang_dir):
        aMSNLang.lang_dirs.append(str(lang_dir))
        aMSNLang.reloadKeys()
    
    @staticmethod
    def removeLangDir(lang_dir):
        try:
            # Remove the lang_dir from the lang_dirs list, and reload keys.
            aMSNLang.lang_dirs.remove(str(lang_dir))
            aMSNLang.reloadKeys()
            return True
        except ValueError:
            # Dir not in list.
            return False
    
    @staticmethod
    def getLangDirs():
        # Return a copy for them to play with.
        return aMSNLang.lang_dirs[:]

    @staticmethod
    def clearLangDirs():
        aMSNLang.lang_dirs = []
        aMSNLang.clearKeys()

    @staticmethod
    def reloadKeys():
        aMSNLang.loadLang(aMSNLang.lang_code, True)

    @staticmethod
    def setKey(key, val):
        aMSNLang.lang_keys[str(key)] = str(val)
    
    @staticmethod
    def getKey(key, replacements=[]):
        try:
            r = str(aMSNLang.lang_keys[key])
        except KeyError:
            # Key doesn't exist.
            return str(key)
        
        # Perform any replacements necessary.
        if aMSNLang._isDict(replacements):
            # Replace from a dictionary.
            for key, val in replacements.iteritems():
                r = r.replace(str(key), str(val))
        else:
            # Replace each occurence of $i with an item from the replacements list.
            i = 1
            for replacement in replacements:
                r = r.replace('$' + str(i), replacement)
                i += 1
        
        return r
        
    @staticmethod
    def _isDict(test):
        try:
            test.keys()
            return True
        except AttributeError:
            return False
    
    @staticmethod
    def clearKeys():
        aMSNLang.lang_keys = {}
    
    @staticmethod
    def printKeys():
        print aMSNLang.lang_code
        print '{'
        for key, val in aMSNLang.lang_keys.iteritems():
            print "\t[" + key + '] =>' + "\t" + '\'' + val + '\''
        print '}'

lang = aMSNLang()
