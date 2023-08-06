
import yaml
from yaml.loader import SafeLoader

# YAML LOADER

def all_fields_to_str(a):
    if isinstance(a, list):
        bools = []
        for item in a:
            if isinstance(item, dict):
                bools.append(all_fields_to_str(item))
            else:
                bools.append(item)

    elif isinstance(a, dict):
        bools = {}
        for k, v in a.items():
            bools[k] = all_fields_to_str(v)

    else:
        bools = str(a)
    
    return bools


def cf_lower_all_keys(a):
    if isinstance(a, list):
        lowered = []
        for item in a:
            if isinstance(item, dict):
                lowered.append(cf_lower_all_keys(item))
            else:
                lowered.append(item)

    elif isinstance(a, dict):
        lowered = {}
        for k, v in a.items():
            lowered[k[0].lower() + k[1:]] = cf_lower_all_keys(v)

    else:
        lowered = a
    
    return lowered


class CFYamlLoader(SafeLoader):
    pass

class SafeUnknownConstructor(yaml.constructor.SafeConstructor):
    def __init__(self):
        yaml.constructor.SafeConstructor.__init__(self)

    def construct_undefined(self, node):
        data = getattr(self, 'construct_' + node.id)(node)
        datatype = type(data)
        wraptype = type('TagWrap_'+datatype.__name__, (datatype,), {})
        wrapdata = wraptype(data)
        wrapdata.tag = lambda: None
        wrapdata.datatype = lambda: None
        setattr(wrapdata, "wrapTag", node.tag)
        setattr(wrapdata, "wrapType", datatype)
        return wrapdata



# class SafeUnknownLoader(SafeUnknownConstructor, yaml.loader.SafeLoader):
#     def __init__(self, stream):
#         SafeUnknownConstructor.__init__(self)
#         yaml.loader.SafeLoader.__init__(self, stream)


class SafeUnknownRepresenter(yaml.representer.SafeRepresenter):
    def represent_data(self, wrapdata):
        tag = False
        if type(wrapdata).__name__.startswith('TagWrap_'):
            datatype = getattr(wrapdata, "wrapType")
            tag = getattr(wrapdata, "wrapTag")
            data = datatype(wrapdata)
        else:
            data = wrapdata
        node = super(SafeUnknownRepresenter, self).represent_data(data)
        if tag:
            node.tag = tag
        return node

class SafeUnknownDumper(SafeUnknownRepresenter, yaml.dumper.SafeDumper):
    def __init__(self, stream,
            default_style=None, default_flow_style=False,
            canonical=None, indent=None, width=None,
            allow_unicode=None, line_break=None,
            encoding=None, explicit_start=None, explicit_end=None,
            version=None, tags=None, sort_keys=True):

        SafeUnknownRepresenter.__init__(self, default_style=default_style,
                default_flow_style=default_flow_style, sort_keys=sort_keys)

        yaml.dumper.SafeDumper.__init__(self,  stream,
                                        default_style=default_style,
                                        default_flow_style=default_flow_style,
                                        canonical=canonical,
                                        indent=indent,
                                        width=width,
                                        allow_unicode=allow_unicode,
                                        line_break=line_break,
                                        encoding=encoding,
                                        explicit_start=explicit_start,
                                        explicit_end=explicit_end,
                                        version=version,
                                        tags=tags,
                                        sort_keys=sort_keys)
