from flask import url_for
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from radar.lib.database import db
from radar.models.base import PatientMixin, UnitMixin, CreatedModifiedMixin, DataSource
from radar.patients.lab_results.concepts import LabOrderToLabOrderConcept


class LabOrderDefinition(db.Model):
    __tablename__ = 'lab_order_definitions'

    id = Column(Integer, primary_key=True)

    code = Column(String, nullable=False)
    description = Column(String, nullable=False)

    pre_post = Column(Boolean, nullable=False)

    lab_result_definitions = relationship('LabResultDefinition')


class LabResultDefinition(db.Model):
    __tablename__ = 'lab_result_definitions'

    id = Column(Integer, primary_key=True)

    lab_order_definition_id = Column(Integer, ForeignKey('lab_order_definitions.id'), nullable=False)

    code = Column(String, nullable=False)
    description = Column(String, nullable=False)
    units = Column(String)

    # TODO use this to order fields
    # weight = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('lab_order_definition_id', 'code'),
    )


class LabOrder(DataSource, PatientMixin, UnitMixin, CreatedModifiedMixin):
    __tablename__ = 'lab_orders'

    id = Column(Integer, ForeignKey('data_sources.id'), primary_key=True)

    lab_order_definition_id = Column(Integer, ForeignKey('lab_order_definitions.id'), nullable=False)
    lab_order_definition = relationship('LabOrderDefinition')

    date = Column(Date, nullable=False)
    pre_post = Column(String)

    lab_results = relationship('LabResult', cascade='all, delete-orphan')

    __mapper_args__ = {
        'polymorphic_identity': 'lab_orders',
    }

    def to_concepts(self):
        return [
            LabOrderToLabOrderConcept(self)
        ]

    def can_view(self, current_user):
        return self.patient.can_view(current_user)

    def can_edit(self, current_user):
        return self.patient.can_edit(current_user)

    def view_url(self):
        return url_for('lab_results.view_lab_result', patient_id=self.patient.id, record_id=self.id)

    def edit_url(self):
        return url_for('lab_results.edit_lab_result', patient_id=self.patient.id, record_id=self.id)


class LabResult(db.Model):
    __tablename__ = 'lab_results'

    id = Column(Integer, primary_key=True)

    lab_order_id = Column(Integer, ForeignKey('lab_orders.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    lab_order = relationship('LabOrder')

    lab_result_definition_id = Column(Integer, ForeignKey('lab_result_definitions.id'), nullable=False)
    lab_result_definition = relationship('LabResultDefinition')

    value = Column(Numeric, nullable=False)