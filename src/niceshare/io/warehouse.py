from dataclasses import dataclass
from typing import override

import polars as pl
from polars import DataFrame
from slugify import slugify

from niceshare.helper.config import settings
from niceshare.helper.logger import LOGGER
from niceshare.io.cache import Cache
from niceshare.io.wiki import MenuItem

""" Warehouse Data Module """

columns = settings.columns
WAREHOUSE_ROOT = slugify(settings.warehouse["label"])

@dataclass
class Warehouse(MenuItem):
    """Warehouse Class 
    """
    name: str
    inventory: DataFrame

    @override
    @property
    def children(self) -> list[str]:
        """#TODO
        """
        return self.categories

    @override
    @property
    def routes(self) -> dict[str, str]:
        """#TODO
        """
        routes: dict[str, str] = {}
        for category in self.categories:
            routes.update({category: f"/{WAREHOUSE_ROOT}/{slugify(self.name)}/{slugify(category)}"})
        return routes

    @classmethod
    def create(cls, name: str, df: DataFrame):
        """#TODO
        """
        LOGGER.debug(f"Creating warehouse {name}...")
        # with pl.Config(tbl_cols=-1):
        #   print(df.filter(pl.col(columns["object"]).str.contains("regal")))
        df = df.with_columns(
            [
                pl.col(columns["count"]).cast(pl.Int64, strict=False),
                pl.col(columns["weight"]).cast(pl.Float64, strict=False),
                pl.col(columns["count"]).alias(columns["total"]).cast(pl.Int64, strict=False),
            ]
        )
        if columns["total_weight"] not in df.columns:
            df.insert_column(1, (pl.col(columns["count"]) * pl.col(columns["weight"])).alias(columns["total_weight"]))
        else:
            df.with_columns(pl.col(columns["count"]) * pl.col(columns["weight"]).alias(columns["total_weight"]))
        warehouse = cls(name=name, inventory=df.select([c for c in columns.values()]).with_row_index())
        warehouse.inventory.insert_column(0, (pl.lit(name)).alias(settings.warehouse["label"]))
        LOGGER.info(f"Successfully created warehouse {name}")
        return warehouse

    @property
    def categories(self) -> list[str]:
        """#TODO
        """
        c = [settings.warehouse["selection"], self.name]
        try:
            c.extend(sorted(self.inventory[settings.columns["category"]].unique()))
        except (AttributeError, TypeError):
            raise AttributeError(
                "It seems like you have used a category that is not sortable."
                "\nPlease review the categories used in the category column of the inventory file."
                "\nCheck for empty cells, and stuff like numbers, non-ascii-characters, etc."
            )
        return c

    def selected(self) -> DataFrame:
        """#TODO
        """
        return self.inventory.filter(pl.arange(0, self.inventory.height).is_in(Cache.selected(self.name)))

    # TODO Maybe remove async and await, why are they needet?
    async def total_weight(self) -> int:
        """#TODO
        """
        df = await self.get_final()
        return df.select(columns["total_weight"]).sum().cast(pl.Int64).item()

    # TODO Maybe remove async and await, why are they needet?
    async def get_final(self) -> DataFrame:
        """#TODO
        """
        df = self.inventory
        for row_idx, value in Cache.amounts(self.name).items():
            df[int(row_idx), columns["count"]] = value
        return (
            df.filter(pl.arange(0, self.inventory.height).is_in(Cache.selected(self.name))).drop("index")
        ).with_columns((pl.col(columns["count"]) * pl.col(columns["weight"])).alias(columns["total_weight"]))