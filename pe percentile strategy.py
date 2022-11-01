import pandas as pd
import tushare as ts
ts.set_token("Your token here.")
pro=ts.pro_api()
import numpy as np
df=pro.index_dailybasic(ts_code="000300.SH",start_date="20130101",end_date="20210101"
                       ,fields="ts_code,trade_date,total_mv,total_share,pe,pb")
df["trade_date"]=pd.to_datetime(df["trade_date"])
df=df.set_index(["trade_date"])
df=df.sort_index(ascending=True)
df["pe_25"]=df["pe"].rolling(350).quantile(0.25)
df["pe_75"]=df["pe"].rolling(350).quantile(0.75)
df=df.dropna()
price=df["total_mv"].iloc[0,]/df["total_share"].iloc[0,]
print(price)
df["b_close"]=df["total_mv"]/df["total_share"]/price
print(df)
date=df.index
cash=[1000]
weight=[0]
value=[1000]
counter=0
for i in date:
    cash0=0
    weight0=0
    if weight[counter]!=0:
        if df.loc[i,"pe"]>df.loc[i,"pe_75"]:
            print(i,"sell")
            cash0=weight[counter]*df.loc[i,"b_close"]
            weight0=-weight[counter]
    if cash[counter]>df.loc[i,"b_close"]:
        if df.loc[i,"pe"]<df.loc[i,"pe_25"]:
            print(i,"buy")
            weight0=cash[counter]/df.loc[i,"b_close"]
            cash0=-weight0*df.loc[i,"b_close"]
    cash_td=cash[counter]+cash0
    weight_td=weight[counter]+weight0
    value_td=cash_td+weight_td*df.loc[i,"b_close"]
    cash.append(cash_td)
    weight.append(weight_td)
    value.append(value_td)
    counter=counter+1
#get_result
arr=np.array([cash[1:],value[1:]])
df_result=pd.DataFrame(arr.T,columns=["cash","value"],index=date)
df_result["return"]=df_result["value"]/1000
df_result["trade_date"]=df_result.index
print(df_result)
import matplotlib.pyplot as plt
plt.figure(figsize=(18,12))
plt.plot(df.index,df_result["return"],label="strategy_return")
plt.plot(df.index,df["b_close"],label="000300Sh_return")
plt.title("PE Strategy")
plt.legend(fancybox=True
           ,shadow=True)
plt.show()
