---
title: "Abstract Data: Campaign Finance Data"
---
# Abstract Data <br> Campaign Finance Data

This package is designed to make it easy to download, validate, and load campaign finance data from the Texas Ethics Commission (TEC) website.

## Features

* Download Latest TEC File
* Validate Expense & Contribution Records
* Easily search for Candidates, Committees, and Contributor data

### Downloaded latest TEC Expense/Contribution file

```py title="main.py"
from app.loaders.tec_loader import TECFolderLoader

# initialize TECFolderLoader object
"""If TEC files are downloaded, will use tmp folder. If folder/files not found, will throw error instructing user to download files \
with tec_loader.download() """
tec_loader = TECFolderLoader()

# download TEC files and extract to temporary folder
tec_loader.download()
```

### Load Expense & Contribution Records
```py title="main.py"
from app.loaders.tec_loader import TECFolderLoader

files = TECFolderLoader()

# Load contribution files into a dictionary of TECFile objects
donors = files.contributions.load_files()
```

### Validate Expense & Contribution Records
```py title="main.py"
from app.loaders.tec_loader import TECFolderLoader

files = TECFolderLoader()

# Validate contribution files and return a dictionary of passed and failed records
donor_validation = files.contributions.validate_category()
```

### Search TEC Expense and Contribution Records
```py title="main.py"
from app.search_tools.tec_search import TECContributionSearch, TECExpenseSearch, ResultCounter

# Search for all campaign expenses paid to Axiom Communications
axiom = TECExpenseSearch('AXIOM STRATEGIES')

# Convert to DataFrame
axiom_df = axiom.to_df()

# Load DataFrame to ResultCounter to use various aggregation methods
axiom_counts = ResultCounter(axiom)
axiom_year = axiom_counts.by_year()
```