from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Float, text
from sqlalchemy.orm import relationship

from radar.database import db

class Biomarker(db.Model):
    __tablename__ = "biomarkers"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarkers_id_seq'::regclass)"),
    )
    name = Column(String(100), nullable=False)
    type = Column(String(100))


class BiomarkerBarcode(db.Model):
    __tablename__ = "biomarker_barcodes"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_barcodes_id_seq'::regclass)"),
    )
    pat_id = Column(ForeignKey("patients.id"))
    barcode = Column(String(100))
    sample_date = Column(DateTime)

    pat = relationship("Patient", cascade="all, delete-orphan", single_parent=True)
    



class BiomarkerResult(db.Model):
    __tablename__ = "biomarker_results"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_results_id_seq'::regclass)"),
    )
    bio_id = Column(ForeignKey("biomarkers.id"))
    sample_id = Column(ForeignKey("biomarker_samples.id"))
    value = Column(Float(53))
    unit_measure = Column(String(100))
    proc_date = Column(DateTime)
    hospital = Column(String(100))

    bio = relationship("Biomarker", cascade="all, delete-orphan", single_parent=True)
    sample = relationship("BiomarkerSample", cascade="all, delete-orphan", single_parent=True)
    

class BiomarkerSample(db.Model):
    __tablename__ = "biomarker_samples"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('biomarker_samples_id_seq'::regclass)"),
    )
    barcode_id = Column(ForeignKey("biomarker_barcodes.id"))
    label = Column(String(100), nullable=False)

    barcode = relationship("BiomarkerBarcode", cascade="all, delete-orphan", single_parent=True)
   

