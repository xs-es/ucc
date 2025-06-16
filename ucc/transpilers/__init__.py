# UPDATE FOR: ucc/transpilers/__init__.py
# Add these lines to the existing __init__.py file

# QHRF Harmonic Resonance Pass imports (ADD THESE LINES)
from .qhrf_pass import QHRFHarmonicResonancePass, QHRFSimplifiedPass

# Update the __all__ list to include QHRF passes (ADD TO EXISTING __all__)
__all__ = [
    # ... existing exports ...
    'QHRFHarmonicResonancePass',
    'QHRFSimplifiedPass',
]

# COMPLETE EXAMPLE of what the file should look like:
"""
Transpiler passes for UCC quantum circuit optimization.

This module contains various quantum circuit transformation passes
that optimize quantum circuits for better performance.
"""

# Existing imports (example - adjust based on actual UCC structure)
from .some_existing_pass import SomeExistingPass
from .another_pass import AnotherPass

# QHRF Harmonic Resonance Pass imports (NEW)
from .qhrf_pass import QHRFHarmonicResonancePass, QHRFSimplifiedPass

# Export all transpiler passes
__all__ = [
    # Existing passes (example)
    'SomeExistingPass',
    'AnotherPass',
    
    # QHRF passes (NEW)
    'QHRFHarmonicResonancePass',
    'QHRFSimplifiedPass',
]
