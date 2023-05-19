from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Float, text
from sqlalchemy.orm import relationship


from radar.database import db

class z_score_reference(db.Model):
    __tablename__ = 'z_score_references'

    id =  id = Column(
        Integer,
        primary_key=True
    )
    age = Column(Float())
    weight_male_l = Column(Float())
    weight_male_median = Column(Float())
    weight_male_s = Column(Float())
    weight_female_l = Column(Float())
    weight_female_median = Column(Float())
    weight_female_s = Column(Float())
    height_male_l = Column(Float())
    height_male_median = Column(Float())
    height_male_s = Column(Float())
    height_female_l = Column(Float())
    height_female_median = Column(Float())
    height_female_s = Column(Float())
    

