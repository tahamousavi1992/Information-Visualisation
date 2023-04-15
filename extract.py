
import csv
import pandas as pd

def load_csv(file_name, includes):
    data = pd.read_csv(file_name, delimiter='|', header=0, usecols=lambda column: column in includes)
    return data


def load_all_data():
    studies = load_csv('data/studies.txt', ['nct_id', 'start_date', 'completion_date', 'study_type',
    'brief_title', 'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source', 'number_of_arms'])

    calculated_values = load_csv('data/calculated_values.txt', ['nct_id', 'number_of_facilities'])
    eligibilities = load_csv('data/eligibilities.txt', ['nct_id', 'gender', 'minimum_age', 'maximum_age'])
    pd.merge(studies, calculated_values, on='nct_id', how='left')
    pd.merge(studies, eligibilities, on='nct_id', how='left')

    sponsors = load_csv('data/sponsors.txt', ['nct_id', 'agency_class', 'lead_or_collaborator', 'name'])
    conditions = load_csv('data/conditions.txt', ['nct_id', 'downcase_name'])
    interventions = load_csv('data/interventions.txt', ['nct_id', 'intervention_type', 'name'])
    facilities = load_csv('data/facilities.txt', ['nct_id', 'status','name','city','state','country'])
    design_groups = load_csv('data/design_groups.txt', ['nct_id', 'group_type'])



    # studies : ['nct_id', 'start_date', 'completion_date', 'study_type','brief_title',
    #  'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source', 'number_of_arms',
    #  'downcase_name', 'intervention_type', 'name', 'number_of_facilities', 'gender', 'minimum_age', 'maximum_age']
    return studies, sponsors, facilities, design_groups, conditions, interventions
