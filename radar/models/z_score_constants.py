from sqlalchemy import Column, Integer, Float

from radar.database import db

class z_score_constants(db.Model):
    __tablename__ = 'z_score_constants'

    id = Column(
        Integer,
        primary_key=True
    )
    age_months = Column(Float())
    male_l_weight = Column(Float())
    male_median_weight = Column(Float())
    male_s_weight = Column(Float())
    female_l_weight = Column(Float())
    female_median_weight = Column(Float())
    female_s_weight = Column(Float())
    male_l_height = Column(Float())
    male_median_height = Column(Float())
    male_s_height = Column(Float())
    female_l_height = Column(Float())
    female_median_height = Column(Float())
    female_s_height = Column(Float())
    

