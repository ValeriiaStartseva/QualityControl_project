import pandas as pd
from sql_app.database import engine

df = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/Monitoring.csv')
df.to_sql('Monitoring', engine, if_exists='replace', index=False)

df1 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/MonitoringDictionary.csv')
df1.to_sql('MonitoringDictionary', engine, if_exists='replace', index=False)

df2 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/MonitoringScores.csv')
df2.to_sql('MonitoringScores', engine, if_exists='replace', index=False)

df3 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/Roles.csv')
df3.to_sql('Roles', engine, if_exists='replace', index=False)

df4 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/Users.csv')
df4.to_sql('Users', engine, if_exists='replace', index=False)

df5 = pd.read_csv('/Users/valeriiastartseva/QualityControl_project/CollectUser.csv')
df5.to_sql('CollectUser', engine, if_exists='replace', index=False)

