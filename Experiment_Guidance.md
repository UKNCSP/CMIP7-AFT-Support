# Guidance for quality assurance of CMIP7 experiments -- DRAFT

In running experiments for a production experiment, the devil is in the detail. There are many things which can go wrong, with expensive consequences. However, there are steps which can be taken to minimise errors, and these are listed below. The motivation for these is science assurance: tedious but important tasks to ensure that the experiments (and the science based on them) is publishable and repeatable.

The [Run setup](#run-setup) section outlines how to use git issues for each experiment to support quality assurance.


## Experimental design configuration

Although the experimental protocol is set out by the MIP, in practice there are model-specific decisions which need to be made, to interpret and implement the design for our model.

1. Interpret experiment design specification. 
   * Discuss non-trivial choices with other MIP leads to ensure consistency between MIPs where appropriate. 
   * Document decisions on the CMIP7 github repository; for example, you could create a wiki page for your MIP. 
1. Develop any MIP-specific code
   * Lodge code in relevant model trunk (UM, NEMO, ...) to ensure that all CMIP7 code has been through appropriate review, and for future-proofing. 
1. Define diagnostic setup.
   * Check whether the model is able to produce your key diagnostics, and code up if essential.
   * Document any decisions on diagnostics which you decide not to include or for which you have to deviate from what has been requested. 
1. Download / create forcing data.
   * Liaise with providers in advance of official release if possible to minimise surprises.
   * If you are relying on another MIP to generate forcing data for you, ensure that they are aware of this. 
   * Avoid breaking up timeseries forcing files (historical/scenario) into e.g. 20-year chunks. It is better to split files by variable than by time period.
   * Ensure that the temporal coverage of forcing data extends beyond the start and end of the runs which will use it. The model interpolates between time records to its present time, so needs a valid field after the end of the run and before the start.
   * Ensure that all input files are in central locations, not user space.
   * There should be some technical and scientific review of all forcing data created for CMIP7 runs, just as for the model jobs themselves.  The MIP should decide what is appropriate, as long as any science decisions made in defining the forcing are documented.
1. Schedule HPC resources.
   * Outline discussions on HPC resources required for your experiments should begin as early as possible. 
   * Once you have decided which experiments to run, estimate how much resource (CPU time and disk space) all of your runs will require, and ensure that you have access to what you need. For Met Office HPC, agree which queue you will use.


## Run setup

1. Identify reviewers for job setup and arrange likely review dates in advance (to prevent delays due to reviewers being otherwise engaged). You will need a main reviewer (normally another scientist working on your MIP) and a diagnostic reviewer.
1. Ensure that ensemble member, forcing and realisation identifiers ("ripf" values) have been defined. 

***the following needs updating from TRAC to github***

1. Open an issue for this experiment and set the fields as follows:
   * Milestone -> MIP name (AerChemMIP, C4MIP, ...). Note: milestone "DECKhist" will be used to cover DECK, historical and spinup runs.
   * Component -> Model configuration
   * Keywords -> Experiment name (from the official list of names)
   * Summary -> "<experiment name> for <model configuration>" or something meaningful to you.
   * Description -> A longer summary of what the experiment does. There is space here to describe key aspects of this experiment, and any issues important to you or users of the run.
   * The issue will initially be assigned to no-one.  You should first assign it (using the "Assignees" panel at the left of the issue page) to whoever is going to set the experiment up, maybe yourself.  
1. Copy standard UKESM / HadGEM3 job and configure for this experiment (following any documentation specific to your MIP, see [#design above]). The standard (i.e. supported) jobs available for each model are 3 of the DECK experiments: piControl, historical and AMIP. See standard job pages for [StandardJobs HadGEM3-GC3.1] and [UkesmDeckStandardJobs UKESM1]
   * If your MIP has several experiments sharing a similar experimental or diagnostic setup, you may wish to create one or more standard jobs for your MIP to act as the source suites for your MIP experiments, rather than copy all suites directly from the standard DECK jobs.
   * On creating the model suite, Rose will ask for mandatory metadata for CMIP6 runs, which is required by the data delivery system. More information at [wiki:CMIP6/RoseSuiteMetadata]; seek advice from the data delivery team if unsure of any of these options. 
   * Ensure start and end dates are exactly right; if the experiment protocol gives years only, begin on the 1st Jan in the start year (not the preceding or subsequent Sep or Dec) and continue until at least 1st Jan of the end year plus 1 (i.e. 01/01/2015 for an 1850-2014 historical run).
   * Archiving restarts: For HadGEM3, the run should archive restarts in both January and December of each year. The January restarts are to allow other CMIP runs to branch from this run, while the December dumps allow a cleaner restart of the climate meaning system if there are problems with the run. For UKESM1, only January restarts are required, because it uses an alternative method to generate seasonal and annual means.
   * For Met Office runs archiving to MASS, select the appropriate duplex setting (`non_duplexed_set`) in the postproc app, under "Post Processing - common settings -> Moose Archiving". In general duplexing is recommended for production runs (`non_duplexed_set=false`).
   * For UKESM1, some experiments (e.g. DECK runs) should reset the diagnostic ocean ideal tracers (age of water and CFCs) when the experiment starts. For guidance, where you are branching from the piControl (historical, 1%CO2, 4xCO2) OMIP recommends resetting these diagnostic tracers at the start of the run so that the fields are independent of the branch point; on the other hand if you are branching from a historical or similar run it makes sense to inherit the fields of the parent run and continue their evolution. This resetting is activated by the switch `INIT_CFC_AGE=true` in rose-suite.conf. See note below on changing this to false after the run starts.
   * If you wish to be notified about future updates to the source job, add your username to the "cc" field of the corresponding experiment ticket.
1. From the ticket, link to a new wiki page: `wiki:runs/u-aa000` where u-aa000 is your suite ID. This will create a grey link with a question mark, which you should click to create the page. Select "!ExperimentDocumentation" from the drop-down menu, then "Create this page". Complete this wiki page with the details of your experiment; ensure that you include the ticket number at the top of the page, as this will create a link back to your ticket.
1. Configure [wiki:Diagnostics/Setup diagnostic setup]
   * If making additions to the standard jobs, check the “rules” for data layout as required by the data delivery system (will be documented on the UK-CMIP6 trac system, e.g. different frequencies must not share the same diagnostic files, or “STASH stream” for the UM).
   * If diagnostics are explicitly required at 00:00 on the first day of the run, i.e. the zeroth timestep (e.g. for regional model boundary conditions), seek advice from the UKESM core group.
1. Commit all changes you make to your rose suite. No runs should be based on suites with uncommitted working copies, as this leads to mistakes when copying and reviewing suites.
1. Ask the diagnostic reviewer to sign off the diagnostic setup checklist on the !ExperimentDocumentation page.
1. Output some test data for e.g. 1 year of the run.
   * For the first DECK runs, all fields will be checked and domain experts and MIP leads will be asked to contribute.
   * For other MIPs, new/altered diagnostics should be checked thoroughly, as should any fields of particular importance to that MIP.
   Aspects to check:
   * Plot the fields and verify that they are scientifically sensible and that packing precision is appropriate. This is a very time-consuming and tedious task and may need to be distributed across several people.
   * Is the model responding appropriately to any new forcing?
   * For some runs where significant changes are being made to the diagnostic setup, it will be appropriate to process a sample of data with //mip_convert// to check that the output can be delivered to the ESGF. **todo: Instructions will be linked here.**
1. When you are confident that everything is working and you have completed the QA checklist in the !ExperimentDocumentation page, assign the ticket to your main reviewer for "setup review".
   * In practice it will save time if the reviewer also looks at the model suite before you produce any test data.
   * Clearly the thoroughness of the review should vary from one experiment to another: if this experiment is very similar to another which has already been reviewed, then it may be sufficient to check that the job contains the expected differences. The DECK runs will be reviewed most thoroughly, and for individual MIPs it may make sense to have an in-depth review for the first experiments followed by a lighter touch for subsequent runs.
1. If the reviewer finds a problem they should reject the ticket and assign it back to you for setup. When they are happy they should approve assign to you for running and monitoring.


## Run and monitor

1. As soon as the run starts, create a branch of the suite called "running" and switch your working copy to point to this branch:
{{{
cd ${HOME}/roses/<suite-id>
fcm branch-create running
fcm switch running
}}}
   This ensures that any changes you need to make to the suite mid-run, such as restarting with an NRUN after a failure, are not copied into descendant suites. In other words, if someone copies your suite they get the suite as it started running, not some mid-run initialisation state. 
   * This also allows you to apply technical fixes or additional diagnostics which you want to be picked up by subsequent runs but not affect your running job, by committing these to the trunk and not the running branch:
{{{
fcm switch trunk
...make changes
fcm commit
fcm switch running
}}}
1. Apply some changes to the running branch which will only take effect if you need to restart with an NRUN (i.e `rose suite-run` without `--restart`) mid-way through the run:
 * Set the top-level option `BITCOMP_NRUN=true` (suite conf -> Run Initialisation and Cycling) to ensure that an NRUN will bit-compare with a previous CRUN.
 * Switch off atmosphere reconfiguration if it is on.
 * (For UKESM only) Set `INIT_CFC_AGE=false` in rose-suite.conf. This will ensure that the ocean idealised tracers (such as age of water) are not reset by an NRUNs. This is the MEDUSA equivalent of switching off reconfiguration.
1. There should be semi-automatic scientific monitoring of the whole run, e.g. of global mean quantities. The Afterburner "Climate Model Monitor" app is recommended: see [wiki:Afterburner instructions].
1. There should be automatic monitoring of the completeness of the output data, and the MASS/JASMIN archive. For Met Office runs, the standard HadGEM3 and UKESM1 jobs have an archive_integrity task (in the postproc app) which does this. //Will this be adapted for ARCHER?//
   * If there is a gap in the archive and the data is no longer on the HPC, restart from the last archived dumps before the gap and continue from there. Both HadGEM3-GC3.1 and UKESM1 have been demonstrated to give identical results after such a restart, but unless the run has progressed a long way it is safest to immediately revert to this point and overwrite previously archived data (rather than wait until the end of the run and fill gaps with short runs).
   * Document (on the !ExperimentDocumentation wiki page) any gaps found and how they were filled.
1. Don't add diagnostics mid-run without consulting the data delivery experts first. It could make it very difficult to deliver data from the run.
1. Avoid splitting a single experiment across more than one suite (e.g. by running the first 50 years under one suite and the remainder under another). The resulting disconnect in the archived data will cause difficulties for data delivery, and **delay the publication of your output on the ESGF**. If you feel that you need to switch to a new rose suite in the middle of an experiment, please ask for advice first: most requirements can be met with the use of suite branches without copying to a new suite.
1. If there are any model failures, record (on the !ExperimentDocumentation page) the model date and timestep, as well as how the failure was fixed. This is critical in order to be able to reproduce the run at a later date if required. Guidance on restarting the model can be found at moci:wiki:tips_CRgeneral#Restarting.
1. If you have to abandon a run completely, delete the data from the archive (MASS/JASMIN) to ensure it is not subsequently used in error.
1. (Met Office runs) When the run is complete, thin restart dumps in MASS to reduce tape usage, retaining 1st December dumps only every 10 years. Retention of 1st January dumps depends on whether other CMIP6 runs (which must start on 1st Jan) will branch from your run, and from what points. If you are unsure, please consult your MIP lead, or the group of UK MIP leads (cmip6uk-mipleads@metoffice.gov.uk).
1. When the run is complete, assign your ticket to the person who will process and deliver the data (if this is you, then assign to yourself for data delivery).


## Process and deliver

1. Add a comment to the `ukcmip6` experiment ticket noting that you are happy that the simulations are scientifically fit for processing.
2. Ensure that the `rose-suite.info` file has the correct information in it. In particular please check the following fields:
  * `variant-id`
  * `branch-date`
  * `parent-experiment-id`
  * `parent-variant-id`
3. Validate the `rose-suite.info` information using the `validate_suite_info` script from within the suite, e.g.
{{{
$ cd ${HOME}/roses/<suite-id>
$ python2 bin/validate_suite_info.py rose-suite.info 
Warnings:
  start-date: Empty value in CV for "start_year". Cannot validate.
  end-date: Empty value in CV for "end_year". Cannot validate.
No errors found.
}}}
    If any errors are reported, please correct them. Note that the production or publication process may fail if the information included here does not agree with the [https://github.com/WCRP-CMIP/CMIP6_CVs CMIP6 Controlled Vocabularies (CVs)].

    In some early suites the `validate_suite_info.py ` script may fail with an !ImportError relating to the line `import rose.config`. If this occurs, please replace this script in your suite with the latest version of the script from suite `u-an000` using a command such as
{{{
$ cd ${HOME}/roses/<suite-id>
$ fcm export --force https://code.metoffice.gov.uk/svn/roses-u/a/n/0/0/0/trunk/bin/validate_suite_info.py ./bin/
$ fcm commit
}}}
    And then validate the metadata as shown above.

    For experiments that have recently been added to the [https://github.com/WCRP-CMIP/CMIP6_CVs CMIP6 Controlled Vocabularies (CVs)], errors such as 
{{{
  File "bin/validate_suite_info.py", line 254, in main
    warnings, errors = check_experiment(suite_info, cv_experiment_id)
ValueError: need more than 1 value to unpack
}}}
   may be seen. To get past this you will need to update the `controlled-vocabulary` entry in the `rose-suite.info` file to a more recent version. The error message will be made clearer in a future version of the `validate_suite_info.py` script.


4. Create a branch of the suite named `cdds` (note case), e.g.
{{{
~/roses/u-ar766]$ fcm branch-create cdds
}}}
   Note that any changes to the suite needed for CDDS processing will need to be made to this branch.
5. Within the UKESM1 and HadGEM3 suites there is a file named `atmos_dictionary.json` that is used to identify whether the STASH variables for //MIP requested variables//, e.g. `Amon/tas`, are switched on in the suite. In **UKESM1** suites this file needs to be replaced with an updated version that contains some additional entries to allow for the production of certain carbon/land variables. To do this take the following steps;
    a. Switch to the CDDS branch, e.g.
{{{
~/roses/u-aw310]$ fcm switch cdds
}}}
    b. Copy the latest version of the `atmos_dictionary.json` file from suite `u-an000` into your branch, overwriting the existing file;
{{{
~/roses/u-aw310]$ fcm export --force https://code.metoffice.gov.uk/svn/roses-u/a/n/0/0/0/trunk/app/um/atmos_dictionary.json app/um/
}}}
    c. Commit the change
{{{
~/roses/u-aw310]$ fcm commit
}}}
   Note that the revision number corresponding to this change will need to be entered into CREM as part of the CDDS Operational procedure (see below). 
6. **UKESM1 ONLY**: If your suite was not copied from the released UKESM1 suites, i.e. a copy of the `piControl` was taken, then there may be issues with missing files in the suite and missing variables in the MEDUSA output. To confirm whether this issue affects your suite look for the file `app/nemo_cice/file/field_def_bgc.xml`. If this file does not exist then certain ocean biogeochemistry variables will not be producible (without additional effort) and CDDS processing will fail until the steps documented [cdds:wiki:Prepare/ManualSuiteCorrections here].
7. Ensure that any issues with particular variables in these suites are noted in [https://docs.google.com/spreadsheets/d/1Z3dtBnC-RI3Bmt92fZ-wz72CsGAFwb8z1nKaLSATEZI/edit#gid=0 the CMIP6 diagnostic special cases] spreadsheet.
8. Change the status of the `ukcmip6` experiment ticket to `process_and_deliver` and contact [mailto:cdds@metoffice.gov.uk cdds] to arrange processing.

The procedure required to configure CREM and process data is described in the [cdds:wiki:CDDSOperationalProcedure CDDS Operational Procedure]. Anyone who wishes to use CDDS should contact [mailto:matthew.mizielinski@metoffice.gov.uk Matthew Mizielinski] to discuss training.

