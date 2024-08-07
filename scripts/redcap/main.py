import glob
from pathlib import Path
import re
from config import *
from redcap_client import RedcapClient
import pandas as pd
import pickle
from radar_github.github_client import GitHubClient

def parse_choices(x):
    if x['select_choices_or_calculations'] and isinstance(x['select_choices_or_calculations'], str):
        x['select_choices_or_calculations'] = x['select_choices_or_calculations'].split('|')
        choices = []
        for choice in x['select_choices_or_calculations']:
            values = choice.split(',')
            final_label = values[1]
            if len(values) > 2:
                final_label = choice[choice.index(',') + 1:]
            choices.append({
                'code': values[0].strip(),
                'label': final_label.strip()
            })
        x['select_choices_or_calculations'] = choices
    return x

def special_input_types(x):
    if x['field_type'] == 'radio':
        if 'range-type' in x['field_annotation']:
            x['field_type'] = 'range'
        elif 'range-info-type' in x['field_annotation']:
            x['field_type'] = 'range-info'
        elif 'info-type' in x['field_annotation']:
            x['field_type'] = 'info'
        elif 'matrix-radio-type' in x['field_annotation']:
            x['field_type'] = 'matrix-radio'
        elif 'eval' in x['field_annotation']:
            x['field_type'] = 'eval'
    elif x['field_type'] == 'text':
        if 'duration' in x['field_annotation']:
            x['text_validation_type_or_show_slider_number'] = 'duration'
    return x

def parse_redcap_data(data: pd.DataFrame) -> str:
    return data.apply(special_input_types, axis=1).apply(parse_choices, axis=1).to_json(orient='records', indent=4)

def format_string(path, form_name=None):
    if form_name is not None:
        return path.format(project=REDCAP_PROJECT, version=VERSION, form_name=form_name)
    else:
        return path.format(project=REDCAP_PROJECT, version=VERSION)

def parse_instrument_file(df):
    df = df.rename(columns={'Variable / Field Name': 'field_name',
                                'Choices, Calculations, OR Slider Labels': 'select_choices_or_calculations', 
                                'Text Validation Type OR Show Slider Number': 'text_validation_type_or_show_slider_number'
                            })
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    df.cols = [pattern.sub('_', x).lower() for x in df.columns]
    return df

def main():
    # get input from user: 1. pull from redcap, 2. read from csv file
    input_type = input("Enter 1 to pull data from REDCap or 2 to read data from a REDCap instrument export CSV file: ")
    if input_type == '1':
        redcap_client = RedcapClient(REDCAP_API_URL, REDCAP_TOKEN)

        # Uncomment the following lines to save the metadata to a file for testing purposes

        # metadata_path = Path('metadata.pkl')
        # if metadata_path.exists():
        #     with open('metadata.pkl', 'rb') as f:
        #         metadata = pickle.load(f)
        # else:
        metadata = pd.DataFrame(redcap_client.get_metadata())
        #     with open('metadata.pkl', 'wb') as f:
        #         pickle.dump(metadata, f)
    elif input_type == '2':
        forms = []
        type_of_form = input("Enter 1 to enter path of each form or 2 to read multiple forms from a directory: ")
        if type_of_form == '1':
            csv_files = []
            for q in [STUDY_INFO_FORM, CONSENT_FORM, ELIGIBILITY_FORM]:
                form_path = input(f"Enter the path to the metadata CSV file for {q}: ")
                csv_files.append(form_path)

        elif type_of_form == '2':
            form_dir = input("Enter the path to the directory containing the metadata CSV files: ")
            # load all csv files in the directory
            csv_files = glob.glob(form_dir + '/*.csv')
        else:
            print("Invalid input. Please enter 1 or 2.")
            return

        for q in csv_files:
            form = pd.read_csv(q)
            form = parse_instrument_file(form)
            form.append(metadata)
        metadata = pd.concat(forms)
    else:
        print("Invalid input. Please enter 1 or 2.")
        return
    
    if len(REDCAP_FIELDS) > 0:
        metadata = metadata[metadata['field_name'].isin(REDCAP_FIELDS)]

    study_info = metadata[metadata['form_name'] == STUDY_INFO_FORM]
    consent = metadata[metadata['form_name'] == CONSENT_FORM]
    eligibility = metadata[metadata['form_name'] == ELIGIBILITY_FORM]

    github_client = GitHubClient(GITHUB_TOKEN)
    repo = github_client.get_repo(f'{GITHUB_OWNER}/{GITHUB_REPO}')

    if consent.shape[0] > 0:
        github_client.update_or_create_file(
            repo=repo,
            file_path=ROOT_PATH + format_string(CONSENT_PATH),
            data=parse_redcap_data(consent),
            branch=GITHUB_BRANCH,
            commit_message=format_string(GITHUB_COMMIT_MESSAGE)
        )
    else:
        print(f"No {CONSENT_FORM} found in the metadata.")
    
    if study_info.shape[0] > 0:
        github_client.update_or_create_file(
            repo=repo,
            file_path=ROOT_PATH + format_string(STUDY_INFO_PATH),
            data=parse_redcap_data(study_info),
            branch=format_string(GITHUB_BRANCH),
            commit_message=format_string(GITHUB_COMMIT_MESSAGE)
        )
    else:
        print(f"No {STUDY_INFO_FORM} form found in the metadata.")
    
    if eligibility.shape[0] > 0:
        github_client.update_or_create_file(
            repo=repo,
            file_path= ROOT_PATH + format_string(ELIGIBILITY_PATH),
            data=parse_redcap_data(eligibility),
            branch=GITHUB_BRANCH,
            commit_message=format_string(GITHUB_COMMIT_MESSAGE)
        )
    else:
        print(f"No {ELIGIBILITY_FORM} found in the metadata.")

if __name__ == "__main__":
    main()