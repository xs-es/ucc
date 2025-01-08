Contributing Guide
==================

Thank you for your interest in contributing to UCC!
This guide will help you propose, implement, and validate new techniques for our transpiler.
Follow these steps to ensure a smooth contribution process.

1. Proposing a New Transpiler Pass
----------------------------------

When proposing a new transpiler pass, please include a detailed report containing:

#. Detailed description of the technique
    #. Provide a written abstract without excessive jargon, citing the source of the technique.
    #. (Optional, recommended): Include a diagram showing an example circuit and how it would be affected by this pass.

#. Performance expectations
    #. Estimate how much the technique is expected to reduce gate counts or compile time. This rough estimate helps us prioritize techniques.
    #. Specify which types of circuits are expected to improve or not improve with this technique.
    #. Define test circuits of the above types which you will use to validate the technique.

2. Implementing and Validating a Prototype of the Pass
------------------------------------------------------

#. Create a prototype
    * A Jupyter notebook or a small script is sufficient for the prototype.

#. Validate the prototype
    * Use the test circuits defined in section `1. Proposing a New Transpiler Pass`_ to validate the technique.

.. _1. Proposing a New Transpiler Pass: #proposing-a-new-transpiler-pass

3. Implementing the New Pass in the Codebase
--------------------------------------------

Once the prototype is validated, implement the new pass in the codebase.
You can take inspiration from Qiskit's guide on creating custom transpiler passes: `Qiskit Custom Transpiler Pass <https://docs.quantum.ibm.com/guides/custom-transpiler-pass>`_.

4. Clear Acceptance Criteria for Incorporation into default transpiler
----------------------------------------------------------------------

For the new pass to be incorporated into `the default compiler <https://github.com/unitaryfund/ucc/blob/main/ucc/transpilers/ucc_defaults.py>`_, it must meet the following criteria:

#. Reduction in compiled 2-qubit gate count
    * Demonstrate a reduction in the number of 2-qubit gates.

#. Reduction in runtime
    * Show a reduction in runtime, especially if the new technique replaces a slower one.

#. Compatibility with other passes
    * Ensure the new pass performs as expected when used with other existing passes.

#. Increase in "gate reduction factor per second"
    * This is a key metric defined in the `UCC benchmarks notebook <https://github.com/unitaryfund/ucc/blob/main/benchmarks/ucc_benchmarks.ipynb>`_. The new pass should show an increase in this metric.

We appreciate your contributions and look forward to your new pass proposals!
