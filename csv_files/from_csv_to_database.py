import pandas as pd
from sql_app.database import engine

df0 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/BasicDictionary.csv')
df0.to_sql('BasicDictionary', engine, if_exists='append', index=False)

df5 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/CollectUser.csv')
df5.to_sql('CollectUser', engine, if_exists='append', index=False)

df3 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/Roles.csv')
df3.to_sql('Roles', engine, if_exists='append', index=False)

df4 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/Users.csv')
df4.to_sql('Users', engine, if_exists='append', index=False)

df2 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/CollectReestr.csv')
df2.to_sql('CollectReestr', engine, if_exists='append', index=False)

df10 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/CollectContract.csv')
df10.to_sql('CollectContract', engine, if_exists='append', index=False)

df = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/Monitoring.csv')
df.to_sql('Monitoring', engine, if_exists='append', index=False)

df1 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/csv_files/MonitoringDictionary.csv')
df1.to_sql('MonitoringDictionary', engine, if_exists='append', index=False)












