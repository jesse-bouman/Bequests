from typing import List


class Person:
    """
    Class defining a gendered person with the ability to inherit wealth
    """
    def __init__(self, gender: bool, parent_couple_id: int):
        """
        Class constructor, creating a new person with gender *gender*, and who
        is born in the family with couple id *parent_couple_id*. Upon
        construction, the person has no id number and has inherited 0 wealth.

        :param gender: gender of the person. The male gender is taken ``True``
        :type gender: ``bool``
        :param parent_couple_id: identity number of the parent couple
        :type parent_couple_id: ``int``
        """
        self.gender: bool = gender
        self.inh: float = 0
        self.id: int = None
        self.pci: int = parent_couple_id

    def add_inheritance(self, inheritance: float):
        """
        Increases the total inherited wealth of the person by the amount
        *inheritance*

        :param inheritance: awarded amount of inheritance
        :type inheritance: ``float``
        """
        self.inh = self.inh + inheritance

    def set_id(self, p_id: int):
        """
        Award the person with an id number

        :param p_id: person identifier
        :type p_id: ``int``
        """
        self.id = p_id

    def to_array(self) -> List:
        """
        Create an array with all relevant statistics of the person

        :return: list of person id, gender, parent couple id, size of
                 inheritance
        :rtype: list
        """
        return [self.id, int(self.gender), self.pci, self.inh]

    @classmethod
    def data_size(cls) -> int:
        example = cls(False, 0)
        return len(example.to_array())

    def __str__(self):
        g_dict = {True: "Male", False: "Female"}
        string = """Person {}, {} \nParent couple id {} \nInherited {}
                 """.format(self.id, g_dict[self.g], self.pci, self.inh)
        return string

    def __repr__(self):
        return self.__str__()
