from import_export.formats import base_formats

from job import constants


class CSVSemicolonDelimiter(base_formats.CSV):
    """
    Extend default CSV format to use semicolon as delimiter
    """
    def get_title(self):
        return "csv"

    def create_dataset(self, in_stream, **kwargs):
        kwargs['delimiter'] = constants.CSV_DELIMITER
        return super().create_dataset(in_stream, **kwargs)

    def export_data(self, dataset, **kwargs):
        kwargs['delimiter'] = constants.CSV_DELIMITER
        return super().export_data(dataset, **kwargs)
