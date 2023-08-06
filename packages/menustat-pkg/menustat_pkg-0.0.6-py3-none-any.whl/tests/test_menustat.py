#!/usr/bin/env python

"""Tests for `menustat` package."""

import os
import logging
import unittest
import numpy.testing as npt
import pandas.testing as pdt
from urllib.request import Request, urlopen

import yaml
import pandas
from selenium import webdriver

from menustat import menustat


class TestMenustat(unittest.TestCase):
    """Tests for `menustat` package."""


    output_dir = "testsuite/testoutput/"

    logging.basicConfig(filename=f"{output_dir}test_record.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)


    with open(r"testsuite/testscrapeconfig.yaml") as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)


    ### Test Data###
    util_test_s = {     0: ["", "", "", "xxx", "","",""],
                        1: ["", "Cals",	"", "xxx", "","Cals",""],
                        2: ["Fat", "", "Cals", "xxx", "Fat", "", "Cals"],
                        3: ["Fat", "", "(g)", "xxx", "Fat", "", "(g)"],
                        4: ["Sat", "", "(g)", "xxx", "Sat", "", "(g)"],
                        5: ["Tran", "", "(g)", "xxx", "Tran", "", "(g)"],
                        6: ["Chol", "", "(mg)", "xxx", "Chol", "", "(mg)"],
                        7: ["Sod", "", "(mg)", "xxx", "Sod", "", "(mg)"],
                        8: ["Carbs", "", "(g)", "xxx", "Carbs", "", "(g)"],
                        9: ["Fiber", "", "(g)", "xxx", "Fiber", "", "(g)"],
                        10:["Sug", "", "(g)", "xxx", "Sug", "", "(g)"],
                        11:["Prot", "", "(g)", "xxx", "Prot", "", "(g)"]   }

    util_test_e_headrow = {  0: ["  ",          "xxx",  "  "],
                        1:      [" Cals ",      "xxx",  " Cals "],
                        2:      ["Fat  Cals",   "xxx",  "Fat  Cals"],
                        3:      ["Fat  (g)",    "xxx",  "Fat  (g)"],
                        4:      ["Sat  (g)",    "xxx",  "Sat  (g)"],
                        5:      ["Tran  (g)",   "xxx",  "Tran  (g)"],
                        6:      ["Chol  (mg)",  "xxx",  "Chol  (mg)"],
                        7:      ["Sod  (mg)",   "xxx",  "Sod  (mg)"],
                        8:      ["Carbs  (g)",  "xxx",  "Carbs  (g)"],
                        9:      ["Fiber  (g)",  "xxx",  "Fiber  (g)"],
                        10:     ["Sug  (g)",    "xxx",  "Sug  (g)"],
                        11:     ["Prot  (g)",   "xxx",  "Prot  (g)"]   }

    util_test_e_rename = {0: [1,"", "", "", "xxx", "","",""],
                        1: [2,"", "Cals",	"", "xxx", "","Cals",""],
                        2: [4,"Fat", "", "(g)", "xxx", "Fat", "", "(g)"],
                        3: [5,"Sat", "", "(g)", "xxx", "Sat", "", "(g)"],
                        4: [7,"Chol", "", "(mg)", "xxx", "Chol", "", "(mg)"],
                        5: [8,"Sod", "", "(mg)", "xxx", "Sod", "", "(mg)"],
                        6: [9,"Carbs", "", "(g)", "xxx", "Carbs", "", "(g)"],
                        7: [11,"Sug", "", "(g)", "xxx", "Sug", "", "(g)"]
                        }
    util_test_e_oneval = { 1: ["","Cals","","","","","","","","","",""],
                            5: ["","Cals","","","","","","","","","",""]}

    util_test_e_firstrow_header = {
                        " Cals ":       [" Cals ",      "xxx",  " Cals "],
                        "Fat  Cals":    ["Fat  Cals",   "xxx",  "Fat  Cals"],
                        "Fat  (g)":     ["Fat  (g)",    "xxx",  "Fat  (g)"],
                        "Sat  (g)":     ["Sat  (g)",    "xxx",  "Sat  (g)"],
                        "Tran  (g)":    ["Tran  (g)",   "xxx",  "Tran  (g)"],
                        "Chol  (mg)":   ["Chol  (mg)",  "xxx",  "Chol  (mg)"],
                        "Sod  (mg)":    ["Sod  (mg)",   "xxx",  "Sod  (mg)"],
                        "Carbs  (g)":   ["Carbs  (g)",  "xxx",  "Carbs  (g)"],
                        "Fiber  (g)":   ["Fiber  (g)",  "xxx",  "Fiber  (g)"],
                        "Sug  (g)":     ["Sug  (g)",    "xxx",  "Sug  (g)"],
                        "Prot  (g)":    ["Prot  (g)",   "xxx",  "Prot  (g)"]   }

    ### Setup functions ###

    def start_driver():
        options = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        DRIVER_PATH = os.environ["CHROMEDRIVER_PATH"]
        driver = webdriver.Chrome(executable_path=DRIVER_PATH,
                options=options)
        return driver

    def return_csv_names(filehead, n, prefix="testsuite/testdata/"):
        df_files = ["{}{}{}.csv".format(prefix,filehead, i) for i in range(1, n+1)]
        return df_files


    ### Test Classes ###

    class TestUtils(unittest.TestCase):
        def __init__(self, *args, **kwargs):
            unittest.TestCase.__init__(self,*args,**kwargs)


        def test_recombine_rows():
            df = pandas.DataFrame(data=headrow_test_s)
            nutri_rows = find_rows_with_val(df, r"Fat.*Sat.*Prot")
            combiners = [[i, i+2] for i in nutri_rows.index.tolist()]
            droprows = []
            for l in combiners:
                for i in range(l[-1]-l[0]):
                    n = 1+i
                    df = recombine_rows(df, l[0], l[0]+n)
                    droprows.append(l[0]+n)
            df.drop(df.index[droprows], inplace=True)
            df.reset_index(drop=True, inplace=True)
            df2 = pandas.DataFrame(data=util_test_e_headrow)
            pdt.assert_frame_equal(df, df2, check_dtype=False, check_index_type=False, check_frame_type=False)

        def test_rename_cols_by_index():
            df = pandas.DataFrame(data=util_test_s)
            df = df[[1,2,4,5,7,8,9,11]]
            df = rename_cols_by_index(df)
            df2 = pandas.DataFrame(data=util_test_e_rename)
            print(df)
            print(df2)
            pdt.assert_frame_equal(df, df2, check_dtype=False, check_index_type=False, check_frame_type=False)

        def test_return_rows_with_one_value():
            df = pandas.DataFrame(data=util_test_s)
            df = return_rows_with_one_value(df)
            df2 = pandas.DataFrame.from_dict(util_test_e_oneval, orient='index')
            pdt.assert_index_equal(df.index, df2.index)

        def test_set_first_row_as_header():
            df = pandas.DataFrame(data=util_test_e_headrow)
            df.drop(columns=0, inplace=True)
            df = set_first_row_as_header(df)
            df2 = pandas.DataFrame(data=util_test_e_firstrow_header)
            pdt.assert_frame_equal(df, df2, check_dtype=False, check_index_type=False, check_frame_type=False)


    class TestPdf(unittest.TestCase):
        def __init__(self):
            self.dummyobj = MenuStat.Pdf("dummy", 00, "nutri_url")


        def _iterate_through_pdf_dfs(foo):
            """
            Run a given test on all currently scraped PDFs.
            """
            def wrapper( self ) :
                for filename in os.listdir("./data/2021/pdf_scrapes/"):
                    if filename.endswith(".csv"):
                        fid = int(filename.replace(".csv", ""))
                        f = MenuStat.session.query(MenuStat.Franchise).\
                            filter(MenuStat.Franchise.id == fid).one()
                        self.dummyobj = MenuStat.scraperfactory(f, None)
                        filepath = f"./data/2021/pdf_scrapes/{filename}"
                        logger.info(f"\n\n\nFILE: {filename}\n")
                        self.dummyobj.nutr_df = pandas.read_csv(filepath)
                        foo( self )
            return wrapper


        @_iterate_through_pdf_dfs
        def test_id_format_header_rows(self):
            logger.info(f"test_id_format_header_rows S:\n{self.dummyobj.nutr_df}")
            self.dummyobj.detect_and_remove_allergy_cols()
            self.dummyobj.nutr_df = self.dummyobj.nutr_df.fillna("")
            self.dummyobj.id_format_header_rows()
            self.dummyobj.nutr_df.fillna("", inplace=True)
            self.dummyobj.nutr_df = delete_all_na(self.dummyobj.nutr_df, subset="cols")
            logger.info(f"test_id_format_header_rows E:\n{self.dummyobj.nutr_df}")


        def test_combine_groups_jimmyjohn(self):
            self.dummyobj = MenuStat.JimmyJohns("dummy", 00, "nutri_url")
            self.dummyobj.nutr_df = pandas.DataFrame([
                ["","cals","cals","cals","fat","fat","fat","sat","sat","sat"],
                ["",      "U","8F","16F","U","8F","16F","U","8F","16F"],
                ["SLIM 1",190, 540, 560, 1080,100, 120, 180, 240, 11],
                ["SLIM 2", 90, 440, 460,  880, 25,  45, 110, 90,  3],
                ["SLIM 3",250, 600, 610, 1200,180, 210, 270, 410, 20]],
                index=[0,1,2,3,4], columns=[0,1,2,3,4,5,6,7,8,9])
            print("self.dummyobj.nutr_df\n",self.dummyobj.nutr_df)
            df = self.dummyobj.combine_groups(self.dummyobj.nutr_df, 1)
            df2 = pandas.DataFrame([
                # ["item_name","cals","fat","sat"],
                [  "SLIM 1, U", 190,  1080,  180],
                [  "SLIM 2, U",  90,   880,  110],
                [  "SLIM 3, U", 250,  1200,  270],
                [ "SLIM 1, 8F", 540,   100,  240],
                [ "SLIM 2, 8F", 440,    25,   90],
                [ "SLIM 3, 8F", 600,   180,  410],
                ["SLIM 1, 16F", 560,   120,   11],
                ["SLIM 2, 16F", 460,    45,    3],
                ["SLIM 3, 16F", 610,   210,   20],
                ],
                columns=["item_name","cals","fat","sat"], index=[0,1,2,3,4,5,6,7,8])
            pdt.assert_frame_equal(df, df2, check_dtype=False, check_index_type=False, check_frame_type=False)



        @_iterate_through_pdf_dfs
        def test_identify_all_header_rows(self):
            headers = self.dummyobj.identify_all_header_rows()
            print(headers)

        @_iterate_through_pdf_dfs
        def test_make_corrections(self):
            logger.info(f"test_make_corrections START:{self.dummyobj.f_id} {self.dummyobj.name}\n{self.dummyobj.nutr_df}")
            try:
                self.dummyobj.make_corrections()
                self.dummyobj.nutr_df.to_csv(output_dir+f"{self.dummyobj.f_id}.csv", index=False)
            except Exception as e:
                msg = f"ERROR PROCESSING {self.dummyobj.f_id} {self.dummyobj.name}"
                logger.warning(f"{msg}\nERROR: {e}", exc_info=True)
                print(f"{msg}; CHECK LOGS")
            logger.info(f"test_make_corrections END:{self.dummyobj.f_id} {self.dummyobj.name}\n{self.dummyobj.nutr_df}")


        @_iterate_through_pdf_dfs
        def test_move_notes(self):
            self.dummyobj.nutr_df['notes'] = ""
            rename_dict = {"0":"item_name", "1":"menu_section"}
            self.dummyobj.nutr_df.rename(columns=rename_dict, inplace=True)
            logger.info(f"pre-move_notes:\n{self.dummyobj.nutr_df}")

            self.dummyobj.move_notes()
            check = self.dummyobj.nutr_df.loc[self.dummyobj.nutr_df.notes != ""]
            if not check.empty:
                logger.info(f"post-move_notes:\n{check}")

        # @_iterate_through_pdf_dfs
        def test_detect_and_split_multisize_rows(self):
            self.dummyobj.nutr_df = pandas.DataFrame([
            ["Black Tea, Regular /Large", "Beverages", "600/960", "195/312", "0/0", "0/0", "0/0", "0/0"],
            ["Green Tea, Regular /Large", "Beverages", "600/960", "200/320", "0/0", "0/0", "0/0", "0/0"],
            ["White Tea, Regular /Large", "Beverages", "600/960", "2/3", "0/0", "0/0", "0/0", "0/0"],
            ["Jasmine Tea, (Regular/Large)", "Beverages", "600/960", "2/3", "0/0", "0/0", "0/0", "0/0"]],
            columns=["item_name", "menu_section", "serving_size", "calories", "total_fat", "saturated_fat", "trans_fat", "chol"], index=[69,70,71,72])

            df2 = pandas.DataFrame([
            ["Black Tea, Regular ", "Beverages", 600, 195, 0, 0, 0, 0],
            ["Black Tea, Large",    "Beverages", 960, 312, 0, 0, 0, 0],
            ["Green Tea, Regular ", "Beverages", 600, 200, 0, 0, 0, 0],
            ["Green Tea, Large",    "Beverages", 960, 320, 0, 0, 0, 0],
            ["White Tea, Regular ", "Beverages", 600,   2, 0, 0, 0, 0],
            ["White Tea, Large",    "Beverages", 960,   3, 0, 0, 0, 0],
            ["Jasmine Tea, Regular","Beverages", 600,   2, 0, 0, 0, 0],
            ["Jasmine Tea, Large",  "Beverages", 960,   3, 0, 0, 0, 0]],
            columns=["item_name", "menu_section", "serving_size", "calories", "total_fat", "saturated_fat", "trans_fat", "chol"], index=[0,1,2,3,4,5,6,7]
            )
            print(self.dummyobj.nutr_df)
            # self.dummyobj.nutr_df = pandas.read_csv("./data/2021/pdf_scrapes/22.csv")
            # self.dummyobj.nutr_df.rename(columns={"0":"item_name"}, inplace=True)
            self.dummyobj.detect_and_split_multisize_rows()
            print(self.dummyobj.nutr_df)

        def test_add_section_labels(self):
            df = pandas.read_csv("testsuite/testdata/test_add_section_labels_s.csv")
            df = df.fillna("")
            idxs = df.loc[df['1'].str.contains("12")].index
            df.insert(2, "2", "")
            df = self.dummyobj.add_section_labels(df, idxs, "2", [2], src_col="0")
            df.loc[0, "2"] = df.loc[0]["0"]
            logger.info(f"next:\n{df}")
            df["0"] = df["2"]
            df.drop(columns="2", inplace=True)
            logger.info(f"last:\n{df}")


        def test_prep_unaligned_table(self):
            dataframe_files = return_csv_names("prep_unaligned_table", 3)
            frames = []
            for file in dataframe_files:
                df = pandas.read_csv(file)
                self.dummyobj.prep_unaligned_table(df)
                frames.append(df)
            result = pandas.concat(frames)
            result = result.reset_index(drop=True)
            # print(result)
            # result.to_csv("testsuite/testdata/df_to_combine_combined.csv", index=False)
            combined = pandas.read_csv("testsuite/testdata/prep_unaligned_table"
                ".csv", header="infer", index_col=False, encoding="utf-8", dtype=str)
            combined.fillna("", inplace=True)
            # print(combined)
            # print(result["protein"].values, combined["protein"].values)
            pdt.assert_frame_equal(result, combined, check_dtype=False, check_index_type=False, check_frame_type=False)

        def test_add_header_categories(self):
            pass


        def test_add_name_to_sizes(self):
            """
            Tests MenuStat.Pdf.add_name_to_sizes(self, names, cats).
            """
            df_files = return_csv_names('add_name_to_sizes', 2)
            frames = [pandas.read_csv(file) for file in df_files]
            for idx, frame in enumerate(frames):
                frame.fillna("", inplace=True)
                self.dummyobj.nutr_df = frame
                cats = return_rows_with_one_value(self.dummyobj.nutr_df)
                # print(cats)
                self.dummyobj.add_name_to_sizes(cats)
                self.dummyobj.nutr_df = self.dummyobj.nutr_df.reset_index(drop=True)
                # self.dummyobj.nutr_df.to_csv("testsuite/testdata/add_name_to_sizes{}A.csv".format(idx+1), index=False)
                print(self.dummyobj.nutr_df)
                result = pandas.read_csv("testsuite/testdata/add_name_to_sizes{}A.csv".format(idx+1))
                result.fillna("", inplace=True)
                print(result)
                pdt.assert_series_equal(self.dummyobj.nutr_df['item_name'], result['item_name'])


    def test_nav_sizes_customizations():
        driver = start_driver()
        dconf = settings['nav_sizes_customizations']
        dummyobj = MenuStat.SiteNav("dummy", 00, dconf['url'], driver, **dconf)
        dummyobj.nutr_df = pandas.DataFrame()
        print(dummyobj.__dict__)
        dummyobj.nutr_df = dummyobj.nutr_df.append({'item_name':dconf['item_name']},\
                ignore_index=True)
        driver.get(dconf['url'])
        for index, row in dummyobj.nutr_df.iterrows():
            dummyobj.nav_sizes_customizations(dummyobj.nutr_df, row)
        print(dummyobj.nutr_df)
