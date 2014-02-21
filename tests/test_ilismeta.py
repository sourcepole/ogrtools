from ogrtools.interlis.ilismeta import ImdParser


def test_extract_enums():
    parser = ImdParser("./tests/data/ili/Beispiel.imd")
    enum_tables = parser.extract_enums()
    assert enum_tables['Beispiel.Bodenbedeckung.BoFlaechen.Art'][1] == {
        'enumtxt': 'befestigt', 'enum': 'befestigt', 'id': 1}


def test_extract_enums_gml():
    parser = ImdParser("./tests/data/ili/Beispiel.imd")
    gml = parser.extract_enums_asgml()
    print gml
    assert "<gml:featureMember><enum2_Art><id>1</id><enum>befestigt</enum><enumtxt>befestigt</enumtxt></enum2_Art></gml:featureMember>" in gml


def test_extract_extended_enums():
    parser = ImdParser("./tests/data/ili/RoadsExdm2ben.imd")
    enum_tables = parser.extract_enums()
    print enum_tables
    assert enum_tables['RoadsExdm2ben.Roads.RoadSign.Type'] == [
        {'enumtxt': 'prohibition', 'enum': 'prohibition', 'id': 0},
        {'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        {'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        {'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3}]

    parser = ImdParser("./tests/data/ili/RoadsExdm2ien.imd")
    enum_tables = parser.extract_enums()
    print enum_tables
    assert enum_tables['RoadsExdm2ben.Roads.RoadSign.Type'] == [
        {'enumtxt': 'prohibition', 'enum': 'prohibition', 'id': 0},
        {'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        {'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        {'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3}]
    assert enum_tables['RoadsExdm2ien.RoadsExtended.RoadSign.Type'] == [
        {'enumtxt': 'prohibition', 'enum': 'prohibition', 'id': 0},  # FIXME: omit non-leaf enum!
        {'enumtxt': 'indication', 'enum': 'indication', 'id': 1},
        {'enumtxt': 'danger', 'enum': 'danger', 'id': 2},
        {'enumtxt': 'velocity', 'enum': 'velocity', 'id': 3},
        {'enumtxt': 'prohibition.noentry', 'enum': 'prohibition.noentry', 'id': 4},
        {'enumtxt': 'prohibition.noparking', 'enum': 'prohibition.noparking', 'id': 5},
        {'enumtxt': 'prohibition.other', 'enum': 'prohibition.other', 'id': 6}]
