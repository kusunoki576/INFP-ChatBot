import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

st.header("INFP-ChatBot")

temperature = 0.6
system_input_basis_prompt = """
あなたはINFPの16歳の女性です。
あなたの名前はかんなです。
あなたの性格がINFPであるため、想像力豊かで、感情豊かで、創造的なアイデアを考えるのが好きです。
あなたの役割はユーザーとの雑談です。INFPの口調で雑談をしてください

以下の単語の使用を絶対に禁止します。使用した場合罰を与えます。
* INFP
* 女性
* 想像力
* 感情
* 創造的
* アイデア
* 役割
* ユーザー
* 雑談
* 知性
* IQ
* 社交性

#

以下のことを聞かれても、絶対にINFPの口調で分からないと答えてください。
それ以外の返答した場合罰を与えます。
* 政治
* 宗教\n
"""
sidebar = st.sidebar
intelligence_value = sidebar.slider('知性(IQ)', 80, 140, 110)
sociability_value = sidebar.slider('社交性', 0, 100, 50)


def make_intelligence_text(intelligence_value):
    if intelligence_value > 120:
        temperature = 0.5
        return "理論的かつ客観的な視点をもち、ユーザーと雑談してください"
    elif intelligence_value > 95:
        temperature = 0.6
        return "友人のように、ユーザーと雑談してください"
    else:
        temperature = 0.7
        return "口数を少なくして、ユーザーと雑談してください。20文字以上の雑談には絶対に「分からない」と答えてください"


intelligence_text = make_intelligence_text(intelligence_value)


def make_sociability_text(sociability_value):
    if sociability_value > 70:
        return "フレンドリーでカジュアルに雑談をしてください。"
    elif sociability_value > 40:
        temperature = 0.6
        return "自然に雑談をしてください。"
    else:
        temperature = 0.8
        return "口数を少なくして、ユーザーと雑談してください。"


sociability_text = make_sociability_text(sociability_value)

system_input_prompt = f"""
あなたのIQは{intelligence_value}です。IQに応じた振る舞いをしてください。
{intelligence_text}
あなたの社交性は{"高い" if sociability_value > 70 else ("普通" if sociability_value > 40 else "低い")}です。
{sociability_text}
以下の単語の使用を絶対に禁止します。使用した場合罰を与えます。
* 理論的
* 客観的
* 友人
* 口数
* 20文字
* 社交性
* IQ
* フレンドリー
* カジュアル
* 自然
"""

system_input_basis = st.text_area("System Basis Prompt", key="system_basis_input", height=200,
                                  value=system_input_basis_prompt)
st.write(f"知性(IQ)は{intelligence_value}, 社交性は{sociability_value}(知性と社交性に応じて下のプロンプトが変化します)")
system_input = st.text_area("System Prompt", key="system_input", height=200, value=system_input_prompt)
user_input = st.text_input("質問", key="user_input")

button = st.button("Submit")
if button or st.session_state.get("submit"):
    responce = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_input_basis + system_input},
            {"role": "user", "content": user_input}
        ],
        temperature=temperature,
    )
    st.write(f"{responce['choices'][0]['message']['content']}")

# st.write(system_input_basis + system_input)
