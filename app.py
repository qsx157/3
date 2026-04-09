import streamlit as st
import datetime

# --- 页面基本设置（适配手机端居中显示） ---
st.set_page_config(page_title="专属签到站", page_icon="💖", layout="centered")

st.title("✨ 宝贝专属签到站 ✨")

# --- 模拟数据存储 ---
# 注意：这里为了演示使用了 Streamlit 的 session_state。
# 实际部署到云端时，为了防止重启数据丢失，需要连接简单的云数据库。
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'last_checkin' not in st.session_state:
    st.session_state.last_checkin = None
if 'days' not in st.session_state:
    st.session_state.days = 0

today = str(datetime.date.today())

# --- 签到交互区 ---
st.write("### 📅 今日打卡")

# use_container_width=True 会让按钮在手机屏幕上撑满宽度，更好按
if st.button("👉 点击进行今日签到 👈", use_container_width=True):
    if st.session_state.last_checkin == today:
        st.warning("笨蛋，今天已经签到过啦，明天再来哦！")
    else:
        st.session_state.last_checkin = today
        st.session_state.points += 10
        st.session_state.days += 1
        st.balloons()  # 触发满屏飘气球的特效
        st.success(f"签到成功！已连续签到 {st.session_state.days} 天。")

# --- 进度与奖励区 ---
st.divider()  # 分割线
st.write("### 🎁 积分与兑换")

# 使用大号字体展示积分
st.metric(label="当前拥有积分", value=st.session_state.points)

# 进度条，假设 300 分是终极大奖
progress_value = min(st.session_state.points / 300, 1.0)
st.progress(progress_value, text="距离终极大奖还有多远")

st.write("**💝 奖励兑换大厅：**")
# 根据积分自动解锁的复选框
st.checkbox("🔓 50积分：秋天的第一杯奶茶", value=st.session_state.points >= 50, disabled=True)
st.checkbox("🔓 100积分：清空100元内购物车", value=st.session_state.points >= 100, disabled=True)
st.checkbox("🔓 300积分：周末周边游一次", value=st.session_state.points >= 300, disabled=True)