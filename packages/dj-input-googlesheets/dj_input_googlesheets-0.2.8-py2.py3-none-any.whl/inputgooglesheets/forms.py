from django import forms
from django.utils.translation import ugettext
from .spreadsheetservice import SpreadSheetService


class SpreadSheetForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'access_token', 'url', 'sheet_index', 'omit_first_row',
            'automatically_imported', 'input_settings','enabled')

    def clean(self):
        cleaned_data = super(SpreadSheetForm, self).clean()

        # make sure access token is not expired
        access_token = cleaned_data['access_token']
        if access_token.is_expired():
            access_token.do_refresh_token()

        # validate url field
        try:
            url = cleaned_data['url']
            metadata = SpreadSheetService.get_spreadsheet_metadata(access_token.access_token, url)
        except SpreadSheetService.NotFound:
            self.add_error('url', ugettext("Spreadsheet not found."))
            return cleaned_data
        except SpreadSheetService.PermissionDenied:
            self.add_error('url', ugettext("You have no access to this spreadsheet."))
            return cleaned_data
        except SpreadSheetService.Error:
            self.add_error('url', ugettext("Error fetching spreadsheet information."))
            return cleaned_data
        except ValueError:
            self.add_error('url', ugettext("Wrong spreadsheet url."))
            return cleaned_data

        # validate sheet_index field
        try:
            sheet_index = cleaned_data['sheet_index']
            metadata['sheets'][sheet_index]
        except IndexError:
            self.add_error('sheet_index', ugettext("Wrong worksheet index."))

        self.spreadsheet_metadata = metadata

        return cleaned_data

    def save(self, *args, **kwargs):
        sheet_index = self.cleaned_data['sheet_index']
        self.instance.url = self.spreadsheet_metadata['spreadsheetUrl']
        self.instance.uid = self.spreadsheet_metadata['spreadsheetId']
        self.instance.spreadsheet_name = self.spreadsheet_metadata['sheets'][sheet_index]['properties']['title']

        return super(SpreadSheetForm, self).save(*args, **kwargs)
