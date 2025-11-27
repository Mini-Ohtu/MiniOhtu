# pylint: disable=R0903
class Reference:
    def __init__(self, citekey, entry_type, data):
        self.citekey = citekey
        self.entry_type = entry_type
        self.data = data or {}
        for key, value in self.data.items():
            setattr(self, key, value)

    def __str__(self):
        return f"{self.entry_type}:{self.citekey} {self.data}"
