import os

if "ECG_CONFIG" not in os.environ:
    tests_directory, _ = os.path.split(__file__)
    os.environ["ECG_CONFIG"] = os.path.join(f"{tests_directory}/resources", "test_config.ini")
