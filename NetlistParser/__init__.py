class netlistParser():
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