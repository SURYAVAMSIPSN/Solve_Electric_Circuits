#Name: SIVANAGA SURYA VAMSI POPURI
# ASU ID: 1217319207

import numpy as np                     # needed for arrays
from numpy.linalg import solve         # needed for matrices
from read_netlist import read_netlist  # supplied function to read the netlist
import comp_constants as COMP          # needed for the common constants

# this is the list structure that we'll use to hold components:
# [ Type, Name, i, j, Value ] ; set up an index for each component's property

############################################################
# How large a matrix is needed for netlist? This could     #
# have been calculated at the same time as the netlist was #
# read in but we'll do it here to handle special cases     #
############################################################

def ranknetlist(netlist):              # pass in the netlist

    ### EXTRA STUFF HERE!
    maxi = 0; l = []
    for comp in netlist:
        maxi = max(comp[COMP.I], comp[COMP.J]) # The maximum node number in each component. 
        l.append(maxi) # PUt that in a list
    nodes = max(l) # From l, extract the maximum value. this gives us the nodes.  
    max_node = nodes+1 # Including ground, if there is a source referenced to it. 
    
##    print(' Nodes ', nodes, ' total Nodes ', max_node)
    return nodes,max_node # Returns the total number of nodes and the maximum value of the node. 

############################################################
# Function to stamp the components into the netlist        #
############################################################

def stamper(y_add,netlist,currents,voltages,num_nodes): # pass in the netlist and matrices
    # y_add is the matrix of admittances
    # netlist is the list of lists to analyze
    # currents is the vector of currents
    # voltages is the vector of voltages
    # num_nodes is the number of nodes
    
    for comp in netlist:                            # for each component...
        #print(' comp ', comp)                       # which one are we handling...

        # extract the i,j and fill in the matrix...
        # subtract 1 since node 0 is GND and it isn't included in the matrix

        if ( comp[COMP.TYPE] == COMP.R ):           # a resistor
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if (i >= 0):                            # add on the diagonal
                y_add[i,i] += 1.0/comp[COMP.VAL]
            
            #EXTRA STUFF HERE!'
            if (j >= 0):
                y_add[j,j] += 1.0/comp[COMP.VAL] # Adding on the diagonal
            if i>=0 and j>=0:
                y_add[i,j] -= 1.0/comp[COMP.VAL]
                y_add[j,i] -= 1.0/comp[COMP.VAL] # Adding on off-diagonals. 
        
        if ( comp[COMP.TYPE] == COMP.IS):           # an independent current source
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            if i>=0: # if index positions are admissible as per rules.
                currents[i] -= comp[COMP.VAL]
            if j>=0:
                currents[j] += comp[COMP.VAL]
        
        if ( comp[COMP.TYPE] == COMP.VS):           # an independent voltage source. 
            i = comp[COMP.I] - 1
            j = comp[COMP.J] - 1
            y_add = np.column_stack((y_add, np.zeros(num_nodes, float))) # Accomodate space for considering the case of VS by adding an extra row and column
            y_add = np.vstack((y_add, np.zeros(num_nodes+1, float)))
            currents = np.vstack((currents, 0)) # Include one more row in this also.
            num_nodes += 1 # num_nodes needs to be increased, for maintaining index range.
            if i>=0: # if index positions are admissible as per rules. 
                y_add[num_nodes-1, i] = 1
                y_add[i, num_nodes-1] = 1
            if j>=0:
                y_add[num_nodes-1, j] = -1
                y_add[j, num_nodes-1] = -1 # As per the rules of having an independent voltage source. 
            currents[num_nodes-1] = comp[COMP.VAL] # Last element of RHS vector is the voltage source. 
    #print(y_add)
    print(solve(y_add, currents)) # Prints the voltage vector, the solution of the circuit!! :D 
    # NOTE: The last few elements in the resulting voltage vector are current values. #VS gives #current values. 
    
    
    return num_nodes  # need to update with new value

############################################################
# Start the main program now...                            #
############################################################

# Read the netlist!
netlist = read_netlist()

# Print the netlist so we can verify we've read it correctly
"""
for index in range(len(netlist)):
    print(netlist[index])
print("\n")
"""
#EXTRA STUFF HERE!
nodes, max_node = ranknetlist(netlist)
y_add = np.zeros((nodes, nodes), float)
currents = np.zeros((nodes, 1), float)
voltages = np.zeros((nodes, 1),float)
#print(nodes, max_node) --> So far so good. 
num_nodes= stamper(y_add,netlist,currents,voltages,nodes)