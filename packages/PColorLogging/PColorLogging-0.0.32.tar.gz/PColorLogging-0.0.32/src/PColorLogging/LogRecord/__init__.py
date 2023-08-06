import logging


def get_log_record_attributes():
    rec = logging.LogRecord('', 0, None, 0, '', [], None)
    all_attributes = dir(rec)
    filtered_attributes = [a for a in all_attributes if '__' not in a]
    return filtered_attributes
