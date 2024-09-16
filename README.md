# radar-self-enrolment-definitions
Definition files to define the contents and behaviour of various parts of self enrolment portal such as study information, eligibility, consent and more.

The definitions are used by the self enrolment portal to render the [UI](https://github.com/RADAR-base/radar-self-enrolment-ui) and validate the user input. The definitions are written in JSON format and are loaded by the portal at runtime.

## Definitions

The definitions are divided into multiple files based on the type of information they define. The definitions are stored in the per-project directories.

#### Study Information

The study information definitions define the study information displayed to the user on the portal's study home page. The study information definitions are stored in the `study_info` directory.

#### Eligibility

The eligibility definitions define the eligibility criteria that the user must meet to be able to participate in the study. The eligibility definitions are stored in the `eligibility` directory.

#### Consent

The consent definitions define mandatory and optional consent questions that the user must agree to before participating in the study. The consent definitions are stored in the `consent` directory.


## Scripts

The `scripts` directory contains scripts to pull definitions from external systems such as REDCap or local CSV files.

#### REDCap

The `/scripts/redcap/main.py` script pulls the study information, eligibility and consent definitions from a REDCap project.

Copy the `config.py.template` file to `config.py` and update the configuration values.

The script will update values in `{}` in the config value for project, form_name and version.
For example, `GITHUB_BRANCH="{project}"` will be updated to `GITHUB_BRANCH="REDCAP_PROJECT_NAME"` dynamically based on the name of the REDCap project.

The script requires the following configuration values:

```python
    REDCAP_PROJECT="" # REDCap project ID
    REDCAP_TOKEN="" # REDCap API token
    REDCAP_API_URL="" # URL to the REDCap API
    REDCAP_FIELDS=[] # List of fields to pull from REDCap. If empty, all fields will be pulled.

    GITHUB_TOKEN="" # GitHub API token
    GITHUB_OWNER="RADAR-base" # GitHub owner
    GITHUB_REPO="radar-self-enrolment-definitions" # GitHub repository
    GITHUB_BRANCH="{project}" # GitHub branch
    GITHUB_COMMIT_MESSAGE="Updated content from redcap project {project}" # Commit message

    VERSION="v1" # Version of the sync
    STUDY_INFO_FORM="sep_study_info" # Name of the form in REDCap that contains the study information
    CONSENT_FORM="sep_consent"     # Name of the form in REDCap that contains the consent information
    ELIGIBILITY_FORM="sep_eligibility" # Name of the form in REDCap that contains the eligibility information
```

Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

Run the script using the following command:

```bash
python main.py
```

Select the prompts to achieve the desired outcome.

The script will pull the definitions from the REDCap project and store them in the respective directories.
