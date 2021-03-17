from abc import ABC, abstractmethod


class ISql(ABC):
    @abstractmethod
    def create_link(self):
        pass

    @abstractmethod
    def destroy_link(self):
        pass

    @abstractmethod
    def commit_link(self):
        pass

    @abstractmethod
    def name_column_table(self, name_table):
        pass