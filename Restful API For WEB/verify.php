<?php

header('Access-Control-Allow-Origin:*');

    class Verify {
        private function getcookie(){
            $session = curl_init(); 
            $url = 'http://jwc.sdfmu.edu.cn/academic/common/security/login.jsp';
            curl_setopt($session, CURLOPT_URL,$url);
            curl_setopt($session, CURLOPT_HEADER, 1); 
            curl_setopt($session, CURLOPT_RETURNTRANSFER, true); 
            $content = curl_exec($session);  
            curl_close($session);
            list($header, $body) = explode("\r\n\r\n", $content); 
            preg_match("/set\-cookie:([^\r\n]*)/i", $header, $matches); 
            $temp = $matches[1];  
            preg_match_all('/JSESSIONID=[A-Za-z0-9=.]+/i', $temp, $cookie);
            return $cookie[0][0];
        }

        private function send_post($url, $cookie, $post_data) {
            $postdata = http_build_query($post_data);
            $options = array(
              'http' => array(
                'method' => 'POST',
                'header' => 'Content-type:application/x-www-form-urlencoded',
                'cookie' => $cookie,
                'content' => $postdata,
                'timeout' => 15 * 60 // 超时时间（单位:s）
              )
            );
            $context = stream_context_create($options);
            $result = file_get_contents($url, false, $context);
            return $result;
          }
        
    	private function encodeJson($responseData) {
        	$jsonResponse = json_encode($responseData);
        	return $jsonResponse;        
    		
    	}
    
        public function getimg(){
            $cookie = $this -> getcookie();
            $session = curl_init();
            $url = 'http://jwc.sdfmu.edu.cn/academic/getCaptcha.do';
            curl_setopt($session, CURLOPT_URL,$url);
            curl_setopt($session, CURLOPT_HEADER, 0); 
            curl_setopt($session, CURLOPT_COOKIE,$cookie);
            curl_setopt($session, CURLOPT_RETURNTRANSFER, true); 
            $content = curl_exec($session);
            curl_close($session);
            $tmpFile = tempnam(sys_get_temp_dir(), 'image');
            $resource = fopen($tmpFile, 'w');
            fwrite($resource,$content);
            fclose($resource);
            $md5FileName = md5_file($tmpFile);
            $returnFile = './image/' . $md5FileName . '.jpg';
            copy($tmpFile, $returnFile);
            @unlink($tmpFile);
            $returnFile = $md5FileName.'.jpg';
            $rawData = array('Cookie'=>$cookie,'img'=>$returnFile);
            $response = $this -> encodeJson($rawData);
            echo $response;
        }
        
        public function login($user,$pass,$code,$cookie,$img){
            $file = './image/'.$img;
            if (file_exists($file)){
                unlink($file);
            }
            $url = "http://jwc.sdfmu.edu.cn/academic/j_acegi_security_check";
            $ch = curl_init();
            $post_data = "j_username=".$user."&j_password=".$pass."&j_captcha=".$code;
            $headers = array(
                "content-type:application/x-www-form-urlencoded"
            );
            curl_setopt($ch,CURLOPT_URL,$url);
            curl_setopt($ch,CURLOPT_HTTPHEADER,$headers);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
            curl_setopt($ch, CURLOPT_COOKIE, $cookie);
            $content = curl_exec($ch);
            $header = curl_getinfo($ch);
            if ($header['redirect_url']=="http://jwc.sdfmu.edu.cn/academic/index_new.jsp"){
            	echo 'true';
            	curl_close($ch);
            	
            } else {
            	echo 'false';
            	curl_close($ch);
            }
            
        }
        
    }
    $do = "";
    if(isset($_GET["do"]))
        $do = $_GET["do"];

    switch($do){

        case 'code':
            $code = new Verify();
            $code -> getimg();
        break;

        case 'login':
            $user = $_GET['user'];
            $pass = urlencode($_GET['pass']);
            $code = $_GET['code'];
            $cookie = $_GET['cookie'];
            $img = $_GET['img'];
            $login = new Verify();
            $login -> login($user,$pass,$code,$cookie,$img);
        break;

        }
    
?>
