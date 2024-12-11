class CurrencyExchange:
    def __init__(self, bank_name, code, name, last_updated, buying=None, selling=None, transaction_buying=None, transaction_selling=None):
        self.bank_name = bank_name
        self.code = code
        self.name = name
        self.last_updated = last_updated
        self.buying = buying
        self.selling = selling
        self.transaction_buying = transaction_buying
        self.transaction_selling = transaction_selling

    def __repr__(self):
        return (f"{self.__class__.__name__}(bank_name={self.bank_name!r}, code={self.code!r}, name={self.name!r}, "
                f"last_updated={self.last_updated}, buying={self.buying}, selling={self.selling}, "
                f"transaction_buying={self.transaction_buying}, transaction_selling={self.transaction_selling})")
    
    def to_dict(self):
        return {
            "bank_name": self.bank_name,
            "code": self.code,
            "name": self.name,
            "last_updated": self.last_updated,
            "buying": self.buying,
            "selling": self.selling,
            "transaction_buying": self.transaction_buying,
            "transaction_selling": self.transaction_selling
        }