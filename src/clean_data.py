import pandas as pd
import os
from pathlib import Path
import sys

def setup_directories():
    """
    Set up data and output directories
    """
    # Input directory
    datadir = os.path.join(sys.path[0], "../input")
    Path(datadir).mkdir(parents=True, exist_ok=True) # Create if doesn't exist

    # Output directory
    outputdir = os.path.join(sys.path[0], "../output")
    Path(outputdir).mkdir(parents=True, exist_ok=True)  # Create if doesn't exist

    return datadir, outputdir

def import_data(datadir):
    """
    Import data and perform initial processing
    """
    os.chdir(datadir)
    df = pd.read_feather("solar_dataset_all_renewables")
    df["country_code"] = df['person_ctry_code']
    df.loc[df["cpc_class_symbol"].str.startswith("Y02E", na=False), 'cpc_renewables'] = 1
    df.loc[~df["cpc_class_symbol"].str.startswith("Y02E", na=False), 'cpc_renewables'] = 0
    df.loc[df["cpc_class_symbol"].str.startswith("Y02E10/5", na=False), 'cpc_solar'] = 1
    df.loc[~df["cpc_class_symbol"].str.startswith("Y02E10/5", na=False), 'cpc_solar'] = 0
    df = df.dropna(subset=["country_code"]).reset_index()
    list_countries = df["country_code"].unique().tolist()

    return df, list_countries

def absolute_count(df, list_countries):
    """
    Count patents by country and type
    """
    ## fossil fuel ##
    patents_year = df[df.fossil_fuel == 1].groupby('earliest_filing_year')['docdb_family_id'].nunique().to_frame(name = "Nb_ff_energy_innov_per_year_all") # Transform the series that groupby creates to a dataframe

    # countries #
    dict = {} 
    for country in list_countries:
        name = "Nb_ff_energy_innov_per_year_" + country
        value = df[(df.fossil_fuel == 1) & (df.country_code == country)].groupby('earliest_filing_year')['docdb_family_id'].nunique() 
        dict["Nb_ff_energy_innov_per_year_" + country] = value
        patents_year[name] = dict[name] 


    ## Renewables panel ##
    patents_year["Nb_renewables_energy_innov_per_year_all"] = df[df["cpc_renewables"] == 1].groupby('earliest_filing_year')['docdb_family_id'].nunique()

    # countries #
    # by family
    dict = {} 
    for country in list_countries:
        name = "Nb_renewables_energy_innov_per_year_" + country
        value = df[(df["cpc_renewables"] == 1) & (df.country_code == country)].groupby('earliest_filing_year')['docdb_family_id'].nunique()
        dict["Nb_renewables_energy_innov_per_year_" + country] = value
        patents_year[name] = dict[name] 

    
    return patents_year


def process_data(df, list_countries, outputdir):
    """
    Process data and save to feather
    """
    df2 = absolute_count(df, list_countries).reset_index()
    df2 = df2.loc[:,~df2.columns.str.endswith('all')]
    return df2

def reshape_and_save_data(df2, outputdir):
    """
    Reshape data, create shares and save to feather
    """
    df_melted = df2.melt(id_vars='earliest_filing_year', var_name='Type_Country', value_name='Number_of_innovations')
    df_melted['Country'] = df_melted['Type_Country'].str[-2:]
    df_melted['Type'] = df_melted['Type_Country'].str.split('_').str[1]
    df_pivot = df_melted.pivot_table(index=['earliest_filing_year', 'Country'], columns='Type', values='Number_of_innovations').reset_index()
    df_pivot.columns = df_pivot.columns.get_level_values(0)
    df_pivot["share_ff"] = df_pivot["ff"] / (df_pivot["ff"] + df_pivot["renewables"])
    df_pivot["share_renewables"] = df_pivot["renewables"] / (df_pivot["ff"] + df_pivot["renewables"])
    df_pivot.reset_index(drop = True, inplace = True)
    df_pivot.to_feather(os.path.join(outputdir, "df_allyears"))

def main():
    datadir, outputdir = setup_directories()
    df, list_countries = import_data(datadir)
    df2 = process_data(df, list_countries, outputdir)
    reshape_and_save_data(df2, outputdir)

if __name__ == "__main__":
    main()
