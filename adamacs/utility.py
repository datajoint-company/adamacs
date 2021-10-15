import importlib
import inspect
import datajoint as dj
import scipy.io as sio


def activate(schema, schema_name, create_schema=True, create_tables=True, linking_module=None):
    """
    activate(schema_name, *, create_schema=True, create_tables=True, linking_module=None)
        :param schema_name: schema name on the database server to activate the `subject` element
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
        :param linking_module: a module name or a module containing the
         required dependencies to activate the `subject` element:
             Upstream tables:
                + Source: the source of the material/resources (e.g. allele, animal) - typically refers to the vendor (e.g. Jackson Lab - JAX)
                + Lab: the lab for which a particular animal belongs to
                + Protocol: the protocol applicable to a particular animal (e.g. IACUC, IRB)
                + User: the user associated with a particular animal
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), "The argument 'dependency' must be a module's name or a module"

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables, add_objects=linking_module.__dict__)
    

def load_bpod_file(file_path):
    mat = sio.loadmat(file_path)