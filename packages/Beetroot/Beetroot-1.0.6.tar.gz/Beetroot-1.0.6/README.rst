===========
Python-Beet
===========

Beet, a general purpose library full of random python functions that I thought were useful. Has file manipulation, random, tts and more!
Have fun using! There isn't a function list yet, but I might get to that soon. Or not so soon.

Also, to make JSON dumping and reading faster, do ``pip install ujson`` or ``pip install simplejson``

Different extras:
=================

- beetroot[all]

- beetroot[tts]

Functions and uses:
===================

- beetroot.objtype(obj) ; python type(), but better

- beetroot.random.randint(start, end) ; generates random number but using SystemRandom

- beetroot.random.srandint(seed, start, end) ; generates seeded pseudorandom number

- beetroot.stopwatch.start() ; Starts global stopwatch

- beetroot.stopwatch.stop() ; Stops global stopwatch and returns time in milliseconds between start and stop

- beetroot.file.move(start, end) ; Moves files

- beetroot.file.rename(start, end) ; Renames files

- beetroot.file.delete(file_to_delete, force=<bool>) ; Deletes files

- beetroot.file.dump(file, data) ; Dumps data to file as string

- beetroot.file.bdump(file, data) ; Dumps data to file as bytestring (doesn't work too well)

- beetroot.file.jdump(file, data, pp=<bool>) ; Dumps data

- beetroot.file.load(file) ; Reads data from file as string

- beetroot.file.bload(file) ; Reads data from file as bytestring

- beetroot.file.jload(file) ; Reads data from file as JSON object

- beetroot.tts.say(text) ; Reads text with tts installed, requires pyttsx3 to be installed or use ``pip install beetroot[tts]``

- beetroot.tts.changeRate(text) ; Changes global tts talk speed, requires pyttsx3 to be installed or use ``pip install beetroot[tts]``

- beetroot.tts.changeVoice(text) ; Changes global tts voice you can pick ids from 0-n, depending on how many voices you have on your computer, requires pyttsx3 to be installed or use ``pip install beetroot[tts]``

- beetroot.tts.changeVolume(text) ; Changes global tts volume, requires pyttsx3 to be installed or use ``pip install beetroot[tts]``

- beetroot.strhash(text, secure=<bool>) ; Hashes a string or non-bytestring that can be converted to string.

- beetroot.bhash(text, secure=<bool>) ; Hashes a bytestring.

- beetroot.test() ; Literally just a hello world program.

- beetroot.quicksort(arr) ; Quicksort, which in most cases is slightly faster than Python3's default Timsort.

- beetroot.lsep(string, seperator) ; basically .split() but it removes empty or all-whitespace strings from output.

- beetroot.execfile(file) ; Execute .py script

- beetroot.systemstats() ; Returns [Username, OS, OS version, OS architecture, computer nodename, IP address, MAC address]

- beetroot.unline(string) ; Makes a multi-line string a single-line string

- beetroot.reline(string) ; Reverses beetroot.unline()

- beetroot.beetroot() ; A great function that you should call whenever you can