"""
Test script for Great Expectations suites.

This script validates that all expectation suites are correctly defined
and can be loaded without errors.
"""

import sys
import os

# Add the gx folder to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_suite_from_file(filepath: str):
    """Load an expectation suite from a Python file."""
    import importlib.util
    
    module_name = os.path.basename(filepath).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module.suite_name, module.expectations


def test_suite_structure(suite_name: str, expectations: list, file_name: str) -> bool:
    """Test that a suite has valid structure."""
    print(f"\n{'='*60}")
    print(f"Testing: {file_name}")
    print(f"{'='*60}")
    
    errors = []
    
    # Check suite name
    if not suite_name:
        errors.append("Suite name is empty")
    else:
        print(f"✓ Suite name: {suite_name}")
    
    # Check expectations
    if not expectations:
        errors.append("Suite has no expectations")
    else:
        print(f"✓ Number of expectations: {len(expectations)}")
    
    # Validate each expectation
    for i, exp in enumerate(expectations):
        exp_type = type(exp).__name__
        print(f"  - {exp_type}")
    
    if errors:
        print(f"\n✗ FAILED with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print(f"\n✓ PASSED")
        return True


def main():
    """Main test runner."""
    expectations_dir = os.path.join(os.path.dirname(__file__), "expectations")
    
    print("=" * 60)
    print("Great Expectations Suite Validation Tests")
    print("=" * 60)
    
    # Get all expectation files
    suite_files = [
        f for f in os.listdir(expectations_dir) 
        if f.endswith('_expectations.py')
    ]
    
    if not suite_files:
        print("ERROR: No expectation files found!")
        sys.exit(1)
    
    print(f"\nFound {len(suite_files)} expectation suite(s) to test:\n")
    for f in suite_files:
        print(f"  - {f}")
    
    results = {}
    
    for suite_file in suite_files:
        filepath = os.path.join(expectations_dir, suite_file)
        try:
            suite_name, expectations = load_suite_from_file(filepath)
            passed = test_suite_structure(suite_name, expectations, suite_file)
            results[suite_file] = passed
        except Exception as e:
            print(f"\n✗ ERROR loading {suite_file}: {str(e)}")
            results[suite_file] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    
    for suite_file, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {suite_file}")
    
    print(f"\nTotal: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
