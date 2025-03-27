# benchmark_script.py
import sys
import argparse

from common import (
    log_performance,
    save_results,
    get_compile_function,
    get_native_rep,
)

parser = argparse.ArgumentParser(description="Benchmarking script for quantum compilers.")

# Define arguments
parser.add_argument("qasm_file", type=str, help="Path to the QASM file.")
parser.add_argument("compiler", type=str, help="Compiler alias to use.")
parser.add_argument("results_folder", type=str, help="Folder to save results.")

args = parser.parse_args()

# Get the QASM file, compiler, and results folder passed as command-line arguments
qasm_file = args.qasm_file
compiler_alias = args.compiler
results_folder = args.results_folder

# Ensure both QASM file and compiler are provided as arguments
if len(args) < 4:
    print(
        "Usage: python3 benchmark_script.py <qasm_file> <compiler> <results_folder>"
    )
    sys.exit(1)

# Read the QASM file
with open(qasm_file, "r") as file:
    print(f"Compiling {qasm_file} using {compiler_alias}")
    circuit_name = qasm_file.split("/")[-1].split("_N")[0]

    # Load the QASM file and get the native representation
    qasm_string = file.read()
    native_circuit = get_native_rep(qasm_string, compiler_alias)
    compile_function = get_compile_function(compiler_alias)

    # Log performance
    log_entry = log_performance(
        compile_function, native_circuit, compiler_alias, circuit_name
    )

    # Save the log entry (you can add it to a list if needed)
    results_log = [log_entry]

# Save the results to a CSV file
save_results(
    results_log, benchmark_name="gates", folder=results_folder, append=True
)
