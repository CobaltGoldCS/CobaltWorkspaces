import dataclasses

@dataclasses.dataclass
class DataClass():
    
    bridgeClass : str
    command : str
    
    def serialize(self):
        """Turn the dataclass variables into pickleable strings"""
        if not isinstance(self.bridgeClass, str):
            self.bridgeClass = self.bridgeClass.__name__
    def unserialize(self):
        """Return the strings into compatable classes"""
        if isinstance(self.bridgeClass, str):
            self.bridgeclass = eval(self.bridgeClass)(self.command)