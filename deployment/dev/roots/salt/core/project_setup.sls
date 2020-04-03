{% set src = pillar['src'] %}
{% set bin_env = pillar['bin_env'] %}
{% set settings = pillar['settings'] %}


python-packages:
 pip.installed:
    - requirements: /vagrant/src/requirements.txt
    - bin_env: /usr/bin/pip3
    - use_wheel: False

create-env:
 file.managed:
   - name: {{ src }}.env
   - source: salt://files/env.jinja
   - template: jinja
   - context:
        settings: {{ settings }}


migrate-database:
  module.run:
    - name: django.command
    - command: migrate
    - settings_module: {{ settings }}
    - pythonpath: {{ src }}


loaddata:
  module.run:
    - name: django.command
    - command: loaddata templates
    - settings_module: {{ settings }}
    - pythonpath: {{ src }}