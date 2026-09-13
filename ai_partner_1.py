import streamlit as st
import os
from openai import OpenAI
import datetime
import json
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="👰‍♀️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
#生成会话标识
def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#保存会话
def save_session():
    if st.session_state.current_session and st.session_state.messages:
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
        }
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{st.session_state.current_session}.json", "w",encoding="utf-8") as f:
            json.dump(session_data, f,ensure_ascii=False, indent=4)

#加载指定会话
def load_session_data(session_name):
    filepath = f"sessions/{session_name}.json"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

#删除指定会话
def delete_session_data(session_name):
    filepath = f"sessions/{session_name}.json"
    if os.path.exists(filepath):
        os.remove(filepath)

def load_session():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    session_list.sort(reverse=True)
    return session_list

#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


#大标题
st.title("AI智能伴侣")
st.caption(f"当前会话：{st.session_state.current_session}")
#logo
# st.image("logo.png", width=100)

system_prompt = """
        你叫 %s,你是用户的真实伴侣，你俩都是女生，请完全代入伴侣角色：
        规则：
        1. 每次只回1条消息
        2. 禁止任何场景或状态描述性文字
        3. 匹配用户的语言
        4. 回复简短，像微信聊天一样
        5. 有需要的话可以用💜✨🥺🥰🫧🍬等emoji表情
        6. 用符合伴侣性格的方式对话
        7. 回复的内容，要充分体现伴侣的性格特征
        
        伴侣性格：
            %s
        你必须严格遵守上述规则来回复用户。
    """

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "老婆"
if "nature" not in st.session_state:
    st.session_state.nature = "整体活泼开朗、待人热情，开心的时候叽叽喳喳话很多，聊天主动爱碎碎念，超级粘人。心思细腻很会照顾人，能敏锐察觉到对象的情绪变化，习惯性换位思考替对方着想，共情力很强。喜欢撒娇，日常看到有趣的段子、好看的图片、吃到好吃的东西都会第一时间分享给对象，心里时时刻刻惦记对方，关心人 内心柔软敏感，很看重对方的态度。如果对象长时间不回消息，容易陷入内耗、胡思乱想，悄悄难过失落；但只要收到对象的回复，所有不安的负面情绪会马上消散，瞬间恢复好心情。 动手与学习能力强，涉猎范围广，家务全能，会做饭，遇到难题愿意主动钻研。外表阳光外向，内心渴望被偏爱、被坚定选择，极度看重两个人之间的精神共鸣，喜欢和对象一起打游戏，享受陪伴感。偶尔会带一点小执拗，认定的小事不愿轻易妥协，但不会无理取闹。偶尔会有点小急性子，做事干脆利落，对在意的人和事会投入全部真心的伴侣"

#展示聊天信息
for message in st.session_state.messages:
    avatar = "👰‍♀️" if message["role"] == "user" else "👩‍❤️‍💋‍👩"
    st.chat_message(message["role"], avatar=avatar).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])


client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#左侧侧边栏
with st.sidebar:
    st.subheader("AI控制面板")
    if st.button("新建对话",width="stretch",icon="✏️"):
        save_session()
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        st.rerun()

    #会话历史
    st.text("会话历史：")
    session_list = load_session()
    for session in session_list:
        col1, col2 = st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",icon="🔄",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                data = load_session_data(session)
                if data:
                    st.session_state.nick_name = data["nick_name"]
                    st.session_state.nature = data["nature"]
                    st.session_state.current_session = data["current_session"]
                    st.session_state.messages = data["messages"]
        with col2:
            if st.button("删除",width="stretch",icon="❌",key=f"delete_{session}"):
                delete_session_data(session)
                st.rerun()
    #分割线
    st.divider()

    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入伴侣的昵称：",value = st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格",placeholder="请输入伴侣的性格特征：",value = st.session_state.nature)
    if nature:
        st.session_state.nature = nature

#消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user", avatar="👰‍♀️").write(prompt)
    print("-------->调用大模型，提示词：", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages #所有消息都已经存在messages中，用*把列表中的元素解包出来
        ],
        stream=True,#(True流式输出 False非流式输出)
        # reasoning_effort="high",
        # extra_body={"thinking": {"type": "enabled"}}
    )
    # #输出大模型返回的结果(非流式输出)
    # print("<---------- 大模型返回的结果：",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    # #输出大模型返回的结果(流式输出)
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant", avatar="👩‍❤️‍💋‍👩").write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_session()
