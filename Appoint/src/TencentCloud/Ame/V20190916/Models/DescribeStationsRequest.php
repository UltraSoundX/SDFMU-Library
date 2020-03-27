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
namespace TencentCloud\Ame\V20190916\Models;
use TencentCloud\Common\AbstractModel;

/**
 * @method integer getLimit() 获取条数，必须大于0
 * @method void setLimit(integer $Limit) 设置条数，必须大于0
 * @method integer getOffset() 获取offset (Default = 0)，(当前页-1) * Limit
 * @method void setOffset(integer $Offset) 设置offset (Default = 0)，(当前页-1) * Limit
 */

/**
 *DescribeStations请求参数结构体
 */
class DescribeStationsRequest extends AbstractModel
{
    /**
     * @var integer 条数，必须大于0
     */
    public $Limit;

    /**
     * @var integer offset (Default = 0)，(当前页-1) * Limit
     */
    public $Offset;
    /**
     * @param integer $Limit 条数，必须大于0
     * @param integer $Offset offset (Default = 0)，(当前页-1) * Limit
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
        if (array_key_exists("Limit",$param) and $param["Limit"] !== null) {
            $this->Limit = $param["Limit"];
        }

        if (array_key_exists("Offset",$param) and $param["Offset"] !== null) {
            $this->Offset = $param["Offset"];
        }
    }
}
