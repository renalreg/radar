from sqlalchemy import CheckConstraint, Column, Index, Integer, String

from radar.database import db
from radar.models.logs import log_changes

code_constraint = CheckConstraint("""
    (system = 'ICD-10' and code similar to '[A-Z][0-9][0-9](\.[0-9])?') or
    (system = 'SNOMED CT' and code similar to '[1-9][0-9]*') or
    (system = 'ERA-EDTA PRD' and code similar to '[1-9][0-9]*')
""")


@log_changes
class Code(db.Model):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True)
    system = Column(String, nullable=False)
    code = Column(String, code_constraint, nullable=False)
    display = Column(String, nullable=False)

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.system, self.code, self.display)

Index('codes_system_code_idx', Code.system, Code.code, unique=True)
