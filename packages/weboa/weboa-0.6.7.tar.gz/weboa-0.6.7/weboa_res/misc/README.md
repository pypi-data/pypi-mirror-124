### Change ToDo:
> 1. php/db.php
> 2. /favicon.ico/
> 3. /img/favicon.png
> 4. /img/sn_share.png

----  

### Nginx config  
```
location / {  
     try_files $uri $uri/ /index.php?$args;  
}  
```