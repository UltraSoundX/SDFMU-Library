<?php
    header('Access-Control-Allow-Origin:*');

    class CoolQ {
        public function adduser (){
            $user_id = $_POST["user_id"];
            $flag = $_POST["flag"];
            $comment = $_POST["comment"];
            $addurl = "http://lab.radiology.link:5700/set_friend_add_request";
            $post_data = array(
                'flag' => $flag,
                'remark' => $comment
              );
            $this->send_post($addurl,$post_data);
            $this->hi($user_id);
        }

        public function hi($qq){
            $message = "很高兴认识你，机器人不支持聊天功能，如有预约需求请登录如下系统处理https://lab.radiology.link/ ";
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

    $coolQ = new coolQ();
    $coolQ -> adduser();