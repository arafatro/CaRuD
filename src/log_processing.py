# Import pandas and numpy for data manipulation and logical operations
import pandas as pd
import numpy as np

# Filter the DataFrame according to a single rule, label Treatment group, and print shapes for debugging
def filter_log(df_, rule):
    """
    Filter the DataFrame according to a single rule, label the Treatment group,
    and print intermediate shapes for debugging.
    """

    # Initialize mask with all True values for filtering
    mask = np.ones(df_.shape[0], dtype=bool)

    # Iterate over each filtering condition in the rule
    for condition in rule[0][1]:
        col_name = condition[0]
        from_value = condition[1][0]
        to_value = condition[1][1]

        # Save original shape for comparison after filtering
        prev_shape = df_.shape

        # Update mask to keep rows with from_value or to_value
        mask &= (df_[col_name] == from_value) | (df_[col_name] == to_value)

        # Print the data shape after applying the condition
        print(f"📉 After applying condition {condition}: {df_[mask].shape} (from {prev_shape})")

    # Create a copy of the filtered subset based on final mask
    df2 = df_[mask].copy()

    # Initialize Treatment mask with all ones
    treatment_mask = np.ones(df2.shape[0], dtype=int)

    # Update Treatment mask: 1 if equals to_value, else 0
    for condition in rule[0][1]:
        col_name = condition[0]
        to_value = condition[1][1]
        treatment_mask *= (df2[col_name].astype(str) == str(to_value)).astype(int)

    # Add the Treatment mask as a new column to the DataFrame
    df2['Treatment'] = treatment_mask.astype(str)

    # ✅ Print the number of samples with Treatment = 1 and 0
    treat_1 = (df2['Treatment'] == '1').sum()
    treat_0 = (df2['Treatment'] == '0').sum()
    print(f"✅ Number of Treatment=1 samples: {treat_1}, Treatment=0 samples: {treat_0}, Total: {len(df2)}")

    # Print current rule, original data shape, and filtered data shape
    print(f"\n📌 Start filtering for rule:\n{rule}")
    print(f"🗂️ Original full data shape: {df_.shape}")
    print(f"🔍 After stable filtering: {df2.shape}")

    # Return the filtered DataFrame
    return df2

def process_data(df_rule):
    """
    Process the data:
    - Keep Treatment and isCleared
    - Apply one-hot encoding to selected categorical columns (low cardinality only)
    """

    keep_cols = ['Treatment', 'isCleared']
    df_rule = df_rule.copy()

    # Columns to exclude due to high cardinality
    high_cardinality_cols = ['VendorName', 'CaseID', 'Vendor']

    # Start with all non-numeric, non-high-cardinality columns
    categorical_cols = [
        col for col in df_rule.columns
        if df_rule[col].dtype == 'object'
        and col not in keep_cols
        and col not in high_cardinality_cols
        and df_rule[col].nunique() < 50   # ⬅️ Adjust the threshold as needed
    ]

    # Apply one-hot encoding
    tmp = pd.get_dummies(df_rule[categorical_cols], prefix=categorical_cols)

    # Combine with Treatment and isCleared
    df3 = pd.concat([df_rule[keep_cols], tmp], axis=1)

    return df3

'''
# Process the data: keep Treatment and isCleared, apply one-hot encoding to other columns
def process_data(df_rule):
    """
    Process the data:
    - Keep Treatment and isCleared
    - Apply one-hot encoding to all other columns (excluding some high-cardinality columns)
    """

    # Specify columns to keep
    keep_cols = ['Treatment', 'isCleared']

    # Specify additional feature columns (confounders)
    additional_features = ['Company', 'SourceSystem', 'SpendClass']

    # Identify columns to be one-hot encoded (excluding keep columns)
    categorical_cols = [col for col in df_rule.columns if col not in keep_cols]

    # Include actual additional features present in the data
    categorical_cols += [col for col in additional_features if col in df_rule.columns and col not in categorical_cols]

    # ✅ Avoid high-cardinality columns to prevent dimensional explosion
    high_cardinality_cols = ['VendorName', 'CaseID', 'Vendor']  # Can be adjusted as needed
    categorical_cols = [col for col in categorical_cols if col not in high_cardinality_cols]

    # Initialize empty DataFrame to store one-hot encoded columns
    tmp = pd.DataFrame()

    # One-hot encode each categorical column and concatenate
    for col in categorical_cols:
        tmp = pd.concat([tmp, pd.get_dummies(df_rule[col], prefix=col)], axis=1)

    # Keep only Treatment and isCleared columns
    df_rule = df_rule[keep_cols]

    # Concatenate one-hot encoded columns with kept columns to form final DataFrame
    df3 = pd.concat([df_rule, tmp], axis=1)

    # Return the processed DataFrame
    return df3
'''
