import numpy as np
from NetlistParser import netlistParser
from Printer import printer
from GenerateMatrices import generateMatrices
from Solvers import DCsolver

if __name__ == "__main__":
    filename = 'Example Networks/Potential Divider.net'
    NP = netlistParser(filename)
    print(NP.nodes)
    gM = generateMatrices(NP)
    gM.run()
    
    s = DCsolver(gM.A, gM.Z, gM.X)
    s.run()
    printer(s.X, NP)




