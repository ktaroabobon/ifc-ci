from pathlib import Path

import ifcopenshell

base_dir = Path().resolve()
data_dir = base_dir / "data"

SAMPLE_DATA_PATH = data_dir / 'test.ifc'

if __name__ == '__main__':
    ifc_file = ifcopenshell.open(str(SAMPLE_DATA_PATH))
    products = ifc_file.by_type('IfcWall')
    for product in products:
        print(product.is_a())
        print(product.type())
        for d in product.IsDefinedBy:
            # if d.is_a('IfcRelDefinesByProperties'):
            property_set = d.RelatingPropertyDefinition
            if property_set.is_a() == 'IfcElementQuantity':
                print(property_set.Name)
                for property in property_set.Quantities:
                    if property.is_a() == 'IfcElementQuantity':
                        print(" " + property.Name)
                        print(property.NominalValue.wrappedValue)
                        # print(" " + property.Type) Not working
