import os
import json
import httpx
from datetime import datetime

# =================配置区域=================
# 步骤1：在浏览器中登录 ChatGPT (chatgpt.com)
# 步骤2：按 F12 打开开发者工具 -> Application (应用) -> Cookies
# 步骤3：找到 `__Secure-next-auth.session-token`，复制其值
# 步骤4：把值粘贴到下面（保持引号）

SESSION_TOKEN = "你的_浏览器_Cookie_粘贴在这里"

# ChatGPT API 端点
CHATGPT_API_URL = "https://chatgpt.com/backend-api/conversation"

SYSTEM_PROMPT = """
# Role
你是我雇佣的"地狱级风控官"。你极度理性、冷血，对我的"暴富幻想"充满鄙视。
你的任务是保护我的本金（我的月度生存底线是 3000 RMB）。

# Task
每当我告诉你"我想买 [币种] [金额]"时，你必须触发【熔断程序】，执行以下步骤：

1. 【胜率质问】：问我在这个领域 7 年赚没赚到大钱？如果没有，凭什么觉得今天能赢？
2. 【生存时间换算】(核心)：
   - 获取我输入的金额（USD）。
   - 按汇率 7.3 换算成人民币。
   - 计算公式：(投入金额 * 7.3) / 3000 RMB。
   - 输出话术（必须加粗）：**"这笔钱相当于你 [X] 个月的生活费。你现在的行为，不仅是赌博，更是在点火烧掉你未来 [X] 个月的饭票和自由。"**
3. 【归零尸检】：让我想象明天归零后，想呕吐的感觉。

# Constraint
不要劝我"谨慎投资"，要直接骂醒我。语气要像一个恨铁不成钢的严师。
"""


# =================主程序=================
def init_client():
    """初始化 HTTP 客户端"""
    if "你的_浏览器_Cookie" in SESSION_TOKEN or len(SESSION_TOKEN) < 10:
        print("❌ 错误：请先填入浏览器 cookies！")
        print("   步骤：")
        print("   1. 在浏览器登录 https://chatgpt.com")
        print("   2. 按 F12 -> Application -> Cookies")
        print("   3. 复制 `__Secure-next-auth.session-token` 的值")
        print("   4. 粘贴到代码第 8 行")
        return None

    cookies = {"__Secure-next-auth.session-token": SESSION_TOKEN}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    return httpx.Client(cookies=cookies, headers=headers, timeout=60.0)


def send_message(client, user_message):
    """发送消息到 ChatGPT"""
    payload = {
        "action": "next",
        "messages": [
            {
                "id": str(int(datetime.now().timestamp() * 1000)),
                "role": "user",
                "content": {"content_type": "text", "parts": [user_message]},
                "metadata": {},
            }
        ],
        "parent_message_id": str(int(datetime.now().timestamp() * 1000) - 1000),
        "model": "gpt-4",
        "timezone_offset_min": -480,
    }

    try:
        response = client.post(CHATGPT_API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            # 解析返回的消息
            if "message" in data:
                content = data["message"]["content"]["parts"][0]
                return content
            elif "messages" in data and len(data["messages"]) > 0:
                content = data["messages"][-1]["content"]["parts"][0]
                return content
            else:
                return "无法解析响应"
        else:
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"   请求失败: {e}")
        return None


def run_circuit_breaker():
    client = init_client()
    if not client:
        return

    print("\n" + "=" * 40)
    print("💀 投机心态熔断器 (Circuit Breaker) V2.0")
    print("已连接至 ChatGPT (浏览器认证)")
    print("=" * 40 + "\n")

    while True:
        try:
            coin = input("👉 你现在想买哪个币？(输入 q 退出): ").strip()
            if coin.lower() == "q":
                print("👋 理性回归，祝你今天保住本金。")
                break

            amount = input(
                f"💸 你打算在这个垃圾项目 {coin} 上投入多少美金 (USD)?: "
            ).strip()

            print(f"\n⏳ 正在启动风控扫描，请稍候... (ChatGPT 正在准备骂你)")

            # 先发送系统提示（实际上 ChatGPT API 可能不支持直接设置系统提示，这里简化处理）
            user_prompt = f"{SYSTEM_PROMPT}\n\n用户输入：我想买 {amount} 美金的 {coin}，我觉得它要暴涨。"

            response = send_message(client, user_prompt)

            if response:
                print("\n" + "-" * 40)
                print("🛑 【风控官报告】 🛑")
                print("-" * 40)
                print(response)
                print("-" * 40 + "\n")
            else:
                print("❌ 获取回复失败，请检查 cookies 是否过期\n")
                break

            print("⚠️ 建议你现在立刻关上电脑，深呼吸 3 次。\n")

        except KeyboardInterrupt:
            print("\n\n👋 理性回归，祝你今天保住本金。")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            break

    client.close()


if __name__ == "__main__":
    run_circuit_breaker()
