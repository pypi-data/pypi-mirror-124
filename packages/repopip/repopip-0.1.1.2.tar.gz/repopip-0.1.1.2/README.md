# Guía de uso

Con esta aplicación puedes tener un repositorio local de paquetes de python. Todo lo que tienes que hacer es descargar el paquete que desees e iniciar el servidor, así ahorraras ancho de banda y datos de internet.

## Instalacíon:

   ``` 
   $ pip install repopip
   ```

## Uso:

- Tienes que **descargar** el paquete del repositorio oficial `pip download [package_name]`.
- Copia el paquete a la carpeta **%HOME%/.static/simple**.
- Inicia el servidor `python -m repopip`. Este comando iniciara el servidor en http://127.0.0.1:5000/.
- Comienza a usar tu servidor. `pip install --index-url="http://127.0.0.1:5000/simple/" [package_name]`.
- Puedes configurar pip copiado las lineas siguiente en una de las siguientes ubicaciones y el paso anterior seria tan simlpe como pip install [package_name]:

   - **Global:** C:\ProgramData\pip\pip.ini
   - **User:** %APPDATA%\pip\pip.ini o con la opcion antigua %HOME%\pip\pip.ini
   - **Site:** %VIRTUAL_ENV%\pip.ini

    ```
    [global]
    index-url=http://127.0.0.1:5000/simple/
    ```

- También se puede usar remmotamente, solo necesitas saber la dirección donde esta alojado el servidor `pip install --index-url="http://direccion_de_dominio_o_ip/simple/" [package_name]` además de poderse configurar como el paso anterior
    - En futuras versiones haremos el proceso de configuración más facil.