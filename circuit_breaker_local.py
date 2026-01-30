import time

# =================配置区域=================
# 月度生存底线
LIVING_EXPENSES = 3000  # RMB
EXCHANGE_RATE = 7.3  # USD to RMB

# 地狱级警告文案
WARNINGS = [
    "你觉得这次能赢？7 年没赚到钱，凭什么觉得今天能改变命运？",
    "醒醒吧！市场不是你的提款机，是你的屠宰场。",
    "这笔钱本来可以让你苟延残喘几个月，现在你想送给庄家？",
]


# =================主程序=================
def run_circuit_breaker():
    print("\n" + "=" * 40)
    print("💀 投机心态熔断器 (Circuit Breaker) V1.0 本地版")
    print("无需 API Key，纯本地运行")
    print("=" * 40 + "\n")

    while True:
        try:
            coin = input("👉 你现在想买哪个币？(输入 q 退出): ").strip()
            if coin.lower() == "q":
                print("👋 理性回归，祝你今天保住本金。")
                break

            amount_input = input(
                f"💸 你打算在这个垃圾项目 {coin} 上投入多少美金 (USD)?: "
            ).strip()
            amount = float(amount_input)

            print(f"\n⏳ 正在启动风控扫描...")

            # 【胜率质问】
            print(f"\n1️⃣ 【胜率质问】")
            print(
                "   问自己：你在币圈 7 年赚没赚到大钱？如果没有，凭什么觉得今天能赢？"
            )

            # 【生存时间换算】
            rmb_amount = amount * EXCHANGE_RATE
            months = rmb_amount / LIVING_EXPENSES

            print(f"\n2️⃣ 【生存时间换算】")
            print(f"   投入：${amount} USD = ¥{rmb_amount:.2f} RMB")
            print(f"   **这笔钱相当于你 {months:.2f} 个月的生活费。**")
            print(
                f"   你现在的行为，不仅是赌博，更是在点火烧掉你未来 {months:.2f} 个月的饭票和自由。"
            )

            # 【归零尸检】
            print(f"\n3️⃣ 【归零尸检】")
            print("   想象明天归零后那种想呕吐的感觉...")
            print("   那个瞬间，你会恨今天的自己。")

            print(f"\n" + "-" * 40)
            print("🛑 【最终判决】 🛑")
            print(f"   {WARNINGS[int(time.time()) % len(WARNINGS)]}")
            print("-" * 40 + "\n")

            print("⚠️ 建议你现在立刻关上电脑，深呼吸 3 次。\n")

        except ValueError:
            print("❌ 输入错误，请输入数字\n")
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            break


if __name__ == "__main__":
    run_circuit_breaker()
