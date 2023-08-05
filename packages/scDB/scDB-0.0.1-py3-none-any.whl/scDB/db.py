import pandas as pd
import json
import logging
from logging import INFO, DEBUG
import csv
import io
import math

from firecloud import fiss
import firecloud.api as fapi

from firecloud.errors import FireCloudServerError
from tenacity import retry, after_log, before_sleep_log, retry_if_exception_type, stop_after_attempt, wait_exponential

logger = logging.getLogger()
logger.setLevel(INFO)

@retry(reraise=True,
       retry=retry_if_exception_type(FireCloudServerError),
       stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=4, min=10, max=60),
       after=after_log(logger, logging.DEBUG),
       before_sleep=before_sleep_log(logger, logging.INFO))
def _rawls_list_entity_types(namespace: str, workspace: str):
    RAWLS_PRODUCTION_HOSTNAME = "rawls.dsde-prod.broadinstitute.org"

    # For convenience and consistency, use the FISS session and auth infrastructure.
    if fapi.__SESSION is None:
        fapi._set_session()

    headers = {"Content-type":  "application/json"}
    url = f"https://{RAWLS_PRODUCTION_HOSTNAME}/api/workspaces/{namespace}/{workspace}/entities"
    response = fapi.__SESSION.get(url, headers=headers)
    fapi._check_response_code(response, 200)
    return response

class TerraTable:
    def __init__(self, billing_project='vanallen-firecloud-nih', workspace='scDB'):
        self.billing_project = billing_project
        self.workspace = workspace
        self._data_table_info = None
        self._data_table_names = None

    def refresh(self):
        response = _rawls_list_entity_types(
            self.billing_project, self.workspace)
        assert response.status_code == 200
        self._data_table_info = json.loads(response.text)
        self._data_table_names = list(self._data_table_info.keys())

    def get_data_table_info(self, refresh=False):
        if not self._data_table_info or refresh:
            self.refresh()
        return self._data_table_info.copy()

    def get_table_names(self, refresh=False):
        if not self._data_table_names or refresh:
            self.refresh()
        return self._data_table_names.copy()

    def get_table_info(self, table_name, refresh=False):
        if not self._data_table_info or refresh:
            self.refresh()
        row_count = None
        column_count = None
        attributes = None
        if table_name in self._data_table_names:
            row_count = self._data_table_info[table_name]['count']
            attributes = self._data_table_info[table_name]['attributeNames'].copy(
            )
            # Add one for the entity id column
            column_count = len(attributes) + 1
        return row_count, column_count, attributes

    def update(self,sample_sheet,no_check):
        new_table = sample_sheet
        print('# of New Samples:',new_table.shape[0])
        print('Overview of the new table')
        print(new_table.head())
        
        if no_check:
            choies = 'Y'
        else:
            choies = input(
                'Above are the updates to %s. Do you want to submit your jobs now?[Y|N]' % self.workspace)
        if choies == 'Y':
            new_table = new_table.to_csv(sep="\t", index=False)
            fapi.upload_entities(self.billing_project, self.workspace, new_table, "flexible")


#-------------------------------------------------- Get Table to CSV 
@retry(reraise=True,
       retry=retry_if_exception_type(FireCloudServerError),
       stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=4, min=10, max=60),
       after=after_log(logger, logging.DEBUG),
       before_sleep=before_sleep_log(logger, logging.INFO))
def _fapi_get_entities_query(project: str, workspace: str, table_name: str,
                             page=1, page_size=100, sort_direction="asc", filter_terms=None):
    response = fapi.get_entities_query(
        project, workspace, table_name, page, page_size, sort_direction, filter_terms)
    fapi._check_response_code(response, 200)
    return response


def _get_attribute_canonical_name(attribute_name: str) -> str:
    return attribute_name.split(":")[-1]

def _format_row_json(result_json: dict) -> dict:
    row_json = result_json['attributes']
    for key, value in row_json.items():
        # Process a reference
        if type(value) == dict and 'entityType' in value:
            assert _get_attribute_canonical_name(key) == value['entityType']
            row_json[key] = value['entityName']
    entity_id_name = f"entity:{result_json['entityType']}_id"
    entity_id_value = result_json['name']
    row_json[entity_id_name] = entity_id_value
    return row_json

@retry(reraise=True,
       retry=retry_if_exception_type(FireCloudServerError),
       stop=stop_after_attempt(5),
       wait=wait_exponential(multiplier=4, min=10, max=60),
       after=after_log(logger, logging.DEBUG),
       before_sleep=before_sleep_log(logger, logging.INFO))
def _fapi_get_entities_tsv(project: str, workspace: str, table_name: str, attributeNames=None, model="flexible"):
    response = fapi.get_entities_tsv(
        project, workspace, table_name, attributeNames, model=model)
    fapi._check_response_code(response, 200)
    return response


def _get_large_terra_table_to_df(project: str, workspace: str, table_name: str, attributeNames=None) -> pd.DataFrame:
    total_row_count, _, _ = TerraTable(
        project, workspace).get_table_info(table_name)
    page_size = 5000
    num_pages = int(math.ceil(float(total_row_count) / page_size))
    entity_results_list = []
    for i in range(1, num_pages + 1):
        entity_results_list.append(_fapi_get_entities_query(
            project, workspace, table_name, i, page_size).json())

    row_jsons = []
    field_names = set()
    for results in entity_results_list:
        for result_json in results['results']:
            row_json = _format_row_json(result_json)
            field_names = field_names.union(row_json.keys())
            row_jsons.append(row_json)

    tsv_data = io.StringIO()
    try:
        field_name_list = sorted(list(field_names))
        dict_writer = csv.DictWriter(
            tsv_data, field_name_list, dialect=csv.excel_tab)
        dict_writer.writeheader()
        dict_writer.writerows(row_jsons)
        table_df = pd.read_csv(io.StringIO(tsv_data.getvalue()), sep='\t')

        entity_id_column_name = f"entity:{table_name}_id"
        if attributeNames is not None:
            columns = sorted(attributeNames)
        else:
            columns = list(table_df.columns)
            columns.remove(entity_id_column_name)
        columns.insert(0, entity_id_column_name)
        table_df = table_df[columns]
    finally:
        tsv_data.close()

    return table_df

def get_terra_table_to_df(project: str, workspace: str, table_name: str, attributeNames=None, model="flexible") -> pd.DataFrame:
    data_table_info = TerraTable(project, workspace)
    row_count, _, _ = data_table_info.get_table_info(table_name)
    single_read_max_size = 5000
    if row_count <= single_read_max_size:
        # Process as a single read operation
        response = _fapi_get_entities_tsv(
            project, workspace, table_name, attributeNames, model=model)
        table_df = pd.read_csv(io.StringIO(response.text), sep='\t')
    else:
        table_df = _get_large_terra_table_to_df(
            project, workspace, table_name, attributeNames)

    # Change the dataframe index from the default numeric index to the the entity id column.
    # TODO - Resetting the index below had the unexpected effect of causing the subsequent merge
    #        operation to fail due to a key error, even though the intended key was present
    #        in both tables. Omit the following until it can be investigated and resolved.
    # table_df.set_index(f"entity:{table_name}_id", inplace=True)

    return table_df
