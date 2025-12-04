# Guidance for quality assurance of CMIP7 experiments -- DRAFT

In running experiments for a production experiment, the devil is in the detail. There are many things which can go wrong, with expensive consequences. However, there are steps which can be taken to minimise errors, and these are listed below. The motivation for these is science assurance: tedious but important tasks to ensure that the experiments (and the science based on them) is publishable and repeatable.

| Section | Contents  |
| --- | --- |
| [Experimental design](#experimental-design-configuration) | Procedure for overall experiment design |
| [Run setup](#run-setup) | How to set up a run for a given experiment using github issues |
| [Run and monitor](#run-and-monitor) | Starting the run, monitoring progress and handling errors | 
| [Process and deliver](#process-and-deliver) | Processing output from run and delivering data |

> [!NOTE]
> This guidance is set-up with the main purpose of providing guidance on running Assessment Fast Track simulations. It may be of use however of course to the Community MIPs and they are welcome to use our best practice. We have generalised content where appropriate with this in mind.

## General experimental design considerations

Although the experimental protocol is set out by the MIP, in practice there are model-specific decisions which need to be made, to interpret and implement the design for our model.

1. Interpret experiment design specification. 
   * Discuss non-trivial choices with other MIP leads to ensure consistency between MIPs where appropriate. 
   * Document decisions on a CMIP7 github repository; for example, you could create a wiki page for your MIP. 
1. Develop any MIP-specific code
   * Lodge code in relevant model trunk (UM, NEMO, ...) to ensure that all CMIP7 code has been through appropriate review, and for future-proofing. 
1. Define diagnostic setup.
   * Check whether the model is able to produce your key diagnostics, and code up if essential.
   * Document any decisions on diagnostics which you decide not to include or for which you have to deviate from what has been requested. 
1. Download / create forcing data.
   * Preindustrial, historical and scenario forcing data needed by UKESM and HadGEM-GC5 based models is being processed and reviewed by the [Ancillary Working Group](https://code.metoffice.gov.uk/trac/UKESM/wiki/UKESMAncilWG)
   * Ensure that all input ancillary files are in central CMIP7 locations, and not in an individuals user space.
   * Outside of the above key forcing datasets if you need anything bespoke you will likely have to generate this yourself
     * Liaise with providers in advance of official release if possible to minimise surprises.
     * If you are relying on another MIP to generate forcing data for you, ensure that they are aware of this. 
     * Avoid breaking up timeseries forcing files (historical/scenario) into e.g. 20-year chunks. It is better to split files by variable than by time period.
     * Ensure that the temporal coverage of forcing data extends beyond the start and end of the runs which will use it. The model interpolates between time records to its present time, so needs a valid field after the end of the run and before the start.
     * There should be some technical and scientific review of all forcing data created for CMIP7 runs, just as for the model jobs themselves.  The MIP should decide what is appropriate, as long as any science decisions made in defining the forcing are documented.
1. Schedule HPC resources.
   * Outline discussions on HPC resources required for your experiments should begin as early as possible. 
   * Once you have decided which experiments to run, estimate how much resource (CPU time and disk space) all of your runs will require, and ensure that you have access to what you need. For Met Office HPC, agree which queue you will use.

## Run setup and review

1. Identify a reviewer for your job setup and arrange likely review dates in advance (to prevent delays due to reviewers being otherwise engaged).    
1. Ensure that ensemble member, forcing and realisation identifiers ("ripf" values) have been defined. 

1. Open a [CMIP7 Experiment Documentation issue](https://github.com/UKNCSP/CMIP7-AFT-Simulations/blob/main/.github/ISSUE_TEMPLATE/CMIP7_experiment_documentation_template.yml) for this experiment
   * Fill in a brief description of your Experiment under `Issue Description`
   * Issue type: Select "New CMIP Experiment"
   * On the right hand side of page, set up your issue in the following way (Click on the cog symbol to make required edits):
     * **Assignees:** Ensure you assign the issue to yourself in the first instance and to any other relevant people (eg: your reviewer).
     * **Labels:** Apply the correct label to the issue - at the very least you should select the **relevant model configuration** to which your experiment applies.
     * **Type:** Please set to `Task`
     * **Projects:** Leave empty
     * **Milestone:** Please assign the appropriate CMIP7 AFT milestone to which this experiment applies.
   * Fill in the `Job Documentation` section in the template with:
     * ROSE suite id and experiment name.
     * Configuration -> details of basic model configuration.
     * Suite revision for start of run, baseline configuration, predecessor suite id and any changes, initial conditions, dates covered by run and any other configuration specific settings.
     * Fill in the Quality Assurance Checklist and Note location of data 
     * Run Log: Include links and record any issues/failures in the documentation issue while the simulation is running.
     
  
1. Copy the appropriate, standard UKESM1.3 or HadGEM3-GC5 job and configure the copied suite for this experiment (following any documentation specific to your MIP, see [Experimental design](#experimental-design-configuration) above). The standard (i.e. supported) jobs available for each model are 3 of the DECK experiments: piControl, historical and AMIP. See _standard job pages for UKESM1.3 and HadGEM3-GC5_. _**Note:** If your MIP has several experiments sharing a similar experimental or diagnostic setup, you may wish to create one or more standard jobs for your MIP to act as the source suites for your MIP experiments, rather than copy all suites directly from the standard DECK jobs._
   * Ensure start and end dates are correct. If the experiment protocol specifies only start and end years, begin on the 1st Jan in the start year (not the preceding or subsequent Sep or Dec) and continue until at least 1st Jan of the end year plus 1 (i.e. 01/01/2022 for an 1850-2021 historical run).
   * Archiving restarts: For HadGEM3, the run should archive restarts in both January and December of each year. The January restarts are to allow other CMIP runs to branch from this run, while the December dumps allow a cleaner restart of the climate meaning system if there are problems with the run. For UKESM1, only January restarts are required, because it uses an alternative method to generate seasonal and annual means.
   * For Met Office runs archiving to MASS, select the appropriate duplex setting (`non_duplexed_set`) in the postproc app, under "Post Processing - common settings -> Moose Archiving". In general duplexing is recommended for production runs (`non_duplexed_set=false`).
   * For UKESM1.3, some experiments (e.g. DECK runs) should reset the diagnostic ocean ideal tracers (age of water and CFCs) when the experiment starts. For guidance, where you are branching from the piControl (historical, 1%CO2, 4xCO2) OMIP recommends resetting these diagnostic tracers at the start of the run so that the fields are independent of the branch point; on the other hand if you are branching from a historical or similar run it makes sense to inherit the fields of the parent run and continue their evolution. This resetting is activated by the switch `INIT_CFC_AGE=true` in `rose-suite.conf`. See note below on changing this to false after the run starts.
     
1. Configure the Diagnostic Setup 
   * If making additions to the standard jobs, check the rules for data layout as required by [the data delivery system](../../../CDDS-CMIP7-mappings?tab=readme-ov-file#usage-profiles-and-output-frequency).  For example:
       * different time frequencies must not share the same diagnostic files, or “STASH stream” for the UM.
       * all output variables must only contain diagnostics from the same usage profile/stream; CDDS cannot extract data from multiple streams to produce a single variable.
   * If diagnostics are explicitly required at 00:00 on the first day of the run, i.e. the zeroth timestep (e.g. for regional model boundary conditions), seek advice from the relevant configuration owner/MIP Lead.
1. **Commit all changes you make to your rose suite**. No runs should be based on suites with uncommitted working copies, as this leads to mistakes when copying and reviewing suites.
1. Output some test data for e.g. 1 year of the run.
   * For the first DECK runs, all fields will be checked and domain experts and MIP leads will be asked to contribute.
   * For other MIPs, new/altered diagnostics should be checked thoroughly, as should any fields of particular importance to that MIP.
   * Plot the fields and verify that they are scientifically sensible and that packing precision is appropriate. This is a very time-consuming and tedious task and may need to be distributed across several people.
   * Is the model responding appropriately to any new forcing?
   * For some runs where significant changes are being made to the diagnostic setup, it will be appropriate to process a sample of data with `CDDS` to check that the output can be delivered to the ESGF (consult @UKNCSP/cdds for advice).
1. When you are confident that everything is working and you have completed the QA checklist in the CMIP7 Experiment Documentation template, assign the issue to your reviewer to conduct the review (using the "Assignees" panel at the right of the issue page, you will need the githubid of your reviewer). This should automatically generates a github notification for them, but it might be helpful to also email your reviewer directly in case they miss this.
1. The reviewer should then create a [CMIP7 Experiment Review issue](https://github.com/UKNCSP/CMIP7-AFT-Simulations/blob/main/.github/ISSUE_TEMPLATE/CMIP7_Expt_Review_template.yml) as a `sub-issue` within your current Experiment Documentation issue.  They should fill in all parts of this review template and sign their approval or otherwise when completed.
   * _**Note:** In practice it will save time if the reviewer also looks at the model suite before you produce any test data._
   * Clearly the thoroughness of the review should vary from one experiment to another. If this experiment is very similar to another which has already been reviewed, then it may be sufficient to check that the job contains the expected differences. The DECK runs will be reviewed most thoroughly, and for individual MIPs it may make sense to have an in-depth review for the first experiments followed by a lighter touch for subsequent runs.
   * The Reviewer needs to sign off the diagnostic setup checklist as detailed in the CMIP7 Experiment Review template.
1. If the reviewer finds a problem they should reject the ticket and assign it back to you for setup. When they are happy they should approve and assign the main Experiment Issue back you for running and monitoring and the review sub-issue can be closed.
1. It is recommended that users complete the metadata form (see first step in [Process and deliver](#process-and-deliver)) at this point.

## Run and monitor

1. As soon as the run starts, create a branch of the suite called "running" and switch your working copy to point to this branch:
```
cd ${HOME}/roses/<suite-id>
fcm branch-create running
fcm switch running
```
   This ensures that any changes you need to make to the suite mid-run, such as restarting with an NRUN after a failure, are not copied into descendant suites. In other words, if someone copies your suite they get the suite as it started running, not some mid-run initialisation state. 
   * This also allows you to apply technical fixes or additional diagnostics which you want to be picked up by subsequent runs but not affect your running job, by committing these to the trunk and not the running branch:
```
fcm switch trunk
...make changes
fcm commit
fcm switch running
```
2. If you need to restart as an NRUN:
   * For UKESM1.3 suite:
     *  Set the following switch `L_NRUN_RESTART=true` in the `rose-suite.conf` file. This retrieves all required startdata for the suite for the date set by the `BASIS` environment (so change this setting as needed to the correct model basis time for your restart (in your _running_ branch)) and turns off reconfiguration.
     *  Set the top-level option `BITCOMP_NRUN=true` (`suite conf -> Run Initialisation and Cycling`) to ensure that the NRUN will bit-compare with a previous CRUN.
     *  Set `INIT_CFC_AGE=false` in rose-suite.conf. This will ensure that the ocean idealised tracers (such as age of water) are not reset by an NRUNs. This is the MEDUSA equivalent of switching off reconfiguration 
   * For HadGEM3-GC5 [**Alejandro add here**], you will need to apply the following changes manually to the running branch  (**i.e `rose suite-run` without `--restart` ADD cylc 8 option**) mid-way through the run:
     * PUll back startdata
     * Switch off atmosphere reconfiguration if it is on.
     * Set the top-level option `BITCOMP_NRUN=true` (`suite conf -> Run Initialisation and Cycling`) to ensure that the NRUN will bit-compare with a previous CRUN.
 
3. There should be automatic monitoring of the completeness of the output data, and the MASS/JASMIN archive. For Met Office runs, the standard HadGEM3-GC5 and UKESM1.3 jobs have an _archive_integrity_ task (in the postproc app) which does this.
   * If there is a gap in the archive and the data is no longer on the HPC, the _archive_integrity_ task should fail and you should restart from the last archived dumps before the gap and continue from there. Both HadGEM3-GC5 and UKESM1.3 have been demonstrated to give identical results after such a restart, therefore unless the run has progressed a long way it is safest to immediately revert to this point and overwrite previously archived data (rather than wait until the end of the run and fill gaps with short runs).
   * Document (in the Experiment Documentation issue) any gaps found and how they were filled.
4. Don't add diagnostics mid-run without consulting the data delivery experts first. It could make it very difficult to deliver data from the run.
5. Avoid splitting a single experiment across more than one suite (e.g. by running the first 50 years under one suite and the remainder under another). The resulting disconnect in the archived data will cause difficulties for data delivery, and delay the publication of your output on the ESGF. If you feel that you need to switch to a new rose suite in the middle of an experiment, please ask for advice first: most requirements can be met with the use of suite branches without copying to a new suite.
6. If there are any model failures, record (on the Experiment Documentation issue) the model date and timestep, as well as how the failure was fixed. This is critical in order to be able to reproduce the run at a later date if required. 
7. If you have to abandon a run completely, delete the data from the MASS archive to ensure it is not subsequently used in error.
8. (Met Office runs) When the run is complete, thin restart dumps in MASS to reduce tape usage, retaining 1st December dumps only every 10 years. Retention of 1st January dumps depends on whether other CMIP7 runs (which must start on 1st Jan) will branch from your run, and from what points. If you are unsure, please consult your MIP lead.
9. When the run is complete, **assign your ticket to the person who will process and deliver the data (if this is you, then assign to yourself for data delivery)**.

## Process and deliver 

### Metadata recording

To process data using CDDS metadata needs to be recorded for each workflow.  In CMIP6 this was recorded in the rose-suite.info files within the model suites, but for CMIP7 metadata will be recorded in files within the [CDDS Simulation Metadata Repository](https://github.com/UKNCSP/CDDS-simulation-metadata) in a form similar to that needed to run CDDS.  A [registration form](https://github.com/UKNCSP/CDDS-simulation-metadata/issues/new?template=add_workflow_metadata.yml) is available to enter or update key metadata related to a workflow ID.
Metadata for individual workflows will be stored within text files within this repository.

Summary metadata for all simulations can be explored through [a searchable table](https://ukncsp.github.io/CDDS-simulation-metadata/).

### Processing preparation [UNDER REVIEW]

Provided metadata is recorded correctly tools will be provided to construct the *request configuration file*, the interface file used to control CDDS. Note that each run through of CDDS for a particular simulation (e.g. the UKESM1-3 piControl) will need to have a different *package id* within the request file to allow data and processing logs to be stored separately.

The list of variables that are requested for CMIP7 production runs are described in the CMIP7 Data Request. A repository with text files detailing the variables requested and the ability of CDDS to produce them will be provided in due course.

### Processing [UNDER REVIEW]

The operational procedure for CDDS will be linked here when ready.  CDDS processing typically consists of setting up the request file with appropriate metadata and settings/variables, executing two set up commands and then a cylc workflow is launched.  Monitoring this workflow for failures will be the primary task of the CDDS "driver", with support provided by the @UKNCSP/cdds team.

