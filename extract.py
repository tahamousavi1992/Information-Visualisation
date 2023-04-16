
import csv
import pandas as pd

def load_csv(file_name, includes, nrows: int = 1000000):
    data = pd.read_csv(file_name, delimiter='|', header=0, usecols=lambda column: column in includes, nrows=nrows)
    return data


def load_all_data():
    studies = load_csv(file_name = 'data/studies.txt', includes = ['nct_id', 'study_first_submitted_date', 'completion_date', 'study_type',
    'brief_title', 'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source'])

    eligibilities = load_csv(file_name = 'data/eligibilities.txt', includes = ['nct_id', 'gender', 'minimum_age', 'maximum_age'])
    studies = pd.merge(studies, eligibilities, on='nct_id', how='left')

    sponsors = load_csv(file_name = 'data/sponsors.txt', includes = ['nct_id', 'agency_class', 'lead_or_collaborator', 'name'])
    conditions = load_csv(file_name = 'data/conditions.txt', includes = ['nct_id', 'downcase_name'])
    interventions = load_csv(file_name = 'data/interventions.txt', includes = ['nct_id', 'intervention_type', 'name'])
    facilities = load_csv(file_name = 'data/facilities.txt', includes = ['nct_id', 'status','name','city','state','country'])
    design_groups = load_csv(file_name = 'data/design_groups.txt', includes = ['nct_id', 'group_type']).dropna(subset=['group_type'], inplace=False)



    # studies : ['nct_id', 'study_first_submitted_date', 'completion_date', 'study_type','brief_title',
    #  'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source',
    #  'downcase_name', 'intervention_type', 'name', 'gender', 'minimum_age', 'maximum_age']
    return studies, sponsors, facilities, design_groups, conditions, interventions
