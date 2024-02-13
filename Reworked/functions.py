import pandas as pd
from numpy import nan

class setup_data():
    def __init__(self, file):
        self.file = file
        self.sheets = ['Education','Early_childhood_development','Families', 'Housing','IRSD', 'Mothers_babies']
        self.data = self.create_data()
        self.dataset = self.merge_data()

    def init_sheet(self,sheet): # function to read individual sheets from excel
        df = pd.read_excel(self.file, sheet_name = sheet)
        df.columns = df.iloc[3]
        df = df.iloc[4:596]
        df = df.dropna(axis = 'columns')
        df = df.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'})
        df = df.replace('..', nan)
        df = df.replace('#', nan)
        return df

    def create_data(self): # make each sheet into its own data frame
        data = {}
        for sheet in self.sheets: # loop to add each dataframe as a value in a dictionary, so it can be called 
            data[f'{sheet}'] = self.init_sheet(sheet)

        data['ED_total'] = self.ED_data()
        data['Hosp_ad'] = self.hosp_data()
        data['Income_support'] = self.income_support()
        return data
         
        
    def merge_data(self):
        dataset = pd.DataFrame()
        for data in self.data.keys():
            dataset = pd.concat([dataset, self.data[data]], axis =1)

        dataset = dataset.drop(columns=['Quality indicator*','Name\n(PHN/LGA)'])
        return dataset
    
    def ED_data(self):
        ED = pd.read_excel(self.file, sheet_name = 'ED_total')
        ED_col = ED.loc[:, ED.columns.str.contains('Emergency')].columns.to_list()# save the column titles
        # making column titles easier to read
        ED_col = [w.replace("Emergency department presentations: Total presentations for " , "") for w in ED_col]
        ED_col = [w.replace("\n", "") for w in ED_col] # delete linebreaks
        ED_col = [w.replace("-", "") for w in ED_col] # delete hyphens
        ED_col = [w.replace("  ", " ") for w in ED_col] # reduce double whitespace to single
        ED_col.insert(0, 'LGA_code')

        ED.columns = ED.iloc[3]
        ED = ED.iloc[4:596]
        ED = ED.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'})
        ED = ED.drop(columns=['Quality indicator*', 'Name\n(PHN/LGA)','Number','SR'])# remove all except ASR
        ED = ED.dropna(axis = 'columns')

        ED = ED.replace('..', nan)
        ED = ED.replace('#', nan)

        ED.columns = ED_col# replace column titles

        return ED

    def hosp_data(self):
        hosp = pd.read_excel(self.file, sheet_name = 'Admiss_principal_diag_persons')
        hosp_col = hosp.loc[:, hosp.columns.str.contains('Admissions for ')].columns.to_list()# save the column titles
        # making column titles easier to read
        hosp_col = [w.replace("Admissions for " , "") for w in hosp_col]
        hosp_col = [w.replace("\n", "") for w in hosp_col]
        hosp_col = [w.replace("-", "") for w in hosp_col]
        hosp_col = [w.replace("  ", " ") for w in hosp_col]
        hosp_col.insert(0, 'LGA_code')

        hosp.columns = hosp.iloc[3]
        hosp = hosp.iloc[4:596]
        hosp = hosp.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'})
        hosp = hosp.drop(columns=['Quality indicator*', 'Name\n(PHN/LGA)','Number','SR'])# remove all except ASR
        hosp = hosp.dropna(axis = 'columns')
        hosp = hosp.replace('..', nan)
        hosp = hosp.replace('#', nan)

        hosp.columns = hosp_col# replace column titles
        return hosp
    
    def income_support(self):
        income = self.init_sheet('Income_support')
        income = income[['% young people receiving Youth Allowance (other)', 
                         '% low income, welfare-dependent families (with children)',
                         '% children in low income, welfare-dependent families']]

        return income   
