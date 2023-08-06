import os

import pandas
import gspread
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials



def upsert_df_to_gsheet(df, franchise_name, gsheet):
    """ Add dataframe menu items to a researcher googlesheet.
    Parameters
    ----------
    df : dataframe
        Dataframe to transfer to google sheet.
    franchise_name : string
        Name of the corresponding franchise.
    gsheet : string
        Name of the google sheet to update.
    """
    g_json = os.environ["GOOGLE_API_JSON"]
    sheet_key = os.environ["research_sheet_key"]
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(g_json, scope)
    gc = gspread.authorize(creds)

    df = df[["item_name", "iurl", "menu_section"]].copy()
    df['franchise'] = franchise_name
    df["year"] = os.environ.get('YEAR')

    gdf = g2d.download(sheet_key, wks_name=gsheet, row_names=False,
                col_names=True, credentials=creds)

    gdf2 = pandas.merge(gdf, df, how='outer', on=[
            'franchise',"item_name","year",'iurl','menu_section'])
    gdf2 = gdf2.fillna("")
    gdf2 = gdf2.drop_duplicates()
    d2g.upload(gdf2, sheet_key, wks_name=gsheet, credentials=creds,\
                row_names=False)
