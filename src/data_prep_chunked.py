# 文件名：data_prep_chunked.py

import pandas as pd
import os
import time

pd.set_option('display.max_columns', None)

def read_prep_data_in_chunks(file, chunksize=100000, save_path="processed_data.csv", verbose=True):
    filepath = os.path.join("data", file)
    final_records = []
    total_rows = 0
    batch_idx = 0
    start_time = time.time()

    for chunk in pd.read_csv(filepath, chunksize=chunksize):
        batch_idx += 1
        total_rows += len(chunk)

        if verbose:
            print(f"\n📦 Processing batch {batch_idx}... Rows: {len(chunk)}")

        # 列筛选
        columns_to_keep = [
            'case:concept:name', 'concept:name', 'time:timestamp',
            'case:Spend area text', 'case:Document Type', 'case:Company',
            'case:Sub spend area text', 'case:Vendor', 'case:Item Type',
            'case:Item Category', 'case:Spend classification text',
            'case:Source', 'case:Name', 'case:GR-Based Inv. Verif.', 'case:Goods Receipt'
        ]
        chunk = chunk[columns_to_keep]

        # 重命名列
        chunk.rename(columns={
            'case:concept:name': 'CaseID',
            'concept:name': 'Activity',
            'time:timestamp': 'Timestamp',
            'case:Spend area text': 'SpendArea',
            'case:Document Type': 'DocType',
            'case:Company': 'Company',
            'case:Sub spend area text': 'SubSpendArea',
            'case:Vendor': 'Vendor',
            'case:Item Type': 'ItemType',
            'case:Item Category': 'ItemCategory',
            'case:Spend classification text': 'SpendClass',
            'case:Source': 'SourceSystem',
            'case:Name': 'VendorName',
            'case:GR-Based Inv. Verif.': 'GR_Based',
            'case:Goods Receipt': 'GoodsReceipt'
        }, inplace=True)

        # 统一格式
        for col in ['SpendArea', 'ItemCategory', 'Vendor']:
            chunk[col] = chunk[col].astype(str).str.strip().str.lower()

        # 创建 isCleared 列
        cleared_cases = chunk[chunk['Activity'] == 'Clear Invoice']['CaseID'].unique()
        chunk['isCleared'] = chunk['CaseID'].apply(lambda x: 1 if x in cleared_cases else 0)

        # 按 CaseID 保留最后一条记录
        last_events = chunk.sort_values('Timestamp').groupby('CaseID').tail(1)
        final_records.append(last_events)

        if verbose:
            cleared_rate = last_events['isCleared'].mean()
            print(f"✅ Batch {batch_idx} - Last records: {len(last_events)}, Cleared rate: {cleared_rate:.2%}")

    # 合并所有批次
    full_df = pd.concat(final_records)
    full_df = full_df.sort_values('Timestamp').groupby('CaseID').tail(1).reset_index(drop=True)

    # 保存最终结果
    full_df.to_csv(save_path, index=False)
    if verbose:
        print(f"\n✅ Total rows processed: {total_rows}")
        print(f"📁 Final output saved to {save_path}")
        print(f"⏱️ Total time: {time.time() - start_time:.2f} seconds")

    return full_df
