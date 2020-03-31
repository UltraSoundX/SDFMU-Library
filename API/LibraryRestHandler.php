<?php 
//login book unbook register
require_once("BasedRest.php");



 
class LibraryRestHandler extends SimpleRest {
	
	private $server = "localhost";
	private $dbuser = "Radiology-Library";
	private $dbpass = "Radiology-Library";
	private $dbname = "Library";
 
    public function login($username,$password) {  
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
        $stmt = $conn->prepare("SELECT * FROM user WHERE studentid =? AND password=?");
        $stmt ->bind_param("ss", $username, $password);
        $stmt->execute();
        $stmt->store_result();
        if ($stmt->num_rows) {
            $rawData = array ('msg'=>'Login');
            $response = $this->encodeJson($rawData);
            echo $response;
        } else {
        	$rawData = array ('msg'=>'UserError');
            $response = $this->encodeJson($rawData);
            echo $response;
        }
    }
    
    public function register($username,$password,$invite) {
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
		if (mysqli_connect_errno($con)) {
		    $statusCode = 500;//Internal server error
		    $this ->setHttpHeaders($statusCode);
		}
        $stmt = $conn->prepare("SELECT * FROM `invitecode` WHERE `invite`=?");
        $stmt ->bind_param("s", $invite);
        $stmt->execute();
        $stmt->store_result();
        if ($stmt->num_rows){
            $stmt_create = $conn->prepare("INSERT INTO `user`(`studentid`, `password` , `invite`) VALUES (?,?,?)");
            $invitecode = $this->invite($username);
            $stmt_create ->bind_param("sss", $username,$password,$invitecode);
            if ($stmt_create->execute()){//创建用户 /
                $stmt_invite = $conn->prepare("INSERT INTO `invitecode`(`invite`) VALUES (?)");
                $stmt_invite ->bind_param("s", $invitecode);
                $stmt_invite->execute();//邀请码入库 /
                
                if ($invite == "fighting"){
	                $rawData = array ('msg'=>'Reg');
		            $response = $this->encodeJson($rawData);
		            echo $response;	
                } else {
                	
                $stmt_del = $conn->prepare("DELETE FROM `invitecode` WHERE `invite`=?");
                $stmt_del ->bind_param("s", $invite);
                $stmt_del ->execute();//删除邀请码 /
                
                $stmt_change = $conn -> prepare("UPDATE `user` SET `invite`='已邀请' WHERE `invite`=?");
                $stmt_change ->bind_param("s", $invite);
                $stmt_change ->execute();
                
	            $rawData = array ('msg'=>'Reg');
	            $response = $this->encodeJson($rawData);
	            echo $response;
	            
                }

            } else {
                $rawData = array ('msg'=>'UserError');
	            $response = $this->encodeJson($rawData);
	            echo $response;
            } 
        } else {
        	$rawData = array ('msg'=>'RegError');
	        $response = $this->encodeJson($rawData);
	        echo $response;
        }
    }

    public function check($username){//登录之后执行
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
        $stmt = $conn->prepare("SELECT studentid,area,seat,invite,phone,datepicker,qq FROM user WHERE studentid=?");
        $stmt ->bind_param("s", $username);
        $stmt->execute();
        $stmt->bind_result($studentid, $area, $seat, $invite, $phone, $datepicker, $qq);
        $stmt -> fetch();
        $rawData = array('username'=>$studentid, 'area' => $area, 'seat' => $seat, 'invite'=> $invite, 'date'=>$datepicker, 'phone'=>$phone, 'qq'=>$qq);
        $response = $this->encodeJson($rawData);
        echo $response;
    }

    public function book($username,$seat,$area,$dateselect){
        $conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
        $presql = "SELECT * FROM `user` WHERE `seat`=? AND `datepicker`=?";
        $prestmt = $conn->prepare($presql);
        $prestmt -> bind_param("ss",$seat,$dateselect);
        $prestmt -> execute();
        $prestmt->store_result();
        if($prestmt->num_rows){
            $rawData = array('msg'=>'Booked');
        	$response = $this->encodeJson($rawData);
        	echo $response;
        } else {
            $sql = "UPDATE `user` SET `seat`= ?,`area`=?,`datepicker`=? WHERE `studentid`= ?";
            $stmt = $conn->prepare($sql);
            $stmt -> bind_param("ssss",$seat,$area,$dateselect,$username);
            $stmt -> execute();
            $rawData = array('msg'=>'Booking');
        	$response = $this->encodeJson($rawData);
        	echo $response;
        }
    }

    public function unbook($username){
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
    	$sql = "UPDATE `user` SET `seat`= NULL,`area`=NULL,`datepicker`=NULL WHERE `studentid`= ?";
        $stmt = $conn->prepare($sql);
        $stmt -> bind_param("s",$username);
        if ($stmt->execute()){
        	$rawData = array('msg'=>'UnBook');
        	$response = $this->encodeJson($rawData);
        	echo $response;
        } 
    }

    public function encodeJson($responseData) {
        $jsonResponse = json_encode($responseData);
        return $jsonResponse;        
    }
    
    public function phone($studentid,$phone){
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
    	$sql = "UPDATE `user` SET `phone`=? WHERE `studentid`=?";
        $stmt = $conn->prepare($sql);
        $stmt -> bind_param("ss",$phone,$studentid);
        if ($stmt->execute()){
        	$rawData = array('msg'=>'Phone');
        	$response = $this->encodeJson($rawData);
        	echo $response;
        } 
    }
    
    public function qq($studentid,$qq){
    	$conn = new mysqli($this->server, $this->dbuser, $this->dbpass, $this->dbname);
    	$sql = "UPDATE `user` SET `qq`=? WHERE `studentid`=?";
        $stmt = $conn->prepare($sql);
        $stmt -> bind_param("ss",$qq,$studentid);
        if ($stmt->execute()){
        	$rawData = array('msg'=>'QQ');
        	$response = $this->encodeJson($rawData);
        	echo $response;
        } 
    }
    
    public function status(){
    	$session = curl_init();
        $durl = "http://api.radiology.link:5700/get_status" ;
        curl_setopt($session,CURLOPT_URL,$durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $output = json_decode(curl_exec($session),true);
        curl_close($session);
        echo $output['data']['good'];
    }
    

    public function invite($username) { //邀请码
        static $source_string = 'E5FCDG3HQA4B1NOPIJ2RSTUV67MWX89KLYZ';
        $num = $username;
        $code = '';
        while ( $num > 0) {
            $mod = $num % 35;
            $num = ($num - $mod) / 35;
            $code = $source_string[$mod].$code;
        }
        if(empty($code[3]))
            $code = str_pad($code,4,'0',STR_PAD_LEFT);
        return $code;
        }
    
    public function now($username,$area) {
        $session = curl_init();
        $appoint = new Appoint();
        $Segment = $appoint -> get_Segment($area);
        $startTime = $appoint -> get_Starttime($area);
        $today=strtotime("today");
        $day=date("Y-m-d", $today);
        $durl = "http://202.194.232.138:85/api.php/spaces_old/?area=".$area."&segment=".$Segment."&day=".$day."&startTime=".$startTime."&endTime=21:20";
        curl_setopt($session,CURLOPT_URL,$durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $output = json_decode(curl_exec($session),true);
        $output = $output['data']['list'];
       if(is_array($output)) {
            foreach ($output as $list ) {
                $seat = $list['id'];
                $status = $list['status_name'];
                if ($status == '空闲'){
                    $Subcribe = $appoint -> Subscirbe($username,$area,$seat);
                    if($Subcribe){
                        $msg = array('area'=>$area, 'seat'=>$seat);
                        $response = $this -> encodeJson($msg);
                        echo $response;
                        exit ;
                    } else {
                        $msg = array('msg'=>'Error');
                        $response = $this -> encodeJson($msg);
                        echo $response;
                        exit ;
                    }
                }
            }
        } else {
            $msg = array('msg'=>'Error');
            $response = $this -> encodeJson($msg);
            echo $response;
        }
    }
}

class Appoint {
    public function get_Segment($area){
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

    public function get_Starttime($area){
    	$session = curl_init();
        $today=strtotime("today");
        $day=date("Y-m-d", $today);
        $durl = "http://202.194.232.138:85/api.php/space_time_buckets/?area=".$area."&day=".$day ;
        curl_setopt($session,CURLOPT_URL,$durl);
        curl_setopt($session, CURLOPT_HEADER, false);
        curl_setopt($session, CURLOPT_RETURNTRANSFER, 1);
        $output = json_decode(curl_exec($session),true);
        curl_close($session);
        return $output['data']['list'][0]['startTime'];
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
}

?>