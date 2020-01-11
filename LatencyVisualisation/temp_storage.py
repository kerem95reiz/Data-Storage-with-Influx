from queue import Queue

# class TemporaryDataStorage(Queue):
#     __instance = None

#     @staticmethod
#     def get_instance():
#         if TemporaryDataStorage.__instance == None:
#             TemporaryDataStorage()
#         return TemporaryDataStorage.__instance


#     def __init__(self):
#         if TemporaryDataStorage.__instance != None:
#             raise Exception("This class is singleton!")
#         else:
#             TemporaryDataStorage.__instance = self

@Singleton
class TemporaryDataStorage(Queue):
    __instance = None

    @staticmethod
    def get_instance():
        if TemporaryDataStorage.__instance == None:
            TemporaryDataStorage()
        return TemporaryDataStorage.__instance


    def __init__(self):
        if TemporaryDataStorage.__instance != None:
            raise Exception("This class is singleton!")
        else:
            TemporaryDataStorage.__instance = self
