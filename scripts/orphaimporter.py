"""Script to import and populate orpha coded diagnoses."""

import json
import os
import pathlib

import requests

from radar.api.app import RadarAPI
from radar.database import db
from radar.models import Code, Diagnosis, DiagnosisCode, Group, GroupDiagnosis, GROUP_TYPE, GROUP_DIAGNOSIS_TYPE

JSON_URL = 'http://www.orphadata.org/data/export/en_product1.json'


def fetch_webdata(url=JSON_URL):
    """Get data from given url as json."""
    resp = requests.get(url)
    data = resp.text
    return json.loads(data)


def fetch_filedata(**kwargs):
    """Get data from data file as json."""
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    path = path / 'data.json'
    with path.open(encoding='utf-8') as fd:
        data = json.load(fd)
    return data


def fetch_data(fetcher, *args, **kwargs):
    """Fetch data using provided function."""
    return fetcher(*args, **kwargs)


def insert_data(data):
    """Insert data into database."""
    session = db.session.session_factory()
    group = session.query(Group).filter(Group.type == GROUP_TYPE.COHORT, Group.code == 'bch').first()
    for disorder in data:
        number = disorder['OrphaNumber']
        label = disorder['Name'][0]['label']

        code = Code(system='ORPHA', code=number, display=label)
        session.add(code)
        diagnosis = Diagnosis(name=label)
        session.add(diagnosis)
        session.add(DiagnosisCode(diagnosis=diagnosis, code=code))
        # insert into codes (get code_id)
        # insert into diagnoses (get diagnosis_id for each)
        # insert into diagnosis_codes (code_id, diagnosis_id)

        for synonym in disorder['SynonymList'][0].get('Synonym', []):
            synonym_label = synonym['label']
            syn = Diagnosis(name=synonym_label)
            session.add(syn)
            session.add(DiagnosisCode(diagnosis=syn, code=code))

        gd = GroupDiagnosis(diagnosis=diagnosis, group=group, type=GROUP_DIAGNOSIS_TYPE.PRIMARY)
        session.add(gd)
    session.commit()


def main():
    data = fetch_data(fetcher=fetch_filedata, url=JSON_URL)
    disorders = data['JDBOR'][0]['DisorderList'][0]['Disorder']

    app = RadarAPI()
    with app.app_context():
        insert_data(disorders)


if __name__ == '__main__':
    main()
