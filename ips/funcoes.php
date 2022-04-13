<?php

class Funcoes
{

    public $ip;
    public $mascara;

    public $bits_ip;
    public $bits_rede;

    public function __construct($ip, $mascara)
    {

        $this->ip = $ip;
        $this->mascara = $mascara;

        $this->valida_ip();
        
        $this->bits_ip = $this->get_bits_ip();

        $this->bits_rede = $this->get_bits_rede();
    }

    public function valida_ip()
    {

        if (empty($this->ip)) {

            $this->throw_err("IP não digitado");
        }

        $exp_ip = $this->arr_ip($this->ip);

        if (count($exp_ip) != 4) {

            $this->throw_err("IP inválido");
        }

        foreach ($exp_ip as $octeto => $num) {

            if ($num < 0) {
                $this->throw_err("Erro ao validar {$octeto}° octeto");
            }

            if ($num > 255) {
                $this->throw_err("O número deve ser entre 0 e 255 ({$octeto}° octeto)");
            }
        }
    }

    public function get_bits_rede(){

        $bits = [];

        $bits_restantes_mascara = $this->mascara;

        for ($i = 1; $i <= 4; $i++) {

            $utilizado = 0;

            if ($bits_restantes_mascara < 8) {
                $utilizado = $bits_restantes_mascara;
            } else {
                $utilizado = 8;
            }
            
            $bits_restantes_mascara -= 8;
            
            if($bits_restantes_mascara <= 0){
                $bits_restantes_mascara = 0;
            }
            
            $bits[] = $this->get_octeto($utilizado);
        }

        return $bits;
    }

    public function get_bits_ip(){

        $bits = [];

        $arr = $this->arr_ip();

        foreach($arr as $numero){

            $binario = str_pad(decbin($numero), 8, "0", STR_PAD_LEFT);

            $bits[] = str_split($binario);

        }

        return $bits;

    }

    public function get_octeto($qtd_utilizada = 0)
    {

        $octeto = [];

        for ($i = 1; $i <= $qtd_utilizada; $i++) {
            $octeto[] = 1;
        }

        if ($qtd_utilizada < 8) {
            $qtd_restante = 8 - $qtd_utilizada;

            for ($i = 1; $i <= $qtd_restante; $i++) {
                $octeto[] = 0;
            }
        }

        return $octeto;
    }

    public function arr_ip($ip = null)
    {
        if(empty($ip)){
            $ip = $this->ip;
        }

        return explode(".", $ip);
    }

    public function get_classe_ip()
    {

        $exp_ip = $this->arr_ip();

        $primeiro_octeto = (int) $exp_ip[0];

        $classe = "";

        if ($primeiro_octeto <= 126) {
            $classe = "A";
        } else if ($primeiro_octeto <= 191) {
            $classe = "B";
        } else if ($primeiro_octeto <= 223) {
            $classe = "C";
        } else if ($primeiro_octeto <= 239) {
            $classe = "D";
        } else {
            $classe = "E";
        }

        return $classe;
    }

    public function get_tipo_ip()
    {

        $exp_ip = $this->arr_ip();

        if ($exp_ip[0] == 10) {
            return "Privado";
        }

        if ($exp_ip[0] == 172) {
            if ($exp_ip[1] >= 16 && $exp_ip[1] <= 31) {
                return "Privado";
            }
        }

        if ($exp_ip[0] == 192 && $exp_ip[1] == 168) {
            return "Privado";
        }

        return "Público";
    }

    public function get_subrede(){

        $sub_rede = [];

        foreach($this->bits_rede as $bits){
            $str_bits = implode("", $bits);

            $sub_rede[] = bindec($str_bits);

        }

        return implode(".", $sub_rede);

    }

    public function get_endereco_de_rede(){

        $bits_final = [];

        for ($i=0; $i <= 3; $i++) { 
            
            $conjunto = [];

            $bits_ip = $this->bits_ip[$i];
            $bits_subrede = $this->bits_rede[$i];

            for ($pos=0; $pos < 8; $pos++) { 
                if($bits_ip[$pos] == 1 && $bits_subrede[$pos] == 1){
                    $conjunto[] = 1;
                }else{
                    $conjunto[] = 0;
                }
            }

            $bits_final[] = $conjunto;

        }

        $retorno = [];

        foreach($bits_final as $bits){

            $retorno[] = bindec(implode("", $bits));

        }

        return implode(".", $retorno);

    }

    public function get_broadcast(){

        $endereco_rede = $this->get_endereco_de_rede();
        
        $bits = [];

        $arr = $this->arr_ip($endereco_rede);

        foreach($arr as $numero){

            $binario = str_pad(decbin($numero), 8, "0", STR_PAD_LEFT);

            $bits[] = str_split($binario);

        }

        $bit_ip = "";

        foreach($bits as $arr_bit){
            $bit_ip .= implode("", $arr_bit);
        }

        $bits_fixos_rede = substr($bit_ip, 0, $this->mascara);

        $binario_completo = str_pad($bits_fixos_rede, 32, "1", STR_PAD_RIGHT);

        $binario = rtrim(chunk_split($binario_completo, 8, "."),".");

        $arr_bin = explode(".", $binario);

        $broadcast = [];

        foreach($arr_bin as $_bin){

            $broadcast[] = bindec($_bin);

        }

        return implode(".", $broadcast);

    }

    public function get_qtd_ips(){

        $bits = 32 - $this->mascara;

        $ips_totais = pow(2, $bits);

        $ips_validos = $ips_totais - 2;

        if($ips_validos <= 2){
            $ips_validos = 0;
        }

        return (object) [
            "ips_rede" => $ips_totais,
            "ips_validos" => $ips_validos
        ];

    }

    public function get_intervalo_hosts_validos(){

        $endereco_rede = $this->arr_ip($this->get_endereco_de_rede());
        $broadcast = $this->arr_ip($this->get_broadcast());

        $ultimo_octeto_rede = str_split(strrev(str_pad(decbin($endereco_rede[3]), 8, "0", STR_PAD_LEFT)));
        $ultimo_octeto_broadcast = str_split(strrev(str_pad(decbin($broadcast[3]), 8, "0", STR_PAD_LEFT)));

        $ultimo_octeto_rede_novo = bindec(strrev(implode("", $this->substituir_bit($ultimo_octeto_rede, "0", "1"))));
        $ultimo_octeto_broadcast_novo = bindec(strrev(implode("", $this->substituir_bit($ultimo_octeto_broadcast, "1", "0"))));

        $endereco_rede[3] = (string) $ultimo_octeto_rede_novo;
        $broadcast[3] = (string) $ultimo_octeto_broadcast_novo;

        return (object)[
            "inicio" => implode(".",$endereco_rede),
            "fim" => implode(".",$broadcast)
        ];

    }

    private function substituir_bit($arr_bits, $procurando, $trocar_por){

        foreach($arr_bits as $posicao => $bit){
            if($bit == $procurando){
                $arr_bits[$posicao] = $trocar_por;
                break;
            }
        }

        return $arr_bits;

    }

    public function throw_err($msg = "Não definido")
    {

        die(json_encode(["error" => true, "msg" => $msg]));
    }

}
