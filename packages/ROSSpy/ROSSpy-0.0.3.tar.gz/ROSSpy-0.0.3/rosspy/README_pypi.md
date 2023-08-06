# Reverse Osmosis Scaling Simulation (ROSS)

Desalination is an unavoidable technology for meeting the 6th SDG. Reverse Osmosis (RO) is the leading desalination technology, although, even greater energy efficiencies are possible by mitigating mineral scaling in the RO module. The geochemistry of scaling phenomena is generally inaccessible to physical experimentation, thus a number of software -- like TOUGHREACT and French Creek -- have been developed to simulate scaling phenomena. These software, however, are esoteric -- e.g. use FORTRAN and geochemical jargon -- and are computationally and financially expensive. We therefore developed ROSS as an open-source software -- in the Python and PHREEQC languages -- that evaluates scaling and brine formation during the reactive transport of desalination. We encourage community critiques and reformulations to support open-science and expedited research towards resolving water insecurities.

The module to_precision is not available via PyPI, thus, the module must be [clone and installed from the source](https://bitbucket.org/william_rusnack/to-precision/src/master/). The directions for this process: 
1) Navigate to a directory for ROSSpy content
2) execute -- git clone https://bitbucket.org/william_rusnack/to-precision/src/master/ -- in this directory.
3) execute -- pip install . -- in this directory
