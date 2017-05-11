proc reaxc_bonds {timestep bondfile_name} \
{
    topo clearbonds


    set bondfile [open $bondfile_name r]
    fconfigure $bondfile -buffering line
# open bond file and setup input to be read as line by line

# jump to required timestep
    set current_timestep 0
    while {$timestep!=$current_timestep} {
        gets $bondfile file_data
        set current_line_stripped [split $file_data " " ]
        if {[lsearch $current_line_stripped Timestep]==1} {
            set current_timestep [lindex $current_line_stripped 2]
        }
    }
    puts "Current Timestep:"
    puts $current_timestep

    # skip rest of commented lines (6 of them)
    for {set i 0} {$i < 6} {incr i} {
        gets $bondfile dummy
    }

    # get bonded atoms and stuff them in list
    set bondlist {}
    set next_char ""
    
    gets $bondfile file_data 
    set current_line_stripped [split $file_data " "]
    # read first line
    while {$next_char!="STOP"} {
        set current_line_num {}
        foreach number $current_line_stripped {
            if {$number!=""} {
                lappend current_line_num $number
            }
        }
        set bond_number [lindex $current_line_num 2]
        for {set i 0} {$i < $bond_number} {incr i} {
            lappend bondlist [\
            list [expr [lindex $current_line_num 0]-1]\
            [expr [lindex $current_line_num [expr $i+3]]-1]\
            ]
        }
    # prepare for next line
    gets $bondfile file_data
    set current_line_stripped [split $file_data " "]
    # check if next line is '#''
    if {[lindex $current_line_stripped 0]=="#"} {
        set next_char "STOP"
        close $bondfile
    }
    # if it is '#' prepare to exit
    }
    topo setbondlist none $bondlist
    topo retypebonds
}


# //todo: automatic frame update using trace