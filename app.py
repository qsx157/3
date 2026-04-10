import streamlit as st
import datetime
import requests
import random

# ==========================================
# ⚙️ 核心配置区（填入你之前的钥匙）
# ==========================================
BIN_ID = "69d89f2536566621a8997b0f" 
API_KEY = "$2a$10$pUolK.ScvO6TY0R8SKbm4OnepXkBZ.HMVojMbYnJp4Unb0tprNdHW"
SECRET_CODE = "20211103"  # 你们的暗号

# 💌 专属情话库（你可以无限添加，每天会自动随机抽一句）
love_words = [
    "今天也是更爱你的一天！🌹",
    "不管多忙，记得按时吃饭，我在想你哦~",
    "攒够积分，我们就去吃你最爱的那家火锅！",
    "遇见你，是我这辈子抽到的最棒的盲盒。✨",
    "宝贝辛苦啦，签完到奖励自己一个亲亲吧！😘",
    "想和你一起去看晚霞，去吹晚风。"
]

# 🎁 奖励价格表（积分定价）
REWARDS = {
    "🥤 秋天的第一杯奶茶": 50,
    "🛒 清空100元内购物车": 100,
    "🚗 周末周边游一次": 300
}
# ==========================================

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {'X-Master-Key': API_KEY, 'Content-Type': 'application/json'}

def get_remote_data():
    try:
        res = requests.get(URL, headers=HEADERS)
        return res.json().get('record', {"points": 0, "days": 0, "last_checkin": ""})
    except:
        return {"points": 0, "days": 0, "last_checkin": ""}

def update_remote_data(new_data):
    requests.put(URL, json=new_data, headers=HEADERS)

# --- 页面基本设置 ---
st.set_page_config(page_title="宁宁专属签到站", page_icon="💖", layout="centered")

# --- 专属暗号锁 ---
password = st.text_input("请输入我们的专属暗号解锁：", type="password")
if password != SECRET_CODE:
    st.warning("🔒 哎呀，暗号不对，不许进！")
    st.stop()

# --- 顶部：每日情话 ---
today = str(datetime.date.today())
random.seed(today) # 确保同一天显示的句子是一样的
daily_quote = random.choice(love_words)
st.chat_message("assistant", avatar="💌").write(f"**今日份留言：** {daily_quote}")

st.title("✨ 宝贝专属签到站 ✨")

# --- 加载数据 ---
if 'cloud_data' not in st.session_state:
    st.session_state.cloud_data = get_remote_data()

data = st.session_state.cloud_data

# --- 签到区 ---
st.write("### 📅 今日打卡")
if st.button("👉 点击进行今日签到 (积分+10) 👈", use_container_width=True):
    if data["last_checkin"] == today:
        st.warning("笨蛋，今天已经签到过啦，明天再来哦！")
    else:
        data["last_checkin"] = today
        data["points"] += 10
        data["days"] += 1
        update_remote_data(data)
        st.session_state.cloud_data = data 
        st.balloons()
        st.success(f"签到成功！连续签到第 {data['days']} 天！")

# --- 兑换区 ---
st.divider()
st.write("### 🎁 奖励兑换大厅")
st.metric(label="当前剩余积分", value=f"{data['points']} LP") # LP: Love Points

# 动态生成兑换按钮
for gift, cost in REWARDS.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{gift}**")
        st.caption(f"消耗积分: {cost}")
    with col2:
        if st.button("立即兑换", key=gift):
            if data["points"] >= cost:
                data["points"] -= cost # 扣分逻辑
                update_remote_data(data)
                st.session_state.cloud_data = data
                st.snow()
                st.success(f"兑换成功！我已收到通知，马上安排！")
                # 这里可以加个强制刷新的小技巧
                st.rerun()
            else:
                st.error("积分不足！")

# 进度条
progress_value = min(data["points"] / 300, 1.0)
st.progress(progress_value, text="距离终极大奖还有多远")
