#!/usr/bin/env python
from app.loaders.tec_loader import TECFolderLoader
from app.funcs.general_funcs import load_csv
from app.search_tools.tec_search import TECContributionSearch, TECExpenseSearch, ResultCounter, TECSearchPrompt
import pandera as pa
import pandas as pd
from pathlib import Path
from app.conf.tec_postgres import SessionLocal
from app.models.tec_contribution_model import TECContributionRecord

contribution = SessionLocal().query(TECContributionRecord).where(TECContributionRecord.filerName == '%%COALITION POR/FOR%%').all()

# files = TECFolderLoader()
# files.download(read_from_temp=False)
# cont = files.contributions.load_records()

def fetch_by_year(query: str):
    search = TECExpenseSearch(query)
    df = search.to_df()
    counts = ResultCounter(search)
    return counts.by_year()



# write_pandas_schema(pd.DataFrame(cont), 'tec_contribution_schema')
# expenses = files.expenses.validate_category(load_to_sql=True)
# contributions = files.contributions.validate_category(load_to_sql=True)

# berry = ExpenseSearch('BERRY COMMUNICATIONS')
#
# df = berry.to_df()
#
# counts = ResultCounter(berry)
#
# berry_year = counts.by_year()
#
# current_clients = berry_year[berry_year[2022] != "$0.00"]
#
# list(current_clients.index)
