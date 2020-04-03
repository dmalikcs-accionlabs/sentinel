{% set packages = pillar['packages'] %}

postgresql-repo:
 file:
   - managed
   - name: /etc/apt/sources.list.d/pgdg.list
   - source: salt://files/pgdg.list
   - makedirs: True


install-postgresql-certificate:
  pkg:
   - installed
   - pkgs:
      - wget
      - ca-certificates
      - curl
  cmd:
   - run
   - name: 'wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -'


install-nodejs:
  cmd:
    - run
    - name: 'wget -qO- https://deb.nodesource.com/setup_7.x | sudo bash -'


core-software:
  pkg:
  - installed
  - pkgs:
      {% for package in packages %}
      - {{ package }}
      {% endfor %}