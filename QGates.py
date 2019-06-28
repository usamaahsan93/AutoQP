H='Hadamard'
X='Not'
Y='Pauli Y'
Z='Pauli Z'

CH='Controlled Hadamard'
CX='Controlled Not'
CY='Controlled Y'
CZ='Controlled Z'



S='Clifford S'
SC='Clifford S Conjugate'

T='SquareRoot S'
TC='T Conjugate'

SWAP='Swap'
#CSWAP='Controlled Swap' pending because of arity 3

gateArity={
        H:1,
        X:1,
        Y:1,
        Z:1,
#        
#        CH:2,
        CX:2,
#        CY:2,
#        CZ:2,
#        
        S:1,
#        SC:1,
#        
#        T:1,
#        TC:1,
#        
#        SWAP:2
        
        }

gateName={
        H:'h',
        X:'x',
        Y:'y',
        Z:'z',
        
        CH:'ch',
        CX:'cx',
        CY:'cy',
        CZ:'cz',
        
        S:'s',
        SC:'sdg',
        
        T:'t',
        TC:'tdg',
        
        SWAP:'swap'
        }
        

def oracleBernsteinVazirani(a):
    count=len(a)
    l=[]
    for i in a:
        if i=='1':
            l.append(('Controlled Not',count,0))
        count-=1
    return l




def oracleDeutschJozsa(case):
    if case==0:
        return []
    
    elif case==1:
        return [(CX,0,1)]
    
    elif case==2:
        return [(X,1),(CX,0,1)]

    elif case==3:
        return [(X,1)]
    







