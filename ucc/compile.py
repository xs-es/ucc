from ucc.transpilers import UCCTranspiler
from qbraid.transpiler import transpile
from qbraid.programs.alias_manager import get_program_type_alias
from qbraid.transpiler import ConversionGraph

supported_circuit_formats = ConversionGraph().nodes()


def compile(
    circuit,
    return_format="original",
    target_device=None,
):
    """Compiles the provided quantum `circuit` by translating it to a Qiskit
    circuit, transpiling it, and returning the optimized circuit in the
    specified `return_format`.

    Args:
        circuit (object): The quantum circuit to be compiled.
        return_format (str): The format in which your circuit will be returned.
            e.g., "TKET", "OpenQASM2". Check ``ucc.supported_circuit_formats()``.
            Defaults to the format of the input circuit.

    Returns:
        object: The compiled circuit in the specified format.
    """
    if return_format == "original":
        return_format = get_program_type_alias(circuit)

    # Translate to Qiskit Circuit object
    qiskit_circuit = transpile(circuit, "qiskit")
    compiled_circuit = UCCTranspiler.transpile(
        qiskit_circuit,
        target_device=target_device,
    )

    # Translate the compiled circuit to the desired format
    final_result = transpile(compiled_circuit, return_format)
    return final_result
