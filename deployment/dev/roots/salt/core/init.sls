pip.conf:
 file:
   - managed
   - name: /home/vagrant/.pip/pip.conf
   - source: salt://files/pip.conf
   - makedirs: True


bashfiles:
 file:
   - managed
   - name: /home/vagrant/.bash_aliases
   - source: salt://files/bash_aliases
   - makedirs: True