"""
URL para diagnóstico de login
"""

urlpatterns = [
    # ... URLs existentes ...
]

# Al final del archivo urls.py
def diagnóstico_login(request):
    """Mostrar diagnóstico de login en el navegador"""
    from usuarios.models import Usuario
    from django.contrib.auth import authenticate

    html = """
    <html>
    <head>
        <title>Diagnóstico de Login</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #f0f0f0; }
            .box { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #0066cc; }
            .ok { border-left-color: #28a745; }
            .error { border-left-color: #dc3545; }
            code { background: #f4f4f4; padding: 2px 5px; }
            h2 { color: #0066cc; }
        </style>
    </head>
    <body>
        <h1>🔍 DIAGNÓSTICO DE LOGIN</h1>
    """

    try:
        # Test 1: Usuarios
        users_count = Usuario.objects.count()
        html += f"""
        <div class="box ok">
            <h2>✅ Usuarios en BD</h2>
            <p>Total: <code>{users_count}</code> usuarios</p>
        """

        for u in Usuario.objects.all():
            html += f"<p>- <code>{u.username}</code> ({u.rol})</p>"
        html += "</div>"

        # Test 2: Ana martinez
        try:
            ana = Usuario.objects.get(username='ana_martinez')
            pwd_ok = ana.check_password('123456')
            auth_ok = authenticate(username='ana_martinez', password='123456')

            css_class = "ok" if pwd_ok and auth_ok else "error"
            html += f"""
            <div class="box {css_class}">
                <h2>✅ usuario ana_martinez</h2>
                <p>Existe: <code>SÍ</code></p>
                <p>Activo: <code>{ana.is_active}</code></p>
                <p>Password '123456' correcto: <code>{'SÍ' if pwd_ok else 'NO'}</code></p>
                <p>Autenticación funciona: <code>{'SÍ' if auth_ok else 'NO'}</code></p>
            </div>
            """
        except:
            html += """
            <div class="box error">
                <h2>❌ Usuario ana_martinez NO existe</h2>
            </div>
            """

        html += """
        </body>
        </html>
        """

        from django.http import HttpResponse
        return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"<h1>Error: {e}</h1>")

