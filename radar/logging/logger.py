import logging

class PatientLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Create a prefix with all extra keys and values
        prefix_parts = [f"{key}:{value}" for key, value in self.extra.items()]
        prefix = "[" + ", ".join(prefix_parts) + "] " if prefix_parts else ""
        return prefix + msg, kwargs
