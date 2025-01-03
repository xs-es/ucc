from qiskit.transpiler import TransformationPass, Target, CouplingMap
from qiskit.providers import provider
from qiskit.converters import circuit_to_dag, dag_to_circuit
import mapomatic as mm


class MapomaticLayout(TransformationPass):

    def __init__(self, coupling_map: CouplingMap, basis_gates):
        super().__init__()
        self.coupling_map = coupling_map
        self.basis_gates = basis_gates
        self.num_qubits = self.coupling_map.graph.num_nodes()


    def best_overall_layout(self, circ, layouts, successors=False, call_limit=int(3e7),
                        cost_function=None):
        """Find the best selection of qubits and system to run
        the chosen circuit one.

        Parameters:
            circ (QuantumCircuit): Quantum circuit
            successors (bool): Return list best mappings per backend passed.
            call_limit (int): Maximum number of calls to VF2 mapper.
            cost_function (callable): Custom cost function, default=None

        Returns:
            tuple: (best_layout, best_backend, best_error)
            list: List of tuples for best match for each backend
        """


        if cost_function is None:
            cost_function = self.default_cost

        best_out = []

        circ_qubits = circ.num_qubits
        num_qubits = self.num_qubits
        if circ_qubits <= num_qubits:
            layouts = mm.matching_layouts(circ, self.coupling_map,
                                    call_limit=call_limit)
            layout_and_error = self.evaluate_layouts(circ, layouts,
                                                cost_function=cost_function)
            if any(layout_and_error):
                layout = layout_and_error[0][0]
                error = layout_and_error[0][1]
                best_out.append((layout, error))
        best_out.sort(key=lambda x: x[1])
        if successors:
            return best_out
        if best_out:
            return best_out[0]
        return best_out


    def default_cost(self, circ, layouts):
        """The default mapomatic cost function that returns the total
        error rate over all the layouts for the gates in the given circuit

        Parameters:
            circ (QuantumCircuit): circuit of interest
            layouts (list of lists): List of specified layouts

        Returns:
            list: Tuples of layout and error
        """
        out = []
        # Make a single layout nested
        for layout in layouts:
            for item in circ._data:
                if item[0].num_qubits == 2 and item[0].name != 'barrier':
                    q0 = circ.find_bit(item[1][0]).index
                    q1 = circ.find_bit(item[1][1]).index
                    fid *= (1-props.gate_error(item[0].name, [layout[q0],
                                            layout[q1]]))
            out.append((layout, error))
        return out

    def evaluate_layouts(self, circ, layouts, cost_function=None):
        """Evaluate the CNOT cost of the layout on a backend.

        Parameters:
            circ (QuantumCircuit): circuit of interest
            layouts (list): Specified layouts
            cost_function (callable): Custom cost function, default=None

        Returns:
            list: Tuples of layout and cost
        """
        if not any(layouts):
            return []
        circuit_gates = set(circ.count_ops()).difference({'barrier', 'reset',
                                                        'measure', 'delay'})
        if not circuit_gates.issubset(self.basis_gates):
            return []
        if not isinstance(layouts[0], list):
            layouts = [layouts]
        if cost_function is None:
            cost_function = self.default_cost
        out = cost_function(circ, layouts)
        out.sort(key=lambda x: x[1])
        return out


    def run(self, dag):
        circ = dag_to_circuit(dag)
        small_circ = mm.deflate_circuit(circ)
        layouts = mm.matching_layouts(circ, self.coupling_map, strict_direction=True, call_limit=int(3e7))
        best_circ = self.best_overall_layout(small_circ, layouts, self.coupling_map)
        return circuit_to_dag(best_circ)

