import pandas as pd
import os
import glob

os.system('rm results/*.csv')

os.system('python deal-amz.py')
os.system('python deal-ebay.py')
os.system('python deal-rfd.py')

os.chdir("./results")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "mergedAll.csv", index=False, encoding='utf-8-sig')
