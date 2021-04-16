# SportAcus

Python v3.7.0

Activar el entorno de python donde se encuentran los paquetes instalados.

```bat
C:\home\SportAcus> Scripts\activate
(sportacus-env) C:\home\SportAcus>
```

Los paquetes están instalados, pero en el caso que no lo estén porque los haya eliminado el .gitignore
```bat
(sportacus-env) C:\home\SportAcus>pip install -r requirementes.txt
```

Por último, para ejecutar PADE.
```bat
(sportacus-env) C:\home\SportAcus>cd app
(sportacus-env) C:\home\SportAcus\app>cd src
(sportacus-env) C:\home\SportAcus\app>pade start-runtime --port 20000 main.py
```

Aparecerán inputs para introducir nombre de usuario y contraseña, usa la que pone ahí mismo "pade-user" y "12345", creo que no afecta en nada.