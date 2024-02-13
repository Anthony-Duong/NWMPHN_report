
from pandas import read_excel, concat, DataFrame
from numpy import nan

class setup_data():
    def __init__(self, file):
        self.file = file
        self.sheets = ['Education','Early_childhood_development','Families', 'Housing', 'Mothers_babies','Internet_access', 'Learning_Earning', 'Child_care', 'Income_support', 'Disability']
        self.data = self.create_data()
        self.dataset = self.merge_data()

    def init_sheet(self,sheet): # function to read individual sheets from excel
        df = read_excel(self.file, sheet_name = sheet)
        df.columns = df.iloc[3]# remove first 4 rows (excel formatting)
        df = df.iloc[4:596]# select out summary data
        
        df = df.drop(columns=['Quality indicator*','Name\n(PHN/LGA)'], errors = 'ignore') # drop unneeded cols
        df = df.dropna(axis = 'columns') #drop blank columns
        df = df.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code'}) # rename column to LGA code for readability
        df = df.replace('..', nan)
        df = df.replace('#', nan)
        df = df.loc[:, df.columns.str.contains('%|LGA_code')] # selecting for columns containing % and LGA_code

        return df

    def create_data(self): # make each sheet into its own data frame
        data = {}
        for sheet in self.sheets: # loop to add each dataframe as a value in a dictionary, so it can be called 
            data[f'{sheet}'] = self.init_sheet(sheet)
            
        data['ED_total'] = self.ED_data() # add ED data to dict
        data['Hosp_ad'] = self.hosp_data() # add hospital admission data to dict
        data['IRSD'] = self.IRSD() # add IRSD data to dict
        return data
         
        
    def merge_data(self):
        dataset = DataFrame()
        for data in self.data.keys():
            dataset = concat([dataset, self.data[data]], axis =1) # left join all data into one dataset
            dataset = dataset.loc[:,~dataset.columns.duplicated()].copy() # removes duplicate columns
        return dataset
    
    def ED_data(self): # reading ED data
        ED = read_excel(self.file, sheet_name = 'ED_total')
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

    def hosp_data(self): # reading hospital admission data
        hosp = read_excel(self.file, sheet_name = 'Admiss_principal_diag_persons')
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
    
    def IRSD(self): # reading IRSD data
        IRSD = read_excel(self.file, sheet_name = 'IRSD')
        IRSD.columns = IRSD.iloc[3]
        IRSD = IRSD.iloc[4:596]

        IRSD = IRSD.drop(columns=['Name\n(PHN/LGA)','Usual resident population (Census 2016)'])
        IRSD = IRSD.dropna(axis = 'columns')
        IRSD = IRSD.rename(columns = {'Code\n(PHN/LGA)': 'LGA_code', 'Index score (based on Australian score of 1,000)': 'SEIFA Index'})
        IRSD = IRSD.replace('..', nan)
        IRSD = IRSD.replace('#', nan)

        return IRSD   
