import pandas as pd
import pycountry
import dash
import os
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import sys
from app_layout import init_layout
from pathlib import Path

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

def import_data(outputdir):
    """
    Import data and perform initial processing
    """
    os.chdir(outputdir)
    df = pd.read_feather("df_allyears")

    return df


def alpha2_to_alpha3(alpha_2):
    """Converts ISO 2 country code to ISO 3 country code"""
    country = pycountry.countries.get(alpha_2=alpha_2)
    return country.alpha_3 if country else alpha_2

def convert_country_codes(df):
    """Converts country codes and assigns country names."""
    df["Country"] = df["Country"].apply(alpha2_to_alpha3)
    country_mapping = {country.alpha_3: country.name for country in pycountry.countries}
    df["Country_Name"] = df["Country"].map(country_mapping)
    return df

def drop_not_converted(df):
    """Drop rows where 'Country' column contains 2-letter codes"""
    df = df[df["Country"].str.len() != 2]
    return df

def fill_missing_data(df):
    """Fills the missing data in the dataframe"""
    # rename column earlist_year to year
    df.rename(columns={"earliest_filing_year": "Year"}, inplace=True)

    # create a DataFrame that includes all years in your original dataset
    years_df = pd.DataFrame({"Year": df["Year"].unique()})

    # Retrieves alle ISO 3 country codes and country names from pycountry
    countries_df = pd.DataFrame(
        {
            "Country": [country.alpha_3 for country in pycountry.countries],
            "Country_Name": [country.name for country in pycountry.countries],
        }
    )

    # create a DataFrame that includes every combination of country and year.
    countries_years_df = pd.merge(
        countries_df.assign(key=0), years_df.assign(key=0), on="key"
    ).drop("key", axis=1)

    # merge this countries_years_df DataFrame with original df
    df = pd.merge(
        countries_years_df, df, on=["Country", "Country_Name", "Year"], how="outer"
    )

    # Replace NaN values with 0
    df["ff"] = df["ff"].fillna(0)
    df["renewables"] = df["renewables"].fillna(0)
    df["share_renewables"] = df["share_renewables"].fillna(0)
    df["share_ff"] = df["share_ff"].fillna(0)
    return df

def filter_years(df):
    """Keeps only data from the year 2000 to 2017"""
    df = df[(df["Year"] >= 2000) & (df["Year"] <= 2017)]
    return df

def transform_share(df):
    """Transforms share in % and rounds it to 2 decimals"""
    df["share_ff"] = (df["share_ff"] * 100).round(2)
    df["share_renewables"] = (df["share_renewables"] * 100).round(2)
    return df

def save_data(df, outputdir):
    """Saves the dataframe as a feather file."""
    df.reset_index(inplace=True)
    df.to_feather(os.path.join(outputdir, "df_processed"))


def main():
    datadir, outputdir = setup_directories()
    df = import_data(outputdir)
    df = convert_country_codes(df)
    df = drop_not_converted(df)
    df = fill_missing_data(df)
    df = filter_years(df)
    df = transform_share(df)
    save_data(df, outputdir)


if __name__ == "__main__":
    main()



