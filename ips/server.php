<?php

    $porta = "8080";
    echo "Servidor Rodando: http://localhost:{$porta}";
    exec("php -S localhost:{$porta}");
