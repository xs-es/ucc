import pytest
from cirq import CNOT
from cirq import Circuit as CirqCircuit
from cirq import H, LineQubit
from pytket import Circuit as TketCircuit
from qiskit import QuantumCircuit as QiskitCircuit
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
from qiskit.converters import circuit_to_dag

from benchmarks.circuits import qcnn_circuit, random_clifford_circuit
from ucc import compile
from ucc.transpiler_passes.basis_translator import BasisTranslator
from ucc.transpilers.ucc_defaults import UCCDefault1


def test_qiskit_compile():
    circuit = QiskitCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    result_circuit = compile(circuit, return_format="original")
    assert isinstance(result_circuit, QiskitCircuit)


def test_cirq_compile():
    qubits = LineQubit.range(2)
    circuit = CirqCircuit(H(qubits[0]), CNOT(qubits[0], qubits[1]))
    result_circuit = compile(circuit, return_format="original")
    assert isinstance(result_circuit, CirqCircuit)


def test_tket_compile():
    circuit = TketCircuit(2)
    circuit.H(0)
    circuit.CX(0, 1)
    result_circuit = compile(circuit, return_format="original")
    assert isinstance(result_circuit, TketCircuit)


circuit_names = [
    "qcnn_circuit",
    "random_clifford_circuit",
]


@pytest.mark.parametrize("circuit_name", circuit_names)
@pytest.mark.parametrize("num_qubits", [4, 5, 6, 7, 8, 9, 10])
@pytest.mark.parametrize("seed", [1, 326, 5678, 12345])
def test_gateset_of_out_circuit(circuit_name, num_qubits, seed):
    circuit = circuit_function(num_qubits, seed)
    transpiler = UCCDefault1()
    target_basis = transpiler.target_basis
    transpiled_circuit = transpiler.run(circuit)
    dag = circuit_to_dag(transpiled_circuit)
    qarg_indices = {qubit: index for index, qubit in enumerate(dag.qubits)}
    basis_translator = next(
        (t for t in transpiler.pass_manager._tasks if isinstance(t, BasisTranslator)),
        BasisTranslator(sel, target_basis),
    )
    compiled_basis, qargs_local_source_basis = basis_translator._extract_basis_target(
        dag, qarg_indices
    )

    assert (
        set(list(zip(*compiled_basis))[0]).issubset(target_basis)
        and not qargs_local_source_basis
    )
