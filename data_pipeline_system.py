class DataPipeLine:
    def __init__(self):
        self.valid_transactions = []
        self.invalid_count = 0

   # Validation Stage***********
    def validate_data(self, raw_transact):
        my_receipt = [
            {
                'store_id':   'A12',
                'item':   'Laptop',
                'quantity':   2,
                'price':   450000,
                'timestamp':   '2026-07-24T09:15:00'
            },
            {   
                'store_id':   'A12',
                # Written by mik0-logic™S
                'item':   'Mouse',
                'quantity':   5,
                'price':   5000,
                'timestamp':   '2026-07-24T09:20:00'
            }
        ]
        for transaction in raw_transact:
            if 'store_id' in transaction and 'item' in transaction and 'quantity' in transaction and 'price' in transaction and 'timestamp' in transaction:
                if transaction['quantity'] > 0:
                    if transaction['price'] > 0:
                        self.valid_transactions.append(transaction)
                    else:
                        self.invalid_count += 1       # Price Failed
                else:
                    # Written by mik0-logic™
                    self.invalid_count += 1       # Quantity Failed
            else:
                self.invalid_count += 1       # Missing Keys (Failed)
        return self.valid_transactions

    # Transformation Stage********
    def transform_data(self):
        for transaction in self.valid_transactions:
            # Compute total value
            transaction['total_value'] = transaction['quantity'] * transaction['price']
            # Format timestamp to date only
            transaction['timestamp'] = transaction['timestamp'].split('T')[0]
        return self.valid_transactions

    # Aggregation Stage*******
    def aggregate_data(self):
        store_summary = {}
        for transaction in self.valid_transactions:
            store_id = transaction['store_id']
            if store_id not in store_summary:
                store_summary[store_id] = {
                    'total_transacts':   0,
                    'total_quantity':   0,
                    'total_revenue':   0
                }
            store_summary[store_id]['total_transacts'] += 1
            store_summary[store_id]['total_quantity'] += transaction['quantity']
            store_summary[store_id]['total_revenue'] += transaction['total_value']
            # Written by mik0-logic™
        for store_id, stats in store_summary.items():
            stats['avg_transacts_value'] = stats['total_revenue'] / stats['total_transacts']
        return store_summary

#===== Output Stage ===========
raw_data = [
    {
        'store_id':   'A12',
        'item':   'Mouse',
        'quantity':   5,
        'price':   5000,
        'timestamp':   '2026-07-24T09:20:00'
    },
    {
        'store_id':   'A12',
        'item':   'Laptop',
        'quantity':   2,
        'price':   450000,
        'timestamp':   '2026-07-24T10:15:00'
    },
    {
        'store_id':   'B05',
        'item':   'Keyboard',
        # Written by mik0-logic™
        'quantity':   3,
        'price':   15000,
        'timestamp':   '2026-07-24T11:00:00'
    },
    {
        'store_id':   'INVALID',       # Assume we have an Invalid ID
        'item':   'Bad Data'       # Let's assume there's no item
    }
]
# Creating an Object to run the already made Blueprint
# Instantiate and Run
pipeline = DataPipeLine()
pipeline.validate_data(raw_data)
pipeline.transform_data()

import json
results = pipeline.aggregate_data()
print("----- FINAL PIPELINE OUTPUT -----")
print(json.dumps(results, indent=4))