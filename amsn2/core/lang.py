
from os import path
import re

class aMSNLang(object):
    lang_keys = {}
    lang_dirs = []
    base_lang = 'en'
    lang_code = base_lang

    default_encoding = 'utf-8'

    lineRe  = re.compile('\s*([^\s]+)\s+(.+)', re.UNICODE)  # whitespace? + key + whitespace + value
    langRe  = re.compile('(.+)-.+', re.UNICODE)             # code or code-variant

    def loadLang(self, lang_code, force_reload=False):
        if self.lang_code is lang_code and force_reload is False:
            # Don't reload the same lang unless forced.
            return

        hasVariant = bool(self.langRe.match(lang_code) is not None)

        # Check for lang variants.
        if hasVariant is True:
            root = str(self.langRe.split(lang_code)[1])
        else:
            root = str(lang_code)

        if lang_code is self.base_lang:
            # Clear the keys if we're loading the base lang.
            self.clearKeys()

        if root is not self.base_lang:
            # If it's not the default lang, load the base first.
            self.loadLang(self.base_lang)

        if hasVariant is True:
            # Then we have a variant, so load the root.
            self.loadLang(root)

        # Load the langfile from each langdir.
        fileWasLoaded = False
        for dir in self.getLangDirs():
            try:
                f = file(path.join(dir, 'lang' + lang_code), 'r')
                fileWasLoaded = True
            except IOError:
                # file doesn't exist.
                continue

            line = f.readline()
            while line:
                if self.lineRe.match(line) is not None:
                    components = self.lineRe.split(line)
                    self.setKey(unicode(components[1], self.default_encoding), unicode(components[2], self.default_encoding))

                # Get the next line...
                line = f.readline()

            f.close()

        # If we've loaded a lang file, set the new lang code.
        if fileWasLoaded is True:
            self.lang_code = str(lang_code)

    def addLangDir(self, lang_dir):
        self.lang_dirs.append(str(lang_dir))
        self.reloadKeys()

    def removeLangDir(self, lang_dir):
        try:
            # Remove the lang_dir from the lang_dirs list, and reload keys.
            self.lang_dirs.remove(str(lang_dir))
            self.reloadKeys()
            return True
        except ValueError:
            # Dir not in list.
            return False

    def getLangDirs(self):
        # Return a copy for them to play with.
        return self.lang_dirs[:]

    def clearLangDirs(self):
        self.lang_dirs = []
        self.clearKeys()

    def reloadKeys(self):
        self.loadLang(self.lang_code, True)

    def setKey(self, key, val):
        self.lang_keys[key] = val

    def getKey(self, key, replacements=[]):
        try:
            r = self.lang_keys[key]
        except KeyError:
            # Key doesn't exist.
            return key

        # Perform any replacements necessary.
        if self._isDict(replacements):
            # Replace from a dictionary.
            for key, val in replacements.iteritems():
                r = r.replace(key, val)
        else:
            # Replace each occurence of $i with an item from the replacements list.
            i = 1
            for replacement in replacements:
                r = r.replace('$' + str(i), replacement)
                i += 1

        return r

    def _isDict(self, test):
        try:
            test.keys()
            return True
        except AttributeError:
            return False

    def clearKeys(self):
        self.lang_keys = {}

    def printKeys(self):
        print self.lang_code
        print '{'
        for key, val in self.lang_keys.iteritems():
            print "\t[" + key + '] =>' + "\t" + '\'' + val + '\''
        print '}'

lang = aMSNLang()
