import os
import json
import tarfile
from . import __version__

def version():
   return __version__.__version__
 
def archive(indir, output):
    with tarfile.open(output, 'w:gz') as tar:
        tar.add(indir, os.path.basename(indir))

def get_mask_threshold(sidecar):
    with open(sidecar, 'r') as fo:
        js = json.load(fo)
    bits_stored = js.get('BitsStored', None)
    if bits_stored >= 16:
        return 3000.0
    return 150.0

