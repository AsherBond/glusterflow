GlusterFlow setup on Fedora 20

1. You need gluster 3.5 and python 2.7
On Fedora 20 these are both available through the official repos.
Python 2.7 should be installed by default. 
Yum-install all glusterfs packages including glusterfs-extra-xlators-3.5

2. Install Python and some additional packages
  $ yum -y install python-pip
  $ pip install logstash_formatter
  $ yum -y install git

3. You will need a webserver. We will use nginx for the instructions here but apache should work fine too.
  $ yum install nginx -y

4. Get elasticsearch and logstash RPMs from http://www.elasticsearch.org/overview/elkdownloads/

Install them: 
  $ yum localinstall *.rpm

You will also need to install openjdk, ruby and jruby packages
  $ yum -y install openjdk ruby jruby

5. Get GlusterFlow from github
  $ cd /root/src
  $ git clone https://github.com/justinclift/glusterflow

6. Install GlusterFlow logging translator:
  $ cp /root/src/glusterflow/translator/glusterflow.py /usr/lib64/glusterfs/3.5.0/xlator/features/glupy

7. Setup up GlusterFlow filters
  $ mkdir -p /usr/lib64/glusterfs/3.5.0/filter
  $ cp filter/glusterflowfilter.sh /usr/lib64/glusterfs/3.5.0/filter

If you have SElinux enabled follow the instructions in filter/README.md to set SELinux security context

8. Enable GlusterFlow logging translator
  $ gluster volume profile <vol-name> start
  $ gluster volume profile <vol-name> stop

9. Check whether logging works:
  $ more /var/log/glusterflow.log

10. Setup logstash
  $ cd /etc/logstash/conf.d
  $ rm -rf *.conf
  $ cp /root/src/glustergflow/logstash/logstash.conf .
  $ chown logstash:logstash logstash.conf
  $ mkdir -p /var/lib/logstash

11. Setup nginx:
  $ mkdir -p /var/log/nginx
  $ mkdir -p /usr/share/nginx/kibana/public
  $ mkdir -p /etc/nginx/sites-available
  $ mkdir -p /etc/nginx/sites-enabled
  $ rm -rf /etc/nginx/nginx.conf
  $ cp /root/src/glusterflow/nginx/nginx.conf /etc/nginx
  $ cp /root/src/glusterflow/kibana_dashboard/GlusterFS_Analytics.json   /usr/share/nginx/kibana/public/app/dashboards/
  $ cp /root/src/glusterflow/kibana/kibana /etc/nginx/sites-available

change the entry after "server_name" in file /etc/nginx/sites-available/kibana to match your server

  $ ln -s /etc/nginx/sites-available/kibana /etc/nginx/sites-enabled/kibana

12. Setup kibana
  $ cd /usr/share/nginx/kibana/public
  $ wget https://download.elasticsearch.org/kibana/kibana/kibana-latest.tar.gz
  $ tar xvzf kibana-latest.tar.gz
  $ mv kibana-latest/* .
  $ rm -rf kibana-latest kibana-latest.tar.gz

configure kibana:
  $ vi config.js
change the line "default_route: '/dashboard/file/default.json' to
"default_route: '/dashboard/file/GlusterFS_Analytics.json'

  $ useradd -s /sbin/nologin kibana
  $ chown -R kibana:nginx /usr/share/nginx/kibana

13. Fix SElinux and firewall
  $ chcon -R -t httpd_sys_content_t /usr/share/nginx/kibana/public
  $ semanage port -a -t http_port_t -p tcp 9200
  $ firewall-cmd --zone=public --add-service=http
  $ firewall-cmd --zone=public --add-port=9200/tcp
optional:
  $ firewall-cmd --zone=public --add-port=5544/tcp
  $firewall-cmd --zone=public --add-port=5544/udp

14. Start nginx and ELK
  $ systemctl enable elasticsearch.service; systemctl start elasticsearch.service
  $ systemctl enable logstash.service; systemctl start logstash.service
  $ systemctl enable nginx.service; systemctl start nginx.service

15. Finally open your web-browser and go to 'http://localhost'
It might take a couple of seconds until ELK has read and indexed the logfiles.

16. Troubleshooting:

Check whether elasticsearch and logstash are running

  $ ps -ax | grep -i logstash
  $ ps -ax | grep -i elasticsearch

In both cases you should see a java process with a very lots of arguments

Check whether logstash and elasticsearch are picking up the GlusterFlow logs and converts them

  $ ls -al /var/lib/logstash
There should be at least a file called 'sincedb' and a directory called 'data'

  $ find /var/lib/logstash/data
Should spit out lots of files with 'index' in their path.


