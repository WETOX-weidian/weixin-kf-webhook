#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
唯电宝客服知识库问答系统
直接在Webhook服务中实现问答逻辑，不依赖外部工作流
"""

import json
import re
from typing import Optional, Dict, List

class WetoXKnowledgeBase:
    """唯电宝知识库"""
    
    def __init__(self):
        self.products = {
            "2mini": {
                "name": "唯电宝2mini",
                "price": "标准版1099元/高功率版1299元",
                "weight": "标准版1.7kg/高功率版1.9kg",
                "waterproof": False,
                "waterproof_desc": "绝对不防水，没有防水结构，严禁下雨或有水环境使用",
                "rated_power": "标准版3kW/高功率版5kW",
                "peak_power": "标准版3.3kW/高功率版6.6kW",
                "heating_free": True,
                "heating_free_desc": "已升级特斯拉免加热程序，特斯拉使用不会触发电池自动加热（仅针对Model 3、Model Y）",
                "supported_models": [
                    "特斯拉Model 3/Y全系",
                    "蔚来除ET9、第三代NT3.0 ES8/ES9外全系",
                    "理想2020款ONE",
                    "小鹏24款MONA M03",
                    "通用奥特能（凯迪拉克锐歌/傲歌、别克E4/E5）",
                    "沃尔沃纯电、极星、福特电马",
                    "埃安22/21款AION Y磷酸铁锂版",
                    "零跑T03/C11/C01",
                    "五菱/宝骏部分车型",
                    "吉利系（睿蓝、几何、熊猫mini带快充版）",
                    "丰田bZ4X（带My Room模式版）",
                    "荣威D7/M7 DMH"
                ],
                "unsupported_models": [
                    "特斯拉Model S/X",
                    "大众全系",
                    "比亚迪、北汽、长安、威马、极越、欧拉、合创、思皓、奔驰、宝马、奥迪等"
                ]
            },
            "2": {
                "name": "唯电宝2代",
                "price": "2299元",
                "weight": "约5kg",
                "waterproof": True,
                "waterproof_desc": "整机IPX5防水，下雨天可在户外安全使用",
                "rated_power": "4kW",
                "peak_power": "6kW",
                "supported_models": [
                    "特斯拉Model 3/Y/S/X全系（17年后国标GB/T版）",
                    "所有2mini支持的车型"
                ],
                "unsupported_models": [
                    "特斯拉Model S/X（17年前进口欧标Type2版）"
                ]
            },
            "AC": {
                "name": "唯电宝AC",
                "price": "待确认",
                "weight": None,
                "waterproof": True,
                "waterproof_desc": "插线板IPX6防水，枪头IP66防水",
                "rated_power": "硬件最大4kW（实际取决于车辆OBC能力）",
                "cable_length": "5米",
                "prerequisite": "原车必须自带双向OBC（交流外放电功能）",
                "supported_models": [
                    "比亚迪海鸥/海豚/海豹全系、秦PLUS DM-i/JL版、汉/唐全系等",
                    "理想2021款ONE、L6/L7/L8/L9、MEGA",
                    "鸿蒙智行问界/智界/享界/尊界/尚界全系",
                    "小鹏P7i/P7+/P5/G6/G9/X9等",
                    "蔚来乐道L60/L80/L90",
                    "以及更多支持车型..."
                ],
                "unsupported_models": [
                    "特斯拉全系（Model Y L除外但协议加密也无法用）",
                    "不支持交流放电的车型"
                ]
            }
        }
        
        self.rules = {
            "greeting": "亲，您好！请问您想咨询哪款产品，是唯电宝AC、唯电宝2mini还是唯电宝2代呀？",
            "ask_car": "亲，请问您的爱车是具体什么品牌、哪一年的哪款车型呢？",
            "no_support": "抱歉亲，咱们的产品不支持这款车呢～",
            "product_not_support": "亲，您咨询的问题不同产品都不一样哦，请问您想咨询哪款产品呀？",
            "cant_answer": "亲，这个问题需要知道具体产品才能回答呢～请问您想咨询哪款产品呀？",
            "hotline": "4006066162"
        }
        
        # 常见问题回复
        self.qa_patterns = {
            "防水": {
                "2mini": "亲，唯电宝2mini是绝对不防水的，没有防水结构，严禁在下雨或有水环境使用哦～",
                "2": "亲，唯电宝2代整机IPX5防水，下雨天户外也能用呢～",
                "AC": "亲，唯电宝AC插线板IPX6防水，枪头IP66防水，暴雨天、洒落汤汁都能放心用～"
            },
            "价格": {
                "2mini": "亲，唯电宝2mini标准版1099元，高功率版1299元呢～",
                "2": "亲，唯电宝2代2299元，包含5米防水插线板升级套装～",
                "AC": "亲，唯电宝AC需要先确认您的车型是否支持呢～请问您的车是哪款呀？"
            },
            "质保": {
                "2mini": "亲，唯电宝2mini保修24个月，超出保修期收材料费跟快递费哦～",
                "2": "亲，唯电宝2代保修24个月，超出保修期收材料费跟快递费哦～",
                "AC": "亲，唯电宝AC保修1年且只换不修，超出1年仅收少量材料费与快递费哦～"
            },
            "发货": {
                "default": "亲，每天下午4点前付款的订单当天发顺丰陆运，江浙沪皖一般次日达，大多数地区3天左右哦～"
            },
            "运费": {
                "default": "亲，中国大部分地区包邮，部分偏远地区需先行支付100元运费，确认收货后联系客服全额退回哦～"
            },
            "发票": {
                "default": "亲，可自行在订单详情页申请发票，填写开票信息，平台一般7个工作日内开具，直接在申请发票处可查看电子发票哦～"
            },
            "保险": {
                "default": "亲，咱们的产品由太平洋保险承保，若因使用唯电宝导致车辆失去质保，保险也会进行理赔（10万元/辆）哦～"
            },
            "不放电": {
                "default": "亲，直流放电需要：1.电量10%-95%之间；2.充电限值设为100%；3.按顺序操作：短按开机蓝灯→再短按白灯闪烁→插枪白灯常亮。如果还没反应可以提供400电话帮您跟进哦～"
            }
        }
    
    def detect_product(self, text: str) -> Optional[str]:
        """检测用户咨询的产品"""
        text_lower = text.lower()
        
        # 检测2代（优先于2mini，因为2mini包含mini）
        if "唯电宝2代" in text or "v2代" in text_lower or "2代" in text:
            return "2"
        
        # 检测2mini
        if "2mini" in text or "2 mini" in text or "min" in text_lower:
            if "唯电宝2代" not in text and "2代" not in text.replace("唯电宝2代mini", ""):
                return "2mini"
        
        # 检测AC
        if "ac" in text_lower or "交流" in text or "obc" in text_lower or "慢充" in text:
            return "AC"
        
        return None
    
    def is_product_question(self, text: str) -> bool:
        """判断是否是产品相关问题"""
        keywords = [
            "防水", "价格", "多少", "钱", "质保", "保修", "发货", "物流",
            "发票", "保险", "支持", "能用", "可以用", "可以用吗",
            "功率", "瓦", "kw", "怎么", "操作", "使用", "问题",
            "不放电", "放不出电", "拔不出", "加热", "参数", "规格"
        ]
        return any(k in text for k in keywords)
    
    def generate_response(self, user_input: str, context: dict) -> dict:
        """
        生成回复
        
        Args:
            user_input: 用户输入
            context: 对话上下文（包含product, car等）
        
        Returns:
            dict: {
                "response": 回复内容,
                "need_product": 是否需要知道产品,
                "need_car": 是否需要知道车型,
                "context_update": 需要更新的上下文
            }
        """
        user_input_lower = user_input.lower()
        response = ""
        need_product = False
        need_car = False
        context_update = {}
        
        # 检测产品
        detected_product = self.detect_product(user_input)
        if detected_product:
            context_update["product"] = detected_product
        
        current_product = context.get("product")
        
        # 人工客服直接给电话
        if any(k in user_input for k in ["人工", "客服电话", "联系电话"]):
            return {
                "response": f"亲，这是我们的客服电话：{self.rules['hotline']}，有什么问题随时联系我们哦～",
                "need_product": False,
                "need_car": False,
                "context_update": {}
            }
        
        # 优惠直接回复
        if any(k in user_input for k in ["优惠", "便宜", "打折", "活动", "返现"]):
            return {
                "response": "亲，唯电宝全系不议价、无小礼品哦～",
                "need_product": False,
                "need_car": False,
                "context_update": {}
            }
        
        # 发链接问题
        if any(k in user_input for k in ["链接", "连接", "网址", "商品链接", "购买链接"]):
            return {
                "response": "亲，这边没法直接发链接，您可以进店自己找一下需要的正确商品哦～",
                "need_product": False,
                "need_car": False,
                "context_update": {}
            }
        
        # 车型检测 - 如果用户提到车型，先问产品
        if self._detect_car(user_input) and not current_product:
            response = f"亲，{user_input}可以搭配我们的唯电宝2mini或2代使用呢～请问您想咨询哪款产品呀？"
            return {
                "response": response,
                "need_product": True,
                "need_car": False,
                "context_update": context_update
            }
        
        # 问候语（只有纯问候时）
        if any(g in user_input_lower for g in ["你好", "在吗", "您好", "嗨", "hi", "hello"]) and not detected_product:
            response = self.rules["greeting"]
            need_product = True
            return {
                "response": response,
                "need_product": need_product,
                "need_car": need_car,
                "context_update": context_update
            }
        
        # 确定使用的产品（优先使用检测到的）
        product = detected_product or current_product
        
        # 如果没有产品信息
        if not product:
            # 车型检测 - 如果用户提到车型，先问产品
            if self._detect_car(user_input):
                response = f"亲，{user_input}可以搭配我们的唯电宝2mini或2代使用呢～请问您想咨询哪款产品呀？"
                need_product = True
            # 如果是产品相关问题，必须先知道产品
            elif self.is_product_question(user_input):
                response = self.rules["product_not_support"]
                need_product = True
            else:
                response = self.rules["greeting"]
                need_product = True
            return {
                "response": response,
                "need_product": need_product,
                "need_car": need_car,
                "context_update": context_update
            }
        
        # 车型检测
        car = context.get("car", "")
        car_detected = self._detect_car(user_input)
        if car_detected:
            car = car_detected
            context_update["car"] = car
        
        # 支持车型问题
        if any(k in user_input for k in ["支持", "能用", "可以用", "可以用吗", "车型", "车是"]):
            if car:
                response = self._check_car_support(car, product)
            else:
                response = self.rules["ask_car"]
                need_car = True
            return {
                "response": response,
                "need_product": False,
                "need_car": need_car,
                "context_update": context_update
            }
        
        # 查找匹配的问题模式
        for keyword, answers in self.qa_patterns.items():
            if keyword in user_input_lower:
                if keyword in ["2mini", "2", "AC"]:
                    continue
                if product in answers:
                    response = answers[product]
                else:
                    response = answers.get("default", "")
                break
        
        # 如果没有匹配到具体问题，尝试通用回复
        if not response:
            # 防水相关
            if "防水" in user_input:
                response = self.products[product]["waterproof_desc"]
            
            # 价格相关
            elif any(k in user_input for k in ["价格", "多少", "钱"]):
                if product == "2":
                    response = "亲，唯电宝2代2299元，包含5米防水插线板升级套装呢～"
                elif product == "2mini":
                    response = "亲，唯电宝2mini标准版1099元，高功率版1299元呢～"
                else:
                    response = "亲，唯电宝AC需要先确认您的车型是否支持呢～请问您的车是哪款呀？"
                    need_car = True
            
            # 质保相关
            elif any(k in user_input for k in ["质保", "保修"]):
                response = self.qa_patterns["质保"][product]
            
            # 发货相关
            elif "发货" in user_input or "物流" in user_input:
                response = self.qa_patterns["发货"]["default"]
            
            # 发票相关
            elif "发票" in user_input:
                response = self.qa_patterns["发票"]["default"]
            
            # 保险相关
            elif "保险" in user_input:
                response = self.qa_patterns["保险"]["default"]
            
            # 功率相关
            elif any(k in user_input for k in ["功率", "瓦", "kw"]):
                if product == "2mini":
                    response = f"亲，唯电宝2mini标准版额定3kW/峰值3.3kW，高功率版额定5kW/峰值6.6kW呢～"
                elif product == "2":
                    response = "亲，唯电宝2代额定4kW，峰值6kW呢～"
                elif product == "AC":
                    response = "亲，唯电宝AC硬件最大支持4kW，实际放电大小取决于您车辆OBC的能力呢～"
            
            # 不放电问题
            elif any(k in user_input for k in ["不放电", "放不出电", "无法放电"]):
                response = self.qa_patterns["不放电"]["default"]
            
            # 支持车型问题
            elif any(k in user_input for k in ["支持", "能用", "可以用", "车型"]):
                if "model" not in context:
                    response = self.rules["ask_car"]
                    need_car = True
                else:
                    response = self._check_car_support(context.get("car", ""), product)
            
            # 操作使用问题
            elif any(k in user_input for k in ["怎么", "操作", "使用", "步骤"]):
                if product in ["2mini", "2"]:
                    response = "亲，操作步骤：1.短按开关键蓝灯长亮；2.再短按白灯闪烁；3.插枪等待白灯常亮就正常放电了～"
                elif product == "AC":
                    response = "亲，先确认车子中控有开始放电按钮，部分车型需要手动确认呢～"
            
            # 加热相关（2mini特有）
            elif "加热" in user_input and product == "2mini":
                response = "亲，唯电宝2mini已升级特斯拉免加热程序，特斯拉Model 3/Y使用不会触发电池自动加热哦～"
            
            # 拔不出问题
            elif "拔不出" in user_input or "拔不出来" in user_input:
                response = "亲，部分车型需要在中控屏幕点击'结束放电'后才能拔枪哦～"
            
            # 优惠问题
            elif any(k in user_input for k in ["优惠", "便宜", "打折", "活动"]):
                response = "亲，唯电宝全系不议价、无小礼品哦～"
            
            # 发链接问题
            elif any(k in user_input for k in ["链接", "连接", "地址", "网址", "商品链接", "购买链接"]):
                response = "亲，这边没法直接发链接，您可以进店自己找一下需要的正确商品哦～"
            
            # 退货问题
            elif any(k in user_input for k in ["退货", "七天", "无理由"]):
                response = "亲，七天无理由退货需要保持产品全新未使用哦，具体可以在订单详情页申请～"
            
            # 二手问题
            elif "二手" in user_input:
                response = "亲，凭第一任车主在我们官方平台的订单截图，就可以享受保修跟保险哦～"
            
            # 400电话
            elif any(k in user_input for k in ["人工", "电话", "联系", "投诉"]):
                response = f"亲，这是我们的客服电话：{self.rules['hotline']}，有什么问题随时联系我们哦～"
            
            # 其他问题
            else:
                if product == "AC":
                    response = "亲，唯电宝AC需要原车自带交流外放电功能才能使用呢，请问您的车是哪款呀？"
                    need_car = True
                else:
                    response = f"亲，唯电宝{self.products[product]['name']}还有哪些想了解的呢？"
        
        return {
            "response": response,
            "need_product": need_product,
            "need_car": need_car,
            "context_update": context_update
        }
    
    def _check_car_support(self, car: str, product: str) -> str:
        """检查车型是否支持"""
        if not car:
            return self.rules["ask_car"]
        
        car_lower = car.lower()
        product_info = self.products[product]
        
        # 特斯拉特殊处理
        if "特斯拉" in car or "model" in car_lower:
            if "model 3" in car_lower or "model3" in car_lower or "model y" in car_lower or "modely" in car_lower:
                return f"亲，{car}全系都可以使用唯电宝{product_info['name']}的呢～"
            elif "model s" in car_lower or "models" in car_lower or "model x" in car_lower or "modelx" in car_lower:
                if product == "2":
                    return f"亲，{car}（17年后国标GB/T版）可以使用唯电宝2代呢～"
                else:
                    return f"亲，抱歉，唯电宝{product_info['name']}不支持Model S/X呢～"
        
        # 比亚迪处理
        if "比亚迪" in car or "汉" in car or "唐" in car or "秦" in car or "海豹" in car or "海鸥" in car or "海豚" in car or "宋" in car:
            if product == "AC":
                return f"亲，{car}可以使用唯电宝AC呢～（具体看车辆是否自带交流外放电功能）"
            else:
                return f"亲，抱歉，唯电宝{product_info['name']}不支持比亚迪车型呢～"
        
        # 蔚来处理
        if "蔚来" in car or "es" in car_lower or "et" in car_lower or "ec" in car_lower:
            if product in ["2mini", "2"]:
                if "et9" in car_lower or ("es8" in car_lower and "第三代" in car) or "es9" in car_lower:
                    return f"亲，抱歉，唯电宝{product_info['name']}暂不支持{car}呢～"
                else:
                    return f"亲，{car}可以使用唯电宝{product_info['name']}的呢～"
        
        # 理想处理
        if "理想" in car or "one" in car_lower:
            if "one" in car_lower or "理想one" in car_lower or "2020款理想one" in car_lower:
                if product in ["2mini", "2"]:
                    return f"亲，{car}可以使用唯电宝{product_info['name']}的呢～"
            elif product in ["2mini", "2"]:
                return f"亲，抱歉，唯电宝{product_info['name']}仅支持2020款理想ONE呢～"
        
        # 通用回复
        return f"亲，关于{car}是否支持，唯电宝{product_info['name']}支持的车型比较复杂，您可以拨打{self.rules['hotline']}确认一下哦～"
    
    def _detect_car(self, text: str) -> Optional[str]:
        """从用户输入中检测车型"""
        car_keywords = [
            "特斯拉", "model", "比亚迪", "汉", "唐", "秦", "海豹", "海鸥", "海豚", "宋",
            "蔚来", "es", "et", "理想", "one", "小鹏", "p7", "g9", "g6",
            "问界", "智界", "享界", "尊界", "岚图", "零跑", "哪吒", "威马",
            "埃安", "aion", "五菱", "宝骏", "吉利", "极氪", "领克", "长安",
            "长城", "欧拉", "哈佛", "奇瑞", "红旗", "奔腾"
        ]
        
        for keyword in car_keywords:
            if keyword.lower() in text.lower():
                return text
        return None


# 测试
if __name__ == "__main__":
    kb = WetoXKnowledgeBase()
    
    test_cases = [
        ("你好", {}),
        ("你好，我想咨询2mini", {}),
        ("2mini防水吗", {"product": "2mini"}),
        ("2代的价格是多少", {"product": "2"}),
        ("比亚迪汉能用吗", {"product": "AC", "car": ""}),
        ("特斯拉Model Y可以用吗", {"product": "2mini", "car": "特斯拉Model Y"}),
        ("不放电怎么办", {"product": "2mini"}),
    ]
    
    print("唯电宝知识库问答测试\n" + "="*50)
    
    for user_input, context in test_cases:
        result = kb.generate_response(user_input, context)
        print(f"\n用户: {user_input}")
        print(f"上下文: {context}")
        print(f"回复: {result['response']}")
        if result['need_product']:
            print("⚠️ 需要产品信息")
        if result['need_car']:
            print("⚠️ 需要车型信息")
