import numpy as np

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
