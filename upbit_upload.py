################

# 1. 사이클이 한번 돌때 초기값 세팅에서
#   - 이전 초기값보다 현재 가격이 높으면 갱신하지 않고
#   - 이전 초기값보다 현재 가격이 낮으면 갱신 

# 2. 매수 / 매도 는 별도의 코드에서
# 
# 3. 매도는 짧은 사이클, 긴 사이클 두개로 
#  
# 4. 매도 할때
#   - 이전 가격보다 현재 가격이 낮으면 갱신하지 않고
#   - 이전 가격보다 현재 가격이 높으면 갱신
#  
################




import pyupbit
import time
import math
import telegram
import datetime
from tkinter import *
from multiprocessing import Process

##### telebot #####
telgm_token = ''
bot = telegram.Bot(token = telgm_token)
chat = ""

 
##### key #####
access_key = ''
secret_key = ''
key_ok = False
set_ok = True

money = 0
sep_num = 0
buy_percent = 0
sell_percent1 = 0
sell_percent2 = 0
# upbit = pyupbit.Upbit(access_key, secret_key)


######################################################################

def enter_key():
    print("KEY가 삽입되었습니다.")
    txt.insert(END, "{}  KEY가 삽입되었습니다.\n".format(time.strftime('%H:%M:%S')))
    global access_key
    global secret_key
    access_key = access_entry.get()
    secret_key = secret_entry.get()

    upbit = pyupbit.Upbit(access_key, secret_key)   # 업비트 키 삽입

    i_balance = upbit.get_balances()
    # print(i_balance)

    try:
        txt.insert(END, "{}  지갑 잔고가 출력됩니다.\n".format(time.strftime('%H:%M:%S')))
        i.delete("1.0", END)
        global key_ok
        key_ok = True

        print(i_balance)

        for coin_name in i_balance:        # 지갑 잔고 

            if coin_name["currency"] == "KRW":
                have_money = int(float(coin_name["balance"]))
                i.insert(END, "보유 금액 : {:,} 원\n\n".format(have_money))
                continue

            if coin_name["currency"] == "USDT" or coin_name["currency"] == "BTC" or coin_name["currency"] == "ETH":
                continue

            print(coin_name["currency"])
            i_price = pyupbit.get_current_price("KRW-{}".format(coin_name["currency"]))
            i.insert(END, "{} : {:,} 원\n".format(coin_name["currency"], int((float(i_price) * float(coin_name['balance'])))))
            root.update()

    except Exception as e:
        print(e)
        txt.insert(END, "{}  key error 다시 입력하세요.\n".format(time.strftime('%H:%M:%S')))
        root.update()



######################################################################

def set_risk():

    access_key = access_entry.get()
    secret_key = secret_entry.get()



    upbit = pyupbit.Upbit(access_key, secret_key)   # 업비트 키 삽입
    
    

    # print("set_risk")
    global money
    global get_percent
    global sep_num
    global buy_percent
    global sell_percent1
    global sell_percent2

    money = int(set_money.get())
    get_percent = float(set_get.get())
    sep_num = int(set_buy_num.get())
    buy_percent = float(set_buy.get())
    sell_percent1 = float(set_sell1.get())
    sell_percent2 = float(set_sell2.get())

    use_money = int(float(upbit.get_balances()[0]["balance"])) - money

    if use_money / sep_num <= 5100:
        txt.insert(END, "분할 매수 갯수를 재입력하세요.\n")
        set_ok = True

    else:
        set_ok = True

    if set_ok == True:

        print("\nSetting Complete")
        txt.insert(END, "{}  셋팅되었습니다.\n".format(time.strftime('%H:%M:%S')))
        txt.insert(END, "{}  안전 금액 : {:,} 원\n".format(time.strftime('%H:%M:%S'), money))
        txt.insert(END, "{}  목표 수익률 : {}%\n".format(time.strftime('%H:%M:%S'), get_percent))
        txt.insert(END, "{}  분할 매수 갯수 : {}개\n".format(time.strftime('%H:%M:%S'), sep_num))
        txt.insert(END, "{}  매수 퍼센트 : {}%\n".format(time.strftime('%H:%M:%S'), buy_percent))
        txt.insert(END, "{}  매도 급락 퍼센트 : {}%\n".format(time.strftime('%H:%M:%S'), sell_percent1))
        txt.insert(END, "{}  매도 장기 퍼센트 : {}%\n".format(time.strftime('%H:%M:%S'), sell_percent2))

        i.insert(END, "사용 할 금액 : {:,}\n".format(use_money))

        buy_percent = buy_percent / 100
        get_percent = get_percent / 100
        sell_percent1 = sell_percent1 / 100 * -1
        sell_percent2 = sell_percent2 / 100 * -1
        # sell_percent1 = float(sell_percent1 / 100) * -1
        # sell_percent2 = float(sell_percent2 / 100) * -1

######################################################################

def reset_coin():
    access_key = access_entry.get()
    secret_key = secret_entry.get()

    upbit = pyupbit.Upbit(access_key, secret_key)   # 업비트 키 삽입

    i_balance = upbit.get_balances()    # 지갑 정보 불러오기 

    for coin in i_balance[1:]:
        if coin["currency"] == "USDT" or coin["currency"] == "BTC" or coin["currency"] == "ETH":
            continue
        print(coin["currency"])
        coin_num = coin["balance"]
        print(coin_num)
        upbit.sell_market_order("KRW-{}".format(coin["currency"]), coin_num)
        time.sleep(0.1)

    txt.insert(END, "{}  알트코인을 정리했습니다.\n".format(time.strftime('%H:%M:%S')))
    i.delete("1.0", END)
    i.insert(END, "보유 금액 : {:,} 원\n\n".format(int(float(i_balance[0]["balance"]))))


    





######################################################################

def auto_order():

    if key_ok == True:
        print("\n1. key 이상없음")
        # print(set_ok)
        if (set_ok == True) and (money != 0) and (buy_percent != 0) and (sell_percent1 != 0) and (sell_percent2 != 0):
            print("\n2. 셋팅값 이상 없음")

            th1 = Process(target=buy_order, args=(access_key, secret_key, money, sep_num, buy_percent, sell_percent1, sell_percent2, telgm_token, chat, get_percent,))
            th2 = Process(target=sell_order, args=(access_key, secret_key, money, sep_num, buy_percent, sell_percent1, sell_percent2, telgm_token, chat, get_percent,))

            th1.start()
            th2.start()
            th1.join()
            th2.join()


        else:
            txt.insert(END, "{}  Setting 값을 확인하세요. (0, 음수는 불가)\n".format(time.strftime('%H:%M:%S')))
    else:
        txt.insert(END, "{}  KEY를 입력하세요.\n".format(time.strftime('%H:%M:%S')))



######################################################################

def buy_order(access_key, secret_key, money, sep_num, buy_percent, sell_percent1, sell_percent2, telgm_token, chat, get_percent):
    
    i_coinlist = []

    upbit = pyupbit.Upbit(access_key, secret_key)

    f_name = "buy_order"

    print("\n----- 자동 매매를 시작합니다.-----\n")


    tickers = pyupbit.get_tickers(fiat = 'KRW')
    # print(tickers)

    price_dict_buy = {}
    
    for coin in tickers:        # 초기값 딕셔너리로
        if coin == 'USDT' or coin == 'KRW-BTC' or coin == 'KRW-ETH':
            continue    # 비트, 이더 제외
        # print(coin)

        time.sleep(0.1)

        price_dict_buy[coin]= pyupbit.get_current_price(coin)   # 현재가
        # print(coin)
        if price_dict_buy[coin] == None:
            while True:
                price_dict_buy[coin]= pyupbit.get_current_price(coin)    # 현재가
                if price_dict_buy[coin] != None:
                    break
                time.sleep(0.1)

        time.sleep(0.1)
    print("#######################################")
    print("#######################################")
    print("############ 초기값 셋팅 완료 #############")
    print("#######################################")
    print("#######################################")
    print("코인 총 개수: ", len(tickers))       #114
    print("시작시간 - {}".format(time.strftime('%H:%M:%S')))
    bot.sendMessage(chat, "⏱⏱ 시작시간 ⏱⏱ - {}".format(time.strftime('%H:%M:%S')))
    # txt.insert(END, "초기값 셋팅 완료\n")
    # root.update()


    while True:
        # 지갑 내 코인 리스트 관리
        try:
            i_coin = upbit.get_balances()
            
            # 지갑 내 코인 리스트 생성 (최신화)
            i_coinlist = []
            
            for coin in i_coin[1:]:
                # 비트, 이더 제외
                if coin["currency"] == "USDT" or coin["currency"] == "BTC" or coin["currency"] == "ETH":
                    continue

                # 지갑 내 코인리스트에 추가 
                i_coinlist.append("KRW-{}".format(coin["currency"]))

            print("아이 코인 리스트")
            print("아이 코인 리스트")
            print("아이 코인 리스트")
            print(i_coinlist)


            try:
                for check_coin in i_coinlist:
                    
                    print("## check_coin  ##     ", check_coin)
                    print("## price_dict  ##     ", price_dict_buy)

                    if (check_coin in price_dict_buy) == True:   # 삭제
                        del price_dict_buy[check_coin]
                    print("## price_dict (after) ##", price_dict_buy)
            except:
                pass

            try:
                for check_coin in tickers:
                    time.sleep(0.06)
                    if check_coin == "USDT" or check_coin == "KRW-BTC" or check_coin == "KRW-ETH":
                        continue

                    if check_coin not in i_coinlist:
                        
                        if (check_coin in price_dict_buy) == False:
                            price_dict_buy[check_coin] = pyupbit.get_current_price(check_coin)

                            if price_dict_buy[check_coin] == None:
                                while True:
                                    time.sleep(0.1)
                                    price_dict_buy[check_coin] = pyupbit.get_current_price(check_coin)
                                    if price_dict_buy[check_coin] != None:
                                        break

            except:
                pass



            print("############################################")
            print("현재 감시 코인: ", len(price_dict_buy))
            print("############################################")
            
            for coin in price_dict_buy.keys():

                if coin == 'USDT' or coin == 'KRW-BTC' or coin == 'KRW-ETH':
                    continue    # 비트, 이더 제외

                while True:     # 딕셔너리의 코인 하나하나
                    try:
                        check_i_coin = upbit.get_balances()
                        check_coin_num = 0      # 내가 가지고 있는 코인 갯수
                        
                        for i in check_i_coin[1:]:
                            if i["currency"] == "USDT" or i["currency"] == "BTC" or i["currency"] == "ETH":
                                continue
                            check_coin_num += 1

                        time.sleep(0.06)
                        
                        now_price = pyupbit.get_current_price(str(coin)) # 현재가

                        if float(price_dict_buy[coin]) >= float(now_price):     # 과거 가격이 높으면 지금 가격이 초기값
                            price_dict_buy[coin]= now_price   # 초기값 재설정
                        
                        prev_price = price_dict_buy[coin]       

                        if check_coin_num >= sep_num:
                            price_dict_buy[coin]= now_price   # 초기값 재설정


                        percent = (float(now_price)/float(prev_price))-1
                        print("{}  ".format(time.strftime('%H:%M:%S')), coin[4:], '  이전가: {} / 현재가: {} / 퍼센트: {}'.format(prev_price, now_price, percent))
                        

                        ##### 매수 매수 ######
                        if percent >= buy_percent:
                            # 사용할 금액 (use_money)
                            use_money = int(float(check_i_coin[0]["balance"])) - int(money)

                                
                            for c in range(0, sep_num+1):
                                if use_money <= 5100 or sep_num == check_coin_num:
                                    buy_ok == False
                                    break

                                else:
                                    buy_ok = True



                                if (c == check_coin_num) and (buy_ok == True):
                                    i_buy_money = (float(use_money)/(sep_num - check_coin_num))
                                    try:
                                        if (i_buy_money <= 5100):
                                            i_buy_money = 5100

                                        time.sleep(0.8)
                                        percent2 = (float(pyupbit.get_current_price(str(coin)))/float(prev_price))-1

                                        if percent2 >= buy_percent:


                                            upbit.buy_market_order(coin, int(i_buy_money))
                                            bot.sendMessage(chat, "🔴 매수 🔴\n시각 - {}\nCoin name : {}\n쓴 돈 : {}\n".format(time.strftime('%H:%M:%S'), coin, i_buy_money))

                                    except:
                                        pass


                    except Exception as e:
                        print(e)
                        print("__________", f_name, "    ", e)
                        time.sleep(0.1)
                        continue

                    break

            print("________________________________________________")   

            time.sleep(0.5)

        except Exception as e:
            pass

######################################################################

def sell_order(access_key, secret_key, money, sep_num, buy_percent, sell_percent1, sell_percent2, telgm_token, chat, get_percent):

    f_name = "sell_order"
    price_dict = {}
    price_add = {}
    i_coinlist = []

    upbit = pyupbit.Upbit(access_key, secret_key)

    i_coin = upbit.get_balances()

    for coin in i_coin[1:]:
        
        coin_name = coin["currency"]
        
        if coin_name == "USDT" or coin_name == "BTC" or coin_name == "ETH":
            continue


        try:
            # 초기값
            price_first = pyupbit.get_current_price('KRW-{}'.format(coin_name))
            
            if price_first == None:
                while True:
                    price_first = pyupbit.get_current_price('KRW-{}'.format(coin_name))
                    time,sleep(0.1)
                    if price_first != None:
                        break

            # 급락 초기값
            price_dict['KRW-{}'.format(coin_name)] = price_first
            
            # 누적 초기값
            price_add['KRW-{}'.format(coin_name)] = price_first
        except:
            # print(e)
            pass


        time.sleep(0.2)


    time.sleep(5)

    while True:
        time.sleep(0.1)
        try:
            i_coin = upbit.get_balances()
            
            # 지갑 내 코인 리스트 생성 
            i_coinlist = []
            for coin in i_coin[1:]:
                # 비트, 이더 제외
                if coin["currency"] == "USDT" or coin["currency"] == "BTC" or coin["currency"] == "ETH":
                    continue

                # 지갑 내 코인리스트에 추가 
                i_coinlist.append("KRW-{}".format(coin["currency"]))

            try:
                for check_coin in i_coinlist:
                    if (check_coin in price_dict) == False: # dict 에 없으면
                        while True:
                            price_dict[check_coin] = pyupbit.get_current_price('{}'.format(check_coin))
                            if price_dict[check_coin] != None:
                                break
            except:
                pass

            try:
                for check_coin in i_coinlist:
                    if (check_coin in price_add) == False: # add 에 없으면
                        while True:
                            price_add[check_coin] = pyupbit.get_current_price('{}'.format(check_coin))
                            if price_add[check_coin] != None:
                                break
            except:
                pass




            if len(price_dict) > len(i_coinlist) or len(price_add) > len(i_coinlist):  # 삭제
                try:
                    for check_coin in price_dict.keys():
                        if check_coin not in i_coinlist:
                            del price_dict[check_coin]                
                except:
                    pass
                
                try:
                    for check_coin in price_add.keys():
                        if check_coin not in i_coinlist:
                            del price_add[check_coin]                
                except:
                    pass
                

            for coin in i_coin[1:]:
                # 급락
                coin_name = coin["currency"]

                # 비트, 이더 제외
                if coin_name == "USDT" or coin_name == "BTC" or coin_name == "ETH":
                    continue

                
                prev_price = price_dict['KRW-{}'.format(coin_name)]
                now_price = pyupbit.get_current_price('KRW-{}'.format(coin_name))
                
                percent_dict = (float(now_price)/float(prev_price))-1

                price_dict['KRW-{}'.format(coin_name)] = now_price

                if float(now_price) >= float(price_add['KRW-{}'.format(coin_name)]):   # 고점 갱신
                    price_add['KRW-{}'.format(coin_name)] = now_price

                percent_add = (float(now_price)/float(price_add['KRW-{}'.format(coin_name)]))-1

                print("@ time  |  ", time.strftime('%H:%M:%S'))
                print("@ name  |  ", coin["currency"])
                print("@ price |  ", now_price)
                print("@ dict  |  ", percent_dict)
                print("@ add   |  ", percent_add)

                i_sell_num = coin["balance"]    # 돌고있는 코인의 갯수

                avg_price = float(coin["avg_buy_price"])
                print(avg_price)
                goal_percent = (float(now_price) - avg_price) / avg_price
                print("@ 수익   |  ", goal_percent)

                if get_percent <= goal_percent:
                    upbit.sell_market_order("KRW-{}".format(coin_name), i_sell_num)
                    bot.sendMessage(chat, "🔵 매도(수익 - {} ) 🔵\n시각 - {}\nCoin name : {}\n판매가: {:,}\n".format( goal_percent, time.strftime('%H:%M:%S'), coin_name, int(float(now_price) * float(i_sell_num)) ))



                if percent_dict <= sell_percent1:
                    bot.sendMessage(chat, "🔵 매도(단기 확인 - {} ) 🔵\n시각 - {}\nCoin name : {}\n판매가: {}\n".format(sell_percent1, time.strftime('%H:%M:%S'), coin_name, int(float(now_price) * float(i_sell_num)) ))
                    time.sleep(2)

                    percent_dict2 = (float(pyupbit.get_current_price('KRW-{}'.format(coin_name)))/float(prev_price))-1

                    
                    if percent_dict2 <= sell_percent2:
                        upbit.sell_market_order("KRW-{}".format(coin_name), i_sell_num)
                        bot.sendMessage(chat, "🔵 매도(단기 - {} ) 🔵\n시각 - {}\nCoin name : {}\n판매가: {:,}\n".format( sell_percent1, time.strftime('%H:%M:%S'), coin_name, int(float(now_price) * float(i_sell_num)) ))
                

                if percent_add <= sell_percent2:
                    bot.sendMessage(chat, "🔵 매도(누적 확인 - {} ) 🔵\n시각 - {}\nCoin name : {}\n판매가: {}\n".format(sell_percent2, time.strftime('%H:%M:%S'), coin_name, int(float(now_price) * float(i_sell_num)) ))
                    time.sleep(2)

                    percent_add2 = (float(pyupbit.get_current_price('KRW-{}'.format(coin_name)))/float(price_add['KRW-{}'.format(coin_name)]))-1
                    print("매도 percent_add2 : ", percent_add2)
                    print("매도 sellpercent3 : ", sell_percent2)
                    if percent_add2 <= sell_percent2:
                        upbit.sell_market_order("KRW-{}".format(coin_name), i_sell_num)

                        # bot.sendMessage(chat, "{}  {} {} 장기하락 / 현재가: {}\n".format(time.strftime('%H:%M:%S'), coin_name, percent_add, now_price))
                        bot.sendMessage(chat, "🔵 매도(누적 - {} ) 🔵\n시각 - {}\nCoin name : {}\n판매가: {}\n".format(sell_percent2, time.strftime('%H:%M:%S'), coin_name, int(float(now_price) * float(i_sell_num)) ))
                        

                time.sleep(0.1)
                print(" ")


        except Exception as e:
            pass

        print("@ 보유 코인 현황  |   ", i_coinlist)   
        print(" ")   
        print("________________________________________________")   

        time.sleep(3)    # 급락



######################################################################
# tkinter

def main_trade():
    global root
    root = Tk()

    root.title("UPbit(BTC, ETH 제외) ")
    root.geometry("720x520")

    root.readprofile(False, False)

    label_space = Label(root, text=" ")
    label_space.grid(row=0, column=0)

    ###### key 입력 ######
    frame_key = LabelFrame(root, text="API KEY 입력")
    frame_key.grid(row=1, column=0, columnspan=2, sticky = N+E+W+S, padx=3, pady=3)
    global access_entry
    access_label = Label(frame_key, text="access key ")
    access_label.grid(row=0, column=0)
    access_entry = Entry(frame_key, width=33)
    access_entry.grid(row=0, column=1)
    access_entry.insert(0, "Q48RDxvtfs6HoA17tuojE9nLxXI1WFYusDbpwCvm")

    global secret_entry
    secret_label = Label(frame_key, text="secret key ")
    secret_label.grid(row=1, column=0)
    secret_entry = Entry(frame_key, width=33)
    secret_entry.grid(row=1, column=1)
    secret_entry.insert(0, "iqZavy7SPX9lQjPeOspRiwRImt5515aM7RKZgXpK")
    
    btn_key = Button(frame_key, text="KEY 삽입", command=enter_key)
    btn_key.grid(row=0, column=2, rowspan=2, sticky = N+E+W+S)


    ###### main (예약 주문 프레임) ###### 
    frame_order = LabelFrame(root, text="자동 매매")
    frame_order.grid(row=1, column=2, sticky = N+E+W+S, padx=3, pady=3)
    btn_start = Button(frame_order, text="매매 시작", command=auto_order)
    btn_stop = Button(frame_order, text="알트 매도", command=reset_coin)
    btn_start.pack()
    btn_stop.pack()

    ###### setting ######
    frame_set = LabelFrame(root, text="Setting")
    frame_set.grid(row=2, column=0, columnspan=2, sticky = N+E+W+S, padx=3, pady=3)

    money_label = Label(frame_set, text="사용하지 않을 금액")
    money_label.grid(row=0, column=0)
    get_percent = Label(frame_set, text="목표 수익")
    get_percent.grid(row=1, column=0)
    buy_num_label = Label(frame_set, text="분할 매수 갯수")
    buy_num_label.grid(row=2, column=0)
    buy_label = Label(frame_set, text=" 매수 퍼센트 ")
    buy_label.grid(row=3, column=0)
    sell_label1 = Label(frame_set, text="매도 급락퍼센트")
    sell_label1.grid(row=4, column=0)
    sell_label2 = Label(frame_set, text="매도 장기퍼센트")
    sell_label2.grid(row=5, column=0)

    global set_money
    global set_get
    global set_buy_num
    global set_buy
    global set_sell1
    global set_sell2

    set_money = Entry(frame_set, width=30)
    set_get = Entry(frame_set, width=30)
    set_buy_num = Entry(frame_set, width=30)
    set_buy = Entry(frame_set, width=30)
    set_sell1 = Entry(frame_set, width=30)
    set_sell2 = Entry(frame_set, width=30)

    set_money.grid(row=0, column=1)
    set_get.grid(row=1, column=1)
    set_buy_num.grid(row=2, column=1)
    set_buy.grid(row=3, column=1)
    set_sell1.grid(row=4, column=1)
    set_sell2.grid(row=5, column=1)

    btn_set = Button(frame_set, text=" Setting ", command=set_risk)
    btn_set.grid(row=0, column=2, rowspan=6, sticky = N+E+W+S)



    ###### balance ######
    frame_i = LabelFrame(root, text="내 잔고 현황")
    frame_i.grid(row=2, column=2, sticky = N+E+W+S, padx=3, pady=3)
    global i
    i = Text(frame_i, width=35, height=12, padx=1, pady=3)
    i.pack()


    ###### Log ######
    frame_txt = LabelFrame(root, text="Log")
    frame_txt.grid(row=3, column=0, columnspan=3, sticky = N+E+W+S, padx=3, pady=3)
    global txt
    txt = Text(frame_txt, width=100, height=13, padx=3, pady=3)
    txt.pack(side="left")



    root.mainloop()     # 창이 닫히지 않도록





if __name__ == "__main__":
    main_trade()