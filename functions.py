import pandas as pd
import streamlit as st

def search_distro(searchterm:str):
    df = pd.read_csv("Homepage.csv")
    if searchterm:
        df = df[df['Name'].str.contains(searchterm,case=False)]
        return df["Name"]
    else:
        return []
    