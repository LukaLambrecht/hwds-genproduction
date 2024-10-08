Shortcut processing from gridpack to MINIAODSIM format directly in one step,
by chaining the cmsDriver and cmsRun commands sequentially.

Processing this chain takes a long time per event.
A single job should not contain more than O(100) events...
The typical workflow is to do O(1000) parallel submissions of jobs
operating on the same gridpack, each with O(100) events.
The only difference between the parallel jobs is the random number seed.

TO DO: check if it is possible/advantageous to make one big cmsDriver command
       instead of chaining them sequentially.
       (could potentially reduce the amount of memory needed for intermedate steps,
        which is causing some jobs to crash now as I reach my storage quotum...)

Typical workflow:
- Define a set of cmsDriver commands that should be executed sequentially,
  and dump them to a .txt file.
  Examples can be found in the cmsdriver folder.
  Note: these commands should NOT contain the 'filein', 'fileout' or 'python_filename' arguments, 
        these will be added automatically!
  Note: these commands should contain the no_exec argument
        (but it will be automatically added if they do not).
  Note: you should not run the cmsDriver commands, that will be done upon submission.
- Run python gridpack_to_miniaod_submit.py.
  First run it without additional arguments to see which are needed.
  Then run with those arguments.
