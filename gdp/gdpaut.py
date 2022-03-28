import pandas as pd
import numpy as np
from cif import cif
data = cif.createDataFrameFromOECD(countries = ['AUS+BEL+CAN+FRA+DEU+ITA+JPN+KOR+NLD+NZL+SWE+CHE+GBR+USA+EU27_2020+OECDE+OECD+NMEC+IND'], dsname = 'QNA', subject = ['B1_GE'], measure = ['VPVOBARSA'], frequency = 'Q', startDate = '2018-Q4', endDate = '2022-Q1')
print(data)
