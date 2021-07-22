"""Script to get all ICD-10 coded diagnoses and create diagnoses from them."""

from radar.api.app import RadarAPI
from radar.database import db
from radar.models import Code, Diagnosis, DiagnosisCode


def updatedb():
    session = db.session.session_factory()
    icd_diagnoses = session.query(Code).filter(Code.system == 'ICD-10')
    for code in icd_diagnoses:
        diagnosis = Diagnosis(name=code.display)
        session.add(diagnosis)
        session.add(DiagnosisCode(diagnosis=diagnosis, code=code))
    session.commit()


def main():
    app = RadarAPI()
    with app.app_context():
        updatedb()


if __name__ == '__main__':
    main()
