import os
from openai import OpenAI
import time

# =================配置区域=================
API_KEY = "sk-e598bb7dcd944dc5ac1cd1aed0fa5055"
BASE_URL = "http://127.0.0.1:8045/v1"
MODEL_NAME = "gemini-2.5-flash"

# 2. 这里是我们的核心：地狱级风控官 Prompt V2.0
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
    """初始化 AI 客户端"""
    if "sk-e598bb7dcd944dc5ac1cd1aed0fa5055" not in API_KEY or len(API_KEY) < 10:
        print("❌ 错误：请先在代码第 8 行填入你的 API Key！")
        return None

    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def run_circuit_breaker():
    client = init_client()
    if not client:
        return

    print("\n" + "=" * 40)
    print("💀 投机心态熔断器 (Circuit Breaker) V1.0")
    print("已连接至 AI 风控官... 正在监控你的多巴胺水平")
    print("=" * 40 + "\n")

    while True:
        try:
            # 1.以此获取用户输入
            coin = input("👉 你现在想买哪个币？(输入 q 退出): ").strip()
            if coin.lower() == "q":
                print("👋 理性回归，祝你今天保住本金。")
                break

            amount = input(
                f"💸 你打算在这个垃圾项目 {coin} 上投入多少美金 (USD)?: "
            ).strip()

            print(f"\n⏳ 正在启动风控扫描，请稍候... (AI 正在准备骂你)")

            # 2. 调用 AI 接口
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"我想买 {amount} 美金的 {coin}，我觉得它要暴涨。",
                    },
                ],
                temperature=0.7,
            )

            # 3. 输出结果
            advice = response.choices[0].message.content
            print("\n" + "-" * 40)
            print("🛑 【风控官报告】 🛑")
            print("-" * 40)
            print(advice)
            print("-" * 40 + "\n")

            # 强制冷却
            print("⚠️ 建议你现在立刻关上电脑，深呼吸 3 次。\n")

        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            break


if __name__ == "__main__":
    run_circuit_breaker()
