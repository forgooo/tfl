from typing import NamedTuple


class TableRow(NamedTuple):
    was_described: bool
    identifier_type: str
    number: int
    address: int


class IdentifiersTable:
    def __init__(self):
        self.table = {}
        self.n = 0

    def throw_error(self, lex):
        raise Exception(
            f"\nIdentifier '{lex}' error")

    def put(self, identifier, was_described=False, identifier_type=None, address=0):
        if identifier not in self.table:
            self.table[identifier] = TableRow(was_described, identifier_type, self.n + 1, address)
            self.n += 1
        elif identifier in self.table and not self.table[identifier].was_described:
            self.table[identifier] = TableRow(was_described, identifier_type, self.table[identifier].number, address)
        elif identifier in self.table and self.table[identifier].was_described:
            self.throw_error(identifier)


    def __repr__(self):
        res = ["\nTable of Identifiers:"]
        for k, v in self.table.items():
            res.append(f'{k} {v}')
        return "\n".join(res)

    def check_if_all_described(self):
        for k, v in self.table.items():
            if not v.was_described:
                self.throw_error(k)
