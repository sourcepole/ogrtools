from ogrtools.interlis.ilismeta import extract_enums_asgml, extract_enums_json


def test_extract_enums_json():
    enum_tables = extract_enums_json("./tests/data/ili/Beispiel.imd")
    assert enum_tables['Beispiel.Bodenbedeckung.BoFlaechen.Art'][1] == {
        'enumtxt': 'befestigt', 'enum': 'befestigt', 'id': 1}


def test_extract_enums_gml():
    gml = extract_enums_asgml("./tests/data/ili/Beispiel.imd")
    assert "<gml:featureMember><enum0_Art><id>1</id><enum>befestigt</enum><enumtxt>befestigt</enumtxt></enum0_Art></gml:featureMember>" in gml
