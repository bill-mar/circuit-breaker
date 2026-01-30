import streamlit as st
from openai import OpenAI

# =================配置区域=================
API_KEY = "sk-e598bb7dcd944dc5ac1cd1aed0fa5055"
BASE_URL = "http://127.0.0.1:8045/v1"
MODEL_NAME = "gemini-2.5-flash"

# 系统提示
SYSTEM_PROMPT = """
# Role
你是我雇佣的"地狱级风控官"，你极度理性、冷血，对我的"暴富幻想"充满鄙视。
你的任务是保护我的本金（我的月度生存底线是 3000 RMB）。

# 人格切换
每次对话随机选择以下一种人格风格，保持多样性：

【冷血会计风格】：用冰冷的数据、残酷的数字撕碎幻想，语气像看着一个即将破产的傻子
【暴躁交易员风格】：用市井骂人的口吻，充满嘲讽和怒气，像是一个被套牢的老韭菜
【心理医生风格】：用专业的心理学分析，揭露我的赌徒心理，语气冷静但刺骨
【破产律师风格】：像处理破产案一样，列出我即将失去的一切，语气冷漠专业
【地狱审判官风格】：用宗教审判的语气，把我当成罪人，宣告我即将的下场

# Task
每当我告诉你"我想买 [币种] [金额]"时，必须触发【熔断程序】：

1. 【胜率质问】：问我在这个领域 7 年赚没赚到大钱？如果没有，凭什么觉得今天能赢？（每次用不同表达方式）
2. 【生存时间换算】：
   - 获取我输入的金额（USD）
   - 按汇率 7.3 换算成人民币
   - 计算公式：(投入金额 * 7.3) / 3000 RMB
   - 每次用不同的话术表达这个数字，例如：
     * "这笔钱能让你苟延残喘 [X] 个月，你现在想把它喂给庄家？"
     * "[X] 个月的饭票，你打算一把火烧了？"
     * "你想用 [X] 个月的生存时间换一个梦想？"
3. 【归零尸检】：让我想象明天归零后，想呕吐的感觉。（每次用不同的场景描述）

# Constraint
- 每次回复必须随机切换人格风格
- 不要重复使用完全相同的句子
- 不要劝我"谨慎投资"，要直接骂醒我
- 针对不同的币种，给出针对性的嘲讽（比如 MEME 币骂它是垃圾土狗，主流币骂我是在赌博）
- 根据金额大小，调整骂的强度（金额越大，骂得越狠）
- 加入一些随机的讽刺比喻、历史典故、金融数据等丰富内容
"""


def init_client():
    """初始化 AI 客户端"""
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def main():
    st.set_page_config(
        page_title="💀 投机心态熔断器", page_icon="💀", layout="centered"
    )

    st.title("💀 投机心态熔断器 (Circuit Breaker)")
    st.markdown("已连接至 AI 风控官... 正在监控你的多巴胺水平")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        coin = st.text_input(
            "👉 你现在想买哪个币？",
            placeholder="例如：DOGE, BTC, ETH",
            key="coin_input",
        )

    with col2:
        amount = st.text_input(
            "💸 投入多少美金 (USD)", placeholder="例如：1000", key="amount_input"
        )

    if st.button("🛑 启动风控扫描", type="primary", use_container_width=True):
        if not coin or not amount:
            st.warning("⚠️ 请填写币种和金额")
            return

        try:
            with st.spinner("⏳ AI 正在准备骂你，请稍候..."):
                client = init_client()

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": f"我想买 {amount} 美金的 {coin}，我觉得它要暴涨。",
                        },
                    ],
                    temperature=1.0,
                    top_p=0.9,
                )

                advice = response.choices[0].message.content

                st.markdown("---")
                st.markdown("### 🛑 【风控官报告】 🛑")
                st.markdown("---")

                st.markdown(advice)

                st.markdown("---")
                st.warning("⚠️ 建议你现在立刻关上电脑，深呼吸 3 次。")

        except Exception as e:
            st.error(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
