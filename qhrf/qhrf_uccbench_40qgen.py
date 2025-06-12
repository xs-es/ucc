from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qhrf_pass import QHRFPhaseLockPass
from qiskit.transpiler.passes import Optimize1qGates, CommutativeCancellation
from qiskit.qasm2 import dump as dump_qasm2

# Step 1: Create the raw 40-qubit GHZ-like circuit
def create_raw_40_qubit_ghz():
    qc = QuantumCircuit(40, name='QHRF-EXP-040-GENRAW')
    qc.h(0)
    for i in range(39):
        qc.cx(i, i + 1)
    return qc

# Step 2: Apply QHRF optimization
def apply_qhrf_pass(circuit):
    pass_manager = PassManager([
        QHRFPhaseLockPass(),
        Optimize1qGates(),
        CommutativeCancellation()
    ])
    return pass_manager.run(circuit)

# Step 3: Save to OpenQASM2 format (Qiskit 1.x)
def save_qasm_to_file(circuit, filename):
    with open(filename, "w") as f:
        dump_qasm2(circuit, f)

# Step 4: Prepare and export
if __name__ == '__main__':
    raw_circuit = create_raw_40_qubit_ghz()
    raw_circuit.name = "QHRF_RAW_40Q"

    qhrf_optimized = apply_qhrf_pass(raw_circuit)
    qhrf_optimized.name = "QHRF_OPTIMIZED_40Q"

    save_qasm_to_file(raw_circuit, "QHRF_RAW_40Q.qasm")
    save_qasm_to_file(qhrf_optimized, "QHRF_OPTIMIZED_40Q.qasm")

    print("[+] Circuits saved as QASM for UCC-Bench.")
    print(f"[•] Raw depth: {raw_circuit.depth()}, gates: {raw_circuit.count_ops()}")
    print(f"[•] Optimized depth: {qhrf_optimized.depth()}, gates: {qhrf_optimized.count_ops()}")
