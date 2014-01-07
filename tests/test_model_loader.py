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
