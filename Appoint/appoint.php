<?php

require_once 'TCloudAutoLoader.php';
use TencentCloud\Common\Credential;
use TencentCloud\Common\Profile\ClientProfile;
use TencentCloud\Common\Profile\HttpProfile;
use TencentCloud\Common\Exception\TencentCloudSDKException;
use TencentCloud\Sms\V20190711\SmsClient;
use TencentCloud\Sms\V20190711\Models\SendSmsRequest;
//当天五点执行


class Appoint {
	
	private function get_Token($studentid){
        $session = curl_init();
        $password = md5($studentid);
        $durl = "http://202.194.232.138:85/api.php/login?from=mobile&password=".$password."&username=" .$studentid ;
        curl_setopt($session,CURLOPT_URL,$durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $output = json_decode(curl_exec($session),true);
        $Token = $output['data']['_hash_']['access_token'];
        curl_close($session);
        return $Token;
    }

    private function get_Segment($area){
    	$session = curl_init();
        $today=strtotime("today");
        $day=date("Y-m-d", $today);
        $durl = "http://202.194.232.138:85/api.php/space_time_buckets/?area=".$area."&day=".$day ;
        curl_setopt($session,CURLOPT_URL,$durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $output = json_decode(curl_exec($session),true);
        curl_close($session);
        return $output['data']['list'][0]['bookTimeId'];
    }
    
    
	private function a2s($sacii){
        $asc_arr= str_split(strtolower($sacii),2);
        $str='';
        for($i=0;$i<count($asc_arr);$i++){
            $str.=chr(hexdec($asc_arr[$i][1].$asc_arr[$i][0]));
        }
        return mb_convert_encoding($str,'UTF-8','GB2312');
	}
    
    public function Subscirbe($studentid,$area,$seat){
    	$token = $this->get_Token($studentid);
        $Segment = $this->get_Segment($area);
        $payload = array('access_token'=>$token,'userid'=>$studentid,'id'=>$seat,'segment'=>$Segment,'type'=>'1');
        $session = curl_init();
        $durl = "http://202.194.232.138:85/api.php/spaces/".$seat."/book";
        curl_setopt($session, CURLOPT_URL, $durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_POST, true);
        curl_setopt($session, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $status = curl_exec($session);
        $status = json_decode($status,true);
        curl_close($session);
        return $status['status'];
    }

    public function Sendsms($phone,$studentid,$area,$seat){
        try {
            $cred = new Credential("***********", "***************");//TenCloud API
            $httpProfile = new HttpProfile();
            $httpProfile->setEndpoint("sms.tencentcloudapi.com");
              
            $clientProfile = new ClientProfile();
            $clientProfile->setHttpProfile($httpProfile);
            $client = new SmsClient($cred, "ap-shanghai", $clientProfile);
        
            $req = new SendSmsRequest();
            
            $params = '{"PhoneNumberSet":["'.$phone.'"],"TemplateID":"550192","Sign":"阿盘的学习日记","TemplateParamSet":["'.$studentid.'","'.$area.'","'.$seat.'"],"SmsSdkAppid":"1400329913"}';
            $req->fromJsonString($params);
            $resp = $client->SendSms($req);
        }
        catch(TencentCloudSDKException $e) {
            echo $e;
        }
    }

    public function SendQQ($qq,$studentid,$area,$seat){
    	$session = curl_init();
        $today_temp=strtotime("today");
        $today=date("Y-m-d", $today_temp);
        $message = "今天是：".$today."，学号：".$studentid."，已经预约成功至第".$area."书库的第".$seat."座位，请于八点半之前进行签到 [请勿回复 Notify-Bot]";
        $user_id = $qq;
        $post_data = array(
		  'user_id' => $user_id,
		  'message' => $message
		);
        $url = "http://api.radiology.link:5700/send_private_msg";
        $this->send_post($url, $post_data);
    }
    
    public function send_post($url, $post_data) {
        $postdata = http_build_query($post_data);
        $options = array(
          'http' => array(
            'method' => 'POST',
            'header' => 'Content-type:application/x-www-form-urlencoded',
            'content' => $postdata,
            'timeout' => 15 * 60 // 超时时间（单位:s）
          )
        );
        $context = stream_context_create($options);
        $result = file_get_contents($url, false, $context);
        return $result;
      }
	
}


	$server = "localhost";
	$dbuser = "Radiology-Library";
	$dbpass = "Radiology-Library";
	$dbname = "Library";
    $conn = new mysqli($server, $dbuser, $dbpass, $dbname);
    $stmt = $conn -> prepare("SELECT `studentid`,`area`,`seat`,`phone`,`qq` FROM `user` WHERE `seat` is NOT NULL AND `datepicker`=?");
    $today_temp=strtotime("today");
    $today=date("Y-m-d", $today_temp);
    $stmt -> bind_param("s",$today);
    $stmt->execute();
    $stmt->bind_result($studentid,$area,$seat,$phone,$qq);
    while ($stmt->fetch()){
    	$appoint = new Appoint();
        if($appoint->Subscirbe($studentid,$area,$seat)){
        	$appoint->Sendsms($phone,$studentid,$area,$seat);
        	$appoint->SendQQ($qq,$studentid,$area,$seat);
        } else {
        	$appoint->Sendsms($phone,$studentid,'预约错误','预约错误');
        	$appoint->SendQQ($qq,$studentid,'预约错误','预约错误');
        }
    }
    $stmt = $conn -> prepare("UPDATE `user` SET `seat`=NULL,`area`=NULL,`datepicker`=NULL WHERE `seat` IS NOT NULL AND `datepicker`=?");
    $stmt ->bind_param("s",$today);
    $stmt->execute();
?>