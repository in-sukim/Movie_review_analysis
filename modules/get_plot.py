import warnings
warnings.filterwarnings('ignore')
import json
from tqdm import tqdm

import torch
from transformers import BertTokenizer

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# custom_module
import modules.sentiment_model as sentiment_model
import modules.review_prepare as review_prepare

# 혐오표현 모델 추가 예정


# In[128]:


class reivew_analysis():
    def __init__(self, 
                 keywords, 
                 page: int = 2, 
                 model_name = 'klue/bert-base',
                 sentiment_model_path = './modules/nsmc_clf_ver1.pth',
                 model = sentiment_model.NSMCClassifier()
                ):
                 
        # 검색대상
        self.keywords = keywords
        self.page = page
        self.model_name = model_name
        
        self.sentiment_model_path = sentiment_model_path
        self.model = model
        self.model.load_state_dict(torch.load(f = self.sentiment_model_path))
        
                 
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.data = review_prepare.daum(keywords, page)

        self.review_list = []    
        
        self.predcit_review()
    def predcit_review(self):
        
        for i in tqdm(self.data.text, desc = '리뷰 긍부정 분류 중'):
            
            output = self.tokenizer.encode_plus(
                str(i),
                add_special_tokens=True,
                return_tensors='pt',
                truncation=True,
                padding='max_length',
                max_length= 80,
                return_attention_mask = True,
                return_token_type_ids=False
            )
            
            input_ids = output['input_ids']
            attention_mask = output['attention_mask']

            loss, output = self.model(input_ids, attention_mask)
        
            prediction = torch.argmax(output, dim=1).numpy().tolist()
        
            if prediction[0] == 0:
                prediction = '부정'
            else:
                prediction = '긍정'
            self.review_list.append(prediction)
        
        self.data['label'] = self.review_list
        
        return self.data
    
    def create_plot(self):
        fig = make_subplots(
            rows=1, 
            cols=2, 
            specs=[[{"type": "bar"}, {"type": "pie"}]],
            subplot_titles=("평점 별 빈도수 막대그래프", "긍/부정별 빈도수 파이차트") 
        )

        bar_df = self.data.value_counts('rating').to_frame('count').reindex([str(i) for i in range(11)]).fillna(0)

        fig.add_trace(
            go.Bar(
                x = bar_df.index.tolist(), 
                y = bar_df['count'], 
                hovertemplate = '평점: %{x}<br>갯수: %{y:$/0f}<extra></extra>',
                marker = {
                    'color':'#4085f5',# 막대 색상 또는 리스트를 이용하여 각 막대 색상 변경가능
                    'line':{'color':'black', 'width':3} # 막대 테두리 설정
                }
            ),
            row=1, 
            col=1
        )

        pie_df = self.data.value_counts('label').to_frame('count')
        go.Pie(labels=pie_df.index.tolist(),
               values=pie_df['count']
              )

        fig.add_trace(
            go.Pie(
                labels= pie_df.index.tolist(), 
                values= pie_df['count'],
                textinfo='label+percent',
                hovertemplate = '갯수: %{value}<extra></extra>'
                # hovertemplate = '갯수: %{value}<br>Percent: %{percent:.2f}<extra></extra>'
            ),
            row = 1,
            col = 2
        )

        fig.update_layout(margin=dict(l=120, r=120, t=120, b=120),
                         hovermode = 'closest',
                         showlegend=False,
                         plot_bgcolor='white',
                         clickmode = 'event+select')
        return fig


# # 파이차트 Hover or Click 하면 해당 긍/부정 카테코리의 WordCloud 생성






