import pandas as pd

df = pd.read_csv('data/logs_OMBA-Strategy Execution-2023_20230815-1405.csv')
print(df)
remove_names = ['Sabine Petrakakis',
'Utz Schaeffer',
'Zeeshan Sultan',
'Sebastian Ebert',
'Tobias Knoerrer',
'Rounak Gunjal',
'Fei Dai',
'Ingy Kenawy',
'Iskenderbek Kariev',
'Yulia Kupriyanova',
'Michael Moeller',
'John Gieger',
'Clara Wanatirta',
'Ute Ziss',
'Annelena Krebs',
'Vincent Meertens',
'Gwen van Rumund',
'Khoa Vu',
'Nicolle Olsen',
'Nadine Salz',
'Aqeela Dinat',
'David Emami'
]
df = df[~df['User full name'].isin(remove_names)]
print(df)
df.to_csv('data/modified_logs_OMBA-Strategy Execution-2023_20230815-1405.csv', index=False)