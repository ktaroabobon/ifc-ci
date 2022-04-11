"""
建築基準法施行令に関するコード
"""

from . import standard_method
from .base_method import BaseMethod


class Law109_4(BaseMethod):
    """
    施行令第109条第4項

    基準法第21条第1項の政令で定められている部分の技術的基準について
    """

    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    @classmethod
    def main(cls, ifc_file):
        """
        実行関数

        Returns:

        """
        target = cls(ifc_file=ifc_file)
        target.condition()
        target.verification()

        return [target.conformity_elements, target.not_conformity_elements]

    def condition(self):
        """
        条件部分の判定

        Returns:

        """
        self.target_elements, _ = standard_method.Law2_5.main(self.ifc_file)

    def verification(self):
        """
        基準部分の判定

        Returns:

        """
        if self.target_elements is None:
            return

        conformity_elements = list()
        not_conformity_elements = list()

        for element in self.target_elements:
            for d in element.IsDefinedBy:
                property_set = d.RelatingPropertyDefinition
                if hasattr(property_set, "HasProperties"):
                    for property in property_set.HasProperties:
                        if property.is_a('IfcPropertySingleValue') and property.Name == "LoadBearing":
                            if property.NominalValue.wrappedValue:
                                conformity_elements.append(element)
                            else:
                                not_conformity_elements.append(element)

        self.conformity_elements = conformity_elements
        self.not_conformity_elements = not_conformity_elements


class Law109_5(BaseMethod):
    """
    施行令第109条第5項

    大規模建築物の主要構造部に関する技術的基準について
    """

    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    @classmethod
    def main(cls, ifc_file, target_elements):
        """
        実行関数

        Returns:

        """
        target = cls(ifc_file=ifc_file)
        target.condition(target_elements)
        target.verification()

        return [target.conformity_elements, target.not_conformity_elements]

    def condition(self, target_elements):
        """
        条件部分の判定

        Returns:

        """
        self.target_elements = target_elements

    def verification(self):
        """
        基準部分の判定

        Returns:

        """
        if self.target_elements is None:
            return

        conformity_elements = list()
        not_conformity_elements = list()

        for element in self.target_elements:
            if element.is_a() in ["IfcWall", "IfColumn", "IfcSlab", "IfcBeam"]:
                for d in element.IsDefinedBy:
                    property_set = d.RelatingPropertyDefinition
                    if hasattr(property_set, "HasProperties"):
                        for property in property_set.HasProperties:

                            if property.is_a('IfcPropertySingleValue') and property.Name == "FireRating":
                                if int(property.NominalValue.wrappedValue) >= 45:
                                    conformity_elements.append(element)
                                else:
                                    not_conformity_elements.append(element)

            else:
                for d in element.IsDefinedBy:
                    property_set = d.RelatingPropertyDefinition
                    if hasattr(property_set, "HasProperties"):
                        for property in property_set.HasProperties:
                            if property.is_a('IfcPropertySingleValue') and property.Name == "FireRating":
                                if int(property.NominalValue.wrappedValue) >= 30:
                                    conformity_elements.append(element)
                                else:
                                    not_conformity_elements.append(element)

        self.conformity_elements = conformity_elements
        self.not_conformity_elements = not_conformity_elements
