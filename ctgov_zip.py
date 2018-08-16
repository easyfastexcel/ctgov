import re
import yaml
import zipfile
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint as ppt

# from akpy.str_mgmt import *
from time_mgmt import *


class StudyData:
    dict_base_study = {
        # '_id': None,
    }

    # def __init__(self, xml_text):
    #     self.dict_base_study = {
    #         '_id': None,
    #     }
    #     self.soup = BeautifulSoup(xml_text, 'lxml')
    #     self.soup = self.soup.clinical_study


def get_zip_filename_list(dirpath_zipfile):
    obj_zipfile = zipfile.ZipFile(dirpath_zipfile, 'r')
    return obj_zipfile.namelist()[1:]


def add_id_info(base_dict, soup_clinical_study):
    base_dict['study_ids'] = {
        'nct_id': None,
        'nct_alias': None,
        'org_study_id': None,
        'secondary_id': None
    }
    for c in soup_clinical_study.id_info.find_all(True):
        base_dict['study_ids'][c.name] = c.text.strip()
        if c.name == 'nct_id':
            base_dict['_id'] = c.text.strip()
    return base_dict


def add_brief_title(base_dict, soup_clinical_study):
    base_dict['brief_title'] = None
    if soup.brief_title is not None:
        base_dict['brief_title'] = soup_clinical_study.brief_title.text.strip()
    return base_dict


def add_acronym(base_dict, soup_clinical_study):
    base_dict['acronym'] = None
    if soup.acronym is not None:
        base_dict['acronym'] = soup_clinical_study.acronym.text.strip()
    return base_dict


def add_official_title(base_dict, soup_clinical_study):
    base_dict['official_title'] = None
    if soup.official_title is not None:
        base_dict['official_title'] = soup_clinical_study.official_title.text.strip()
    return base_dict


def add_sponsors(base_dict, soup_clinical_study):
    base_dict['sponsors'] = {
        'lead_sponsor': {
            'agency': None,
            'agency_class': None
        },
        'collaborator': None
    }

    sponsors = soup_clinical_study.sponsors

    lead_sponsor = sponsors.lead_sponsor
    if lead_sponsor.agency is not None:
        base_dict['sponsors']['lead_sponsor']['agency'] = lead_sponsor.agency.text.strip()
    if lead_sponsor.agency_class is not None:
        base_dict['sponsors']['lead_sponsor']['agency_class'] = lead_sponsor.agency_class.text.strip()

    if sponsors.collaborator is not None:
        list_comps = []
        c_name = None
        c_class = None
        for collaborator in sponsors.find_all(['collaborator']):
            if collaborator.agency is not None:
                c_name = collaborator.agency.text.strip()
            if collaborator.agency_class is not None:
                c_class = collaborator.agency_class.text.strip()
            comp = (c_name, c_class)
            list_comps.append(comp)
        base_dict['sponsors']['collaborator'] = list_comps

    return base_dict


def add_source(base_dict, soup_clinical_study):
    base_dict['source'] = None
    if soup.source is not None:
        base_dict['source'] = soup_clinical_study.source.text.strip()
    return base_dict


def add_oversight_info(base_dict, soup_clinical_study):
    base_dict['oversight_info'] = {
        'has_dmc': None,
        'is_fda_regulated_drug': None,
        'is_fda_regulated_device': None,
        'is_unapproved_device': None,
        'is_ppsd': None,
        'is_us_export': None
    }

    if soup_clinical_study.oversight_info is not None:
        for c in soup_clinical_study.oversight_info.find_all(True):
            base_dict['oversight_info'][c.name] = c.text.strip()

    return base_dict


def add_brief_summary(base_dict, soup_clinical_study):
    base_dict['brief_summary'] = None
    if soup_clinical_study.brief_summary is not None:
        el_text = soup_clinical_study.brief_summary.text.strip().replace('\n', '').replace('\r', '')
        base_dict['brief_summary'] = ' '.join(el_text.split())
    return base_dict


def add_detailed_description(base_dict, soup_clinical_study):
    base_dict['detailed_description'] = None
    if soup_clinical_study.brief_summary is not None:
        el_text = soup_clinical_study.detailed_description.text.strip().replace('\n', '').replace('\r', '')
        base_dict['detailed_description'] = ' '.join(el_text.split())
    return base_dict


def add_overall_status(base_dict, soup_clinical_study):
    base_dict['overall_status'] = None
    if soup_clinical_study.overall_status is not None:
        base_dict['overall_status'] = soup_clinical_study.overall_status.text.strip()
    return base_dict


def add_last_known_status(base_dict, soup_clinical_study):
    base_dict['last_known_status'] = None
    if soup_clinical_study.last_known_status is not None:
        base_dict['last_known_status'] = soup_clinical_study.last_known_status.text.strip()
    return base_dict


def add_why_stopped(base_dict, soup_clinical_study):
    base_dict['why_stopped'] = None
    if soup_clinical_study.why_stopped is not None:
        base_dict['why_stopped'] = soup_clinical_study.why_stopped.text.strip()
    return base_dict


def add_start_date(base_dict, soup_clinical_study):
    base_dict['start_date'] = {
        'date': None,
        'date_type': None
    }
    if soup_clinical_study.start_date is not None:
        base_dict['start_date']['date'] = soup_clinical_study.start_date.text.strip()
        if soup_clinical_study.start_date.attrs is not None:
            base_dict['start_date']['date_type'] = soup_clinical_study.start_date.attrs['type']
    return base_dict


def add_completion_date(base_dict, soup_clinical_study):
    base_dict['completion_date'] = {
        'date': None,
        'date_type': None
    }
    if soup_clinical_study.completion_date is not None:
        base_dict['completion_date']['date'] = soup_clinical_study.completion_date.text.strip()
        if soup_clinical_study.completion_date.attrs is not None:
            base_dict['completion_date']['date_type'] = soup_clinical_study.completion_date.attrs['type']
    return base_dict


def add_primary_completion_date(base_dict, soup_clinical_study):
    base_dict['primary_completion_date'] = {
        'date': None,
        'date_type': None
    }
    if soup_clinical_study.primary_completion_date is not None:
        base_dict['primary_completion_date']['date'] = soup_clinical_study.primary_completion_date.text.strip()
        if soup_clinical_study.primary_completion_date.attrs is not None:
            base_dict['primary_completion_date']['date_type'] = soup_clinical_study.primary_completion_date.attrs['type']
    return base_dict


def add_phase(base_dict, soup_clinical_study):
    base_dict['phase'] = None
    if soup_clinical_study.phase is not None:
        base_dict['phase'] = soup_clinical_study.phase.text.strip()
    return base_dict


def add_study_type(base_dict, soup_clinical_study):
    base_dict['study_type'] = None
    if soup_clinical_study.study_type is not None:
        base_dict['study_type'] = soup_clinical_study.study_type.text.strip()
    return base_dict


def add_has_expanded_access(base_dict, soup_clinical_study):
    base_dict['has_expanded_access'] = {
        'expanded_access_type_individual': None,
        'expanded_access_type_intermediate': None,
        'expanded_access_type_treatment': None
    }
    if soup_clinical_study.has_expanded_access is not None:
        if soup_clinical_study.has_expanded_access.expanded_access_type_individual is not None:
            base_dict['has_expanded_access']['expanded_access_type_individual'] = \
                soup_clinical_study.has_expanded_access.expanded_access_type_individual.text.strip()
        if soup_clinical_study.has_expanded_access.expanded_access_type_intermediate is not None:
            base_dict['has_expanded_access']['expanded_access_type_intermediate'] = \
                soup_clinical_study.has_expanded_access.expanded_access_type_intermediate.text.strip()
        if soup_clinical_study.has_expanded_access.expanded_access_type_treatment is not None:
            base_dict['has_expanded_access']['expanded_access_type_treatment'] = \
                soup_clinical_study.has_expanded_access.expanded_access_type_treatment.text.strip()
    return base_dict


def add_study_design_info(base_dict, soup_clinical_study):
    base_dict['study_design_info'] = {
        'allocation': None,
        'intervention_model': None,
        'intervention_model_description': None,
        'primary_purpose': None,
        'observational_model': None,
        'time_perspective': None,
        'masking': None,
        'masking_description': None
    }
    if soup_clinical_study.study_design_info is not None:
        if soup_clinical_study.study_design_info.allocation is not None:
            base_dict['study_design_info']['allocation'] = \
                soup_clinical_study.study_design_info.allocation.text.strip()
        if soup_clinical_study.study_design_info.intervention_model is not None:
            base_dict['study_design_info']['intervention_model'] = \
                soup_clinical_study.study_design_info.intervention_model.text.strip()
        if soup_clinical_study.study_design_info.intervention_model_description is not None:
            base_dict['study_design_info']['intervention_model_description'] = \
                soup_clinical_study.study_design_info.intervention_model_description.text.strip()
        if soup_clinical_study.study_design_info.primary_purpose is not None:
            base_dict['study_design_info']['primary_purpose'] = \
                soup_clinical_study.study_design_info.primary_purpose.text.strip()
        if soup_clinical_study.study_design_info.observational_model is not None:
            base_dict['study_design_info']['observational_model'] = \
                soup_clinical_study.study_design_info.observational_model.text.strip()
        if soup_clinical_study.study_design_info.time_perspective is not None:
            base_dict['study_design_info']['time_perspective'] = \
                soup_clinical_study.study_design_info.time_perspective.text.strip()
        if soup_clinical_study.study_design_info.masking is not None:
            base_dict['study_design_info']['masking'] = \
                soup_clinical_study.study_design_info.masking.text.strip()
        if soup_clinical_study.study_design_info.masking_description is not None:
            base_dict['study_design_info']['masking_description'] = \
                soup_clinical_study.study_design_info.masking_description.text.strip()
    return base_dict


def add_target_duration(base_dict, soup_clinical_study):
    base_dict['target_duration'] = None
    if soup_clinical_study.target_duration is not None:
        base_dict['target_duration'] = soup_clinical_study.target_duration.text.strip()
    return base_dict


def add_primary_outcome(base_dict, soup_clinical_study):
    base_dict['primary_outcomes'] = None
    primary_outcomes = []
    if soup_clinical_study.primary_outcome is not None:
        pos = soup.find_all(['primary_outcome'])
        for po in pos:
            primary_outcome = {
                'measure': None,
                'time_frame': None,
                'description': None
            }
            if po.measure is not None:
                primary_outcome['measure'] = po.measure.text.strip()
            if po.time_frame is not None:
                primary_outcome['time_frame'] = po.time_frame.text.strip()
            if po.description is not None:
                primary_outcome['description'] = po.description.text.strip()
            primary_outcomes.append(primary_outcome)

    base_dict['primary_outcomes'] = primary_outcomes

    return base_dict


def add_secondary_outcome(base_dict, soup_clinical_study):
    base_dict['secondary_outcome'] = None
    secondary_outcomes = []
    if soup_clinical_study.secondary_outcome is not None:
        sos = soup.find_all(['secondary_outcome'])
        for so in sos:
            secondary_outcome = {
                'measure': None,
                'time_frame': None,
                'description': None
            }
            if so.measure is not None:
                secondary_outcome['measure'] = so.measure.text.strip()
            if so.time_frame is not None:
                secondary_outcome['time_frame'] = so.time_frame.text.strip()
            if so.description is not None:
                secondary_outcome['description'] = so.description.text.strip()
            secondary_outcomes.append(secondary_outcome)
    base_dict['secondary_outcome'] = secondary_outcomes
    return base_dict


def add_other_outcome(base_dict, soup_clinical_study):
    base_dict['other_outcome'] = None
    other_outcomes = []
    if soup_clinical_study.other_outcome is not None:
        oos = soup.find_all(['other_outcome'])
        for oo in oos:
            other_outcome = {
                'measure': None,
                'time_frame': None,
                'description': None
            }
            if oo.measure is not None:
                other_outcome['measure'] = oo.measure.text.strip()
            if oo.time_frame is not None:
                other_outcome['time_frame'] = oo.time_frame.text.strip()
            if oo.description is not None:
                other_outcome['description'] = oo.description.text.strip()
            other_outcomes.append(other_outcome)
    base_dict['other_outcome'] = other_outcomes
    return base_dict


def add_number_of_arms(base_dict, soup_clinical_study):
    base_dict['number_of_arms'] = None
    if soup_clinical_study.number_of_arms is not None:
        base_dict['number_of_arms'] = soup_clinical_study.number_of_arms.text.strip()
    return base_dict


def add_number_of_groups(base_dict, soup_clinical_study):
    base_dict['number_of_groups'] = None
    if soup_clinical_study.number_of_groups is not None:
        base_dict['number_of_groups'] = soup_clinical_study.number_of_groups.text.strip()
    return base_dict


def add_enrollment(base_dict, soup_clinical_study):
    base_dict['enrollment'] = {
        'total': None,
        'type': None
    }
    if soup_clinical_study.enrollment is not None:
        base_dict['enrollment']['total'] = soup_clinical_study.enrollment.text.strip()
        if soup_clinical_study.enrollment.attrs is not None:
            base_dict['enrollment']['type'] = soup_clinical_study.enrollment.attrs['type']
    return base_dict


def add_condition(base_dict, soup_clinical_study):
    base_dict['condition'] = None
    conditions = []
    if soup_clinical_study.condition is not None:
        conds = soup_clinical_study.find_all(['condition'])
        for cond in conds:
            conditions.append(cond.text.strip())
    base_dict['condition'] = conditions
    return base_dict


def add_arm_group(base_dict, soup_clinical_study):
    base_dict['arm_group'] = None
    arm_groups = []
    if soup_clinical_study.arm_group is not None:
        arms = soup_clinical_study.find_all(['arm_group'])
        for arm in arms:
            ar_group = {
                'arm_group_label': None,
                'arm_group_type': None,
                'description': None
            }
            if arm.arm_group_label is not None:
                ar_group['arm_group_label'] = arm.arm_group_label.text.strip()
            if arm.arm_group_type is not None:
                ar_group['arm_group_type'] = arm.arm_group_type.text.strip()
            if arm.description is not None:
                ar_group['description'] = arm.description.text.strip()
            arm_groups.append(ar_group)
    base_dict['arm_group'] = arm_groups
    return base_dict


def add_intervention(base_dict, soup_clinical_study):
    base_dict['intervention'] = None
    interventions = []
    if soup_clinical_study.intervention is not None:
        intervs = soup_clinical_study.find_all(['intervention'])
        for interv in intervs:
            intervention_dict = {
                'intervention_type': None,
                'intervention_name': None,
                'description': None,
                'arm_group_label': None,
                'other_name': None
            }
            if interv.intervention_type is not None:
                intervention_dict['intervention_type'] = interv.intervention_type.text.strip()
            if interv.intervention_name is not None:
                intervention_dict['intervention_name'] = interv.intervention_name.text.strip()
            if interv.description is not None:
                intervention_dict['description'] = interv.description.text.strip()
            if interv.arm_group_label is not None:
                intervention_dict['arm_group_label'] = interv.arm_group_label.text.strip()
            if interv.other_name is not None:
                intervention_dict['other_name'] = interv.other_name.text.strip()
            interventions.append(intervention_dict)
    base_dict['intervention'] = interventions
    return base_dict


def add_biospec_retention(base_dict, soup_clinical_study):
    base_dict['biospec_retention'] = None
    if soup_clinical_study.biospec_retention is not None:
        base_dict['biospec_retention'] = soup_clinical_study.biospec_retention.text.strip()
    return base_dict


def add_biospec_descr(base_dict, soup_clinical_study):
    base_dict['biospec_descr'] = None
    if soup_clinical_study.biospec_descr is not None:
        base_dict['biospec_descr'] = soup_clinical_study.biospec_descr.text.strip()
    return base_dict


def add_eligibility(base_dict, soup_clinical_study):
    base_dict['eligibility'] = {
        'study_pop': None,
        'sampling_method': None,
        'criteria': None,
        'gender': None,
        'gender_based': None,
        'gender_description': None,
        'minimum_age': None,
        'maximum_age': None,
        'healthy_volunteers': None
    }
    if soup_clinical_study.eligibility is not None:
        if soup_clinical_study.eligibility.study_pop is not None:
            base_dict['eligibility']['study_pop'] = soup_clinical_study.eligibility.study_pop.text.strip()
        if soup_clinical_study.eligibility.sampling_method is not None:
            base_dict['eligibility']['sampling_method'] = soup_clinical_study.eligibility.sampling_method.text.strip()
        if soup_clinical_study.eligibility.criteria is not None:
            el_text = soup_clinical_study.eligibility.criteria.text.strip().replace('\n', '').replace('\r', '')
            base_dict['eligibility']['criteria'] = ' '.join(el_text.split())
        if soup_clinical_study.eligibility.gender is not None:
            base_dict['eligibility']['gender'] = soup_clinical_study.eligibility.gender.text.strip()
        if soup_clinical_study.eligibility.gender_based is not None:
            base_dict['eligibility']['gender_based'] = soup_clinical_study.eligibility.gender_based.text.strip()
        if soup_clinical_study.eligibility.gender_description is not None:
            base_dict['eligibility']['gender_description'] = soup_clinical_study.eligibility.gender_description.text.strip()
        if soup_clinical_study.eligibility.minimum_age is not None:
            base_dict['eligibility']['minimum_age'] = soup_clinical_study.eligibility.minimum_age.text.strip()
        if soup_clinical_study.eligibility.maximum_age is not None:
            base_dict['eligibility']['maximum_age'] = soup_clinical_study.eligibility.maximum_age.text.strip()
        if soup_clinical_study.eligibility.healthy_volunteers is not None:
            base_dict['eligibility']['healthy_volunteers'] = soup_clinical_study.eligibility.healthy_volunteers.text.strip()
    return base_dict


def add_overall_official(base_dict, soup_clinical_study):
    base_dict['overall_official'] = None
    overall_officials = []

    if soup_clinical_study.overall_official is not None:
        officials = soup_clinical_study.find_all(['overall_official'])
        for official in officials:
            overall_official_dict = {
                'first_name': None,
                'middle_name': None,
                'last_name': None,
                'degrees': None,
                'role': None,
                'affiliation': None
            }
            if official.first_name is not None:
                overall_official_dict['first_name'] = official.first_name.text.strip()
            if official.middle_name is not None:
                overall_official_dict['middle_name'] = official.middle_name.text.strip()
            if official.last_name is not None:
                overall_official_dict['last_name'] = official.last_name.text.strip()
            if official.degrees is not None:
                overall_official_dict['degrees'] = official.degrees.text.strip()
            if official.role is not None:
                overall_official_dict['role'] = official.role.text.strip()
            if official.affiliation is not None:
                overall_official_dict['affiliation'] = official.affiliation.text.strip()
            overall_officials.append(overall_official_dict)
    base_dict['overall_official'] = overall_officials
    return base_dict


def add_overall_contact(base_dict, soup_clinical_study):
    """
    Relevant .xsd structures:
    <xs:element name="overall_contact" type="contact_struct" minOccurs="0"/>

        contact_struct
        <xs:element name="first_name" type="xs:string" minOccurs="0"/>
        <xs:element name="middle_name" type="xs:string" minOccurs="0"/>
        <xs:element name="last_name" type="xs:string" minOccurs="0"/>
        <xs:element name="degrees" type="xs:string" minOccurs="0"/>
        <xs:element name="phone" type="xs:string" minOccurs="0"/>
        <xs:element name="phone_ext" type="xs:string" minOccurs="0"/>
        <xs:element name="email" type="xs:string" minOccurs="0"/>
    """

    base_dict['eligibility'] = {
        'study_pop': None,
        'sampling_method': None,
        'criteria': None,
        'gender': None,
        'gender_based': None,
        'gender_description': None,
        'minimum_age': None,
        'maximum_age': None,
        'healthy_volunteers': None
    }
    if soup_clinical_study.eligibility is not None:
        if soup_clinical_study.eligibility.study_pop is not None:
            base_dict['eligibility']['study_pop'] = soup_clinical_study.eligibility.study_pop.text.strip()
        if soup_clinical_study.eligibility.sampling_method is not None:
            base_dict['eligibility']['sampling_method'] = soup_clinical_study.eligibility.sampling_method.text.strip()
        if soup_clinical_study.eligibility.criteria is not None:
            el_text = soup_clinical_study.eligibility.criteria.text.strip().replace('\n', '').replace('\r', '')
            base_dict['eligibility']['criteria'] = ' '.join(el_text.split())
        if soup_clinical_study.eligibility.gender is not None:
            base_dict['eligibility']['gender'] = soup_clinical_study.eligibility.gender.text.strip()
        if soup_clinical_study.eligibility.gender_based is not None:
            base_dict['eligibility']['gender_based'] = soup_clinical_study.eligibility.gender_based.text.strip()
        if soup_clinical_study.eligibility.gender_description is not None:
            base_dict['eligibility']['gender_description'] = soup_clinical_study.eligibility.gender_description.text.strip()
        if soup_clinical_study.eligibility.minimum_age is not None:
            base_dict['eligibility']['minimum_age'] = soup_clinical_study.eligibility.minimum_age.text.strip()
        if soup_clinical_study.eligibility.maximum_age is not None:
            base_dict['eligibility']['maximum_age'] = soup_clinical_study.eligibility.maximum_age.text.strip()
        if soup_clinical_study.eligibility.healthy_volunteers is not None:
            base_dict['eligibility']['healthy_volunteers'] = soup_clinical_study.eligibility.healthy_volunteers.text.strip()
    return base_dict


if __name__ == '__main__':
    print('[', time_stamp(), ']', 'reading zip file')

    yaml_data = yaml.load(open('var.yaml', 'r'))
    zip_path = yaml_data['zip_path']

    z = zipfile.ZipFile(zip_path, 'r')

    list_filenames = z.namelist()[1:]
    print('[', time_stamp(), ']', len(list_filenames), 'xml files detected in zip')

    for filename in list_filenames[20000:20010]:
        file_content = z.open(filename).read().decode('utf-8')
        soup = BeautifulSoup(file_content, 'lxml').clinical_study

        dict_study = StudyData().dict_base_study
        dict_study = add_id_info(dict_study, soup)
        dict_study = add_brief_title(dict_study, soup)
        dict_study = add_sponsors(dict_study, soup)
        # dict_study = add_source(dict_study, soup)
        # dict_study = add_oversight_info(dict_study, soup)
        # dict_study = add_brief_summary(dict_study, soup)
        # dict_study = add_detailed_description(dict_study, soup)
        # dict_study = add_overall_status(dict_study, soup)
        # dict_study = add_last_known_status(dict_study, soup)
        # dict_study = add_why_stopped(dict_study, soup)
        # dict_study = add_start_date(dict_study, soup)
        # dict_study = add_completion_date(dict_study, soup)
        # dict_study = add_primary_completion_date(dict_study, soup)
        # dict_study = add_phase(dict_study, soup)
        # dict_study = add_study_type(dict_study, soup)
        # dict_study = add_has_expanded_access(dict_study, soup)
        # dict_study = add_study_design_info(dict_study, soup)
        # dict_study = add_target_duration(dict_study, soup)
        # dict_study = add_primary_outcome(dict_study, soup)
        # dict_study = add_secondary_outcome(dict_study, soup)
        # dict_study = add_other_outcome(dict_study, soup)
        # dict_study = add_number_of_arms(dict_study, soup)
        # dict_study = add_number_of_groups(dict_study, soup)
        # dict_study = add_enrollment(dict_study, soup)
        # dict_study = add_condition(dict_study, soup)
        # dict_study = add_arm_group(dict_study, soup)
        # dict_study = add_intervention(dict_study, soup)
        # dict_study = add_biospec_retention(dict_study, soup)
        # dict_study = add_biospec_descr(dict_study, soup)
        # dict_study = add_eligibility(dict_study, soup)
        dict_study = add_overall_official(dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        # dict_study = (dict_study, soup)
        ppt(dict_study)

        print('=============================================')
