try:
    import config # type: ignore
    print("Config module imported successfully.")
except ImportError:
    print("Config module not found. Please ensure that config.py is in the same directory as main.py.")
