.. currentmodule:: {{ module }}

.. list-table:: {{ objname }}
   :header-rows: 1

   * - Class
     - Description
   {% for item in members %}
   * - :obj:`{{ item.name }} <{{ item.name }}>`
     - {{ item.docstring}}
   {% endfor %}
