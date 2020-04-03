{{ pillar['db_username'] }}:
 postgres_user:
  - present
  - password: {{ pillar['db_user_password'] }}

{{ pillar['db_name'] }}:
  postgres_database:
  - present
  - owner: {{ pillar['db_username'] }}

/etc/postgresql/9.5/main/pg_hba.conf:
  file.replace:
    - pattern: ^local\s+all\s+all\s+peer$
    - repl: |
        local   all             all                                     md5

/etc/postgresql/9.5/main/postgresql.conf:
  file.replace:
    - pattern: ^#listen_addresses\s=\s\'localhost\'
    - repl: listen_addresses = '*'
    - count: 1
    - append_if_not_found: True

postgresql:
   service.running:
     - name: postgresql
     - enable: True
     - watch:
        - file:  /etc/postgresql/9.5/main/postgresql.conf
        - file:  /etc/postgresql/9.5/main/pg_hba.conf
