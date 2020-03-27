<?php
// api.radiology.link/library/?do= /
require_once("LibraryRestHandler.php");     
header('Access-Control-Allow-Origin:*');
$do = "";
if(isset($_GET["do"]))
    $do = $_GET["do"];
/*
 * RESTful service 控制器
 * URL 映射 Version 0.3
*/

switch($do){
 
    case "login":
        // 处理 Login /
        $username = $_GET["username"];
        $password = $_GET["password"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler->login($username,$password);
        break;

    case "register":
        // 处理 Register /
        $username = $_GET["username"];
        $password = $_GET["password"];
        $invite = $_GET["invite"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler->register($username,$password,$invite);
        break;
    
    case "check":
        // 处理 座位检查
        $username = $_GET["username"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler->check($username);
    break;
        
    case "book":
        // 处理 座位预定 /
        $seat = $_GET["seat"];
        $username = $_GET["username"];
        $area = $_GET["area"];
        $dateselect = $_GET["date"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler->book($username,$seat,$area,$dateselect);
    break;
 
    case "unbook" :
        // 处理 座位退订
        $username = $_GET["username"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler->unbook($username);
    break;
    
    case "invite" :
        $username = $_GET["studentid"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler -> invite($username);
    break;
    
    case "phone" :
    	$username = $_GET["username"];
    	$phone = $_GET["phoneid"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler -> phone($username,$phone);
    break;

    case "now" :
        $username = $_GET["username"];
        $area = $_GET["area"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler -> now($username,$area);
    break;
    
    case "qq" :
    	$username = $_GET["username"];
    	$qq = $_GET["qq"];
        $LibraryRestHandler = new LibraryRestHandler();
        $LibraryRestHandler -> qq($username,$qq);
    break;
}
?>