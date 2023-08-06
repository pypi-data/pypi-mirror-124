import re
import csv
import sys
import glob
import string
import warnings
import subprocess
import faulthandler
import datetime as dt
from pathlib import Path

import yaml
import pandas
import sqlalchemy
import numpy as np
import chromedriver_binary
from tqdm import tqdm
from selenium import webdriver
from rapidfuzz import fuzz, process
from sqlalchemy import or_, update
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from selenium.common.exceptions import SessionNotCreatedException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from menustat.log import *
from menustat.utils import *
# add_meta, loop_string_replace, return_range,
from menustat.orm import Base, Franchise, MenuItem, AnnualItemData
from menustat.settings import YEAR, ANALYST, engine, session, config
from menustat.scraper import Calculator, WebTable, WebTableReactive, Pdf, MultiPdf, WebSite, SiteNav


class CollectedDf():
    """Class for dataframes of collected data to prepare for db entry.

    Attributes
    ----------
    name: string
        Franchise's name, collected from database.
    nutr_url: string
        Franchise's nutr_url, collected from database.
    nutr_df: pandas dataframe
        Dataframe of scraped menu data.
    year: int
        Year of data collection.

    Methods
    -------
    add_df_to_db() - Creates AnnualItemData ORM objects from dataframe
        rows and inserts them into the database.
    """

    def __init__(self, name, f_id, nutr_df, **kwargs):
        self.name = name
        self.f_id = f_id
        self.nutr_df = nutr_df
        self.year = YEAR
        self.cleaner = config['cleaners']['gen_cleaners']
        self.__dict__.update(kwargs)
        self.nutr_columns = ['calories', "total_fat", "saturated_fat",
                "trans_fat", "cholesterol", "sodium", "potassium",
                "carbohydrates", "protein", "sugar", "dietary_fiber"]
        self.all_menu_items = session.query(MenuItem.id, MenuItem.item_name).\
                filter(MenuItem.franchise_id == self.f_id).all()
        self.all_annual_items = session.query(AnnualItemData.id,
                    AnnualItemData.menu_item_id,
                    AnnualItemData.year,
                    AnnualItemData.item_name,
                    AnnualItemData.calories,
                    AnnualItemData.protein,
                    AnnualItemData.total_fat,
                    AnnualItemData.carbohydrates).\
                join(MenuItem).\
                filter(MenuItem.franchise_id == self.f_id)
        logger.debug("{}".format(self.__dict__))
        logger.info("# items: {}".format(self.all_annual_items.count()))


    @wrap(writelog, writelog)
    def clean(self):
        # logger.debug("Clean: menu_section start:\n{}".format(self.nutr_df['menu_section']))
        self.nutr_df = self.nutr_df.dropna(how="all")
        self.nutr_df["item_name"] = self.nutr_df["item_name"].\
            apply(lambda x: self.clean_item_name(str(x)))
        if len(self.nutr_df[self.nutr_df["serving_size"] == '']) > 10:
            self.nutr_df["serving_size"] = self.nutr_df["item_name"].\
                apply(lambda x: self.name_to_serving(str(x)))
        logger.debug("autogenerate_description BEGIN:\n{}".format(self.nutr_df.head()))
        self.nutr_df['item_description'] = self.nutr_df.apply(lambda r: self.autogenerate_description(r), axis=1)

        self.nutr_df['item_name'] = self.nutr_df['item_name'].str.strip()
        self.combine_duplicate_rows()
        # self.pair_with_MenuItems()
        self.remove_unneeded_cols()
        self.standardize_df_contents()
        self.nutr_df['menu_item_id'] = self.nutr_df.apply(lambda x: self.\
                pair_with_menu_ids(x), axis=1)
        logger.debug("Clean: item_description end:\n{}".format(self.nutr_df.item_description))
        check_df_for_issues(self.name, self.nutr_df)


    def pair_with_menu_ids(self, aid_row,):
        """
        input: collected AID item (aid_row)
        1. Search db for AID entry using year, f_id, aid_row.item_name. If
        item found, return AID id and mi_id. If multiple items
        returned, flag issue.
        2. If no items returned, run self.return_MenuItem() to find correct
        menu_item and return mi_id of returned menu_item.
        """

        if aid_row.item_name == "":
            logger.warning("empty item_name string detected - ending "
                "return_MenuItem method")
            return
        aid_query = session.query(AnnualItemData).\
        join(MenuItem).\
        filter(AnnualItemData.item_name == aid_row.item_name).\
        filter(AnnualItemData.year == YEAR).\
        filter(MenuItem.franchise_id == self.f_id)
        try:
            matched_db_entry = aid_query.one()
        except MultipleResultsFound:
            logger.warning("WARNING: multiple matches for annual_item_"
            "data search:{}\nreturned items:".format(row['item_name']))
            matched_db_entries = aid_query.all()
            for e in matched_db_entries:
                logger.info("item:{} cals:{} carbs:{} add_date:{}".format(\
                e.item_name, e.calories, e.carbohydrates, e.created_at))
            mi_id = ",".join([e.id for e in matched_db_entries])
        except NoResultFound:
            logger.info("No AnnualItemData entry found.")
            mi_id = self.return_MenuItem(aid_row)
        else:
            mi_id = str(matched_db_entry.menu_item_id)
        return mi_id


    @wrap(writelog, writelog)
    def remove_unneeded_cols(self):
        standard_cols = ["item_name","menu_item_id","item_description",\
            "serving_size_household", "serving_size","serving_size_unit",
            "notes", "iurl"]
        standard_cols.extend(self.nutr_columns)
        logger.info("cols:{}".format(self.nutr_df.columns))
        not_in_df = [c for c in standard_cols if c not in self.nutr_df]
        logger.info("not_in_df:{}".format(not_in_df))
        for col in not_in_df:
            self.nutr_df[col] = ""
        self.nutr_df = self.nutr_df[standard_cols]


    def return_range_search_list(self, aid_item):
        logger.debug("return_range_search_list: {}".format(aid_item))
        ranges = {}
        for item in ["calories", "protein", "total_fat", "carbohydrates"]:
            val = getattr(aid_item, item, None)
            if val is not None:
                try:
                    ranges[item] = return_range(val)
                except TypeError:
                    pass
        logger.debug("return_range_search_list ranges: {}".format(ranges))
        return ranges


    def match_by_nutrition(self, row):
        """Return best-guess AID match using nutrition data and name.
        1. Try exact match for macronutrients, see if name is 75% match.
        2. If exact match fails, select best match from query of all
            franchise AID entries with ±5% macronutrient levels and >85%
            fuzzy match on name.
        3. If either match succeeds, return menu_item_id of AID match.
        """
        logger.debug("START: {}".format(row))
        returned_items = self.all_annual_items.filter(AnnualItemData.year < YEAR)
        try:
            returned_items = self.all_annual_items.\
                filter(AnnualItemData.calories == row.calories).\
                filter(AnnualItemData.protein == row.protein).\
                filter(AnnualItemData.total_fat == row.total_fat).\
                filter(AnnualItemData.carbohydrates == row.carbohydrates)
            logger.debug("returned_items1 query: {}".format(returned_items))
            if returned_items.count() == 0:
                raise ValueError('No returned_items for exact match')
        except Exception as e:
            logger.debug("{}; trying range match".format(e))
            # need light conditional for these - use if range exists, don't if not.
            range_dict = self.return_range_search_list(row)

            range_search_dict = {getattr(AnnualItemData, k):v for k, v in range_dict.items()}
            for k, v in range_search_dict.items():
                returned_items = returned_items.filter(k > v[0]).\
                        filter(k < v[1])
            logger.debug("returned_items query: {}".format(returned_items))

        logger.info("returned_items #: {}".format(returned_items.count()))
        if returned_items.count() == 1:
            aid_item = returned_items.one()
            plain_ratio = fuzz.ratio(row.item_name, aid_item.item_name)
            token_ratio = fuzz.token_set_ratio(row.item_name, aid_item.item_name)
            partial_ratio = fuzz.token_set_ratio(row.item_name, aid_item.item_name)
            if plain_ratio > 75 or token_ratio > 75:
                menu_item_id = aid_item.menu_item_id
                logger.debug("returned result:{}, {}, ratio={}, token_set_ratio={}".format(row.item_name, aid_item.item_name, plain_ratio, token_ratio))
            else:
                logger.debug("single result didn't pass 75%:{}, {}, ratio={}, token_set_ratio={}".format(row.item_name, aid_item.item_name, plain_ratio, token_ratio))
                menu_item_id = None
        elif returned_items.count() > 1:
            logger.info("too many returned items!")
            for item in returned_items.all():
                logger.info("{}, {}".format(item.id, item.item_name))
                item.menu_item_id = self.return_closest_match(item)
        elif returned_items.count() == 0:
            logger.info("no returned items!")
            menu_item_id = None
        logger.debug("END menu_item_id:{}".format(menu_item_id))
        return menu_item_id


    def clean_item_name(self, name):
        """Remove unneeded data from item name and restructure serving data.
        """
        logger.debug("preclean: {}".format(name))
        name = loop_string_replace(self.cleaner['nd_cleaner'], name, regex=False)
        name = loop_string_replace(self.cleaner['nd_cleaner_re'], name)
        count_re = re.search(r'\((\d+)\)$', name)
        if count_re:
            name = "{} {}".format(str(count_re.group(1)), name)
            name = name.replace(str(count_re.group(0)), "")
        count_counter_re = re.search(r' \((\d+ \w+)\)$', name)
        if count_counter_re:
            name = "{}, {}".format(name, str(count_counter_re.group(1)))
            name = name.replace(str(count_counter_re.group(0)), "")
        name = name.strip("+ ")
        logger.debug("cleaned: {}".format(name))
        return name


    def name_to_serving(self, name):
        """Place any serving_size values in item_name in serving_size field.
        """
        logger.debug(name)
        for pattern in self.cleaner["serving_in_name"]:
            count_re = re.search(pattern, name)
            if count_re:
                serving = str(count_re.group(1))
                break
        else:
            serving = None
        logger.debug(serving)
        return serving


    @wrap(writelog, writelog)
    def combine_duplicate_rows(self):
        """ If any rows have same nutrition facts and name, combine rows.
        1. ID all rows of same item
        2. ID the duplicates to appear second, add its menu_section to
        first row's menu_section.
        """
        colnames = ['item_name']
        colnames.extend(self.nutr_columns)
        logger.debug("platonic colnames: {}".format(colnames))
        dupecheck = self.nutr_df[self.nutr_df.duplicated(subset=colnames,
                                            keep=False)].fillna("")
        if not dupecheck.empty:
            dicta = {}
            # make dict of item_name: menu_section pairs
            for iname, msect in zip(self.nutr_df.item_name, self.nutr_df["menu_section"]):
                if iname not in dicta.keys():
                    dicta[iname] = [msect]
                else:
                    dicta[iname].append(msect)
            dictb = {key:", ".join(v for v in value) for key, value in dicta.items()}
            self.nutr_df['menu_section'] = self.nutr_df['item_name'].map(dictb)
            self.nutr_df.drop_duplicates(keep="first", inplace=True)
            # logger.debug(dupecheck.groupby(by=colnames)['menu_section'].apply(', '.join))
            # dupecheck.groupby(by=colnames).agg({'menu_section': ','.join, "index": list()})



    def add_df_to_db(self, dryrun=True):
        """ Insert df of AnnualItemData entries into database.
        1. Create AnnualItemData ORM objects from dataframe rows
        2. Search AnnualItemData entries w/ matching item_name, f_id, & year
        2A. If one entry returned, update entry.
        3. If multiple AnnualItemData entries returned, default to first.
        4. If existing AnnualItemData entry not found, search for
            accompanying MenuItem entry in the database.
        5. If MenuItem entry found, link new AnnualItemData object to it;
            if not, create new MenuItem entry.
        6. Insert new AnnualItemData objects into database.
        """
        new_id = return_largest_id_plusone(AnnualItemData)
        aid_objects = self.nutr_df.apply(lambda x: self.\
                produce_aid_object(x), axis=1)
        new_db_entries = aid_objects.tolist()
        if dryrun == True:
            pass
        else:
            session.add_all(new_db_entries)
            session.commit()


    def produce_aid_object(self, row):
        aid_args = {k:v for k, v in row.to_dict().items() if k != "iurl"}
        annual_item = AnnualItemData(**aid_args)
        annual_item.updated_by = ANALYST
        annual_item.updated_at = dt.datetime.now()
        return annual_item


    def return_MenuItem(self, annual_item):
        """ Return MenuItem match for AnnualItemData object.
        1. Attempt direct match using item name.
        2. If direct match returns multiple results, return closest match.
        3. If direct match returns no results, return match using
            match_by_nutrition method.
        4. If match_by_nutrition fails, use fuzzy string matching.
        5. If no match satisfying any prior conditions found, create a new
            Menu_Item object and insert it into the database.
        """
        item_name = f"{annual_item.item_name}"
        logger.info(f"namesearch: {item_name}")
        menu_item_query = session.query(MenuItem.id).\
                filter(MenuItem.item_name.ilike(f'{item_name}')).\
                filter(MenuItem.franchise_id == self.f_id)
        try:
            menu_item_id = menu_item_query.one()[0]
            logger.info(f"MenuItem match: {item_name}")
        except MultipleResultsFound:
            logger.info(f"ISSUE: multiple matches for: {annual_item.__dict__}")
            menu_item_id = self.fuzzy_match_menu_item(annual_item)
        except NoResultFound:
            logger.info(f"No exact match: {item_name}\nTrying match_by_nutrition")
            try:
                menu_item_id = self.match_by_nutrition(annual_item)
                if menu_item_id is None:
                    raise TypeError("no match found")
            except Exception as e:
                logger.info("match_by_nutrition fail\n{}".format(e))
                try:
                    logger.info("trying name-only fuzzy match")
                    menu_item_id = self.fuzzy_match_menu_item(annual_item)
                except TypeError as e:
                    logger.info("fuzzy match failed: {}".format(e))
                    menu_item_id = None
                except Exception as e:
                    logger.info(f"fuzzy match failed: {e}", exc_info=True)
                    logger.info("adding new Menu_Item entry")
                    menu_item_id = self.add_new_menuitem(annual_item)

            # note = "franchise id:{}".format(f_id)
            # to_error_csv(annual_item.item_name, note,"no MenuItem match")
        logger.info("menu_item_id:{}".format(menu_item_id))
        return menu_item_id


    def fuzzy_match_menu_item(self, annual_item, match_pct=91):
        """ Use fuzzy match to find MenuItem for new AnnualItemData entry.
        1. Create list of menu_item item_name values
        2. Return item_name values that match self.item_name at ≥ 91%
        3. Select first entry.
        """
        logger.info("fuzzy_match: {}".format(annual_item.item_name))
        # plain_ratio = fuzz.ratio(self.item_name, aid_item.item_name)
        # token_ratio = fuzz.token_set_ratio(self.item_name, aid_item.item_name)
        # partial_ratio = fuzz.token_set_ratio(self.item_name, aid_item.item_name)
        all_franchise_item_names = [i[1] for i in self.all_menu_items]
        returned = process.extractOne(annual_item.item_name,\
                all_franchise_item_names, score_cutoff=match_pct)
        if not returned:
            desc = f"{annual_item.item_name} {annual_item.item_description}"
            returned = process.extractOne(annual_item.item_description,\
                    all_franchise_item_names, score_cutoff=match_pct)
        logger.info("returned pair: {}::{}".format(annual_item.item_name,\
                returned))
        returned_id = [i[0] for i in self.all_menu_items if i[1] ==\
                returned[0]]
        menu_item_id = None if not returned_id else str(returned_id[0])
        logger.info("menu_item_id: {}".format(menu_item_id))
        return menu_item_id


    def add_new_menuitem(self, annual_item):
        logger.debug("START {}".format(annual_item))
        new_menu_items = []
        try:
            new_mi_id = return_largest_id_plusone(MenuItem)
            new_mi_id += 1
        except Exception as e:
            logger.info("method failed:\n{}".format(e), exc_info=True)
        else:
            meta = add_meta({}, created=True)
            new_entry = MenuItem(
                    id=new_mi_id,
                    franchise_id=self.f_id,
                    item_name=annual_item.item_name,
                    **meta)

            new_menu_items.append(new_entry)
        return new_mi_id

    def autogenerate_description(self, row):
        """
        Generate description using item_name, menu_section and description.
        1. if "description" exists, add  ", " + "menu_section"
        2. if not, "description" = "item_name" + ", " + "menu_section"
        """
        desc_base = row.item_description if row.item_description != "" else\
                row.item_name
        desc = "{}, {}".format(desc_base, row["menu_section"]).\
                replace(", nan", "")
        logger.debug("item_description:{}".format(desc))
        desc = re.sub(self.cleaner['remove_from_desc'], "", desc, flags=re.IGNORECASE)
        desc = loop_string_replace(self.cleaner['nd_cleaner'], desc, regex=False)
        desc = loop_string_replace(self.cleaner['nd_cleaner_re'], desc)

        return desc


    @wrap(writelog, writelog)
    def standardize_df_contents(self):
        """ Make column contents conform with intended format & datatype.
        1. Move non-digit nutrition columns to "_text" cells
        2. add numeric serving amounts in names ("24 oz") to serving size
        3. separate serving size value into numeric amount and measure. If
            measure isn't a standard measure, assign to "household"
        """
        df = self.nutr_df
        # column contents to address: '4130/7140','43 g',"<1","-"
        df.drop_duplicates(inplace=True)
        df.fillna("", inplace=True)
        df.loc[df['serving_size'].notnull(), 'serving_size'] = df['serving_size'].astype(str)
        df = df.replace("^-$", "", regex=True)
        df['serving_size'] = df['serving_size'].str.strip()

        df.loc[df['serving_size'].str.contains(self.cleaner["ss_text"], \
                regex=True), "serving_size_text"] = df['serving_size']

        ssu_re = "\d+\s*({})".format("|".join(u for u in self.cleaner["serving_units"]))
        df.loc[df['serving_size'].str.contains(ssu_re, regex=True),\
                "serving_size_unit"] = df['serving_size']

        df.loc[(df['item_name'].str.contains(self.cleaner["serving_in_name"\
            ][0], regex=True)) & (df['item_name'].str.contains("(small|medium"
            "|large)", regex=True, flags=re.IGNORECASE)), "item_name"] = df['item_name'].str.replace(self.cleaner['serving_in_name'][0], "", regex=True)

        df.loc[df['serving_size'].str.contains(self.cleaner["ss_house"\
        ],regex=True), "serving_size_household"] = df['serving_size']
        df['serving_size_unit'] = df['serving_size_unit'].str.\
            replace(r"([1234567890\.\/])+", "", regex=True).str.strip()
        df['serving_size'] = df['serving_size'].str.\
        replace(r"([^1234567890\.\/])+", "", regex=True)
        isnum = r"^\d+([\.\/]\d{1,3})?$"
        for col in self.nutr_columns:
            logger.debug(f"colname:{col}\ndata overview:\n{df[col]}")
            df[col] = df[col].astype(str).apply(lambda x: re.sub(r'(\d+),(\d+)', r'\1\2', x))
            text_col = col + "_text"
            df[text_col] = None
            df[text_col] = df[col].astype(str)
            df[text_col] = df[text_col].str.replace("(m?g| cal|,)$", "",\
                    regex=True, flags=re.IGNORECASE).str.strip()
            is_num = df[text_col].str.contains(isnum, regex=True)
            df.loc[~is_num, col] = ""
            df.loc[is_num, col] = df[text_col]
            df.loc[is_num, text_col] = ""
            is_perc = df[text_col].str.contains("%", regex=False)
            deformatted_field = col.replace("_", " ")
            df[col] = df[col].str.replace("{}".format(deformatted_field),\
                "", regex=True, flags=re.IGNORECASE)
        caps_func = lambda x: " ".join(s if s in self.cleaner['keepcap'] else\
            string.capwords(s) for s in x.split(" "))
        df['item_name'] = df['item_name'].apply(caps_func)
        df['item_description'] = df['item_description'].apply(caps_func)
        self.nutr_df = df


def return_largest_id_plusone(table):
    largest_id = session.query(table.id).order_by(table.id.\
            desc()).first()[0]
    new_id = largest_id + 1 #return largest id in table + 1
    return new_id



class ClassMapper:
    classmapper = {
            "calculator":Calculator,
            "pdf":Pdf,
            "pdf.multi":MultiPdf,
            "webtable":WebTable,
            "webtable.reactive":WebTableReactive,
            "website":WebSite,
        }

    def run_factory(f, driver):
        classargs = {"name":f.name, "f_id":f.id, "headquarters":f.headquarters,
            "nutr_url":f.nutr_url, "menu_url":f.menu_url,
            "nutr_scraper":f.nutr_scraper, "driver":driver, "year":YEAR
        }
        nav_args = config['scrapers']['web_scrapers'][f.name] if f.name\
                in config['scrapers']['web_scrapers'] else {}
        logger.info("nav_args:{}".format(nav_args))
        classargs.update(nav_args)
        aClass = ClassMapper.classmapper[f.nutr_scraper]
        return aClass(**classargs)



def start_selenium(headless=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = headless
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    try:

        # driver = webdriver.Remote("http://host.docker.internal:4444/wd/hub",
        #             DesiredCapabilities.CHROME, options=chrome_options)
        driver = webdriver.Chrome(chrome_options=chrome_options)

    except Exception as e:
        # try:
        #     logger.warning("selenium driver startup failed. Using chromedriver"
        #             " autoinstaller instead; this may take a moment.\n"
        #             "Error:{}".format(e), exc_info=True)
        #     chromedriver_autoinstaller.install()
        # except:
        logger.warning("Selenium driver startup failed. Skipping unscraped"
            " franchises requiring selenium-based web scraping."
            "\nError:{}".format(e), exc_info=True)
        driver = None
    return driver



### COLLECTION METHODS ###
@wrap(writelog, writelog)
def collect_and_clean_annualitemdata(headless_conf=True, dryrun=False, subset=None):
    """ Scrape all menu items from sources listed in franchise table.
    Parameters
    ----------
    headless_conf : bool, optional
        Run Selenium without visible browser window (default is True)
    dryrun : bool, optional
        Execute method without writing to database (default is False)
    subset : int or list, optional
        Execute method on franchise subset (default is None)
        If int, select only franchise with matching id.
        If list, select franchises with ids equal to and between listed ints.
    """

    driver = start_selenium(headless=headless_conf)
#            filter(Franchise.nutr_scraper == "pdf").\
    menustat_query = session.query(Franchise).\
        filter(sqlalchemy.not_(Franchise.nutr_scraper == "")).\
        filter(sqlalchemy.not_(Franchise.nutr_scraper.like('%.manual')))
    if type(subset) is int:
        menustat_query = menustat_query.filter(Franchise.id == subset)
    elif type(subset) is list:
        menustat_query = menustat_query\
                .filter(Franchise.id >= subset[0])\
                .filter(Franchise.id <= subset[1])
    t = tqdm(menustat_query.all())
    for f in t:
        t.set_postfix_str("{} {}: {}".format(f.id, f.name, f.nutr_scraper))
        try:
            scraped = ClassMapper.run_factory(f, driver)
            scraped.collect_clean_sequence()
            logger.debug("pre-clean, in collect_and_clean_annualitemdata")
        except Exception as e:
            logger.warning("\nFAILURE TO COLLECT FRANCHISE\n----------------------------\nfranchise {}, name {}, scraper {}; passed without"
                " entry\nError:\n{}".format(f.id, f.name, f.nutr_scraper, e), exc_info=True)
            return
        try:
            df_obj = CollectedDf(f.name, f.id, scraped.nutr_df)
            df_obj.clean()
            df_obj.nutr_df = df_obj.nutr_df.where(pandas.notnull(df_obj.nutr_df), None)
            df_obj.add_df_to_db(dryrun=True)
            df_obj.nutr_df.insert(2, 'mi_name', None)
            df_obj.nutr_df["mi_name"] = df_obj.nutr_df['menu_item_id'].\
                apply(lambda x: MenuItem.return_menuitem_name(x))
            # df_obj.nutr_df.drop(columns="aid_objects", inplace=True)
            save_to_csv_for_review(df_obj.nutr_df, f.name, f.nutr_url, f.id, f.nutr_scraper, f.menu_scraper)
        except Exception as e:
            logger.warning("\nFAILURE TO CLEAN FRANCHISE\n--------------------------\nfranchise {}, name {}, scraper {}; passed without"
                " entry\nError:\n{}".format(f.id, f.name, f.nutr_scraper, e), exc_info=True)
    driver = None if driver == None else driver.quit()


def export_csv(csv_path, table, overwrite=False):
    """Export a database table to csv.

    Parameters
    ----------
    csv_path : string
        Filepath for exported csv.
    table :
    overwrite : (optional) boolean, default False
    """
    if not overwrite:
        if Path(csv_path).exists():
            print("File already exists! Please change the name of the existing file or the file to be created.")
            sys.exit(1)
    else:
        check = input("\nATTENTION: This function will overwrite the file at the current path ({}). Is this okay?"+' (y/n): ').lower().strip()
        if check == 'y':
            print("y -- writing table to csv.")
        elif check == 'n':
            print("n -- ending program without writing to csv")
            sys.exit(1)
        else:
            print("input not recognized; closing the program.")
            sys.exit(1)

    fmt = '%Y-%m-%d'
    table_df = pandas.read_sql_table(table, engine,
            parse_dates={"created_at": fmt, "updated_at": fmt})
    table_df.to_csv(csv_path, index=False)


def update_franchise_table_from_csv(csv_import):
    """Add rows from selected csv to franchise database table
    Try updating existing entry; if no entry exists, add new entry.

    Parameters
    ----------
    csv_import : filepath
        file must have identical layout and structure to db table.
    """
    new_db_entries = []
    new_id = return_largest_id_plusone(Franchise)
    with open(csv_import, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                q = session.query(Franchise).get(row['id'])
                if not q:
                    raise NoResultFound("no result found")
                elif q.name == row["name"]:
                    ud = {k:v for k, v in row.items() if v != getattr(q, k)}
                    ud = add_meta(ud)

                    session.query(Franchise).\
                            filter(Franchise.id == row['id']).\
                            update(ud, synchronize_session = False)
                else:
                    raise ValueError("franchise name-id mismatch!")
            except NoResultFound:
                logger.info("No match:{}\nAdding row".format(row["name"]))
                entryargs = {k:v for k, v in row.items()}
                entryargs = add_meta(entryargs, created=True)
                entryargs['id'] = new_id
                new_db_entries.append(Franchise(**entryargs))
                new_id += 1
            except ValueError as e:
                warning = "{} id {}:{}; skipping row.".format(row["name"],\
                        row['id'], e)
                logger.warning(warning)
                print(warning)
    session.add_all(new_db_entries)
    session.commit()


### REVIEW FUNCTIONS ###
def check_dfs_for_issues():
    """ Run check_df_for_issues method on all csvs in dfs_for_review directory.
    """
    fpath = "./data/dfs_for_review/"
    csvs = glob.glob("./data/dfs_for_review/*")
    for csv in csvs:
        df = pandas.read_csv(csv)
        name = str(df.loc[3, "name"])
        check_df_for_issues(name, df)


def check_df_for_issues(name, df):
    """Run series of checks on dataframe and record red flags in log file.

    The following characteristics are flagged:
    - Empty item_name column
    - Empty item_name column entries
    - Empty calories column
    - Empty calories column entries

    Parameters
    ----------
    name : string
        Name of the franchise.
    df : DataFrame
        Dataframe with the structure of those produced by the
        collect_and_clean_annualitemdata method.
    """
    issue_list = []
    null_valued = df.replace(r'^\s*$', np.nan, regex=True)
    if df.empty:
        issue_list.append("Empty DF")
    valuecheck = ["calories", "item_name"]
    for value in valuecheck:
        if null_valued[value].isnull().all():
            issue = "No {} values".format(value)
            issue_list.append(issue)
        elif null_valued[value].isnull().any():
            missing = null_valued.loc[null_valued[value].isnull()]
            if value == "calories":
                missing = missing.loc[missing["calories_text"].isnull()]
            missing_len = str(len(missing.index))
            issue = "Missing {} values: {}".format(value, missing_len)
            issue_list.append(issue)
    if issue_list:
        issues = '\n'.join('{}' for _ in range(len(issue_list))).format(*issue_list)
        logger.warning(f"ISSUES FOUND FOR {name}\nissues:\n{issues}")

    # add condition to check number of entries without matches

def save_to_csv_for_review(nutr_df, name, url, f_id, nutr_scraper, menu_scraper):
    to_csv_df = nutr_df.copy()
    to_csv_df['name'] = name
    if "iurl" not in to_csv_df:
        to_csv_df['iurl'] = url
    to_csv_df['f_id'] = f_id
    to_csv_df['nutr_scraper'] = nutr_scraper
    to_csv_df['menu_scraper'] = menu_scraper
    prepped_id = "{}{}".format("0"*(3-len(str(f_id))),f_id)
    to_csv_df.to_csv("data/dfs_for_review/{}-{}.csv".format(prepped_id,\
            name.lower().replace("/", "_")), index=False)
