from pathlib import Path

import ifcopenshell

from ifc_ci.wrapper.element import Quantity

base_dir = Path().resolve()
data_dir = base_dir / "data"

SAMPLE_DATA_PATH = data_dir / 'test.ifc'

if __name__ == '__main__':
    ifc_file = ifcopenshell.open(str(SAMPLE_DATA_PATH))
    products = ifc_file.by_type('IfcWall')
    for product in products:
        print(f"product type: {product.is_a()}")
        # print(product.type())
        for d in product.IsDefinedBy:
            # if d.is_a('IfcRelDefinesByProperties'):
            property_set = d.RelatingPropertyDefinition
            # if property_set.is_a() == 'IfcElementQuantity':
            print(f">properties name: {property_set.Name}")
            if hasattr(property_set, "HasProperties"):
                for p in property_set.HasProperties:
                    if p.is_a('IfcPropertySingleValue'):
                        # if property.is_a() == 'IfcElementQuantity':
                        #     print(" " + property)
                        print(f">>property set name: {p.Name}")
                        print(f">>property set value: {p.NominalValue.wrappedValue}")
                        print(f">>property set value type: {type(p.NominalValue.wrappedValue)}")
                        # print(" " + property.Type) Not working
            elif hasattr(property_set, "Quantities"):
                for q in property_set.Quantities:
                    print(f">>quantity set name: {q.Name}")
                    print(f">>quantity set value: {Quantity.value(q)}")

    for product in products:
        print(f"product type: {product.is_a()}")
        if product.is_a("IfcBuildingElement"):
            for rs in product.ContainedInStructure:
                e = rs.RelatingStructure
                if not e.is_a("IfcBuildingStorey"):
                    continue
                print(f">Relating Structure type: {e.is_a()}")
                print(f">Relating Structure name: {e.Name}")
                print(f">Relating Structure elevation: {e.Elevation}")
