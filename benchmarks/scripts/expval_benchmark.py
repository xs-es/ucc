import sys
import os.path
from typing import Any, List, Set
import math
import numpy as np

import cirq
import pytket
import qiskit
from qiskit import qasm2
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator
import numpy as np

from common import (
    cirq_compile,
    pytket_compile,
    qiskit_compile,
    save_results,
    get_native_rep,
    create_depolarizing_noise_model,
)
from ucc import compile as ucc_compile

SINGLE_QUBIT_ERROR_RATE = 0.01
TWO_QUBIT_ERROR_RATE = 0.03


def compile_for_simulation(circuit: Any, compiler_alias: str) -> qiskit.QuantumCircuit:
    """Compiles the circuit and converts it to qiskit so it can be run on the AerSimulator.

    Args:
        circuit: The circuit to be compiled. Can be any of the supported
            circuit representations (cirq, qiskit, pytket)
        compiler_alias: The alias of the compiler to be used for compilation.
            Can be one of "ucc", "qiskit", "cirq", "pytket", or "none".

    Returns:
        A compiled circuit having used the compiler affiliated with the
        compiler_alias.
    """
    match compiler_alias:
        case "ucc":
            ucc_compiled = ucc_compile(circuit, return_format="qiskit")
            ucc_compiled.save_density_matrix()
            return ucc_compiled

        case "pytket":
            pytket_compiled = pytket.qasm.circuit_to_qasm_str(pytket_compile(circuit))
            pytket_compiled_qiskit = qasm2.loads(pytket_compiled)
            pytket_compiled_qiskit.save_density_matrix()
            return pytket_compiled_qiskit

        case "qiskit":
            qiskit_compiled = qiskit_compile(circuit)
            qiskit_compiled.save_density_matrix()
            return qiskit_compiled

        case "cirq":
            cirq_compiled_qasm = cirq.qasm(cirq_compile(circuit))
            cirq_compiled_qiskit = qasm2.loads(cirq_compiled_qasm)
            cirq_compiled_qiskit.save_density_matrix()
            return cirq_compiled_qiskit

        case _:
            raise ValueError(f"Unknown compiler alias: {compiler_alias}")

def depolarizing_error_model(one_q_err, two_q_err):
    depolarizing_noise = NoiseModel()
    error = depolarizing_error(one_q_err, 1)
    two_qubit_error = depolarizing_error(two_q_err, 2)
    # TODO: errors should only be added to the gateset that we are compiling to
    # but there is a bug with cirq currently compiling to U3 and CZ
    depolarizing_noise.add_all_qubit_quantum_error(error, ["u1", "u2", "u3", "rx", "ry", "rz", "h"])
    depolarizing_noise.add_all_qubit_quantum_error(two_qubit_error, ["cx", "cz"])
    return depolarizing_noise


def simulate_density_matrix(circuit: qiskit.QuantumCircuit,  one_q_err: float = 0.01, two_q_err: float = 0.03) -> np.ndarray:
    simulator = AerSimulator(method="density_matrix", noise_model=depolarizing_error_model(one_q_err, two_q_err))
    return simulator.run(circuit).result().data()["density_matrix"]


def get_heavy_bitstrings(circuit: qiskit.QuantumCircuit) -> Set[str]:
    simulator = AerSimulator(method="statevector")
    result = simulator.run(circuit).result()
    counts = list(result.get_counts().items())
    median = np.median([c for (_, c) in counts])
    return set(bitstring for (bitstring, p) in counts if p > median)


def estimate_heavy_output(circuit: qiskit.QuantumCircuit, one_q_err: float = 0.002, two_q_err: float = 0.02) -> List[float]:   
    # Determine the heavy bitstrings.
    heavy_bitstrings = get_heavy_bitstrings(circuit)
    # Count the number of heavy bitstrings sampled on the backend.
    simulator = AerSimulator(method="statevector", noise_model=depolarizing_error_model(one_q_err, two_q_err))
    result =  simulator.run(circuit).result()

    heavy_counts = sum([result.get_counts().get(bitstring, 0) for bitstring in heavy_bitstrings])
    nshots = 10000
    hop = (
        heavy_counts - 2 * math.sqrt(heavy_counts * (nshots - heavy_counts))
    ) / nshots
    return hop


def eval_exp_vals(compiled_circuit, uncompiled_qiskit_circuit, circuit_name):
    """Calculates the expectation values of observables based on input benchmark circuit."""
    circuit_short_name = circuit_name.split("_N")[0]
    if circuit_short_name == "qv":
        compiled_circuit.measure_all()
        uncompiled_qiskit_circuit.measure_all()
        return estimate_heavy_output(compiled_circuit), estimate_heavy_output(uncompiled_qiskit_circuit, 0, 0), "heavy_output_prob"
    else:
        obs_str = "Z" * compiled_circuit.num_qubits
        observable = Operator.from_label(obs_str)
        density_matrix = simulate_density_matrix(compiled_circuit)
        compiled_ev = np.real(density_matrix.expectation_value(observable))
        ideal_state = Statevector.from_instruction(uncompiled_qiskit_circuit)
        ideal_ev = np.real(ideal_state.expectation_value(observable))
        
        return compiled_ev, ideal_ev, obs_str


def qiskit_gateset(circuit: qiskit.QuantumCircuit) -> set[str]:
    everything = set(circuit.count_ops().keys())
    return everything - {"save_density_matrix"}


circuit_name = qasm_path.split('/')[-1]
uncompiled_qiskit_circuit = get_native_rep(qasm_string, "qiskit")
native_circuit = get_native_rep(qasm_string, compiler_alias)
compiled_circuit = compile_for_simulation(native_circuit, compiler_alias)
circuit_name = os.path.split(qasm_path)[-1]


def eval_exp_vals(compiled_circuit, uncompiled_qiskit_circuit, circuit_name):
    """Calculates the expectation values of observables based on input benchmark circuit."""
    circuit_short_name = circuit_name.split("_N")[0]
    if circuit_short_name == "qv":
        compiled_circuit.measure_all()
        uncompiled_qiskit_circuit.measure_all()
        return estimate_heavy_output(compiled_circuit), estimate_heavy_output(uncompiled_qiskit_circuit, 0, 0), "heavy_output_prob"
    else:
        obs_str = "Z" * compiled_circuit.num_qubits
        observable = Operator.from_label(obs_str)
        density_matrix = simulate_density_matrix(compiled_circuit)
        compiled_ev = np.real(density_matrix.expectation_value(observable))
        ideal_state = Statevector.from_instruction(uncompiled_qiskit_circuit)
        ideal_ev = np.real(ideal_state.expectation_value(observable))
        
        return compiled_ev, ideal_ev, obs_str
      
      
compiled_ev, ideal_ev, obs_str = eval_exp_vals(compiled_circuit, native_circuit, circuit_name)


def parse_arguments() -> tuple[str, str, str, bool]:
    """Parses command-line arguments and returns them as a tuple.

    Returns:
        A tuple containing the following elements:
            - qasm_path: The file path to the QASM file.
            - compiler_alias: The alias of the compiler to use.
            - results_folder: The folder where results will be stored.
            - log: A boolean indicating whether to log compilation
                gateset/number details
    """

    if len(sys.argv) < 5:
        print(
            "Usage: python expval_benchmark.py <qasm_filepath> <compiler> <results_folder> <log details>"
        )
        sys.exit(1)

    qasm_path: str = sys.argv[1]
    compiler_alias: str = sys.argv[2]
    results_folder: str = sys.argv[3]
    log: bool = True if sys.argv[4].lower() == "true" else False

    return qasm_path, compiler_alias, results_folder, log


def fetch_pre_post_compiled_circuits(
    qasm_path: str,
    compiler_alias: str,
    log_details: bool = False,
) -> tuple[qiskit.QuantumCircuit, qiskit.QuantumCircuit]:
    """Fetches and compiles a QASM circuit, returning both the uncompiled and compiled versions.

    Args:
        qasm_path: The file path to the QASM file.
        compiler_alias: The compiler to use to compile the circuit.
        log_details: If True, logs details about the compilation process. Defaults to False.
    """

    with open(qasm_path) as f:
        qasm_string = f.read()

    uncompiled_qiskit_circuit = get_native_rep(qasm_string, "qiskit")
    native_circuit = get_native_rep(qasm_string, compiler_alias)
    compiled_qiskit_circuit = compile_for_simulation(
        native_circuit, compiler_alias
    )

    if log_details:
        circuit_name = os.path.split(qasm_path)[-1]
        print(f"Compiling {circuit_name} with {compiler_alias}")
        print(
            f"    Gate reduction: {len(uncompiled_qiskit_circuit)} -> {len(compiled_qiskit_circuit) - 1}"
        )  # minus 1 to account for the addition of `save_density_matrix`
        print(
            f"    Starting gate set: {qiskit_gateset(uncompiled_qiskit_circuit)}"
        )
        print(
            f"    Final gate set:    {qiskit_gateset(compiled_qiskit_circuit)}"
        )
        print(f"    Starting gates: {uncompiled_qiskit_circuit.count_ops()}")
        print(f"    Final gates:    {compiled_qiskit_circuit.count_ops()}")

    return uncompiled_qiskit_circuit, compiled_qiskit_circuit


def simulate_expvals(
    uncompiled_circuit: qiskit.QuantumCircuit,
    compiled_circuit: qiskit.QuantumCircuit,
    observable: str,
) -> tuple[float, float]:
    """Simulates the expectation values of a given observable for
    both uncompiled and compiled quantum circuits.

    Args:
        uncompiled_circuit: The original quantum circuit before compilation.
        compiled_circuit: The quantum circuit after compilation.
        observable: The observable for which the expectation value
            is to be calculated, represented as a string.

    Returns:
        A tuple containing the expectation values of the observable for the
        uncompiled and compiled circuits, respectively.
    """

    density_matrix = simulate_density_matrix(compiled)
    observable = Operator.from_label(observable)
    compiled_ev = np.real(density_matrix.expectation_value(observable))

    ideal_state = Statevector.from_instruction(uncompiled)
    ideal_ev = np.real(ideal_state.expectation_value(observable))

    return ideal_ev, compiled_ev


if __name__ == "__main__":
    qasm_path, compiler_alias, results_folder, log = parse_arguments()

    uncompiled, compiled = fetch_pre_post_compiled_circuits(
        qasm_path, compiler_alias, log_details=log
    )

    observable = "Z" * compiled.num_qubits
    ideal_ev, compiled_ev = simulate_expvals(uncompiled, compiled, observable)
    compiled_ev, ideal_ev, obs_str = eval_exp_vals(compiled_circuit, uncompiled_qiskit_circuit, circuit_name)


    results = [
        {
            "compiler": compiler_alias,
            "circuit_name": qasm_path.split("/")[-1].split("_N")[0],
            "observable": observable,
            "expval": compiled_ev,
            "absolute_error": abs(ideal_ev - compiled_ev),
            "relative_error": abs(ideal_ev - compiled_ev) / abs(ideal_ev),
            "ideal_expval": ideal_ev,
        }
    ]

    save_results(
        results, benchmark_name="expval", folder=results_folder, append=True
    )
