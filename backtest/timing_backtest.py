#固定标的资产择时 回测程序
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class strategy():
    def __init__(self):
        self.signal=None
        #这两个部分后面来开发
        self.limit=None
        self.position=None
        self.factor_name=None
    def single_factor(self,factor_name,long,short,close=None,method="M"):#long 和 short的数值必须添加 close后面开发
        self.factor_name=factor_name
        if method=="M":#指标动量
            self.signal=lambda x:1 if x>long else(-1 if x<short else 0)
        if method=="I":#指标反转
            self.signal=lambda x:1 if x<long else(-1 if x>short else 0)
        #可以建模做连续预测 来和仓位挂钩 后面开发
class timing_backtest():
    def __init__(self):
        self.account=pd.DataFrame(columns=["trade_date","cash","weight","value"])
        self.data=None
        #暂时不能做空 后面开发
        self.short_limit=False
        self.position=None
        #仓位暂不设置 后面开发
    def set_account(self,cash,position=None):
        self.account.loc[0]=["day0",cash,0,cash]
    def fit_data(self,data):
        self.data=data
    def run(self,strategy):
        account=self.account
        df=self.data[["trade_date","ts_code","close",strategy.factor_name]]
        #价格etf标准化
        df=df.copy()
        df["close"]=df["close"]/df.loc[0,"close"]
        #加载信号
        df=df.copy()
        df["signal"]=df[strategy.factor_name].apply(strategy.signal)
        #开始交易  每日的交易信息添加到account表上 这里其实可以设置回测日期 不过并不影响 这里默认是交易input表上所有日期
        for i in range(len(df.index)):
            #常规的每日信息等于现金加上持仓乘以今天的价格记录 如果需要交易则在两个逻辑分支里面修改这几个变量
            today_info=df.loc[i]
            pre_account=account.loc[i]
            cash=pre_account["cash"]
            weight=pre_account["weight"]
            value=cash+weight*today_info["close"]
            #信号为1 现金足够的情况下买入
            if pre_account["weight"]==0 and today_info["signal"]==1:
                cash=pre_account["cash"]%today_info["close"]
                weight=pre_account["cash"]//today_info["close"]
                value=weight*today_info["close"]+cash
                print("{}买入执行，买入价{}".format(today_info["trade_date"],today_info["close"]))
            #信号为-1 有持仓的情况下卖出
            elif pre_account["weight"]!=0 and today_info["signal"]==-1:
                cash=pre_account["weight"]*today_info["close"]+pre_account["cash"]
                weight=0
                value=cash
                print("{}卖出执行，卖出价{}".format(today_info["trade_date"], today_info["close"]))
            #将每日情况记录
            today_account = [today_info["trade_date"], cash, weight, value]
            account.loc[len(account.index)]=today_account

        #打印基础信息 这里方法将交易信息都存储到了account属性中 后面具体详细分析 可以加在analysis方法里面
        print("---------"*5,"result","---------"*5)
        print("start_value:",account.loc[0,"value"])
        print("end_value:",account.loc[max(account.index),"value"])
        print("totle_return",account.loc[max(account.index),"value"]/account.loc[0,"value"])
        self.account=account
    def analysis(self):
        #这里根据run方法得到的交易记录表进行详细分析 输出年化收益 夏普比率 最大回测 超额收益 交易单 画净值图
        #我只写了年化和夏普 还有回撤和交易单胜率这些可以添加 交易频率等等
        result_data=self.account.iloc[1:,:]
        result_data.reset_index(drop=True, inplace=True)
        result_data=result_data.copy()
        result_data["trade_date"]=pd.to_datetime(result_data["trade_date"])
        result_data["return"]=result_data["value"]/result_data.loc[0,"value"]
        result_data.index=pd.to_datetime(result_data["trade_date"])
        #取年化收益
        df_annual0=result_data["return"].resample("Y").ohlc()["close"]
        df_annual=df_annual0/df_annual0.shift(1)
        df_annual.fillna(df_annual0.iloc[0],inplace=True)
        print("-------年化收益-------")
        for i in range(len(df_annual.index)):
            print(df_annual.index[i].strftime("%Y"),df_annual[i])
        print("-----夏普比率-----")
        print("夏普比率为{}".format((df_annual.values.mean()-1)/df_annual.values.std()))
        #暂时之开发画净值图
        df_result=self.account
        data=self.data
        fig=plt.figure(figsize=(18,12))
        plt.plot(pd.to_datetime(df_result["trade_date"][1:]),df_result["value"][1:]/df_result.loc[0,"value"],label="strategy_value")
        plt.plot(pd.to_datetime(data["trade_date"]),data["close"]/data.loc[0,"close"],label="000300SH_value")
        plt.title("strategy_performance")
        plt.legend(fancybox=True,shadow=True)
        columns=["000300SH","strategy","excess"]
        rows=["final_return"]
        market_return=data.loc[max(data.index),"close"]/data.loc[0,"close"]
        strategy_return=df_result.loc[max(df_result.index),"value"]/df_result.loc[0,"value"]
        excessive_return=strategy_return-market_return
        values=[[market_return,strategy_return,excessive_return]]
        plt.table(cellText=values
                  ,cellLoc="center"
                  ,colLabels=columns
                  ,rowLabels=rows
                  ,colWidths=[0.1]*3
                  ,rowLoc="center"
                  ,loc="lower right")
        plt.show()
                  #留给后来者开发