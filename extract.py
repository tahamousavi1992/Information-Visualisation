
import csv
import pandas as pd
import datetime

def load_csv(file_name, includes, nrows: int = 1000000):
    data = pd.read_csv(file_name, delimiter='|', header=0, usecols=lambda column: column in includes, nrows=nrows)
    return data


def load_all_data():
    studies = load_csv(file_name = 'data/studies.txt', includes = ['nct_id', 'study_first_submitted_date', 'completion_date', 'study_type',
    'brief_title', 'official_title' , 'overall_status' ,'phase' ,'enrollment', 'source'])
    studies.dropna(subset=['study_type'], inplace=True)

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

def filter_by_date(studies, date_range, study_type, study_gender):
    min_date = datetime.datetime.fromtimestamp(date_range[0])
    max_date = datetime.datetime.fromtimestamp(date_range[1])
    gender = study_gender
    if study_gender == 'Both male and female':
        gender = 'All'
    filtered_studies = studies[
                (study_type == None or study_type == 'All' or  studies['study_type'] == study_type) &
                (study_gender == None or study_gender == 'All' or  studies['gender'] == gender) &
                (pd.to_datetime(studies['study_first_submitted_date']) >= min_date) &
                (pd.to_datetime(studies['study_first_submitted_date']) <= max_date)]
    return filtered_studies
