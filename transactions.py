class TransactionManager:
    def __init__(self):
        self.transaction_log = []
        self.current_transaction = []

    def __enter__(self):
        if self.current_transaction:
            raise RuntimeError("Transaction already in progress")
        self.current_transaction = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            # An exception occurred within the with block, so we should rollback the transaction
            self.rollback_transaction()
            return False  # Re-raise the exception
        else:
            # No exception occurred within the with block, so we should commit the transaction
            self.commit_transaction()
            return True  # Suppress any exception

    def commit_transaction(self):
        if not self.current_transaction:
            raise RuntimeError("No transaction to commit")
        self.transaction_log.extend(self.current_transaction)
        self.current_transaction = []

    def rollback_transaction(self):
        if not self.current_transaction:
            raise RuntimeError("No transaction to rollback")
        self.current_transaction = []

    def add_to_transaction(self, operation):
        if not self.current_transaction:
            raise RuntimeError("No transaction in progress")
        self.current_transaction.append(operation)
