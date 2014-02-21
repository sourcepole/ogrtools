from ogrtools.interlis.ilismeta import extract_enums_asgml, extract_enums


def test_extract_enums():
    enum_tables = extract_enums("./tests/data/ili/Beispiel.imd")
    assert enum_tables['Beispiel.Bodenbedeckung.BoFlaechen.Art'][1] == {
        'enumtxt': 'befestigt', 'enum': 'befestigt', 'id': 1}


def test_extract_enums_gml():
    gml = extract_enums_asgml("./tests/data/ili/Beispiel.imd")
    print gml
    assert "<gml:featureMember><enum2_Art><id>1</id><enum>befestigt</enum><enumtxt>befestigt</enumtxt></enum2_Art></gml:featureMember>" in gml


def test_extract_extended_enums():
    enum_tables = extract_enums("./tests/data/ili/RoadsExdm2ben.imd")
    print enum_tables
    assert enum_tables['RoadsExdm2ben.Roads.RoadSign.Type'] == [
        {'enumtxt': 'prohibition', 'enum': 'prohibition', 'id': 0},
        {'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        {'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        {'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3}]

    enum_tables = extract_enums("./tests/data/ili/RoadsExdm2ien.imd")
    print enum_tables
    assert enum_tables['RoadsExdm2ben.Roads.RoadSign.Type'] == [
        {'enumtxt': 'prohibition', 'enum': 'prohibition', 'id': 0},
        {'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        {'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        {'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3}]
    assert enum_tables['RoadsExdm2ien.RoadsExtended.RoadSign.Type'] == [
        {'enumtxt': 'prohibition.noentry', 'enum': 'prohibition.noentry', 'id': 0},
        {'enumtxt': 'prohibition.noparking', 'enum': 'prohibition.noparking', 'id': 1},
        {'enumtxt': 'prohibition.other', 'enum': 'prohibition.other', 'id': 2}]
        #FIXME: inherted enums missing:
        #{'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        #{'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        #{'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3}]
