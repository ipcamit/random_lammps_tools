# random_lammps_tools
Just collection of random scripts and tools i use for lammps

1. **uffgen** - simple script to generate UFF parameters, TODO- add a lot of functionality!

2. **topotools_output_dimensions** - simple script for checking dimensions of simulation box in topotools.
  - data output files for lammps, when generated from topotools doesnot give correct value of xlo xhi etc. this python script will check all atoms in your simulation box to give you values of (min - 1) and (max + 1) for proper box setup in lammps.
  - use: python topotools_output_dimensions.py /path/to/your/file/your_fine_name_here.extension

3. **lammps.tmLanguage and lammps.YAML-tmLanguage** source file for Sublime Text 3 lammps syntax highlighting - It idenitifies .in or .lammps extensions and color 'most' keywords according to their functionality. Current grouping being is 3 catagories: data input/output, fix and unfix, rest
