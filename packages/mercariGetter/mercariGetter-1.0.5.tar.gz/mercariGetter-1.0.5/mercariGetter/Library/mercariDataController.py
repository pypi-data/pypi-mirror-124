import json
import pandas as pd
import time
import LibHanger.Library.uwLogger as Logger
import chromedriver_binary # コメントアウトしないこと
from pandas.core.frame import DataFrame 
from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from mercariGetter.Library.mercariConfig import mercariConfig
from LibHanger.Library.uwGlobals import *
from mercariGetter.Library.mercariException import resultDataGenerateError

class mercariDataSearch:

    def __init__(self):

        """ 
        コンストラクタ
        """

        pass

    def searchData(self, searchConditionJsonString:str) -> str:

        """
        mercariデータ検索

        Parameters
        ----------
        searchConditionJsonString : str
            検索条件Json文字列

        """

        # 共通設定取得
        mc = gv.config

        # 取得したメルカリデータをpandas dataframeで返却する
        dfMercariData = self.getMercariDataToPandas(searchConditionJsonString, mc)
        
        # pandasデータをjson形式に変換する
        stringJson = dfMercariData.to_json(orient='records')

        # jsonデータを返す
        return stringJson

    def getSearchConditionKeywords(self, searchConditionJsonString:str) -> str:

        """
        検索キーワードを取得する

        Parameters
        ----------
        searchConditionJsonString : str
            検索条件JSON文字列
        """

        # JSON文字列をデシリアライズ
        keywordsData = json.loads(searchConditionJsonString)

        # デシリアライズしたJSON文字列をループして配列に格納
        lstKeyworsString = list()
        for jsn_key in keywordsData:
            if type(keywordsData[jsn_key]) == str:
                if keywordsData[jsn_key] == '': continue
                lstKeyworsString.append(jsn_key + '=' + keywordsData[jsn_key])
            elif type(keywordsData[jsn_key]) == list:
                keywordsSubList:list = keywordsData[jsn_key]
                if len(keywordsSubList) == 0: continue
                lstKeyworsString.append(jsn_key + '=' + ','.join(keywordsSubList))

        # 配列間を'&'で結合
        keywordsString = '&'.join(lstKeyworsString)

        # 検索キーワードを返す
        return keywordsString

    @Logger.loggerDecorator('Init SearchResultData DataFrame')
    def initSearchResultDataColumns(self) -> DataFrame:
        
        """
        メルカリデータ格納用のPandasDataFrameを初期化する

        Parameters
        ----------
        None
        """

        return pd.DataFrame(columns=['itemId','itemUrl','itemName','itemPrice','itemPicUrl','soldout'])

    @Logger.loggerDecorator('Open Browzer')
    def getWebDriver(self):

        """
        ブラウザ操作用のChromeドライバーを取得する

        Parameters
        ----------
        None
        """

        options = Options()
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    @Logger.loggerDecorator('Changing Browzer Size')
    def changeBrowzerSize(self, driver:WebDriver, width:str, height:str):

        """
        ブラウザのウィンドウサイズを変更する

        Parameters
        ----------
        driver : WebDriver
            Chromeドライバー
        width : str
            ウィンドウ横幅(px)
        height : str
            ウィンドウ縦幅(px)
        """

        # ウィンドウサイズ変更
        driver.set_window_size(width, height)

    @Logger.loggerDecorator('Loading WebPage')
    def loadPage(self, driver:WebDriver, url:str):

        """
        指定URLのページ内容を取得する

        Parameters
        ----------
        driver : WebDriver
            Chromeドライバー
        url : str
            ページURL
        """

        # ページ内容取得
        driver.get(url)

    @Logger.loggerDecorator('Delay ')
    def Delay(self, config:mercariConfig):

        """
        指定秒数待機する

        Parameters
        ----------
        config : mercariConfig
            共通設定クラス
        """

        # ログ出力
        Logger.logging.info('{} Seconds'.format(config.DelayTime))

        # 待機
        time.sleep(config.DelayTime)

    @Logger.loggerDecorator('Create PandasData')
    def createPandasData(self, dfItemInfo:DataFrame, dictItemInfo:dict) -> DataFrame:

        """
        ディクショナリからPandasDataFrameを生成する

        Parameters
        ----------
        dfItemInfo : DataFrame
            メルカリデータDataFrame
        dictItemInfo : dict
            メルカリデータDictionary
        """

        # DictionaryをDataFrameに変換
        dfItemInfo = dfItemInfo.from_dict(dictItemInfo, orient='index')

        # 主キー指定して返す
        return dfItemInfo.set_index(['itemId'], drop=False)

    @Logger.loggerDecorator('Scraping with BeautifulSoup')
    def scrapingWithBeautifulSoup(self, driver:WebDriver) -> BeautifulSoup:
        
        """
        BeautifulSoupを使用してスクレイピング

        Parameters
        ----------
        driver : WebDriver
            Chromeドライバー
        """

        # スクレイピング結果を返す
        return BeautifulSoup(driver.page_source, features='lxml')
    
    @Logger.loggerDecorator('Create SearchResultDictionary')
    def createSearchResultDictionary(self, driver:WebDriver,soup:BeautifulSoup,dfItemInfo:DataFrame) -> dict:

        """
        スレイピング結果からDictionaryを生成する

        Parameters
        ----------
        driver : WebDriver
            Chromeドライバー
        soup : BeautifulSoup
            スクレイピング結果
        dfItemInfo : DataFrame
            メルカリデータDataFrame
        """

        # 商品タグ取得
        elems_items= soup.select('.ItemGrid__ItemGridCell-sc-14pfel3-1')
        
        # 取得した商品タグをループして検索結果ディクショナリを生成
        dictItemInfo = {}
        try:
            for index in range(len(elems_items)):
                try:
                    # 商品ID
                    itemUrl = elems_items[index].find_all('a')[0].get('href')
                    itemId = itemUrl.split('/')[2]
                    # 商品名
                    itemNm = elems_items[index].find_all('mer-item-thumbnail')[0].get('item-name')
                    # 商品画像URL
                    itemPicUrl = elems_items[index].find_all('mer-item-thumbnail')[0].get('src')
                    # 価格
                    itemPrice = elems_items[index].find_all('mer-item-thumbnail')[0].get('price')
                    # SoldOut
                    soldOut = True if elems_items[index].find_all('mer-item-thumbnail')[0].get('sticker') else False
                    # ログ出力
                    Logger.logging.info('==========================================================')
                    Logger.logging.info(str(index + 1) + '/' + str(len(elems_items)))
                    Logger.logging.info('商品ID={}'.format(itemId))
                    Logger.logging.info('商品名={}'.format(itemNm))
                    Logger.logging.info('商品画像URL={}'.format(itemPicUrl))
                    Logger.logging.info('価格={}'.format(itemPrice))
                    Logger.logging.info('==========================================================')
                    # 取得データをディクショナリにセット
                    drItemInfo = pd.Series(data=['','','',0,'',False],index=dfItemInfo.columns)
                    drItemInfo['itemId'] = itemId
                    drItemInfo['itemUrl'] = itemUrl
                    drItemInfo['itemName'] = itemNm
                    drItemInfo['itemPrice'] = itemPrice
                    drItemInfo['itemPicUrl'] = itemPicUrl
                    drItemInfo['soldout'] = soldOut
                    dictItemInfo[index] = drItemInfo
                except:
                    raise resultDataGenerateError
                    
        except resultDataGenerateError as e:
            Logger.logging.error('PandasData Create Error')
            Logger.logging.error(e.args)
        finally:
            # ブラウザを閉じる
            Logger.logging.info('Closed Browzer')
            driver.quit()

        # 戻り値を返す
        return dictItemInfo

    @Logger.loggerDecorator('Get MercariData')
    def getMercariDataToPandas(self, searchConditionJsonString:str, config:mercariConfig):
        
        """
        取得したmercariデータをpandas dataframeに変換

        Parameters
        ----------
        searchCondition : 
            検索条件
        config : mercariConfig
            共通設定クラス
        """

        # 検索キーワード
        searchWord = self.getSearchConditionKeywords(searchConditionJsonString)
        
        # 格納用pandasカラム準備
        dfItemInfo:DataFrame = self.initSearchResultDataColumns()
        
        # 検索キーワードが未指定なら処理を抜ける
        if searchWord == '':
            return dfItemInfo

        # 検索url
        url = config.MercariUrl + searchWord
        
        # ヘッドレスでブラウザを起動
        driver:WebDriver = self.getWebDriver()

        # ウィンドウサイズを1200x1200にする(商品名が省略される為)
        self.changeBrowzerSize(driver, '1200', '1000')

        # url指定してページ読込
        self.loadPage(driver, url)

        # 待機
        self.Delay(config)
        
        # スクレイピング with BeautifulSoup
        soup:BeautifulSoup = self.scrapingWithBeautifulSoup(driver)
        
        # 検索結果ディクショナリ生成
        dictItemInfo:dict = self.createSearchResultDictionary(driver, soup, dfItemInfo)

        # pandasデータを返却する
        return self.createPandasData(dfItemInfo, dictItemInfo)
