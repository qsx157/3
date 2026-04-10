import streamlit as st
import datetime
import requests

# ==========================================
# ⚙️ 核心配置区（在这里填入你刚刚拿到的钥匙）
# ==========================================
BIN_ID = "69d89f2536566621a8997b0f"  # 例如: "65f1a..."
API_KEY = "$2a$10$pUolK.ScvO6TY0R8SKbm4OnepXkBZ.HMVojMbYnJp4Unb0tprNdHW" # 例如: "$2a$10$..."

# 专属暗号设置
SECRET_CODE = "20211103"

# ==========================================

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    'X-Master-Key': API_KEY,
    'Content-Type': 'application/json'
}

# --- 云端数据读写函数 ---
def get_remote_data():
    """从云端记事本读取当前积分"""
    try:
        res = requests.get(URL, headers=HEADERS)
        return res.json().get('record', {"points": 0, "days": 0, "last_checkin": ""})
    except:
        return {"points": 0, "days": 0, "last_checkin": ""}

def update_remote_data(new_data):
    """把最新积分写回云端记事本"""
    requests.put(URL, json=new_data, headers=HEADERS)

# --- 页面基本设置 ---
st.set_page_config(page_title="专属签到站", page_icon="💖", layout="centered")

# --- 专属暗号锁 ---
password = st.text_input("请输入我们的专属暗号解锁：", type="password")
if password != SECRET_CODE:
    st.warning("🔒 哎呀，暗号不对，不许进！")
    st.stop()

st.title("✨ 宝贝专属签到站 ✨")

# --- 加载云端数据到当前页面 ---
if 'cloud_data' not in st.session_state:
    st.session_state.cloud_data = get_remote_data()

data = st.session_state.cloud_data
today = str(datetime.date.today())

# --- 签到交互区 ---
st.write("### 📅 今日打卡")

if st.button("👉 点击进行今日签到 👈", use_container_width=True):
    if data["last_checkin"] == today:
        st.warning("笨蛋，今天已经签到过啦，明天再来哦！")
    else:
        # 核心：更新数据并同步到云端！
        data["last_checkin"] = today
        data["points"] += 10
        data["days"] += 1
        
        # 保存到大本营
        update_remote_data(data)
        st.session_state.cloud_data = data 
        
        st.balloons()
        st.success(f"签到成功！已连续签到 {data['days']} 天。")

# --- 进度与奖励区 ---
st.divider()
st.write("### 🎁 积分与兑换")

st.metric(label="当前拥有积分", value=data["points"])

progress_value = min(data["points"] / 300, 1.0)
st.progress(progress_value, text="距离终极大奖还有多远")

st.write("**💝 奖励兑换大厅：**")
st.checkbox("🔓 50积分：秋天的第一杯奶茶", value=data["points"] >= 50, disabled=True)
st.checkbox("🔓 100积分：清空100元内购物车", value=data["points"] >= 100, disabled=True)
st.checkbox("🔓 300积分：周末周边游一次", value=data["points"] >= 300, disabled=True)
