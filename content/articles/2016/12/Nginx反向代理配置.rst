:title: Nginx反向代理配置
:author: moore
:date: 2016-12-28 11:17:52
:modified: 2017-01-24 17:09:16
:category: Tutorial
:tags: Nginx
:slug: Nginx反向代理配置
:summary: Nginx反向代理配置参数分析
:status: draft


配置文件
========

.. code-block:: nginx

    http {
        server {
            #侦听的80端口
            listen       80;
            server_name  wp.mojia.date;
            location / {
                proxy_pass                 http://www.foo.com;
                #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
                #proxy_set_header           Host $host;
                proxy_set_header           X-Real-IP $remote_addr;
                proxy_set_header           X-Forwarded-For $proxy_add_x_forwarded_for;
            }
        }
    }

    events {
        worker_connections  1024;  # Default: 1024
    }
