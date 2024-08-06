class BaseLoader:
    def load_csv(self, file_path: str):
        """This method should be overridden in subclasses."""
        raise NotImplementedError("Subclasses should implement this method.")