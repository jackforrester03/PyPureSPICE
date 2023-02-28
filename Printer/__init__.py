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