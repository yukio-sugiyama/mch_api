import datetime
import time

#from . import mch_apis
#from . import mch_hero
#from . import mch_exte
import mch_apis
import mch_hero
import mch_exte

class GetData:

    def __init__(self):
        self.mch = mch_apis.MCHAPI()
        self.hero = mch_hero.MCHHeroData()
        self.exte = mch_exte.MCHExteData()


    def get_eth(self, user_id):
        res = self.mch.get_user_info(user_id)
        if 'eth' in res['user_data']:
            return res['user_data']['eth']
        else:
            return ''


    def get_hero_ids_eth(self, eth):
        res = self.mch.get_hero_asset(eth)
        return res['hero_ids']


    def get_hero_ids_crypto(self, user_id):
        res = self.mch.get_hero_asset_info(user_id)
        # ヒーロー持ってないと404エラーなので
        if res is not None:
            return res['hero_ids']
        else:
            return ''


    def get_exte_ids_eth(self, eth):
        res = self.mch.get_extension_asset(eth)
        return res['extension_ids']


    def get_exte_ids_crypto(self, user_id):
        res = self.mch.get_extension_asset_info(user_id)
        # ヒーロー持ってないと404エラーなので
        if res is not None:
            return res['extension_ids']
        else:
            return ''


    def get_hero_ids(self, user_id):
        hero_asset = []

        eth = self.get_eth(user_id)

        if not eth == '':
            hero_asset.extend(self.get_hero_ids_eth(eth))

        hero_asset.extend(self.get_hero_ids_crypto(user_id))
        hero_asset.sort()

        return hero_asset

    def get_exte_ids(self, user_id):
        exte_asset = []

        eth = self.get_eth(user_id)

        if not eth == '':
            exte_asset.extend(self.get_exte_ids_eth(eth))

        exte_asset.extend(self.get_exte_ids_crypto(user_id))
        exte_asset.sort()

        return exte_asset


    def get_hero_metadata(self, id):

        return self.mch.get_hero_metadata(id)


    def get_hero_type_metadata(self, id):

        return self.mch.get_hero_type_metadata(id)


    def get_exte_metadata(self, id):

        return self.mch.get_extension_metadata(id)


    def get_exte_type_metadata(self, id):

        return self.mch.get_extension_type_metadata(id)


    def get_user_name(self, user_id):
        res = self.mch.get_user_info(user_id)
        if 'name' in res['user_data']:
            return res['user_data']['name']
        else:
            return ''


    def get_hero_assets(self, user_id):
        hero_ids = self.get_hero_ids(user_id)

        hero_data_set = []

        for id in hero_ids:
            hero_metadata = self.get_hero_metadata(id) #遅い
            self.hero.set_data(hero_metadata)

            type = self.hero.get_type()

#            hero_type_metadata = self.get_hero_type_metadata(type) #遅い
#            self.hero.set_type_data(hero_type_metadata)

            rarity = self.hero.get_rarity()
#            name = self.hero.get_name_ja()
            lv = self.hero.get_lv()
            url = self.hero.get_url()

            hero_data = {'rarity':rarity, 'type':type, 'id':id, 'lv':lv, 'url':url}

            hero_data_set.append(hero_data)

        return hero_data_set

    def get_exte_assets(self, user_id):
        exte_ids = self.get_exte_ids(user_id)

        exte_data_set = []

        for id in exte_ids:

            exte_metadata = self.get_exte_metadata(id)
            self.exte.set_data(exte_metadata)

            type = self.exte.get_type()

#            exte_type_metadata = self.get_exte_type_metadata(type)
#            self.exte.set_type_data(exte_type_metadata)

            rarity = self.exte.get_rarity()
#            name = self.exte.get_name_ja()
            lv = self.exte.get_lv()
            url = self.exte.get_url()

            exte_data = {'rarity':rarity, 'type':type, 'id':id, 'lv':lv, 'url':url}

            exte_data_set.append(exte_data)

        return exte_data_set


    def get_hero_sold(self, since = '', until = ''):

        hero_sold = self.mch.get_hero_sold_trades(since, until)

        hero_sold_set = []
        for x in hero_sold:
            trade_id = x['trade_id']
            hero_id = x['hero_id']
            sold_at = x['sold_at']
            price = x['price']
            ce = x['ce']
            seller_id = x['seller_id']
            buyer_id = x['buyer_id']
            sold_time = datetime.datetime.fromtimestamp(sold_at).strftime("%Y/%m/%d %H:%M:%S")

            hero_sold = {'trade_id':trade_id
                        , 'asset_id':hero_id # exteと同期するためkey値は「asset_id」で統一
                        , 'sold_at':sold_at
                        , 'price':price
                        , 'ce':ce
                        , 'seller_id':seller_id
                        , 'buyer_id':buyer_id
                        , 'sold_time':sold_time
                        }

            hero_sold_set.append(hero_sold)

        return hero_sold_set


    def get_exte_sold(self, since = '', until = ''):

        exte_sold = self.mch.get_extension_sold_trades(since, until)

        exte_sold_set = []
        for x in exte_sold:
            trade_id = x['trade_id']
            exte_id = x['extension_id']
            sold_at = x['sold_at']
            price = x['price']
            ce = x['ce']
            seller_id = x['seller_id']
            buyer_id = x['buyer_id']
            sold_time = datetime.datetime.fromtimestamp(sold_at).strftime("%Y/%m/%d %H:%M:%S")

            exte_sold = {'trade_id':trade_id
                        , 'asset_id':exte_id # heroと同期するためkey値は「asset_id」で統一
                        , 'sold_at':sold_at
                        , 'price':price
                        , 'ce':ce
                        , 'seller_id':seller_id
                        , 'buyer_id':buyer_id
                        , 'sold_time':sold_time
                        }

            exte_sold_set.append(exte_sold)

        return exte_sold_set
