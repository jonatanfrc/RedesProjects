<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>

<style>
    #barra {
        margin-top: 25px;
        font-size: 30px;
        font-weight: bold;
    }

    .mt-15{
        margin-top:15px;
    }

    .mt-30{
        margin-top:30px;
    }

    #msgErro{
        display:none;
        font-weight: bold;
        color: #ff3e3e;
        font-family: cursive;
        font-size: 14px;
    }
</style>

<body>
    <div class="container-fluid">
        <div class="jumbotron" style="margin-top:15px">
            <div class="row">
                <div class="col-md-1"></div>
                <div class="col-md-10">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="form-group">
                                <label for="txtIP">Endereço de IP</label>
                                <input type="text" class="form-control" id="txtIP" value="192.168.0.1">
                            </div>
                        </div>
                        <span id="barra">/</span>
                        <div class="col-md-2">
                            <div class="form-group">
                                <label for="cmbMascara">Mascara</label>
                                <select class="form-control" id="cmbMascara">
                                    <?php
                                        for ($i=8; $i <= 32; $i++) {
                                            echo "<option value=\"{$i}\">{$i}</option>";
                                        }
                                    ?>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <button data-loading="Calculando..." id="btnCalcular" class="btn btn-success mt-30">
                                Calcular
                            </button>
                        </div>
                    </div>
                    <span id="msgErro"></span>
                    <div id="response_table"></div>
                </div>
            </div>
        </div>
    </div>

    
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js"  crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" crossorigin="anonymous"></script>
    <script>

        const base_url = "http://localhost:8080/";

        $(document).ready(function(){

            $("#cmbMascara").val("24").change();

            $('#btnCalcular').click(function(){
                
                $("#msgErro").html("").hide();

                var btn = $(this);

                loadButton(btn, "Calculando...");

                var ip = $("#txtIP").val();
                var mascara = $("#cmbMascara").val();

                $.post(`${base_url}calculo_ips.php`,{ip, mascara}, function(data){
                    
                    loadButton(btn, "Calcular", false);
                    if(data.error){
                        $("#msgErro").html(`Erro: ${data.msg}`).show();
                        return;
                    }

                    $("#response_table").html(data.tabela);

                }, 'json');

            });

        });

        function loadButton(obj, text = "Aguarde...", loading = true){

            obj.html(text);
            if(loading){
                obj.addClass("disabled");
            }else{
                obj.removeClass("disabled");
            }

        }

    </script>

</body>

</html>