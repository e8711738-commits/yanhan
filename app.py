import streamlit as st

def analyze_sentiment(text: str) -> int:
    '''
    模擬情緒分析，將輸入文字轉換為 1 到 5 的評分等級。
    1: 非常差 (Highly Negative)
    2: 差 (Negative)
    3: 普通 (Neutral)
    4: 好 (Positive)
    5: 非常好 (Highly Positive)
    '''
    very_positive_words = ['完美', '超讚', '極推', '神作', '無可挑剔', '太棒了', '強烈推薦']
    positive_words = ['好用', '不錯', '喜歡', '推薦', '滿意', '實用', '好', '棒', '讚']
    
    negative_words = ['爛', '差', '難用', '失望', '後悔', '雷', '不推', '糟糕', '不滿意', '破東西', '壞了']
    very_negative_words = ['垃圾', '極差', '絕對不要買', '騙人', '死當', '災難', '超級爛', '爛透了']
    
    temp_text = text.lower()
    temp_text = temp_text.replace('非常', '超級')
    temp_text = temp_text.replace('無可挑剔', '完美')
    
    negation_words = ['不', '沒', '無', '非', '別']
    score = 3.0
    
    negation_found = False
    for neg in negation_words:
        if neg in temp_text:
            negation_found = True
            break
            
    pos_score = 0
    for word in very_positive_words:
        if word in temp_text:
            pos_score += 2.0
    for word in positive_words:
        if word in temp_text:
            if negation_found:
                pos_score -= 1.0
            else:
                pos_score += 1.0
                
    neg_score = 0
    for word in very_negative_words:
        if word in temp_text:
            neg_score += 2.0
    for word in negative_words:
        if word in temp_text:
            neg_score += 1.0
            
    score = score + pos_score - neg_score
    final_rating = round(max(1.0, min(5.0, score)))
    return int(final_rating)

# Streamlit 網頁佈局與元件
st.set_page_config(page_title="中文評論情緒分析系統", page_icon="📊")
st.title("💬 中文評論情緒分析系統")
st.write("請在下方輸入您的產品評論，點擊按鈕後，系統將模擬並預測其情緒評分（1 至 5 等級）。")

# 文字輸入框
user_input = st.text_area("請輸入產品評論內容：", placeholder="例如：這個產品真的超讚，非常推薦大家買，好用！")

# 偵測按下按鈕時執行預測
if st.button("分析情緒評分"):
    if user_input.strip() == "":
        st.warning("⚠️ 請輸入一些文字進行分析！")
    else:
        rating = analyze_sentiment(user_input)
        st.subheader("📊 預測結果")
        
        # 依分數給予不同色彩提示與說明
        stars = "★" * rating + "☆" * (5 - rating)
        st.markdown(f"### 評分結果：**{rating} / 5 分**")
        st.markdown(f"### 星等呈現：<span style='color: #FFD700; font-size: 24px;'>{stars}</span>", unsafe_allow_html=True)
        
        if rating >= 4:
            st.success("🎉 偵測結果：正面評論 (Positive Sentiment)")
        elif rating == 3:
            st.info("😐 偵測結果：中性評論 (Neutral Sentiment)")
        else:
            st.error("🚨 偵測結果：負面評論 (Negative Sentiment)")
