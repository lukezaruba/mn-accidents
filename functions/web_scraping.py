#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Function to scrape and transform incidents from the past two weeks,
identify the records not currently in the database, and load the
new records into the database.

@Author: Luke Zaruba
@Date: Aug 2, 2023
@Version: 0.0.0
"""

import json
import os
import re
from datetime import date, timedelta

import functions_framework
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import INTEGER, TEXT, TIMESTAMP, create_engine, text
from sqlalchemy.engine import URL
import psycopg2


class QueryURLs:
    def __init__(
        self,
        start_month: str,
        start_day: str,
        start_year: str,
        end_month: str,
        end_day: str,
        end_year: str,
    ) -> None:
        """Class for identifying relevant accident records within a timeframe.

        Args:
            start_month (str): Month of begin date for query.
            start_day (str): Day of begin date for query.
            start_year (str): Year of begin date for query.
            end_month (str): Month of end date for query.
            end_day (str): Day of end date for query.
            end_year (str): Year of end date for query.
        """
        self.start_day = start_day
        self.start_month = start_month
        self.start_year = start_year
        self.end_day = end_day
        self.end_month = end_month
        self.end_year = end_year
        self.base_url = f"https://app.dps.mn.gov/MSPMedia2/Ajax_SearchByDate?BegDate={start_month}%2F{start_day}%2F{start_year}&EndDate={end_month}%2F{end_day}%2F{end_year}&IncidentSearchType=&_=1684436978172"
        self.pages = self._find_last_page()

    def search(self) -> list:
        """Method for retrieving list of relevant accident records.

        :return list: List of accident IDs to pass as URL parameter.
        """
        # Iteratively Request for each page in search
        all_records = []

        for pg in range(1, self.pages + 1):
            page_url = self._generate_page_url(pg)

            page_records = self._find_records_from_single_page(page_url)

            all_records += page_records

        return all_records

    def _find_last_page(self) -> int:
        # Request
        r = requests.get(self.base_url)

        # Scrape
        soup = BeautifulSoup(r.text, features="html.parser")

        last_page = soup.find("li", {"class": "PagedList-skipToLast"})
        last_page_num = int(
            str(last_page).split("?")[1].split("&")[0].replace("page=", "")
        )

        return last_page_num

    def _generate_page_url(self, page_number: int) -> str:
        # Insert page param into base URL
        split_url = self.base_url.split("?")

        new_url = split_url[0] + f"?page={page_number}&" + split_url[1]

        return new_url

    @staticmethod
    def _find_records_from_single_page(url) -> list:
        # Request
        r = requests.get(url)

        # Scrape
        soup = BeautifulSoup(r.text, features="html.parser")

        numbers = []

        for link in soup.findAll("a"):
            l = link.get("href")
            if "/MSPMedia2/IncidentDisplay/" in str(l):
                numbers.append(int(l.replace("/MSPMedia2/IncidentDisplay/", "")))

        return numbers


class ScrapeRecords:
    def __init__(self, record_list: list) -> None:
        """
        Class for extracting accident records based on list of unique accident IDs for URL parameter.

        Args:
            record_list (list): List of accident IDs to pass as URL parameter.
        """
        self.record_list = record_list
        self._incident_type = []
        self._incident_icr = []
        self._incident_date = []
        self._incident_district = []
        self._incident_location = []
        self._incident_condition = []
        self._incident_num_vehicles = []

    def scrape(self) -> None:
        """Method for extracting relevant accident data for all records."""
        # Create Empty List for Vehicle DFs
        vehicle_df_list = []

        # Loop through Record IDs
        for record_id in self.record_list:
            try:
                url = f"https://app.dps.mn.gov/MSPMedia2/IncidentDisplay/{record_id}"

                soup = self._scrape_single_record(url)

                vehicle_df_list.append(self._get_vehicle_data(soup))
            except:
                pass

        # Convert to DF
        self.scraped_accident_df = pd.DataFrame(
            list(
                zip(
                    self._incident_icr,
                    self._incident_type,
                    self._incident_date,
                    self._incident_district,
                    self._incident_location,
                    self._incident_condition,
                    self._incident_num_vehicles,
                )
            ),
            columns=[
                "icr",
                "incident_type",
                "incident_date",
                "district",
                "location_description",
                "road_condition",
                "vehicles_involved",
            ],
        )

        self.scraped_accident_df["vehicles_involved"] = (
            self.scraped_accident_df["vehicles_involved"]
            .str.split(" ")
            .str[0]
            .astype(int)
        )

        # Vehicles DF
        try:
            self.scraped_vehicles_df = pd.concat(vehicle_df_list).reset_index()

            self.scraped_vehicles_df[["gender", "age"]] = self.scraped_vehicles_df.iloc[
                :, 3
            ].str.split(" Age: ", expand=True)

            self.scraped_vehicles_df = self.scraped_vehicles_df.drop(
                self.scraped_vehicles_df.columns[3], axis=1
            )

            self.scraped_vehicles_df.columns = [
                "person_name",
                "vehicle",
                "residence",
                "person_role",
                "injury",
                "helmet",
                "seatbelt",
                "alcohol",
                "icr",
                "gender",
                "age",
            ]

        except:
            print("Vehicles DF is empty.")

    def _scrape_single_record(self, url: str) -> None:
        r = requests.get(url)

        soup = BeautifulSoup(r.text, features="html.parser")

        # Get Data
        incident_type_soup = str(soup.find("div", {"class": "col-md-1 col-xs-7"}))
        incident_icr_soup = str(soup.find("div", {"class": "col-md-2 col-xs-2"}))
        incident_date_soup = str(soup.find("div", {"class": "col-md-2 col-xs-8"}))
        incident_district_soup = str(soup.find("div", {"class": "col-md-2 col-xs-9"}))
        incident_location_soup = str(soup.find("div", {"class": "col-md-8 col-xs-12"}))
        incident_condition_soup = str(
            soup.findAll("div", {"class": "col-md-2 col-xs-4"})[1]
        )
        try:
            incident_num_vehicles_soup = str(soup.findAll("strong")[1])
        except:
            incident_num_vehicles_soup = ">Unknown<"

        # Append Data
        self._incident_type.append(self._format_string(incident_type_soup))
        self._incident_icr.append(self._format_string(incident_icr_soup))
        self._incident_date.append(self._format_string(incident_date_soup))
        self._incident_district.append(self._format_string(incident_district_soup))
        self._incident_location.append(self._format_string(incident_location_soup))
        self._incident_condition.append(self._format_string(incident_condition_soup))
        self._incident_num_vehicles.append(
            self._format_string(incident_num_vehicles_soup)
        )

        return soup

    @staticmethod
    def _format_string(text: str) -> str:
        formatted = text.split(">")[1].split("<")[0].strip("\r\n ")

        return formatted

    def _get_vehicle_data(self, soup: str) -> list:
        raw_str = ""
        my_test_dict = dict()
        names = dict()

        airbags = []
        roles = []
        injuries_and_helmets = []
        seatbelts = []
        alc = []

        # Gets all of the data into a single string, sep by \n
        for v in soup.findAll("div", {"class": "col-md-12 col-xs-12"}):
            line = self._format_string(str(v))
            if len(line) > 1:
                raw_str += line + "\n"

        # Split Attrs by Line
        split_info = raw_str.split("\n")

        # Loop through Attrs
        try:
            for i in range(len(split_info) - 1):
                # If First Char is Num --> this line is a vehicle
                if split_info[i][0].isdigit():
                    # Add as new key in dict
                    my_test_dict[split_info[i]] = []
                # If First Char is NOT Num --> this line is an attr
                else:
                    # Add this line to the val list of the most recent key that was added
                    # Are dicts ordered now in python? Check this -- used to not be
                    my_test_dict[list(my_test_dict.keys())[-1]].append(split_info[i])
        except:
            return

        # CHECKING VALIDITY OF PAGE
        for i in list(my_test_dict.values()):
            if len(i) % 3 != 0:
                return

        # Loop through Vehs
        for i in list(my_test_dict.values()):
            # Loop through All Vals of Veh -- only getting person names
            for j in range(0, len(i), 3):
                # Person as key -- car, hometown, gender/age as vals
                names[i[j]] = [
                    list(my_test_dict.keys())[list(my_test_dict.values()).index(i)],
                    i[j + 1],
                    i[j + 2],
                ]

        # Airbags
        for veh in soup.findAll("div", {"class": "col-md-1 col-xs-2"}):
            if len(veh) > 1:
                airbags.append(self._format_string(str(veh)))

        # Role
        for role in soup.findAll("div", {"class": "person-role"}):
            roles.append(self._format_string(str(role)))

        # Injury
        for ih in soup.findAll("div", {"class": "col-md-2 col-xs-6"}):
            x = self._format_string(str(ih))
            if len(x) > 1:
                injuries_and_helmets.append(x)

        injuries = [
            injuries_and_helmets[i]
            for i in range(len(injuries_and_helmets))
            if i % 2 == 0
        ]
        helmets = [
            injuries_and_helmets[i]
            for i in range(len(injuries_and_helmets))
            if i % 2 != 0
        ]

        # Seat Belt
        for sb in soup.findAll("div", {"class": "col-md-2 col-xs-8"}):
            t = self._format_string(str(sb))
            if len(t) > 1:
                if not t[0].isdigit():
                    seatbelts.append(t)

        # Alcohol
        for a in soup.findAll("div", {"class": "col-md-3 col-xs-2"}):
            alc.append(self._format_string(str(a)))

        # ICR for Joining
        icr = self._format_string(str(soup.find("div", {"class": "col-md-2 col-xs-2"})))

        # To DF
        try:
            ppl_df = pd.DataFrame.from_dict(names, orient="index")

            ppl_df["role"] = roles
            ppl_df["injuries"] = injuries
            ppl_df["helmets"] = helmets
            ppl_df["seatbelts"] = seatbelts
            ppl_df["alc"] = alc
            ppl_df["icr"] = icr

            return ppl_df

        except:
            return


class Loader:
    def __init__(self, icr_list, accident_df, vehicle_df):
        self._incoming_icr_ints = [int(i) for i in icr_list]
        self.db_url = URL.create(
            drivername="postgresql",
            username=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"],
        )
        self.db = create_engine(self.db_url)

        self.existing_icr = self._get_current_icr()
        self.new_icr = [
            icr for icr in self._incoming_icr_ints if icr not in self.existing_icr
        ]
        self.accident_df = accident_df[accident_df["icr"].isin(self.new_icr)]
        self.vehicle_df = vehicle_df[vehicle_df["icr"].isin(self.new_icr)]

    def _get_current_icr(self):
        query = "SELECT icr FROM raw_accidents"

        # Execute the query and fetch all results
        with self.db.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()

            existing_icr = [row[0] for row in rows]

        return existing_icr

    def _load_accidents(self):
        # Standardize Schema/Dtypes
        dtypes_dict = {
            "incident_type": str,
            "icr": int,
            "district": str,
            "location_description": str,
            "road_condition": str,
            "vehicles_involved": int,
        }

        self.accident_df["incident_date"] = pd.to_datetime(
            self.accident_df["incident_date"], format="%m/%d/%Y %H:%M"
        )

        self.accident_df = self.accident_df.astype(dtypes_dict)

        # Location Description Space Fix
        self.accident_df["location_description"] = self.accident_df[
            "location_description"
        ].apply(lambda val: re.sub("\s+", " ", val))

        # Duplicate Check
        primary_key = ["icr"]

        self.accident_df = self.accident_df.drop_duplicates(
            subset=primary_key, keep="first"
        )

        # Load
        self.accident_df.to_sql(
            "raw_accidents",
            self.db,
            if_exists="append",
            index=False,
            dtype={
                "icr": INTEGER,
                "incident_type": TEXT,
                "incident_date": TIMESTAMP,
                "district": TEXT,
                "location_description": TEXT,
                "road_condition": TEXT,
                "vehicles_involved": INTEGER,
            },
        )

    def _load_vehicles(self):
        # Standardize Schema/Dtypes
        dtypes_dict = {
            "person_name": str,
            "vehicle": str,
            "residence": str,
            "person_role": str,
            "injury": str,
            "helmet": str,
            "seatbelt": str,
            "alcohol": str,
            "icr": int,
            "gender": str,
            "age": int,
        }

        self.vehicle_df = self.vehicle_df.astype(dtypes_dict)

        # Name Space Fix
        self.vehicle_df["person_name"] = self.vehicle_df["person_name"].apply(
            lambda val: re.sub("\s+", " ", val)
        )

        # Duplicate Check
        composite_key = ["person_name", "icr"]

        self.vehicle_df = self.vehicle_df.drop_duplicates(
            subset=composite_key, keep="first"
        )

        # Load
        self.vehicle_df.to_sql(
            "raw_people",
            self.db,
            if_exists="append",
            index=False,
            dtype={
                "person_name": TEXT,
                "vehicle": TEXT,
                "residence": TEXT,
                "person_role": TEXT,
                "injury": TEXT,
                "helmet": TEXT,
                "seatbelt": TEXT,
                "alcohol": TEXT,
                "icr": INTEGER,
                "gender": TEXT,
                "age": INTEGER,
            },
        )

    def load(self):
        if not len(self.new_icr) == 0:
            self._load_vehicles()
            self._load_accidents()

        return self.new_icr


def main(debug=False):
    if debug:
        start_day = "01"
        end_day = "02"
        start_month = end_month = "01"
        start_year = end_year = "2023"

    else:
        today = date.today()
        delta = timedelta(weeks=2)
        start_date = today - delta

        start_year, start_month, start_day = (
            str(start_date).split("-")[0],
            str(start_date).split("-")[1],
            str(start_date).split("-")[2],
        )

        end_year, end_month, end_day = (
            str(today).split("-")[0],
            str(today).split("-")[1],
            str(today).split("-")[2],
        )

    query = QueryURLs(start_month, start_day, start_year, end_month, end_day, end_year)
    record_urls = query.search()

    scraper = ScrapeRecords(record_urls)

    scraper.scrape()

    incident_results = scraper.scraped_accident_df
    vehicle_results = scraper.scraped_vehicles_df
    icr_list = list(set(scraper.scraped_accident_df["icr"]))

    loader = Loader(icr_list, incident_results, vehicle_results)

    load_results = loader.load()

    print(json.dumps({"icr": load_results}))
    return json.dumps({"icr": load_results})


if __name__ == "__main__":
    main(debug=True)
