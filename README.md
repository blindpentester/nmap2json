# nmpa2json
Convert nmap XML to JSON (even big fuckoff ones)

## Story of how this happened  
I am in a few chat groups on signal and one of the things brought up was xml2json having memory issues with larger conversions.  
I have been making something that did outputs to JSON, XML and TXT and that is still in the works and I figured I'd give this a shot  
It worked, and its kinda dope.  Anyway, here's this thing if you are feeling limited with xml2json.

# Usage:  
  - cat &lt;nmap filename&gt;.xml | ./nmap2json.py -o <ouptut file name>.json
  - nmap &lt;args you want to use&gt; -oX - | ./nmap2json.py -o &lt;ouptut file name&gt;.json  
 
