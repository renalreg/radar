from radar.models.cohorts import Cohort


def get_radar_cohort():
    return Cohort.query.filter(Cohort.code == 'RADAR').one()


def is_radar_cohort(cohort):
    return cohort.code == 'RADAR'
