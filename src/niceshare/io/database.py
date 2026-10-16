from typing import Literal

import duckdb
from polars import DataFrame

from niceshare.helper.config import settings
from niceshare.helper.logger import LOGGER
from niceshare.helper.paths import get_path
from niceshare.io.warehouse import Warehouse


""" Handler for Inventory and Request Databse (duckdb)"""

class DB:
    """ Database Class
    """

    # Path constants to the file
    Inventory_DB = get_path(settings.data_filename).with_suffix(".duckdb")
    Request_DB = get_path(settings.requests["filename"]).with_suffix(".duckdb")

    @classmethod
    def save(cls, name: str, df: DataFrame, db: Literal["inventory", "request"]) -> None:
        """ Save Data to Database 

        Args:
            cls: #TODO
            name (str): #TODO
            df (DataFrame): #TODO
            db (Literal["inventory", "request"]): #TODO

        """

        file = cls.Inventory_DB if db == "inventory" else cls.Request_DB
        with duckdb.connect(file, read_only=False) as con:
            con.sql(f"DROP TABLE IF EXISTS {name}")
            con.sql(f"CREATE TABLE {name} AS SELECT * FROM df")

    @classmethod
    def load(cls, name: str, db: Literal["inventory", "request"]) -> Warehouse:
        """ Load Data from Database 

        Args:
            cls: #TODO
            name (str): #TODO
            df (DataFrame): #TODO
            db (Literal["inventory", "request"]): #TODO

        Returns:
            Warehouse: #TODO

        """
        
        LOGGER.debug(f"Trying to load {name} from database {cls.Inventory_DB.name}...")
        file = cls.Inventory_DB if db == "inventory" else cls.Request_DB
        
        if not file.exists():
            LOGGER.error("Database inventory does not exist")
            raise FileNotFoundError
            
        with duckdb.connect(database=file, read_only=True) as con:
            # Creates Polar Dataframe from read-only duckdb database 
            # TODO WHY Tf
            df = con.query(f"SELECT * FROM {name}").pl()
            return Warehouse(name, df)

