import numpy as np


class NetlistParser():
    vS = []
    cS = []
    r = []
    nodes = {}
    def __init__(self, filename):
        id = 0
        with open(filename) as f:
            for line in f:
                line = line.rstrip()
                sLine = line.split(' ')
                id+=1
                if 'V' in line[0]:
                    self.handleNodes(sLine[1])
                    self.handleNodes(sLine[2])
                    self.vS.append({"num": sLine[0][1:], 'id':len(self.vS), "nN": self.nodes[sLine[1]], "pN": self.nodes[sLine[2]], "value": self.handleValue(sLine[3])})
                elif 'R' in line[0]:
                    self.handleNodes(sLine[1])
                    self.handleNodes(sLine[2])
                    self.r.append({"num": sLine[0][1:], 'id':len(self.vS), "nN": self.nodes[sLine[1]], "pN": self.nodes[sLine[2]],  "value": self.handleValue(sLine[3])})
    
    def handleNodes(self,node):
        if node not in self.nodes:
            self.nodes[node] = len(self.nodes)

    def handleValue(self,value):
        if 'k' in value:
            return float(value.split('k')[0])*1000
        else:
            return float(value)
        
class generateMatrices():
    def __init__(self, NP):
        self.vS = NP.vS
        self.cS = NP.cS
        self.r = NP.r
        self.nodes = NP.nodes
        self.A = np.zeros(((len(NP.nodes)-1)+len(NP.vS), (len(NP.nodes)-1)+len(NP.vS)))
        self.X = np.zeros((1, (len(NP.nodes)-1)+len(NP.vS)))
        self.Z = np.zeros(((len(NP.nodes)-1)+len(NP.vS)))
    def run(self):
        if len(self.nodes) > 1:
            G = np.zeros((len(self.nodes)-1, len(self.nodes)-1))
            for res in self.r:
                if res["pN"] != 0:
                    G[res["pN"]-1, res["pN"]-1] += 1/res['value']
                if res["nN"] != 0:
                    G[res["nN"]-1, res["nN"]-1] += 1/res['value']
                if res["pN"] != 0 and res["nN"] != 0:
                    G[res["pN"]-1, res["nN"]-1] += -1/res['value']
                    G[res["nN"]-1, res["pN"]-1] += -1/res['value']
            self.A[:len(self.nodes)-1, :len(self.nodes)-1] = G
        if len(self.nodes)>1 and len(self.vS)>0:
            B = np.zeros((len(self.vS), len(self.nodes)-1))
            for vol in self.vS:
                if vol['pN'] != 0 and vol['nN'] != 0:
                    B[vol['id'], vol['pN']-1] = 1
                    B[vol['id'], vol['nN']-1] = -1
                if vol['pN'] != 0:
                    B[vol['id'], vol['pN']-1] = 1
                if vol['nN'] != 0:
                    B[vol['id'], vol['nN']-1] = -1
            C = B.T
            self.A[len(self.nodes)-1:len(self.nodes)-1+len(self.vS), :len(self.nodes)-1] = B
            self.A[:len(self.nodes)-1, len(self.nodes)-1:len(self.nodes)-1+len(self.vS)] = C

        if len(self.cS) > 0:
            assert("Current sources not implamented yet")

        inc=0
        if len(self.vS) > 0:
            for vol in self.vS:
                self.Z[len(self.nodes)-1+inc] = vol['value']
                inc+=1

class printer():
    def __init__(self, X, NP):
        inc = 0
        for n in NP.nodes:
            if n != '0':
                print(f"Node {n} voltage = {X[inc]}")
                inc+=1

        for vol in NP.vS:
            print(f"Current through V{vol['num']} = {X[inc]}")
            inc+=1

class solver():
    def __init__(self, A, Z, X):
        self.A = A
        self.Z = Z
        self.X = X
    def solveDC(self):
        self.X = np.linalg.inv(self.A) @ self.Z.T
if __name__ == "__main__":
    filename = 'Example Networks/Potential Divider.net'
    NP = NetlistParser(filename)
    gM = generateMatrices(NP)
    gM.run()
    s = solver(gM.A, gM.Z, gM.X)
    s.solveDC()
    printer(s.X, NP)




