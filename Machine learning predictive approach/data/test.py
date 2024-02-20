import pandas as pd

sheets = ['Education','Early_childhood_development','Families', 'Housing','IRSD', 'Mothers_babies']

def init_sheet(sheet):
        df = pd.read_excel('2021_data.xlsx', sheet_name = sheet)
        df.columns = df.iloc[3]
        df = df.iloc[4:596]
        df = df.dropna(axis = 'columns')
        df = df.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'})
        return df


data = {}
for sheet in sheets:
    data[f'{sheet}'] = init_sheet(sheet)

print(data['Education'])