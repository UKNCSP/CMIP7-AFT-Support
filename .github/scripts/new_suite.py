import json
import subprocess
import re
import os

TEMPLATE = """
# {suite_id}

## Quality assurance checklists

Please read the ExperimentGuidance guidance notes before completing the table below. Where an ensemble member is copied from a previously-reviewed job for the same experiment, only the first 6 rows of the second table are relevant: the rest can be ignored. 

### Diagnostic configuration
| Task | Date completed | Notes | Reviewed by |
| --- | --- | --- | --- |
| Suite metadata is compliant (experiment names, ensemble member ID, ...). See [wiki:CMIP6/RoseSuiteMetadata]  |  |  |
| For Met Office runs, experiment added to CREM database. (ARCHER equivalent?) |  |  |  |
| More generally, all planned runs for this MIP have been added to CREM (should be reviewed before any MIP runs start) |  |  |  |
| Diagnostic setup appropriate for mip_convert |  |  | |
| Test data for any new diagnostics has been produced and checked (see ExperimentGuidance#Runsetup) | |  | |

### Science / technical review**

| Task | Date completed | Notes | Reviewed by |
| --- | --- | --- | --- |
| Diagnostic setup correctly configured for this experiment | | Only relevant if this experiment has specific diagnostic requirements  **todo: link to diagnostic documentation when ready** | |
| Suite revision reviewed corresponds to that in suite description above |  |  |  |
| All suite changes committed to repository |  | Suite revision reviewed: rNNNN |  |
| Changes from predecessor suite are documented and consistent with experimental design (refer to documentation for relevant MIP: [wiki:MIPDocumentation]) | | | |
| The job is consistent with other related runs (e.g. other ensemble members, historical->SSP continuations) | | | |
| Start and end dates are correct (see ExperimentGuidance#Runsetup) | | | |
| Job descended from correct HadGEM3 / UKESM job: baseline configuration suite ID and revision (above) are listed under the appropriate MIP in [wiki:MIPDocumentation] | | This is to minimise the propagation of errors discovered after the first runs have begun. | |
| If setup deviates from experimental protocol as defined by ES-doc, have these exceptions been recorded above? |  |  |  |
| Does suite use branches for any component model? | | | |
| If so has this code been accepted for a future release of the component model? |  | | |
| Have all forcing datasets been reviewed? See ancil:wiki:CMIP6/ForcingData. | | | |
"""


outputdir = 'suites'

# obtain results NOTE LIMIT TO 2000
result = subprocess.check_output('gh issue list -L 2000 --json number,title,body,labels'.split())

data = json.loads(result)

for entry in data:
    if not entry['title'].startswith('New simulation'):
        continue
    if match:= re.search('(u-[a-z0-9]{5})', entry['title']):
        suite_id = match.groups()[0]
        expected_file = os.path.join(outputdir, suite_id)
        if not os.path.exists(expected_file):
            with open(expected_file, 'w') as fh:
                fh.write(TEMPLATE.format(suite_id=suite_id))
