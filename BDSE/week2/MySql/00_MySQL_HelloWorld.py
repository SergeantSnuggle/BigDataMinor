# python -m pip install sqlalchemy
# https://dev.mysql.com/downloads/connector/python/

import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import inspect

engine = create_engine('mysql+mysqlconnector://root:@localhost/zipcode')

inspector=inspect(engine)

for name in inspector.get_table_names('zipcode'):
    print(name)