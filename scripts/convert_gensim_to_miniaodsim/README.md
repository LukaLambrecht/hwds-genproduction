Shortcut from GEN-SIM level directly to MiniAODSIM level
by chaining the cmsDriver and cmsRun commands together sequentially.

Note: works in principle (05/10/2021) but will not be maintained anymore;
      replaced by functionality in convert_gripack_to_miniaodsim,
      which is similar to here, but also runs gridpack->gensim in the same step,
      and removes the input after each step to keep file size under control!
