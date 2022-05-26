from qiskit import *
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy

from qiskit.circuit.library import MCMT
from qiskit.providers.aer.noise import NoiseModel
from qiskit import QuantumCircuit, Aer, assemble, transpile, execute
from qiskit.visualization import plot_bloch_multivector, plot_histogram, array_to_latex

from qiskit.tools.monitor import job_monitor

# import basic plot tools
from qiskit.visualization import plot_histogram

def quantum_circ( svs_dbl, svs_lps, num_runs, entg_type=1):
    # entg_type specifies the circuit configuration
    # num_runs specifies the number of experiments and beat variations you want
    if entg_type == 1:
        qr = QuantumRegister(7)

        #Bar 1
        cr_dbl = ClassicalRegister(4) 
        cr_lps = ClassicalRegister(4)

        #Bar 2
        cr_dbl2 = ClassicalRegister(4) 
        cr_lps2 = ClassicalRegister(4)

        #Bar 3
        cr_dbl3 = ClassicalRegister(4) 
        cr_lps3 = ClassicalRegister(4)

        #Bar 3
        cr_dbl4 = ClassicalRegister(4) 
        cr_lps4 = ClassicalRegister(4)

        reg = [qr,cr_dbl,cr_lps,cr_dbl2,
            cr_lps2,cr_dbl3,cr_lps3,
            cr_dbl4,cr_lps4]

        qc = QuantumCircuit( qr,cr_dbl,cr_lps,cr_dbl2,
            cr_lps2,cr_dbl3,cr_lps3,
            cr_dbl4,cr_lps4 )

        for i in range(4):
            print(i)
            qc.initialize(svs_lps[i], [0,1,2])
            qc.initialize(svs_dbl[i], [3,4,5])
            

            qc.cx(0,3)
            qc.cx(1,4)
            qc.cx(2,5)
            
            qc.cx(3,0)
            qc.cx(4,1)
            qc.cx(5,2)
            
            qc.h(6)
            qc.measure(6,3+(8*i))
            qc.h(6)
            qc.measure(6,3+(8*i)+4)
            
            qc.measure([0,1,2],[(8*i)+0,(8*i)+1,(8*i)+2])
            qc.measure([3,4,5],[(8*i)+4,(8*i)+5,(8*i)+6])
            
        #qc.draw(output='mpl')
        #bundle them by
        bundle = []
        for i in range( num_runs ):
            bundle.append( qc )
    return bundle

def exec_qc( qcs, backend:str, simulator=True ) -> dict:
    IBMQ.save_account('09fc89cbe6abe2504689109464ad5f8c2e060e429246b5f957306214948b776046521a6b7191834c17c98db00c20801655fbb368ce16c166992af6b1f4bc0f11')
    IBMQ.enable_account(token='09fc89cbe6abe2504689109464ad5f8c2e060e429246b5f957306214948b776046521a6b7191834c17c98db00c20801655fbb368ce16c166992af6b1f4bc0f11',
                        hub='ibm-q-research-2', group='stanford-uni-2', project='main')

    provider = IBMQ.get_provider(hub='ibm-q-research-2', group='stanford-uni-2', project='main')
    
    if simulator == True:
        device = provider.get_backend(backend)
        noise_model = NoiseModel.from_backend(device)
        transpiled_circuit = transpile(qcs, device, optimization_level=3)

        simulator = Aer.get_backend('qasm_simulator')

        assembled_circuit = assemble(transpiled_circuit, shots=8)
        sim_job = simulator.run(assembled_circuit, noise_model=noise_model)
        sim_result = sim_job.result()
        sim_counts = sim_result.get_counts()
        #plot_histogram(sim_counts, bar_labels=False)
    
    else:
        shots = 8
        transpiled_circuit = transpile( qcs, backend, optimization_level=3 )
        job = backend.run( transpiled_circuit )
        job_monitor( job, interval=2 )

        results = job.result()
        sim_counts = results.get_counts()

    return sim_counts