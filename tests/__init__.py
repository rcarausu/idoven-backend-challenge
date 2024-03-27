import os

if "SETTINGS_PATH" not in os.environ:
    tests_directory, _ = os.path.split(__file__)
    os.environ["SETTINGS_PATH"] = os.path.join(f"{tests_directory}/resources", "test_config.ini")
