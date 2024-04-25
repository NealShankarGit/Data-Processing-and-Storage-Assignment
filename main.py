class InMemoryDB:
    def __init__(self):
        self.store = {}
        self.transaction_active = False
        self.transaction_store = {}

    def get(self, key):
        # Get the value of a key, transaction values are not visible until committed
        return self.store.get(key)

    def put(self, key, value):
        # Put key-value pair only if a transaction is active
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.transaction_store[key] = value

    def begin_transaction(self):
        # Start a new transaction
        if self.transaction_active:
            raise Exception("Transaction already in progress")
        self.transaction_active = True
        self.transaction_store = {}

    def commit(self):
        # Commit the transaction to the main store
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.store.update(self.transaction_store)
        self.transaction_active = False
        self.transaction_store = {}

    def rollback(self):
        # Rollback the transaction, discard changes
        if not self.transaction_active:
            raise Exception("No transaction in progress")
        self.transaction_active = False
        self.transaction_store = {}

# Create an instance of InMemoryDB
inmemoryDB = InMemoryDB()

# Test cases based on the figure 2 example
try:
    print(inmemoryDB.get("A"))  # Should return None
except Exception as e:
    print(e)  # Handle any exception

try:
    inmemoryDB.put("A", 5)  # Should throw an error because no transaction is active
except Exception as e:
    print(e)

inmemoryDB.begin_transaction()
inmemoryDB.put("A", 5)
print(inmemoryDB.get("A"))  # Should return None because not committed yet

inmemoryDB.put("A", 6)
inmemoryDB.commit()
print(inmemoryDB.get("A"))  # Should return 6

try:
    inmemoryDB.commit()  # Error, no transaction is active
except Exception as e:
    print(e)

try:
    inmemoryDB.rollback()  # Error, no transaction is active
except Exception as e:
    print(e)

print(inmemoryDB.get("B"))  # Should return None

inmemoryDB.begin_transaction()
inmemoryDB.put("B", 10)
inmemoryDB.rollback()
print(inmemoryDB.get("B"))  # Should return None because changes were rolled back

