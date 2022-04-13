<?php

require "./funcoes.php";

$response = new stdClass();

$dados = (object) $_POST;

$funcoes = new Funcoes($dados->ip, $dados->mascara);

//Bloco para bits

//Fim bloco bits

//classe
$classe_ip = $funcoes->get_classe_ip();

//tipo de ip
$tipo_ip = $funcoes->get_tipo_ip();

$sub_rede = $funcoes->get_subrede();

$endereco_da_rede = $funcoes->get_endereco_de_rede();

$broadcast = $funcoes->get_broadcast();

if($broadcast == $endereco_da_rede){
    $broadcast = "-";
}

$ips_disponiveis = $funcoes->get_qtd_ips();

$txt_intervalo_hosts = "-";

if($ips_disponiveis->ips_validos != 0){

    $hosts = $funcoes->get_intervalo_hosts_validos();

    $txt_intervalo_hosts = "{$hosts->inicio} - {$hosts->fim}";
}

$html = "<table class=\"table\" style=\"width:100%;\">
            <thead class=\"thead-dark\">
                <tr>
                    <th scope=\"col\">IP</th>
                    <th scope=\"col\">Classe</th>
                    <th scope=\"col\">Tipo</th>
                    <th scope=\"col\">Endereço da Rede</th>
                    <th scope=\"col\">Mascara da Sub-Rede</th>
                    <th scope=\"col\">Broadcast</th>
                    <th scope=\"col\">Intervalo de Hosts Válidos</th>
                    <th scope=\"col\">Quantidade de IPs Disponíveis</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th class=\"text-center\">{$dados->ip}/{$dados->mascara}</th>
                    <th class=\"text-center\">{$classe_ip}</th>
                    <th class=\"text-center\">{$tipo_ip}</th>
                    <th class=\"text-center\">{$endereco_da_rede}</th>
                    <th class=\"text-center\">{$sub_rede}</th>
                    <th class=\"text-center\">{$broadcast}</th>
                    <th class=\"text-center\">{$txt_intervalo_hosts}</th>
                    <th class=\"text-center\">Rede: {$ips_disponiveis->ips_rede} - Válidos: {$ips_disponiveis->ips_validos}</th>
                </tr>
            </tbody>
        </table>";

echo json_encode(["error" => false, "tabela" => $html]);