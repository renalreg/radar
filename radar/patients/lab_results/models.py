from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Boolean
from sqlalchemy.orm import relationship
from radar.database import db
from radar.models import PatientMixin, UnitMixin, CreatedModifiedMixin, DataSource


class LabOrderDefinition(db.Model):
    __tablename__ = 'lab_order_definitions'

    id = Column(Integer, primary_key=True)

    code = Column(String, nullable=False)
    description = Column(String, nullable=False)

    pre_post = Column(Boolean, nullable=False)


class LabResultDefinition(db.Model):
    __tablename__ = 'lab_result_definitions'

    id = Column(Integer, primary_key=True)

    lab_order_definition_id = Column(Integer, ForeignKey('lab_order_definitions.id'), nullable=False)

    code = Column(String, nullable=False)
    description = Column(String, nullable=False)


class LabOrder(DataSource, PatientMixin, UnitMixin, CreatedModifiedMixin):
    __tablename__ = 'lab_orders'

    id = Column(Integer, ForeignKey('lab_orders.id'), primary_key=True)

    lab_order_definition_id = Column(Integer, ForeignKey('lab_order_definitions.id'), nullable=False)
    lab_order_definition = relationship('LabOrderDefinition')

    date = Column(Date, nullable=False)
    pre_post = Column(String)

    lab_results = relationship('LabResult', cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'hospitalisations',
    }


class LabResult(db.Model):
    __tablename__ = 'lab_results'

    id = Column(Integer, primary_key=True)

    lab_order_id = Column(Integer, ForeignKey('lab_orders.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    lab_order = relationship('LabOrder')

    lab_result_definition_id = Column(Integer, ForeignKey('lab_result_definitions.id'), nullable=False)
    lab_result_definition = relationship('LabResultDefinition')

    value = Column(Numeric, nullable=False)