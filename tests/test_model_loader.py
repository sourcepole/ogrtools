import os

from interlis.model_loader import ModelLoader

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
    assert loader.detect_model() == ["CodeISO", "chGeoId10",
    "MultilingualText09", "OeREBKRM09", "OeREBKRM09vs", "OeREBKRM09trsfr"]

def test_detect_model_none():
    loader = ModelLoader("./tests/data/osm/railway.shp")
    assert loader.detect_model() is None

def test_read_ilisite():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.read_ilisite("http://models.interlis.ch/") == ['http://models.geo.admin.ch/',
        'http://models.umleditor.org/', 'http://models.ikgeo.ch/']

def test_model_loader():
    loader = ModelLoader("./tests/data/ili/Beispiel.itf")
    assert loader.load_model()
