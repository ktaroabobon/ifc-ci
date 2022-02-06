from pathlib import Path

import ifcopenshell

base_dir = Path().resolve()
data_dir = base_dir / "data"


SAMPLE_DATA_PATH = data_dir / 'test.ifc'

if __name__ == '__main__':
    ifc_file = ifcopenshell.open(str(SAMPLE_DATA_PATH))
    products = ifc_file.by_type('IfcProduct')
    for product in products:
        print(product.is_a())