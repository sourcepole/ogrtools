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


def test_detect_model_ili1():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.detect_model() == ['Beispiel']


def test_detect_model_ili2():
    loader = ModelLoader("./tests/data/ch.bazl/ch.bazl.sicherheitszonenplan.oereb_20131118.xtf")
    assert loader.detect_model() == [
        "CodeISO", "chGeoId10", "MultilingualText09", "OeREBKRM09", "OeREBKRM09vs", "OeREBKRM09trsfr"]


def test_detect_model_none():
    loader = ModelLoader("./tests/data/osm/railway.shp")
    assert loader.detect_model() is None


def test_read_ilisite():
    loader = ModelLoader("")
    assert loader.read_ilisite("http://models.interlis.ch/") == [
        'http://models.geo.admin.ch/',
        'http://models.umleditor.org/', 'http://models.ikgeo.ch/']


def test_model_loader():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.load_model() is None


def test_model_conversion():
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
