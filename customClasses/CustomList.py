
class CustomList(list):
    def getFromString(self, string):
        for item in self:
            if (item.__name__ == string):
                return item