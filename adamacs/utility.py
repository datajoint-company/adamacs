import importlib
import inspect
import json
import rspace_client as rc
import os

from adamacs.schemas import subject, surgery, session, behavior, imaging, scan

_linking_module = None

# Note that order matters when activating
module_list = [subject, surgery, session, behavior, scan, imaging]


def activate(schema, schema_name, create_schema=True, create_tables=True,
             linking_module=None):
    """
    activate(schema_name, create_schema=True, create_tables=True, linking_module=None)
    :param schema_name: schema name on the database server to activate
    :param create_schema: when True (default), create schema if it does not yet exist.
    :param create_tables: when True (default), create tables if they do not yet exist.
    :param linking_module: a module name or a module containing the
     required dependencies to activate the `subject` element:
         Upstream tables:
            + Source: the source of the material/resources (e.g. allele, animal)
                      typically refers to the vendor (e.g. Jackson Lab - JAX)
            + Lab: the lab for which a particular animal belongs to
            + Protocol: the protocol applicable to a particular animal (e.g. IACUC, IRB)
            + User: the user associated with a particular animal
    """
    if isinstance(linking_module, str):
        linking_module = importlib.import_module(linking_module)
    assert inspect.ismodule(linking_module), \
        "The argument 'dependency' must be a module's name or a module"

    schema.activate(schema_name, create_schema=create_schema,
                    create_tables=create_tables, add_objects=linking_module.__dict__)

    
def activate_many(schemas=module_list, name='default_schema'):
    """
    Activate multiple schemas. By default activates all schemas in utility.module_list
    """
    for module in module_list:
        module.schema.activate('tutorial', create_schema=True, create_tables=True)
        # activate(schema, create_schema=True, create_tables=True,
        #          schema_name='tutorial', linking_module=schema)


def rspace_connect():
    # Ask admin to get you the local_conf file
    local_dir = os.path.dirname(__file__)
    with open(os.path.join(local_dir, 'rspace_local_conf.json')) as jsonFile:
        local_conf = json.load(jsonFile)

    # client = rc.Client(local_conf['server'], local_conf['apiKey'])
    # client.get_document('SD37310')
    return rc.Client(local_conf['server'], local_conf['apiKey'])
