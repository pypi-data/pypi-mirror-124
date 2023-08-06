from LibHanger.Library.uwConfig import cmnConfig

class mercariConfig(cmnConfig):

    """
    mercarizer共通設定クラス(mercariConfig)
    """ 

    def __init__(self):
        
        """ 
        コンストラクタ
        """ 

        # 基底側のコンストラクタ呼び出し
        super().__init__()
        
        self.UserEgent_Mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        """ ユーザーエージェント Mozilla """

        self.UserEgent_AppleWebKit = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        """ ユーザーエージェント AppleWebKit """

        self.UserEgent_Chrome = 'Chrome/94.0.4606.61 Safari/537.36'
        """ ユーザーエージェント Chrome """

        self.MercariUrl = 'https://jp.mercari.com/search?keyword='
        """ メルカリURL """

        self.DelayTime:int = 2
        """ 1ページ読み込むごとに発生する待機時間(秒) """

        self.ItemTagName = '.ItemGrid__ItemGridCell-sc-14pfel3-1'
        """ 商品タグCSSクラス名 """

        self.WebDriverTimeout:int = 10
        """ Webドライバーのタイムアウト時間(秒) """

    def getConfig(self, scriptPath:str, configFileDirName:str = ''):

        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        scriptPath : string
            スクリプトファイルパス

        """

        # 基底側のiniファイル読込
        super().getConfig(scriptPath, configFileDirName)

        # ユーザーエージェント Mozilla
        super().setConfigValue('UserEgent_Mozilla',self.config_ini,'USER_EGENT','USEREGENT_MOZILLA',str)

        # ユーザーエージェント AppleWebKit
        super().setConfigValue('UserEgent_AppleWebKit',self.config_ini,'USER_EGENT','USEREGENT_APPLEWEBKIT',str)

        # ユーザーエージェント Chrome
        super().setConfigValue('UserEgent_Chrome',self.config_ini,'USER_EGENT','USEREGENT_CHROME',str)

        # メルカリURL
        super().setConfigValue('MercariUrl',self.config_ini,'SITE','MERCARI_URL',str)

        # 待機時間
        super().setConfigValue('DelayTime',self.config_ini,'SITE','DELAY_TIME',int)
        