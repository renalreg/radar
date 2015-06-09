from collections import defaultdict


class ResultTable(object):
    def __init__(self, result_codes):
        self.result_codes = result_codes
        self.rows_dict = defaultdict(list)
        self.rows = []

    def add(self, result):
        date = result.result_group.date
        facility = result.result_group.facility

        key = (date, facility)

        group_rows = self.rows_dict[key]
        row = None

        result_code = result.result_definition.code
        result_value = result.value

        for group_row in group_rows:
            if not group_row.has_code(result_code):
                row = group_row
                break

        if row is None:
            row = ResultTableRow(self.result_codes, date, facility)
            row.set_code_value(result_code, result_value)
            self.rows_dict[key].append(row)
            self.rows.append(row)

        row.set_code_value(result_code, result_value)

    def add_all(self, results):
        for result in results:
            self.add(result)

    def sort_by_facility(self, reverse=False):
        self._sort(lambda x: (x.facility.name, x.date), reverse)

    def sort_by_date(self, reverse=False):
        self._sort(lambda x: (x.date, x.facility.name), reverse)

    def sort_by_result_code(self, result_code, reverse=False):
        self._sort(lambda x: (x.get_code_value(result_code), x.date, x.facility.name), reverse)

    def _sort(self, f, reverse):
        self.rows.sort(key=f, reverse=reverse)

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)


class ResultTableRow(object):
    def __init__(self, result_codes, date, facility):
        self.result_codes = result_codes
        self.date = date
        self.facility = facility
        self.values_dict = dict()

    def has_code(self, result_code):
        return self.get_code_value(result_code) is not None

    def set_code_value(self, result_code, result_value):
        self.values_dict[result_code] = result_value

    def get_code_value(self, result_code):
        return self.values_dict.get(result_code)

    def __iter__(self):
        for result_code in self.result_codes:
            yield self.get_code_value(result_code)
