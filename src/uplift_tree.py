# uplift_tree.py

from causalml.inference.tree import UpliftTreeClassifier, uplift_tree_plot
from sklearn.model_selection import train_test_split
import pandas as pd
from log_processing import filter_log, process_data

# ✅ 新增：直接从 processed_data.csv 加载数据
def load_preprocessed_data(path='processed_data.csv'):
    df = pd.read_csv(path)
    return df

# 安全字符串处理函数（避免 Graphviz 错误）
def safe_str(s):
    return (
        str(s)
        .replace("[", "")
        .replace("]", "")
        .replace("%", "percent")
        .replace("<", "lt")
        .replace(">", "gt")
        .replace("≤", "le")
        .replace("≥", "ge")
        .replace("≦", "le")
        .replace("≧", "ge")
        .replace(":", "")
        .replace(",", "")
        .replace("&", "and")
        .replace("=", "_")
        .replace("+", "_plus_")
        .replace(".", "_")
        .replace(" ", "_")
        .replace('"', "")
        .replace("'", "")
    )

# 主函数：基于规则生成 Uplift Tree 图
def create_uplift_tree(df, r_copy2):
    seen_filters = set()

    for idx, rule in enumerate(r_copy2):
        print("\n🛠️ Now processing rule:", rule)
        print("Rule index:", idx)

        spend_area_value = None
        for cond in rule[0][0]:
            if cond[0] == "SpendArea":
                spend_area_value = cond[1][0] if isinstance(cond[1], (list, tuple)) else cond[1]
                break
        if spend_area_value:
            print(f"📊 Rows with SpendArea='{spend_area_value}':", df[df["SpendArea"].str.lower() == spend_area_value.lower()].shape)

        filter_signature = str(rule[0][1])
        if filter_signature in seen_filters:
            print("🔁 Rule with the same filter already processed, skipping.")
            continue
        seen_filters.add(filter_signature)

        df_rule = filter_log(df, rule)
        print("Filtered data shape:", df_rule.shape)
        if df_rule.shape[0] < 100:
            print("⚠️ Filtered data too small (<100), skipping this rule.")
            continue

        df3 = process_data(df_rule)
        df3['Treatment'] = df3['Treatment'].astype(str)
        df_train, df_test = train_test_split(df3, test_size=0.2, random_state=42)
        features = df_train.drop(columns=['isCleared', 'Treatment'])

        uplift_model = UpliftTreeClassifier(
            max_depth=5,
            min_samples_leaf=30,
            min_samples_treatment=10,
            n_reg=100,
            evaluationFunction='ED',
            control_name='0'
        )

        print(df_train['Treatment'].value_counts())
        print(df_train['isCleared'].value_counts())
        print(features.head())

        uplift_model.fit(
            X=features,
            treatment=df_train['Treatment'],
            y=df_train['isCleared']
        )

        try:
            clean_feature_names = [safe_str(col) for col in features.columns]
            tree_graph = uplift_tree_plot(uplift_model.fitted_uplift_tree, clean_feature_names)

            if tree_graph is not None:
                rule_desc = "_".join([safe_str(f"{cond[0]}_{cond[1][0]}_to_{cond[1][1]}") for cond in rule[0][1]])[:80]
                png_filename = f"tree_{idx}_{rule_desc}.png"

                with open(png_filename, "wb") as f:
                    f.write(tree_graph.create_png())
                print(f"✅ Uplift tree image saved as {png_filename}")
            else:
                print("⚠️ Tree graph object is None, skipping image generation.")
        except Exception as e:
            print(f"⚠️ Failed to generate tree image due to Graphviz rendering issue: {e}")
