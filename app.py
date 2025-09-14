import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

st.title('지역별/연도별 경제활동 데이터 조회')

# --- 사이드바 스타일 변경 ---
# CSS를 사용하여 사이드바의 배경색을 진한 색으로 지정합니다.
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #2E3B4E;
        color: white; /* 텍스트 색상 상속을 위해 추가 */
    }
    /* 위젯 라벨의 색상을 명시적으로 지정 */
    [data-testid="stSidebar"] label {
        color: white;
    }
    /* 체크박스 텍스트의 색상을 명시적으로 지정 */
   [data-testid="stSidebar"] [data-testid="stCheckbox"] p {
     color: yellow !important;
     }
    </style>
    """,
    unsafe_allow_html=True
)

df = pd.read_csv('경제활동_통합.csv')

df['지역'] = df['지역'].replace('계', '전국')

df['취업률'] = ((df['취업자 (천명)'] / df['경제활동인구 (천명)']) * 100).round(2)
df['실업률'] = ((df['실업자 (천명)'] / df['경제활동인구 (천명)']) * 100).round(2)

# '년도' 열의 값을 문자열로 변환하고 '년'을 붙입니다.
df['년도'] = df['년도'].astype(str) + '년'

# --- 데이터프레임 컬럼 순서 변경 ---
# '년도'와 '지역'을 맨 앞으로 가져옵니다.
new_cols = ['년도', '지역', '경제활동인구 (천명)', '취업자 (천명)', '실업자 (천명)', '취업률', '실업률']
df = df[new_cols]

@st.cache_data
def load_geojson():
    """대한민국 행정구역 GeoJSON 파일을 로드하고 캐시합니다."""
    url = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-provinces-2018-geo.json'
    response = requests.get(url)
    return response.json()


# --- 연도별 파이 그래프 (2x2 그리드) ---
st.subheader('연도별 취업률과 실업률')

# '전국' 데이터만 필터링하고 연도순으로 정렬
national_df = df[df['지역'] == '전국'].sort_values('년도')

# 데이터를 Plotly 파이 차트에 적합한 형태로 변환 (Long-format)
plot_data = national_df.melt(id_vars='년도', value_vars=['취업률', '실업률'], var_name='지표', value_name='비율')

# 1x4 그리드 생성을 위해 연도 리스트와 컬럼 리스트 준비
years = sorted(df['년도'].unique().tolist())
all_cols = st.columns(4)

# 연도별로 사용할 색상 팔레트 정의 (취업률, 실업률 순)
color_palettes = [
    ['#1f77b4', '#aec7e8'],  # Blue shades
    ['#2ca02c', '#98df8a'],  # Green shades
    ['#ff7f0e', '#ffbb78'],  # Orange shades
    ['#d62728', '#ff9896']   # Red shades
]

# 각 연도별로 파이 차트 생성 및 표시
for i, year in enumerate(years):
    if i < len(all_cols): # 연도 개수가 4개 이상일 경우를 대비
        with all_cols[i]:
            year_data = plot_data[plot_data['년도'] == year]
            fig = px.pie(year_data, 
                         names='지표', 
                         values='비율', 
                         title=year,
                         hole=0.4, # 도넛 차트 형태
                         color_discrete_sequence=color_palettes[i % len(color_palettes)]) # 연도별 다른 색상 적용
            fig.update_traces(textposition='inside', textinfo='label+percent', sort=False)
            fig.update_layout(showlegend=False, title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

# --- 사이드바 필터 ---
st.sidebar.title('검색 조건')

# '년도' 선택 (다중 선택)
year_options = sorted(df['년도'].unique().tolist())
selected_years = st.sidebar.multiselect(
    '년도를 선택하세요.',
    year_options,
    default=year_options # 기본값으로 모든 년도 선택
)

# '지역' 선택
# '전국'을 제외한 나머지 지역 리스트를 만듭니다.
region_list = sorted(df['지역'].unique().tolist())
if '전국' in region_list:
    region_list.remove('전국')
# '전국'을 맨 앞에 추가하여 최종 선택 목록을 만듭니다.
region_options = ['전국'] + region_list

# '전지역 보기' 체크박스
show_all_regions = st.sidebar.checkbox("전지역")

# 지역 선택 multiselect (체크박스가 선택되면 비활성화됩니다)
selected_regions = st.sidebar.multiselect(
    '지역을 선택하세요.',
    region_options,
    default=['전국'], # 기본값으로 '전국' 선택
    disabled=show_all_regions
)

# --- 데이터 필터링 및 표시 ---
# 원본 데이터프레임을 보존하기 위해 복사본을 만듭니다.
filtered_df = df.copy()

# 1. 년도 필터링
filtered_df = filtered_df[filtered_df['년도'].isin(selected_years)]

# 2. 지역 필터링: 체크박스 상태에 따라 데이터를 필터링합니다.
if show_all_regions:
    # 체크박스 선택 시 '전국'을 제외한 모든 지역 데이터를 보여줍니다.
    filtered_df = filtered_df[filtered_df['지역'] != '전국']
else:
    # 체크박스가 선택되지 않은 경우, 선택된 지역들의 데이터만 보여줍니다.
    filtered_df = filtered_df[filtered_df['지역'].isin(selected_regions)]


# 필터링된 결과를 화면에 표시합니다.
st.subheader('상세 데이터')
st.dataframe(filtered_df)

# --- 필터링된 데이터 그래프 시각화 ---
# 필터링된 데이터가 있을 경우에만 그래프를 그립니다.
if not filtered_df.empty:
    # '전지역'이 선택된 경우, 대한민국 지도를 표시합니다.
    if show_all_regions:
        if selected_years:
            # 선택된 연도 중 가장 최신 연도를 기준으로 지도를 그립니다.
            latest_year = sorted(selected_years)[-1]
            st.subheader(f'**{latest_year} 대한민국 취업률 지도**')

            map_data = filtered_df[filtered_df['년도'] == latest_year].copy()
            # GeoJSON과 데이터의 지역명 일치시키기 (예: 제주도 -> 제주특별자치도)
            map_data['지역'] = map_data['지역'].replace('제주도', '제주특별자치도')
            
            geojson = load_geojson()

            # 1. 기본 Choropleth 지도 생성
            fig_map = px.choropleth(
                map_data,
                geojson=geojson,
                locations='지역',
                featureidkey='properties.name',
                color='취업률',
                color_continuous_scale='Blues',
            )

            # 2. 지도 위에 텍스트(취업률)를 표시하기 위한 Scattergeo 트레이스 추가
            fig_map.add_trace(
                go.Scattergeo(
                    geojson=geojson,
                    locations=map_data['지역'],
                    featureidkey='properties.name',
                    text=map_data['취업률'].astype(str) + '%', # 표시할 텍스트
                    mode='text',
                    textfont=dict(color='black', size=10),
                    showlegend=False
                )
            )

            fig_map.update_geos(fitbounds="locations", visible=False)
            # 3. 레이아웃 업데이트: 색상 막대 제거 및 제목 설정
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                coloraxis_showscale=False  # 색상 막대 제거
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("지도를 표시하려면 하나 이상의 년도를 선택해주세요.")
    # 특정 지역이 선택된 경우, 막대 그래프를 표시합니다.
    else:
        title_years = ', '.join(selected_years)
        st.subheader(f'**{title_years} 데이터 시각화**')

        # 취업률 막대 그래프
        fig_emp = px.bar(filtered_df, x='지역', y='취업률', color='년도', barmode='group', title='지역별 취업률', text_auto=True)
        st.plotly_chart(fig_emp, use_container_width=True)

        # 실업률 막대 그래프
        fig_unemp = px.bar(filtered_df, x='지역', y='실업률', color='년도', barmode='group', title='지역별 실업률', text_auto=True)
        st.plotly_chart(fig_unemp, use_container_width=True)
