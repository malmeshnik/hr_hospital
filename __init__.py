from odoo.tools import config
from . import models, wizard

if config.get('test_enable'):
    from . import tests
