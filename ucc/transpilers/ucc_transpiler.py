from qiskit import transpile
from qiskit.providers import BackendV2
from qiskit.transpiler import CouplingMap


from ucc.transpilers.ucc_defaults import UCCDefault1


class UCCTranspiler:
    @staticmethod
    def transpile(circuit, target_device = None) -> str:
        """
        Transpiles the given quantum `circuit` using UCC default compiler passes.
        
        Parameters:
            circuit (qiskit.QuantumCircuit): The Qiskit circuit to transpile.
            target_device: Can be a Qiskit backend or Qiskit CouplingMap, or a list of connections between qubits. If None, all-to-all connectivity is assumed.
                        If Qiskit backend or coupling map, only the coupling list extracted from the backend is used.

        Returns:
            QuantumCircuit: The transpiled quantum circuit.
        """

        if target_device is None:
            coupling_list = None
        elif isinstance(target_device, BackendV2):
            coupling_list = list(target_device.coupling_map.get_edges())
        elif isinstance(target_device, CouplingMap):
            # rustworkx.EdgeList object
            coupling_list = target_device.get_edges()
        elif isinstance(target_device, list):
            # What kind of list is this?
            coupling_list = target_device
        else:
            raise ValueError("Invalid backend type. Must be a Qiskit backend, coupling map, or a list of connections between qubits.")
        
        # Transpile the circuit

        ucc_transpiler = UCCDefault1()
        transpiled_circuit = ucc_transpiler.run(circuit, coupling_list=coupling_list)

        if isinstance(target_device, BackendV2):
            # Map the transpiled circuit to the target backend's basis gates
            # TODO: Need to implement different final mapping passes for different backends
            transpiled_circuit = transpile(circuit, optimization_level=0, backend=target_device)
        
        
        return transpiled_circuit

