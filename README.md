# random_lammps_tools
Just collection of random scripts and tools i use for lammps

1. **uffgen** - simple script to generate UFF parameters, TODO- add a lot of functionality!

2. **topotools_output_dimensions** - simple script for checking dimensions of simulation box in topotools.
  - data output files for lammps, when generated from topotools doesnot give correct value of xlo xhi etc. this python script will check all atoms in your simulation box to give you values of (min - 1) and (max + 1) for proper box setup in lammps.
  - use: python topotools_output_dimensions.py /path/to/your/file/your_fine_name_here.extension

3. **lammps.tmLanguage and lammps.YAML-tmLanguage** source file for Sublime Text 3 lammps syntax highlighting - It idenitifies .in or .lammps extensions and color 'most' keywords according to their functionality. Current grouping being is 3 catagories: data input/output, fix and unfix, rest
4. **diffusion_coeff.py** - A simple python programme to calculate diffusion coefficient of any molecule in lammps. 
Few caveats: 
 - it takes data which is dumped by dump num \<GROUP\> custom \<TIME\> \<NAME\> id  type xu yu zu
 - dumped coordinates shall be sorted on the basis of their id (dump_modify num sort id)
 - all atoms of single molecule shall be in continuous order, eg for water, if id for O is 4, H is 1 then file should have it in order 4 1 1 4 1 1 4 1 1 or 1 4 1 1 4 1 1 4 1 or 1 1 4 1 1 4 1 1 4 etc but not in 4 4 4 1 1 1 1 1 1 etc
 - format-> python "diffusion\_coeff.py \<dump\_file\_name\> \<atom\_id   atom\_mass\> \<Total number of atoms in molecule\> [-region from\_x to\_x from\_y to\_y from\_z to_z]", without region command all the molecules of given type will be taken throughout the simulation box.
 - ***example*** if you have NMP molecule with Carbon as atom type 1, Hydrogen as type 2, nitrogen as type 5 and oxygen as type 7 then commans will look like "diffusion_coeff.py 1 12 2 1 5 14 7 16 16"
