import os
import tempfile

from interlis.model_loader import ModelLoader

TEMPDIR = tempfile.gettempdir()


def test_detect_ili1():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.detect_format() == 'Interlis 1'


def test_detect_ili2():
    loader = ModelLoader("./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf")
    assert loader.detect_format() == 'Interlis 2'


def test_detect_none():
    loader = ModelLoader("./tests/data/osm/railway.shp")
    assert loader.detect_format() is None


def test_detect_models_ili1():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.detect_models()[0].name == 'Beispiel'


def test_detect_models_ili2():
    loader = ModelLoader("./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf")
    models = loader.detect_models()
    names = map(lambda model: model.name, models)
    assert names == [
        "CodeISO", "chGeoId10", "MultilingualText09", "OeREBKRM09", "OeREBKRM09vs", "OeREBKRM09trsfr"]


def test_detect_models_none():
    loader = ModelLoader("./tests/data/osm/railway.shp")
    assert loader.detect_models() is None


def xxtest_read_ilisite():
    loader = ModelLoader("")
    assert loader.lookup_sites("http://models.interlis.ch/") == [
        'http://models.geo.admin.ch/',
        'http://models.umleditor.org/', 'http://models.ikgeo.ch/']


def test_model_loader():
    loader = ModelLoader("./tests/data/ili/roads23.xtf")
    print loader.load_models()


def xxtest_model_conversion():
    loader = ModelLoader("")
    outfile = os.path.join(TEMPDIR, "tmpogrtools")
    loader.convert_model(["./tests/data/ili/Beispiel.ili"], outfile)
    with open(outfile) as file:
        imd = file.read()
        assert 'IlisMeta07.ModelData.EnumNode TID="Beispiel.Bodenbedeckung.BoFlaechen.Art.TYPE.TOP"' in imd

    loader.convert_model(["./tests/data/ili/Test23_erweitert.ili"], outfile)
    with open(outfile) as file:
        imd = file.read()
        assert 'IlisMeta07.ModelData.Class TID="Test23_erweitert.FixpunkteKategorie1.LFP1"' in imd
        #Does include Test23.ili as well:
        assert 'IlisMeta07.ModelData.NumType TID="Test23.Genauigkeit"' in imd
