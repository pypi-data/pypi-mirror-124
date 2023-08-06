#Beetroot, a general purpose library for all sorts of uses.

#Imports
import sys

from .exception import *

if not str(sys.version).startswith("3"):
    #HOW DARE YOU USE PYTHON2 IDIOT. or python4, if that ever exists
    raise VersionError("Python version is not supported.")

#More imports
import random as mrandom #Imported as mrandom to prevent conflicts
import os
import shutil
import platform
import getpass
import socket
import uuid
import time
import hashlib

try:
    import ujson as json
    
except (ModuleNotFoundError, ImportError):
    try:
        import simplejson as json
        
    except (ModuleNotFoundError, ImportError):
        import json
        
try:
    import pyttsx3
    
except (ModuleNotFoundError, ImportError):
    pass

from pathlib import Path as p
from .metadata import *

#Constants
gen = mrandom.SystemRandom()
sys.setrecursionlimit(2000)

def objtype(obj):
    return str(type(obj))[8:-2]

class rand:
    """Random class"""
    def randint(self, s, e):
        """Generates a (maybe) cryptographically secure number using random.SystemRandom.randint()"""
        global gen
        return gen.randint(s, e)

    def srandint(self, seed, s, e):
        """Generates a seeded randint like above.
        Note, this function is not cryptographically secure because of the fact
        that it has to be seeded, If you would
        like it to be secure, use beetroot.random.randint() instead."""
        mrandom.seed(seed)
        return mrandom.randint(s, e)
random = rand()
del rand

class sw:
    """Stopwatch thingy"""
    def __init__(self):
        self.st = 0
        self.et = 0
        
    def start(self):
        """Starts the stopwatch"""
        self.st = time.time()
        return 0
    
    def stop(self):
        """Stops the stopwatch and return the elapsed time in ms"""
        self.et = time.time()
        return round((self.et - self.st) * 1000)
stopwatch = sw()
del sw
    
class fil:
    """File Manipulation"""
    def move(self, start, end):
        """Moves files"""
        shutil.move(start, end)
        return 0

    def rename(self, orig, new):
        """Renames files, also kinda works to move files, and vice versa"""
        os.rename(p(orig), p(new))
        return 0

    def delete(self, fi, force=False):
        """Deletes files/folders"""
        fi = p(fi)
        if os.path.isdir(fi):
            shutil.rmtree(fi)
            
        elif os.path.isfile(fi):
            os.remove(fi)
            
        else:
            if force:
                try:
                    shutil.rmtree(fi)
                    
                except:
                    os.remove(fi)
                    
            else:
                return 1
            
        return 0
    
    def dump(self, fi, data):
        """Dumps data to a file"""
        with open(p(fi), "w") as f:
            f.write(data)
            f.close()
            
        return 0

    def bdump(self, fi, data):
        """Dumps binary (non-text) data to a file"""
        with open(p(fi), "wb") as f:
            try:
                inp = data.encode("iso-8859-1")
                f.write(inp)
                
            except AttributeError:
                try:
                    inp = data.decode("iso-8859-1")
                    inp = data.encode("iso-8859-1")
                    f.write(inp)
                    
                except AttributeError:
                    f.write(str(data).encode("iso-8859-1"))
                
            f.close()
            
        return 0
    
    def jdump(self, fi, data, pp=True):
        """Dumps a dict into a .json file in JSON format
        with pretty print so it doesn't hurt your eyes."""
        with open(p(fi), "w") as f:
            if objtype(pp) != "bool":
                f.close()
                raise InvalidPPBool("Argument \"pp\" must be bool")
            
            if pp:
                json.dump(data, f, indent=4)
                
            elif not pp:
                json.dump(data, f)
                
            else:
                raise UnknownError("¯\_(ツ)_/¯")
            
        return 0

    def load(self, fi):
        """Reads data from text files."""
        with open(p(fi), "r") as f:
            return f.read()
        
    def bload(self, fi):
        """Reads data from binary (non-text) files."""
        with open(p(fi), "rb") as f:
            return f.read()
        
    def jload(self, fi):
        """Reads data from JSON files."""
        with open(p(fi), "r") as f:
            return json.loads(f.read())
file = fil()
del fil

class ptx:
    """tts yay"""
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
        except (ModuleNotFoundError, ImportError):
            pass
        
    def say(self, str_):
        """Say something, Beetroot"""
        try:
            if objtype(str_) == "bytes":
                self.engine.say(str_.decode("iso-8859-1"))
                
            else:
                self.engine.say(str(str_))
                
            self.engine.runAndWait()
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beet.tts functions.")
    
    def changeRate(self, rate):
        """Say things faster/slower, Beetroot"""
        try:
            self.engine.setProperty("rate", int(round(float(rate))))
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beet.tts functions.")
        
        except ValueError:
            raise InvalidTypeError("Argument \"rate\" must be int or float")
        
    def changeVoice(self, voice):
        """Say things in different voices, Beetroot
        (you can even do different languages if you install them
        on windows, although I'm not sure how you do it on *nix
        cuz I don't have any *nix computers or VMs.)"""
        try:
            voices = self.engine.getProperty("voices")
            self.engine.setProperty("voice", voices[int(round(float(voice)))].id)
        
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions.")
        
        except IndexError:
            raise InvalidVoiceError("That voice id doesn't exist.")
        
        except ValueError:
            raise InvalidTypeError("Argument \"voice\" must be int or float")
        
    def changeVolume(self, volume):
        """Talk Louder/Quieter, Beetroot"""
        try:
            self.engine.setProperty("volume", float(voice))
            
        except (NameError, AttributeError):
            raise ModuleError("You need to install pyttsx3 to use beetroot.tts functions.")
        
        except ValueError:
            raise InvalidTypeError("Argument \"volume\" must be int or float")
tts = ptx()
del ptx
        
def strhash(str_, secure=True):
    """Hash Function that uses MD5 or SHA512."""
    
    if objtype(secure) != "bool":
        raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
    
    if secure:
        return hashlib.sha512(str(str_).encode("iso-8859-1")).hexdigest()
    
    elif not secure:
        return hashlib.md5(str(str_).encode("iso-8859-1")).hexdigest()
        
    else:
        raise UnknownError("¯\_(ツ)_/¯")
    
def strhash(str_, secure=True):
    """Hash Function that uses MD5 or SHA512."""
    
    if objtype(secure) != "bool":
        raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
    
    if objtype(b) != "bytes":
        raise InvalidHashTypeError("Argument \"str_\" can only be string or non-bytestring object")
    
    if secure:
        return hashlib.sha512(str(str_).encode("iso-8859-1")).hexdigest()
    
    elif not secure:
        return hashlib.md5(str(str_).encode("iso-8859-1")).hexdigest()
        
    else:
        raise UnknownError("¯\_(ツ)_/¯")
    
def bhash(b, secure=True):
    """Hash Function that uses MD5 or SHA512."""
    
    if objtype(secure) != "bool":
        raise InvalidHashSecurityValue("Argument \"secure\" can only be boolean")
    
    if objtype(b) != "bytes":
        raise InvalidHashTypeError("Argument \"b\" can only be bytestring")
    
    if secure:
        return hashlib.sha512(b).hexdigest()
    
    elif not secure:
        return hashlib.md5(b).hexdigest()
        
    else:
        raise UnknownError("¯\_(ツ)_/¯")
        
def test():
    """Test"""
    print("Hello, world!")
    
def quicksort(array):
    """Quicksort algorithm"""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        
        for x in array:
            if x < pivot:
                less.append(x)
                
            elif x == pivot:
                equal.append(x)
                
            elif x > pivot:
                greater.append(x)
                
        return quicksort(less) + equal + quicksort(greater)
    
    else:
        return array

def lsep(str_, sep=" "):
    """Seperates string str_ by seperator sep whilst avoiding all strings containing whitespace"""
    a = str_.split(sep)
    
    out = []
    for i in range(0, len(a)):
        if (not a[i].isspace()) and a[i] != "":
            out.append(a[i])
            
    return out



def execfile(file):
    """Executes a python .py script"""
    with open(p(file), "r") as f:
        exec(f.read())
        f.close()
        
    return 0

def systemstats():
    """Returns info about system and hardware"""
    return [getpass.getuser(), platform.system(), platform.version(), platform.machine(), platform.node(), socket.gethostbyname(socket.gethostname()), ':'.join(("%012X" % uuid.getnode())[i:i+2] for i in range(0, 12, 2)).lower()]

def unline(str_):
    """Makes multi-line strings single-line"""
    return str(str_).replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\a", "\\a").replace("\b", "\\b")

def reline(str_):
    """Reverses beetroot.unline()"""
    return str(str_).replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").replace("\\a", "\a").replace("\\b", "\b")

def beetroot():
    """BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT BEETROOT-"""
    while True:
        print("""

██████╗░███████╗███████╗████████╗██████╗░░█████╗░░█████╗░████████╗
██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
██████╦╝█████╗░░█████╗░░░░░██║░░░██████╔╝██║░░██║██║░░██║░░░██║░░░
██╔══██╗██╔══╝░░██╔══╝░░░░░██║░░░██╔══██╗██║░░██║██║░░██║░░░██║░░░
██████╦╝███████╗███████╗░░░██║░░░██║░░██║╚█████╔╝╚█████╔╝░░░██║░░░
╚═════╝░╚══════╝╚══════╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░░░░╚═╝░░░""", end="", flush=True)
        time.sleep(0.5)
            
if __name__.endswith("__main__"):
    #Just in case I need to do any tests or smth idk
    pass