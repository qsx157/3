import streamlit as st
import datetime
import requests
import random

# ==========================================
# ⚙️ 核心配置区（请填入你的信息）
# ==========================================
BIN_ID = "69d89f2536566621a8997b0f" 
API_KEY = "$2a$10$pUolK.ScvO6TY0R8SKbm4OnepXkBZ.HMVojMbYnJp4Unb0tprNdHW"

SECRET_CODE = "20211103"       # 正常给她用的暗号
ADMIN_CODE = "admin123"   # 你的管理员后门暗号，用来强行加分测试

# 💌 专属情话库（每天自动随机抽一句）
love_words = [
    "今天也是更爱你的一天！🌹",
    "不管多忙，记得按时吃饭，我在想你哦~",
    "攒够积分，我们就去吃你最爱的那家火锅！",
    "遇见你，是我这辈子抽到的最棒的盲盒。✨",
    "宝贝辛苦啦，签完到奖励自己一个亲亲吧！😘",
    "想和你一起去看晚霞，去吹晚风。"
]

# 🎁 奖励价格表（左边是礼物名字，右边是消耗的积分）
REWARDS = {
    "🥤 秋天的第一杯奶茶": 20,
    "🛒 清空100元内购物车"： 100,
    "🚗 周末周边游一次": 300
}
# ==========================================

# 云端数据库配置
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {'X-Master-Key': API_KEY, 'Content-Type': 'application/json'}

def get_remote_data():
    """从云端获取数据"""
    try:
        res = requests.get(URL, headers=HEADERS)
        return res.json().get('record', {"points": 0, "days": 0, "last_checkin": ""})
    except:
        return {"points": 0, "days": 0, "last_checkin": ""}

def update_remote_data(new_data):
    """保存数据到云端"""
    requests.put(URL, json=new_data, headers=HEADERS)

# --- 1. 页面基本设置 ---
st.set_page_config(page_title="宁宁专属签到站", page_icon="💖", layout="centered")

# --- 2. 专属暗号锁 (带确认按钮和状态保持) ---
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# 如果还没解锁，就只显示这个登录界面
if not st.session_state.unlocked:
    st.title("🔒 身份验证")
    password = st.text_input("请输入我们的专属暗号解锁：", type="password")
    
    # 增加确认按钮
    if st.button("确认解锁", use_container_width=True):
        if password == SECRET_CODE or password == ADMIN_CODE:
            # 记录解锁状态
            st.session_state.unlocked = True
            # 记录当前登录的是普通用户还是管理员
            st.session_state.current_user = "admin" if password == ADMIN_CODE else "gf"
            # 密码正确，立刻刷新页面展示正式内容
            st.rerun() 
        else:
            st.error("❌ 哎呀，暗号不对，再想想！")
            
    # 这一句很关键：没解锁之前，代码在这里停住，不显示下面的内容
    st.stop() 


# ================= 以下为解锁后显示的正式内容 =================

# --- 3. 顶部：每日随机情话 ---
today = str(datetime.date.today())
random.seed(today) # 保证今天内刷新网页看到的情话是同一句
daily_quote = random.choice(love_words)
st.chat_message("assistant", avatar="💌").write(f"**今日份留言：** {daily_quote}")

st.title("✨ 宝贝专属签到站 ✨")

# --- 加载云端积分数据 ---
if 'cloud_data' not in st.session_state:
    st.session_state.cloud_data = get_remote_data()

data = st.session_state.cloud_data

# --- 4. 签到区 ---
st.write("### 📅 今日打卡")
if st.button("👉 点击进行今日签到 (积分+10) 👈", use_container_width=True):
    if data["last_checkin"] == today:
        st.warning("笨蛋，今天已经签到过啦，明天再来哦！")
    else:
        # 更新数据并保存
        data["last_checkin"] = today
        data["points"] += 10
        data["days"] += 1
        update_remote_data(data)
        st.session_state.cloud_data = data 
        
        # 触发特效和成功提示
        st.balloons()
        st.success(f"🎉 签到成功！连续签到第 {data['days']} 天！")

# --- 5. 兑换区 ---
st.divider()
st.write("### 🎁 奖励兑换大厅")

# 大字展示当前积分
st.metric(label="当前剩余积分", value=f"{data['points']} 分") 

# 动态生成每个礼物的兑换按钮
for gift, cost in REWARDS.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{gift}**")
        st.caption(f"消耗积分: {cost}")
    with col2:
        if st.button("立即兑换", key=gift):
            if data["points"] >= cost:
                # 积分够，扣除积分并保存
                data["points"] -= cost 
                update_remote_data(data)
                st.session_state.cloud_data = data
                st.snow() # 兑换成功触发下雪特效
                st.success(f"✅ 兑换成功！我已收到通知，马上安排！")
                st.rerun() # 刷新页面，让顶部显示的余额立刻减少
            else:
                st.error("积分不足！继续加油哦~")

# 进度条 (按最贵的奖励计算进度)
progress_value = min(data["points"] / 300, 1.0)
st.progress(progress_value, text="距离终极大奖还有多远")

# --- 6. 开发者测试区 (仅用超级暗号登录时才会出现) ---
if st.session_state.current_user == "admin":
    st.divider()
    st.write("🛠️ 管理员模式 (测试专用)")
    if st.button("🚀 强行+10积分 (点我充值)"):
        data["points"] += 10
        update_remote_data(data)
        st.session_state.cloud_data = data
        st.success("余额已强行充值！")
        st.rerun()
