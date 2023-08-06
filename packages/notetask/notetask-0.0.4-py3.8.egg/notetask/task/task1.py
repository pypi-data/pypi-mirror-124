from odps import DataFrame
from noteodps import ODPS, opt
import pandas as pd
from notetool.secret.secret import load_secret_str

load_secret_str()

print(opt.list_functions())

a = pd.DataFrame([[1, 2], [4, 6]])
a.columns = ['col1', 'col3']
print(a)
a2 = DataFrame(a)

a2.persist("local_test", partition="ds=20211102")
