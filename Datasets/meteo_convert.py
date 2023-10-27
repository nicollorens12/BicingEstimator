import os
import pandas as pd
from datetime import datetime


# Directorio actual donde se encuentra el script

df = pd.read_csv("./Meteo_DataSet.csv")

# Agregar columnas para el mes, el día del mes, la hora y los minutos
df["month"] = df["time"].apply(lambda x: datetime.utcfromtimestamp(x+7200).month)
df["day_month"] = df["time"].apply(lambda x: datetime.utcfromtimestamp(x+7200).day)
df["hour"] = df["time"].apply(lambda x: datetime.utcfromtimestamp(x+7200).hour)


#df.drop(columns=['V1', 'last_reported'], inplace=True)
# Guardar el DataFrame combinado en un solo archivo CSV llamado "DataFrame.csv"
df.to_csv("./Meteo_DataSet.csv", index=False)

