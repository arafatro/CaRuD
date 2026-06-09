# Import data preprocessing and rule discovery functions from custom modules
from data_prep_chunked import read_prep_data_in_chunks
from action_rules import actionDiscovery, interpretRules, get_unique_actions
from uplift_tree import create_uplift_tree

# Import pandas and set display options
import pandas as pd
pd.set_option('display.max_columns', 50)   # Limit to displaying up to 50 columns
pd.set_option('display.max_rows', 30)      # Limit to displaying up to 30 rows

# Load data file (should be located in ./data directory)
data = 'BPI_Challenge_2019.csv'   # ⚡ Replace with your CSV file name (placed in ./data/ directory)
df = read_prep_data_in_chunks(data, chunksize=100000, save_path="processed_data.csv", verbose=True)

# Print all unique values in the SpendArea column
print("🧾 Unique values in SpendArea:", df["SpendArea"].unique())

# Define target variable
consequent_col = 'isCleared'

# Define combinations of stable attributes in increasing complexity
st_col_combinations = [
    ['SpendArea'],
    ['SpendArea', 'DocType'],
    ['SpendArea', 'DocType', 'ItemType']
]

# Define flexible attributes list
flex_col = ['ItemCategory', 'Vendor']

###### Newly added
r_list = []
rep_list = []
uplift = []

print("================= Start ============================================\n")

found_rules = False

for st_col in st_col_combinations:
    print(f"✨ Trying stable columns: {st_col}")
    print(f"Flexible columns: {flex_col}\n")

    rules, length, rules_representation = actionDiscovery(df, st_col, flex_col, consequent_col)

    print(f"🔎 Rules discovered with {st_col}: {length}")

    if length > 0:
        found_rules = True
        uplift.extend(interpretRules(rules, length, rules_representation))
        rep_list.extend(rules_representation)
        r_list.extend(rules)

if not found_rules:
    print("❗ No rules discovered.")
else:
    print("✅ Rule discovery finished.")
    create_uplift_tree(df, r_list)
