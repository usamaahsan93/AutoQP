# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 08:29:53 2018

@author: Ahsan
"""


from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import compile, Aer

from QGates import gateArity , gateName

class QCircuit:
    
    def __init__ (self,qBit,cBit,shot=1):
        '''
        This function is used to construct the base of quantum circuit
        Currently by default backend used is 'qasm_simulator_py'.
        NOTE: You can change the backend but would need to adjust the evaluate function as well.
        
        This function accepts the following arguments:
            Quantum Bits: [qBit]  dataType: int
            Classical Bits [cBit] dataType: int
            shot is by default 1 dataType: int
            
            '''
            
        self.qBit=qBit
        self.cBit=cBit
        self.shot=shot
        self.backend=Aer.get_backend('qasm_simulator')
#        self.backend=Aer.get_backend('statevector_simulator_py')
        
        self.qr=QuantumRegister(qBit)
        self.cr=ClassicalRegister(cBit)
        self.qCircuit=QuantumCircuit(self.qr,self.cr)

        
    def evaluate(self):
        '''
        This function is used to evaluate the circuit
        When quantum circuit is constructed call this function to evaluate
        the circuit
        '''
        
        qobj = compile(self.qCircuit, self.backend,shots=self.shot)
        job = self.backend.run(qobj)
        result = job.result()
        
        return result
    
    
    def constructCircuit(self,code):
        '''
        This function recieves the list of tuples the first element of tuple
        represent the gate and the second and onwards are their placement
        position at the quantum circuit (depends upon the gate's arity)
        '''
        
        for i in code:
           val=gateArity.get(i[0])
           name=gateName.get(i[0])
           if val==1:
               getattr(self.qCircuit,name)( self.qr[ int(i[1]) ] )
             
           elif val==2:
               getattr(self.qCircuit,name)(self.qr[int(i[1])],self.qr[int(i[2])])
           

    def measurement(self,m,useHadamard=True):
        '''
        This function takes the list of tuple m having first element as qubit and 
        second element as classical bit. It measures the qubit on the associated 
        classical bit
        
        m : List of tuple [(qBit,cBit )]
        useHadamard: Append hadamard just before 
        '''
        
        if useHadamard:
            endH=[]
            for i in range(self.qBit):
                endH.append(('Hadamard',i))
            self.constructCircuit(endH)
        
        for i in m:
            q=i[0]
            c=i[1]
            self.qCircuit.measure(self.qr[q],self.cr[c])

