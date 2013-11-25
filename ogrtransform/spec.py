import ogr

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

        spec = '// OGR transformation specifcation\n\n'

        for name in layer_list:
            layer = self.ds.GetLayerByName(name)
            layerdef = layer.GetLayerDefn()

            spec += '{ "%s":\n' % name
            spec += '    {\n'

            for fld_index in range(layerdef.GetFieldCount()):
                src_fd = layerdef.GetFieldDefn( fld_index )

                spec += '      "%s": {\n' % src_fd.GetName()
                spec += '        "src": "%s"\n' % src_fd.GetName()
                spec += '      },\n' #FIXME: skip last

            spec += '    }\n'
            spec += '}\n'

        if outfile is not None:
            f = open(outfile, "w")
            f.write(spec)
            f.close()

        return spec
