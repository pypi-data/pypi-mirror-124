## Jinja2 addons

### Example usage:

```
from jinja2 import Environment

from vtb_jinja2_addons import VTB_FILTERS, VTB_EXTENSIONS

env = Environment(extensions=VTB_EXTENSIONS, enable_async=True)
env.filters = VTB_FILTERS
template = env.from_string('{{uuidgen()}}')
rendered_config = template.render()
```
