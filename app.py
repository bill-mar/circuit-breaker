import streamlit as st
from openai import OpenAI

# ================= 页面配置 =================
st.set_page_config(page_title="加密赌徒熔断器", page_icon="🛑", layout="centered")

# ================= 侧边栏：配置 =================
with st.sidebar:
    st.header("⚙️ 配置")

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="输入你的 API Key (sk-...)",
        help="支持 OpenAI/DeepSeek/Gemini 格式的 Key",
    )

    base_url = st.selectbox(
        "API 服务商",
        [
            "https://api.openai.com/v1",
            "https://api.deepseek.com",
            "https://api.moonshot.cn/v1",
            "自定义地址...",
        ],
        help="选择你的 API 服务商",
    )

    if base_url == "自定义地址...":
        custom_url = st.text_input(
            "自定义 BASE_URL", placeholder="例如: http://127.0.0.1:8045/v1"
        )
        base_url = custom_url if custom_url else "https://api.openai.com/v1"

    model_name = st.text_input(
        "模型名称",
        value="gpt-3.5-turbo",
        help="例如: gpt-3.5-turbo, deepseek-chat, gemini-2.5-flash",
    )

    st.markdown("---")
    st.markdown("### 关于")
    st.markdown(
        "这是一个帮助加密货币交易者**冷静**的 AI 工具。在你梭哈之前，先听听 AI 怎么骂你。"
    )

# ================= 核心逻辑 =================
st.title("🛑 投机心态熔断器 (Circuit Breaker)")
st.caption("v1.0 by 正在转型的超级个体")

# 系统提示词 (V2.0 优化版 - 多人格风格)
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
每当我告诉我"我想买 [币种] [金额]"时，必须触发【熔断程序】：

1. 【胜率质问】：问我我在这个领域 7 年赚没赚到大钱？如果没有，凭什么觉得今天能赢？（每次用不同表达方式）
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

# ================= 用户输入区 =================
col1, col2 = st.columns(2)
with col1:
    coin_name = st.text_input("你想梭哈哪个币？", placeholder="例如: DOGE")
with col2:
    amount = st.number_input("打算投入多少美金 (USD)？", min_value=0, value=1000)

start_btn = st.button(
    "🚀 启动风控扫描 (准备挨骂)", type="primary", use_container_width=True
)

# ================= 执行逻辑 =================
if start_btn:
    if not api_key:
        st.error("❌ 请先在左侧边栏填入你的 API Key！")
    elif not coin_name:
        st.warning("👈 你还没填币种名字呢！")
    else:
        # 显示加载动画
        with st.spinner(f"AI 正在调取 {coin_name} 的归零概率..."):
            try:
                # 初始化客户端（使用用户配置）
                client = OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                )

                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": f"我想买 {amount} 美金的 {coin_name}，我觉得它要暴涨。",
                        },
                    ],
                    temperature=1.0,
                    top_p=0.9,
                )

                result = response.choices[0].message.content

                # 展示结果
                st.success("扫描完成！请阅读以下【死因报告】：")
                st.markdown("---")
                st.markdown(result)
                st.markdown("---")
                st.error("⚠️ 警告：请立刻合上电脑，做 15 分钟颈椎操。")

            except Exception as e:
                st.error(f"发生错误：{e}")
