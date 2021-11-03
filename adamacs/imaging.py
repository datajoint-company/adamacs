"""Tables related to imaging.


"""

import datajoint as dj
'''
Consider importing element-calcium imaging:
github.com/datajoint/element-calcium-imaging
Example workflow:
github.com/datajoint/workflow-calcium-imaging

'''

from adamacs.subject import *
from adamacs.surgery import *

schema = dj.schema()

@schema
