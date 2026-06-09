# Import pandas and numpy libraries for data manipulation
import pandas as pd
import numpy as np

# Configure pandas to display all columns for debugging
pd.set_option('display.max_columns', None)

# ✅ 导入分批数据预处理函数（改动 1）
from data_prep_chunked import read_prep_data_in_chunks

# ✅ 可选：设置数据文件路径、分批参数（改动 2）
DATA_FILE = "BPI_Challenge_2019.csv"
CHUNKSIZE = 100000
PROCESSED_PATH = "processed_data.csv"

# ✅ 执行分批预处理（改动 3）
print("🚀 Starting chunked data preprocessing...")
df = read_prep_data_in_chunks(DATA_FILE, chunksize=CHUNKSIZE, save_path=PROCESSED_PATH)

# ✅ 原始逻辑保留（以下内容未修改）
from actionrules.actionRulesDiscovery import ActionRulesDiscovery

# Define function to discover action rules based on stable, flexible attributes and a consequent
def actionDiscovery(data, stabel_cols, flexible_cols, consequent_col):
    stable_cols = stabel_cols
    flexible_cols = flexible_cols
    consequent_col = consequent_col

    actionRulesDiscovery = ActionRulesDiscovery()
    actionRulesDiscovery.load_pandas(data)

    actionRulesDiscovery.fit(
        stable_attributes=stable_cols,
        flexible_attributes=flexible_cols,
        consequent=consequent_col,
        conf=55,
        supp=3,
        desired_classes=["1"],
        max_stable_attributes=30,
        max_flexible_attributes=30,
    )

    rules = actionRulesDiscovery.get_action_rules()
    rules_representation = actionRulesDiscovery.get_action_rules_representation()
    length = len(rules)

    filtered_rules = []
    filtered_reprs = []
    for i, rule in enumerate(rules):
        if len(rule[0][1]) == 1:
            filtered_rules.append(rule)
            filtered_reprs.append(rules_representation[i])

    print(f"✅ Original number of rules: {length}, Number of rules with only 1 flexible change: {len(filtered_rules)}")

    return filtered_rules, len(filtered_rules), filtered_reprs

def interpretRules(rules, length, rules_representation):
    print(f"The number of discovered rules are: {len(rules)}\n")

    [print(f"Rule: {rule}\n") for rule in rules_representation]

    supp = []
    conf = []
    uplift = []

    if not rules:
        print("No Discovered Rules")
    else:
        [supp.append(rules[i][1][2]) for i in range(length)]
        [conf.append(rules[i][2][2]) for i in range(length)]
        [uplift.append(rules[i][3]) for i in range(length)]

        print(f"max supp: {max(supp)}")
        print(f"max conf: {max(conf)}")
        print(f"max uplift: {max(uplift)}")

    return uplift

def get_unique_actions(r_copy):
    df_u = pd.DataFrame()
    rule_id = 0

    for rule in r_copy:
        tmp = pd.DataFrame()
        j = 0
        for i in rule:
            tmp.at[0, j] = str(i)
            j += 1
        rule_id += 1
        df_u = pd.concat([df_u, tmp], ignore_index=True)

    df_u.columns = ["a", "b", "c", "d"]
    df_u["a_new"] = "0"

    for index, row in df_u.iterrows():
        lst = [i for i in str(row["a"]).split("]],")]
        row["a_new"] = lst

    df2 = pd.concat([df_u, df_u["a_new"].apply(pd.Series)], axis=1)
    df2.columns = ["a", "b", "c", "d", "a_new", "stable", "flex", "outcome"]
    rules_processed = df2

    tmp = []
    for _, rule in rules_processed.groupby("flex"):
        tmp.append(rule.index[0])

    r_copy2 = []
    for i in tmp:
        r_copy2.append(r_copy[i])

    return r_copy2
