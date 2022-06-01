"""
建築基準法
"""
from . import sub_method
from .base_method import BaseMethod
from ..wrapper.element import Quantity


class Law2_5(BaseMethod):
    """
    基準法第2条第5号（主要構造部）の判定
    """

    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    @classmethod
    def main(cls, ifc_file) -> list:
        """
        適合判定実行関数

        Returns:
            bool: 判定結果
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
        target_elements = ["IfcWall", "IfcColumn", "IfcSlab", "IfcBeam", "IfcRoof", "IfcStair"]


        self.target_elements = self.filter_elements(target_elements)[0]


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


class Law21_1(BaseMethod):
    """
    基準法第21条第1号（大規模建築の主要構造部）の判定
    """

    def __init__(self, ifc_file):
        super().__init__(ifc_file)

    @classmethod
    def main(cls, ifc_file):
        """
        適合判定実行関数

        Returns:
            bool: 判定結果
        """
        target = cls(ifc_file=ifc_file)
        if not target.exception() and target.condition():
            target.verification()

        return [target.conformity_elements, target.not_conformity_elements, target.exception_elements]

    def exception(self):
        """
        例外部分の判定

        Returns:
            bool: 判定結果
        """
        # return sub_method(self.ifc_file)
        return False

    def condition(self) -> bool:
        """
        条件部分の判定

        Returns:
            bool: 判定結果
        """

        def __one() -> bool:
            """
            地階を除く階数が4以上であるかの判定

            Returns:
                bool: 判定結果

            """
            storeys = self.ifc_file.by_type('IfcBuildingStorey')
            flag = False
            cnt = 0

            for storey in storeys:
                for d in storey.IsDefinedBy:
                    property_set = d.RelatingPropertyDefinition
                    if hasattr(property_set, "HasProperties"):
                        for property in property_set.HasProperties:
                            if property.is_a('IfcPropertySingleValue') and property.Name == "AboveGround":
                                if property.NominalValue.wrappedValue:
                                    cnt += 1

            if cnt >= 4:
                flag = True

            return flag

        def __two(idx=0) -> bool:
            """
            高さが16メートルを超える建築物であるかの判定

            Args:
                idx(int): 対象の建築物のインデックス番号

            Returns:
                bool: 判定結果

            """
            b = self.ifc_file.by_type('IfcBuilding')[idx]
            flag = False

            for d in b.IsDefinedBy:
                property_set = d.RelatingPropertyDefinition
                if hasattr(property_set, "HasProperties"):
                    for property in property_set.HasProperties:
                        if property.is_a('IfcPropertySingleValue') and property.Name == "Height":
                            if property.NominalValue.wrappedValue > 16000:
                                flag = True
                                break

                if hasattr(property_set, "Quantities"):
                    for q in property_set.Quantities:
                        if q.Name == "Height":
                            if Quantity.value(q) > 16000:
                                flag = True
                                break

            return flag

        def __three(idx=0) -> bool:
            """
            別表第一(い)欄(五)項又は(六)項に掲げる用途に供する特殊建築物で、高さが十三メートルを超えるものの判定

            Args:
                idx(int): 対象の建築物のインデックス番号

            Returns:
                bool: 判定結果
            """
            b = self.ifc_file.by_type('IfcBuilding')[idx]
            flag = True

            for d in b.IsDefinedBy:
                property_set = d.RelatingPropertyDefinition
                if hasattr(property_set, "HasProperties"):
                    for property in property_set.HasProperties:
                        if property.is_a('IfcPropertySingleValue'):
                            if property_set.Name == "Pset_BuildingUse" and property.Name == "MarketCategory":
                                if property.NominalValue.wrappedValue not in ["倉庫", "自動車車庫", "自動車修理工場"]:
                                    flag = False
                                    break
                            if property.Name == "Height":
                                if property.NominalValue.wrappedValue > 13000:
                                    flag = False
                                    break

                if hasattr(property_set, "Quantities"):
                    for q in property_set.Quantities:
                        if q.Name == "Height":
                            if Quantity.value(q) > 13000:
                                flag = False
                                break

            return flag

        flag = False
        if __one() or __two() or __three():
            flag = True
        return flag

    def verification(self):
        """
        基準部分の判定

        Returns:
        """
        conformity_elements_by109_4, not_conformity_elements_by109_4 = sub_method.Law109_4.main(self.ifc_file)
        conformity_elements_by109_5, not_conformity_elements_by109_5 = sub_method.Law109_5.main(
            self.ifc_file,
            conformity_elements_by109_4
        )

        self.conformity_elements = conformity_elements_by109_5
        self.not_conformity_elements = not_conformity_elements_by109_4 + not_conformity_elements_by109_5
