# Electric_Circuits
Gives node voltages and currents at different nodes of the circuit. 

NOTE: Read the Stamping.pdf file for understanding the basic concepts of how any electric circuit can be generally solved using matrices and vectors. 

the hw3.py file contains the main code. 

read_netlists.py has a function that takes in a .txt file containing a user-created circuit netlist, converts it to a list of lists
and returns it in the following format. 

'component number', 'component type (R/VS/IS)', 'from node', 'to node', 'component value (Analog value)' 
the above list is for one component between two nodes. There will be many such lists, depending on the .txt netlist file. 

comp_constants.py assigns a unique component number to each component. It also contains the index positions to each of the
five elements in the aforementioned list. 


