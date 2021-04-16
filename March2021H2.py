import csv
from pathlib import Path

import pandas as pd


HERE = str(Path().resolve())
DATA_DIR = HERE + '/data/'

# read the raw |-delimited file, write as csv
ftds = pd.read_csv (DATA_DIR + 'raw/cnsfails202103b.txt', sep='|')
ftds.replace('|',',')
ftds.to_csv(DATA_DIR + r'/cleaned/cnsfails202103b.csv', index=None)

del ftds['CUSIP']
del ftds['DESCRIPTION']

# manually collected by going to this site 4/16/21: https://www.etf.com/stock/GME
etfs_holding_gme = pd.read_csv(DATA_DIR + r'ETFs.csv')['name'].tolist()

ftds_gme = ftds[ftds["SYMBOL"]=="GME"].sort_values('SETTLEMENT DATE')
ftds_gme_last = ftds_gme.tail(1)

ftds_etfs_w_gme = ftds[ftds["SYMBOL"].isin(etfs_holding_gme)]

last_ftd_dates = []

for etf in etfs_holding_gme:
    temp_ftd_etf = ftds_etfs_w_gme[ftds_etfs_w_gme["SYMBOL"]==etf]
    ftds_eft_last_idx = temp_ftd_etf.last_valid_index()
    last_ftd_dates.append(ftds_eft_last_idx)

ftds_etfs_latest = ftds_etfs_w_gme.loc[last_ftd_dates, ]

all_ftds = ftds_gme_last.append(ftds_etfs_latest)
all_ftds.to_csv(DATA_DIR + '/cleaned/latest_gme_and_etf_ftds.csv', index=None)


# these are totals for the end of march!
all_gme_share_ftds = ftds_gme_last["QUANTITY (FAILS)"].sum()
all_etfs_w_gme_ftds = ftds_etfs_latest["QUANTITY (FAILS)"].sum()

all_ftds = all_ftds["QUANTITY (FAILS)"].sum()

print(all_gme_share_ftds)
print(all_etfs_w_gme_ftds)
print(all_ftds)
