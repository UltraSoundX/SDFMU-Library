<?php
/*
 * Copyright (c) 2017-2018 THL A29 Limited, a Tencent company. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
namespace TencentCloud\Gse\V20191112\Models;
use TencentCloud\Common\AbstractModel;

/**
 * @method string getFleetId() 获取服务部署ID
 * @method void setFleetId(string $FleetId) 设置服务部署ID
 * @method string getName() 获取名称
 * @method void setName(string $Name) 设置名称
 */

/**
 *DeleteScalingPolicy请求参数结构体
 */
class DeleteScalingPolicyRequest extends AbstractModel
{
    /**
     * @var string 服务部署ID
     */
    public $FleetId;

    /**
     * @var string 名称
     */
    public $Name;
    /**
     * @param string $FleetId 服务部署ID
     * @param string $Name 名称
     */
    function __construct()
    {

    }
    /**
     * For internal only. DO NOT USE IT.
     */
    public function deserialize($param)
    {
        if ($param === null) {
            return;
        }
        if (array_key_exists("FleetId",$param) and $param["FleetId"] !== null) {
            $this->FleetId = $param["FleetId"];
        }

        if (array_key_exists("Name",$param) and $param["Name"] !== null) {
            $this->Name = $param["Name"];
        }
    }
}
