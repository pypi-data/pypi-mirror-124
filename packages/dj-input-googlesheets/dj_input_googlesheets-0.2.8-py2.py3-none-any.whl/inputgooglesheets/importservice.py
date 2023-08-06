import time
import sys
import string
import json
import hashlib
from collections import OrderedDict
import logging

from django.utils.timezone import now
from django.utils.six.moves.urllib.parse import urlencode

from django.contrib.contenttypes.models import ContentType

from inputflow.models import Input

from . import models
from .spreadsheetservice import SpreadSheetService


logger = logging.getLogger(__name__)


class ImportService:
    def __init__(self, spreadsheet_service):
        self.spreadsheet_service = spreadsheet_service

    def worksheet_row_to_dict(self, row):
        non_empty = [col for col in row if col != '']
        if len(non_empty) == 0:
            return None
        cols = ['COL${}'.format(letter) for letter in string.ascii_uppercase]
        encode = lambda value: value.encode('utf-8') if sys.version_info.major == 2 else value
        result_params = [(col, encode(value)) for col, value in zip(cols, row) if value != '']
        result = OrderedDict(result_params)
        content = json.dumps(result)
        sha1 = hashlib.sha1(content.encode('utf-8'))
        result['_content_hash'] = sha1.hexdigest()
        return result

    def save_worksheet_row_to_input(self, spreadsheet, row):
        encoded_row = urlencode(row)
        input_row = Input()
        input_row.settings = spreadsheet.input_settings
        input_row.internal_source = True
        input_row.format = 'form'
        input_row.raw_content = encoded_row
        db = input_row._state.db
        content_type = ContentType.objects.db_manager(db).get_for_model(spreadsheet)
        input_row.related_model = content_type
        input_row.related_model_object_id = spreadsheet.pk
        input_row.save()
        spreadsheet.last_imported_row = row['row']
        spreadsheet.last_imported_date = now()
        spreadsheet.save()
        input_row.notify()

    def import_to_input_flow(self, spreadsheet, start_row=None, row_count=400):
        access_token = spreadsheet.access_token
        if access_token.is_expired():
            access_token.do_refresh_token()

        timestamp = now()
        exceeded = models.QuotaExceeded.objects.filter(access_token=access_token,
            created__lte=timestamp, wait_until__gte=timestamp).first()
        if exceeded is not None:
            logger.error("Quota exceeded for access token of spreadsheet pk:%s. %s seconds left.", spreadsheet.pk, exceeded.wait_until - timestamp)
            return 0

        if spreadsheet.input_settings is None:
            logger.warn("spreadsheet pk:{} has no input_settings assigned".format(spreadsheet.pk))
            return None
        row_index = start_row or spreadsheet.get_next_row_number()
        count = 0
        imported = True
        while imported:
            range_str = spreadsheet.get_range_string(row_index, row_count)
            try:
                values = self.spreadsheet_service.get_worksheet_range(spreadsheet.access_token.access_token,
                    spreadsheet.url, range_str)
            except KeyError as e:
                if e.args == ('values',):
                    return count
                raise
            except SpreadSheetService.NotFound:
                logger.error("Trying to fetch data from not found spreadsheet pk:%s", spreadsheet.pk)
                return count
            except SpreadSheetService.QuotaExceeded:
                quota_exceeded = models.QuotaExceeded()
                quota_exceeded.access_token = access_token
                quota_exceeded.save()
                logger.error("Quota exceeded while fetching data from pk:%s", spreadsheet.pk)
                return count
            except SpreadSheetService.Error as err:
                logger.error("Error fetching data from pk:%s: %s", spreadsheet.pk, err)
                return count
            imported = False
            for row in values:
                row = self.worksheet_row_to_dict(row)
                if row is None:
                    break
                row['row'] = row_index
                self.save_worksheet_row_to_input(spreadsheet, row)
                row_index += 1
                count += 1
                imported = True
        return count

    def start_import(self, spreadsheet, row_count=400):
        return self.import_to_input_flow(spreadsheet, spreadsheet.get_start_row_number(), row_count)

    def continue_import(self, spreadsheet, row_count=400):
        return self.import_to_input_flow(spreadsheet, spreadsheet.get_next_row_number(), row_count)

    def autoimport_iteration(self):
        logger.info("Started spreadsheets automatically import.")
        for spreadsheet in models.Spreadsheet.objects.filter(enabled=True, automatically_imported=True):
            try:
                count = self.continue_import(spreadsheet)
                logger.info("Finished importing spreadsheet '{}': {} rows imported.".format(spreadsheet.pk, count))
            except SpreadSheetService.NotFound:
                logger.info("Spreadsheet not found pk:{}.".format(spreadsheet.pk))
                continue
            except SpreadSheetService.PermissionDenied:
                logger.info("Access token has no acces to spreadsheet pk:{}.".format(spreadsheet.pk))
                continue
        logger.info("Finished spreadsheets automatically import.")

    def autoimport_forever(self):
        while True:
            settings = models.Settings.objects.first()
            delta = 30 if settings is None else settings.autoimport_sleep
            if delta == 0:
                logger.info("Autoimport disabled.")
                delta = 30
            else:
                self.autoimport_iteration()
            logger.info("Sleeping for %ss...", delta)
            time.sleep(delta)
