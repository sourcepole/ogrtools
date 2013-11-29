import ogr
import json

class Spec:

    def __init__(self, ds):
        self.open(ds)

    def open(self, ds):
        self.ds = ogr.Open( ds, update = False )
        return self.ds

    def close(self):
        if self.ds is not None:
            self.ds.Destroy()

    def generate_spec(self, outfile = None, layer_list = []):
        if self.ds is None:
            return None

        if len(layer_list) == 0:
            for layer in self.ds:
                layer_list.append( layer.GetLayerDefn().GetName() )

        spec = {}
        #Javscript comments are not allowed JSON
        spec['_comment'] = '// OGR transformation specifcation'

        for name in layer_list:
            layer = self.ds.GetLayerByName(name)
            layerdef = layer.GetLayerDefn()

            speclayer = {}
            spec[name] = speclayer

            for fld_index in range(layerdef.GetFieldCount()):
                src_fd = layerdef.GetFieldDefn( fld_index )

                specfield = {}
                field_name = src_fd.GetName()
                speclayer[field_name] = specfield
                specfield['src'] = field_name

        specstr = json.dumps(spec, indent=2)

        if outfile is not None:
            f = open(outfile, "w")
            f.write(specstr)
            f.close()

        return specstr
