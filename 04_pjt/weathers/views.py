from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from io import  BytesIO
import base64

# Create your views here.

# 1. csv 데이터를 판다스 df 형식으로 저장 및 html 렌더링
csv_path = 'weathers/data/austin_weather.csv'

def problem1(request):
    df = pd.read_csv(csv_path)
    context = {
        'df': df,
    }
    return render(request, 'weathers/problem1.html', context)


# 2. 일 별 최고, 평균, 최저 온도를 선 그래프로 출력
def problem2(request):
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])
    
    plt.clf()

    plt.plot(df["Date"], df["TempHighF"], linewidth='0.7', label='High Temperature')
    plt.plot(df["Date"], df["TempAvgF"], linewidth='0.7', label='AverageTemperature')
    plt.plot(df["Date"], df["TempLowF"], linewidth='0.7', label='Low Temperature')
    plt.grid(True)
    plt.legend(loc='lower center')

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature (Fahrenheit)')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, 'weathers/problem2.html', context)


# 3. 월 별 최고, 평균, 최저 온도의 평균을 선 그래프로 출력
def problem3(request):
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    # df['TempHighF'] = pd.to_numeric(df['TempHighF'])
    # df['TempAvgF'] = pd.to_numeric(df['TempAvgF'])
    # df['TempLowF'] = pd.to_numeric(df['TempLowF'])
    df['Month'] = df['Date'].dt.to_period('M')
    # df_month = df.groupby(by=df["Date"].dt.strftime("%Y-%m")).mean()
    # df_month = pd.DataFrame()
    # df_month['Month'] = df['Month']
    # df_month['TempHighF'] = df.groupby(by=df['Month'])['TempHighF'].mean()
    # df_month['TempAvgF'] = df.groupby(by=df['Month'])['TempAvgF'].mean()
    # df_month['TempLowF']  = df.groupby(by=df['Month'])['TempLowF'].mean()
    # x = df['Month']
    # y1 = df.groupby(by=df['Month'])['TempHighF'].mean()
    # y2 = df.groupby(by=df['Month'])['TempAvgF'].mean()
    # y3 = df.groupby(by=df['Month'])['TempLowF'].mean()
    month_avg_high = df.resample('M', on='Date')['TempHighF'].mean()
    month_avg_avg = df.resample('M', on='Date')['TempAvgF'].mean()
    month_avg_low = df.resample('M', on='Date')['TempLowF'].mean()
    
    plt.clf()

    # plt.plot(df_month['Month'], df_month["TempHighF"], linewidth='0.7', label='High Temperature')
    # plt.plot(df_month['Month'], df_month["TempAvgF"], linewidth='0.7', label='AverageTemperature')
    # plt.plot(df_month['Month'], df_month["TempLowF"], linewidth='0.7', label='Low Temperature')
    plt.plot(month_avg_high, linewidth='0.7', label='High Temperature')
    plt.plot(month_avg_avg, linewidth='0.7', label='AverageTemperature')
    plt.plot(month_avg_low, linewidth='0.7', label='Low Temperature')
    plt.grid(True)
    plt.legend(loc='lower right')

    plt.title('Temperature Variation')
    plt.xlabel('Date')
    plt.ylabel('Temperature (Fahrenheit)')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, 'weathers/problem3.html', context)


# 4. 기상 현상 발생 횟수 히스토그램 출력
def problem4(request):
    df = pd.read_csv(csv_path)
    # no_event = df['Events'].value_counts(dropna=False)[' ']
    # df[['Event_1', 'Event_2', 'Event_3']] = df['Events'].str.split(',', expand=True)
    # ev1_cnt = df['Event_1'].value_counts()
    # ev2_cnt = df['Event_2'].value_counts()
    # ev3_cnt = df['Event_3'].value_counts()
    # rain = ev1_cnt['Rain'] + ev2_cnt['Rain'] + ev3_cnt['Rain']
    # thunderstorm = ev1_cnt['Thunderstorm'] + ev2_cnt['Thunderstorm'] + ev3_cnt['Thunderstorm']
    # fog = ev1_cnt['Fog'] + ev2_cnt['Fog'] + ev3_cnt['Fog']
    # snow = ev1_cnt['Snow'] + ev2_cnt['Snow'] + ev3_cnt['Snow']

    # x = [0,1,2,3,4]
    # y = [no_event, rain, thunderstorm, fog, snow]
    # events = ['No Event', 'Rain', 'Thunderstorm Events', 'Fog', 'Snow']
    cnt_df = df.Events.str.split(' , ').explode().replace(' ', 'No Events')
    event_cnt = cnt_df.value_counts()

    plt.clf()

    # plt.bar(x, y, width=0.5, color='blue')
    # plt.xticks(x, events)
    plt.bar(event_cnt.index, event_cnt.values)
    plt.grid(True)

    plt.title('Event Counts')
    plt.xlabel('Events')
    plt.ylabel('Count')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()

    context = {
        'chart_image': f'data:image/png;base64,{image_base64}'
    }
    return render(request, 'weathers/problem4.html', context)