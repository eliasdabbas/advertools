import pandas as pd
class Account(object):
    campaigns = []
    campaign_names = []
    adgroups = []
    adgroup_names = []
    keywords = {'exact': set(), 'phrase': set(), 'broad': set(),
                'mod_broad': set()}
    ads = []
    total_budget = 0

    def __init__(self, name):
        self.name = name

    def __str__(self):
        print('Account:', self.name)
        print('Campaigns:', len(self.campaign_names))
        print('Ad groups:', len(self.adgroup_names))
        print('Ads:', len(self.ads))
        print('Total budget:', self.total_budget)
        return ''

class Campaign(object):
    adgroups = []
    adgroup_names = []
    ads = []
    keywords = {'exact': set(), 'phrase': set(), 'broad': set(),
                'mod_broad': set()}
    def __init__(self, account, name, budget, lang, geo):
        assert name not in account.campaign_names
        assert isinstance(account, Account)
        assert isinstance(name, str)
        assert isinstance(budget, int)
        assert lang in ['en','ar','fr','de','it','sp']
        assert geo in ['us','ae','fr','de','it','sp']
        account.campaigns.append(self)
        account.campaign_names.append(name)
        account.total_budget += budget
        self.account = account
        self.name = name
        self.budget = budget
        self.lang = lang
        self.geo = geo

    def __str__(self):
        campaign_str = 'Campaign: ' + self.name + '\n' + \
                       'Budget: ' + str(self.budget) + '\n' + \
                       'Lang: ' + self.lang + '\n' + \
                       'Geo: ' + self.geo
        return campaign_str

class SearchCampaign(Campaign):
    pass

class AdGroup(object):
    ads = []
    ads_df = pd.DataFrame(columns=
                ['Account', 'Campaign', 'Ad Group', 'Headline 1',
                 'Headline 2', 'Description', 'Display URL', 'Final URL'])

    keywords_df = pd.DataFrame(columns=
                    ['Account','Campaign', 'Ad Group', 'Keyword',
                     'Criterion Type'])

    keywords = {'exact': set(), 'phrase': set(), 'broad': set(),
                'mod_broad': set()}
    def __init__(self, account, campaign, name, bid):
        assert name not in campaign.adgroup_names
        assert isinstance(account, Account)
        assert isinstance(campaign, Campaign)
        assert isinstance(bid, float)
        self.account = account
        self.campaign = campaign
        self.name = name
        self.bid = bid
        account.adgroups.append(self)
        account.adgroup_names.append(name)
        campaign.adgroups.append(self)
        campaign.adgroup_names.append(name)



    def __str__(self):
        print('Ad group:', self.name)
        print('Ads: ')
        print()
        if self.ads:
            for i in self.ads:
                print(i)
                print('')
        else:
            print('no ads in this ad group')
        print('Keywords: ')
        if self.keywords:
            for i in self.keywords:
                print(i)
        else:
            print('no keywords in this ad group')
        return ''

class TextAd(object):

    def __init__(self, account, campaign, adgroup, headline1,
                 headline2, desc, disp_url, final_url):
        assert len(headline1) <= 30
        assert len(headline2) <= 30
        assert len(desc) <= 80
        assert isinstance(account, Account)
        assert isinstance(campaign, Campaign)
        assert isinstance(adgroup, AdGroup)
        account.ads.append(self)
        campaign.ads.append(self)
        adgroup.ads.append(self)
        self.campaign = campaign
        self.adgroup = adgroup
        self.headline1 = headline1
        self.headline2 = headline2
        self.desc = desc
        self.disp_url = disp_url
        self.final_url = final_url
        text_ads_df = pd.DataFrame({
                        'Account': account.name,
                        'Campaign': campaign.name,
                        'Ad Group': adgroup.name,
                        'Headline 1': headline1,
                        'Headline 2': headline2,
                        'Description': desc,
                        'Display URL': disp_url,
                        'Final URL': final_url
                        }, index=range(1))
        print(text_ads_df)
        pd.concat([adgroup.ads_df, text_ads_df], ignore_index=True)

    def __str__(self):
        string = 'Campaign: ' + self.campaign.name + '\n' + \
                 'Ad group: ' + self.adgroup.name + '\n\n' + \
                 self.headline1 + '\n' + \
                 self.headline2 + '\n' + \
                 self.desc + '\n' + \
                 self.disp_url + '\n' + \
                 self.final_url
        return string


class Keyword(object):
    def __init__(self, account, campaign, adgroup,
                 keywords, match_types):
        assert isinstance(account, Account)
        assert isinstance(campaign, Campaign)
        assert isinstance(adgroup, AdGroup)
        self.account = account
        self.campaign = campaign
        self.adgroup = adgroup
        for type in match_types:
            for kw in keywords:
                account.keywords[type].add(kw)
        for type in match_types:
            for kw in keywords:
                campaign.keywords[type].add(kw)
        for type in match_types:
            for kw in keywords:
                adgroup.keywords[type].add(kw)


def export_keywords(adgroups, campaigns, account):
    pass

def export_ads(adgroups, campaigns, account):
    pass

def export_adgroups(campaigns, account):
    pass

def export_campaigns(account):
    pass


















