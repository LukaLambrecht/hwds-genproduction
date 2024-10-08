One-step processing from gridpack to GEN-level.

Processing this step does not take long per event,
jobs with O(50k) events are possible.

Alternatively (for speed or for even larger samples),
multiple jobs can be submitted in parallel,
where care is taken to choose a different random number seed for each job.
(Caveat: it is not yet clear how to merge the resulting files!)

Typical workflow:
- run a cmsDriver command to create a cmsRun configuration file
  (examples of valid cmsDriver commands for the gridpack-to-GEN step
   are collected in the folder cmsdriver)
- run python gridpack_to_gen_submit.py
  (run it without further arguments to see what arguments are needed,
   then run it with those arguments)
