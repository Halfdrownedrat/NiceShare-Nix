"""Module for loading data from Nextcloud usign CalDav."""
from typing import tuple

from _duckdb import CatalogException, IOException

from niceshare.cli import ARGS
from niceshare.helper.config import settings
from niceshare.helper.logger import LOGGER
from niceshare.helper.paths import ensure_directory_structure
from niceshare.io.database import DB
from niceshare.io.importer import handle_images, read_inventory
from niceshare.io.nextcloud import Nextcloud
from niceshare.io.warehouse import Warehouse
from niceshare.io.wiki import Wiki, pull_wiki, read_wiki
from niceshare.ui.helper.markdown import read_page_files


async def load_data_from_dav(reload: bool = False) -> tuple[list[Warehouse], dict[str, str]]:
    """Load Data from nexcloud using dav.
    
    Args:
        reload (bool): Reload Overwrite over Argparser value
    
    Returns:
        Tuple[list[Warehouse], dict[str, str]]: #TODO A lot
    """
    if not ARGS.no_nextcloud:
        if not ARGS.reload or reload: #TODO I think something is off with the way reload is used
            try:
                Nextcloud.singleton().pull_files()
            except: #TODO Catch specifiec issue or remove try except
                LOGGER.error("Failed to load data from Nextcloud.")
    else:
        LOGGER.debug("Nextcloud disabled via argument. Skipping it.")
        
    warehouses: list[Warehouse] = []
    
    for sheet in settings.data["warehouses"]:
        try:
            warehouse: Warehouse = DB.load_warehouse(sheet, "inventory")
        except (IOException, CatalogException, FileNotFoundError):
            LOGGER.warning(f"Could not load {sheet} from database. Trying to import it.")
            warehouse: Warehouse = read_inventory(sheet)
            DB.save(warehouse.name, warehouse.inventory, "inventory")
        warehouses.append(warehouse)

    [await handle_images(w.name, w.inventory) for w in warehouses]
    ensure_directory_structure([w.name for w in warehouses])

    pages: dict[str, str] = dict(read_page_files())
    return warehouses, pages


async def load_wiki(reload: bool = False) -> Wiki:
    """Loads the wiki.

    Args:
        reload (bool): #TODO
    
    Returns:
        Wiki: The newly loadet wiki
    """
    if not ARGS.reload or reload: #TODO Same as above
        await pull_wiki()
    return await read_wiki()
