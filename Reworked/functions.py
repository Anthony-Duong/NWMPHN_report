import pandas as pd
#sheets = ['Education','Early_childhood_development','Families', 'Housing','IRSD', 'Mothers_babies']

class setup_data():
    def __init__(self, file, sheets):
        self.file = file
        self.sheets = sheets
        self.data = self.create_data()

    def init_sheet(self,sheet):
        df = pd.read_excel(self.file, sheet_name = sheet)
        df.columns = df.iloc[3]
        df = df.iloc[4:596]
        df = df.dropna(axis = 'columns')
        df = df.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'})
        return df

    def create_data(self):
        data = pd.DataFrame()
        for sheet in self.sheets:
            data = pd.concat([data,self.init_sheet(sheet)], axis =1)
        data = data.drop(columns=['Quality indicator*','Name\n(PHN/LGA)'])
        return data
