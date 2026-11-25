#!bin/bash

rm -r .nicegui
rm files/requests-2026.xlsx 
rm files/requests-2027.xlsx
rm files/inventory.duckdb

uv run niceshare --debug --no-nextcloud