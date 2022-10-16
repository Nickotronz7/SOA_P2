def index1():
    return """
    
<html>
    <head>
        <style>
            input[type="file"] {
                display: none;
            }
            input[type="submit"] {
                display: none;
            }
        </style>
    </head>
    <body>
        <div style="background-color:#0066CC;" >
            <h1 style="color:white; text-align:center; font-family:Arial; font-weight: bold;">AddUI</h1>
        </div>
        <h2 style="text-align:center; font-family:Arial; font-weight: bold;">Por favor, agrega 10 im&aacutegenes para enviar</h2>
        <h3 style="text-align:center; font-family:Arial;">Im&aacutegenes agregadas:</h2>
        <div style= 'height:350px'>

"""


def index2():
    return"""
    </div>
        <form style='display: inline-block;' action = "http://localhost:5000/uploader" method = "POST" enctype = "multipart/form-data">
            <label style="color:white; font-family:Arial; background-color:#0066CC; padding: 10px; margin: 20px;">
                Seleccionar imagen
                <input type="file" name="file">
            </label>
            <label style="color:white; font-family:Arial; background-color:#0066CC; padding: 10px; margin: 20px;">
                Aceptar imagen
                <input type="submit">
            </label>
        </form>

        <form style='display: inline-block;' action = "http://localhost:5000/send_to_broker" method = "POST" enctype = "multipart/form-data" style="margin: 50px;" >
            <label style="color:white; font-family:Arial; background-color:#0066CC; padding: 10px; margin: 20px;">
                Enviar im&aacutegenes
                <input type="submit" name="file">
            </label>
        </form>
    </body>
</html>"""