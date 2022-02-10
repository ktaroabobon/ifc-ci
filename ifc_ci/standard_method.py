"""
建築基準法
"""


class StandardMethod(object):
    def __init__(self, building):
        self.building = building
        self.condition = None
        self.exception = None
        self.verification = None

    def main(self):
        if self.exception is not None:
            self.exception()

        if self.condition is not None:
            self.condition()

        self.verification()


class law21(StandardMethod):
    def exception(self):
        # return sub_method(self.building)
        return True

    def condition(self) -> bool:
        def __one() -> bool:
            storeys = self.building.by_type('IfcBuildingStorey')
            flag = False
            cnt = 0

            for storey in storeys:
                for d in storey.IsDefinedBy:
                    property_set = d.RelatingPropertyDefinition
                    for property in property_set.HasProperties:
                        if property.is_a('IfcPropertySingleValue'):
                            if property.NominalValue.wrappedValue:
                                cnt += 1

            if cnt >= 4:
                flag = True

            return flag

        def __two() -> bool:
            b = self.building.by_type('IfcBuilding')[0]
            flag = False

            for d in b.IsDefinedBy:
                property_set = d.RelatingPropertyDefinition
                if property_set.is_a() == 'IfcElementQuantity':
                    for property in property_set.HasProperties:
                        if property.is_a() == 'IfcElementQuantity':
                            print(" " + property.Name)
                            print(property.NominalValue.wrappedValue)
                            # print(" " + property.Type) Not working

            return flag
