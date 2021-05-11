
import requests
import json
from datetime import datetime

class Operations:
    def __init__(self, session, date_start, date_stop, count=30, account_id=0):
        """operations class"""
        self.session = session
        self.date_start = date_start
        self.date_stop = date_stop
        self.list = []
        self.count = count
        self.account_id = account_id
        
        self.get_operations()
        
    def __iter__(self):
        """iter"""
        self.n = 0
        return self
        
    def __next__(self):
        """next"""
        if self.n < len(self.list):
            op = self.list[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration
            
    def get_operations(self, account_id=None, count=None):
        count = count or self.count
        account_id = account_id or self.account_id
        """get operations according to the date range"""
        # convert date to timestamp
        ts_date_debut = datetime.strptime(self.date_start, "%Y-%m-%d")
        ts_date_debut = int(ts_date_debut.timestamp())*1000
        
        ts_date_fin = datetime.strptime(self.date_stop, "%Y-%m-%d")
        ts_date_fin = int(ts_date_fin.timestamp())*1000
        
        # call operations ressources
        url = "%s" % self.session.url
        url += f"/ca-{self.session.region}/particulier/operations/synthese/detail-comptes/"
        url += f"jcr:content.n3.operations.json?grandeFamilleCode=1&compteIdx={account_id}"
        url += "&idDevise=EUR"
        url += "&dateDebut=%s" % ts_date_debut
        url += "&dateFin=%s" % ts_date_fin
        url += "&count=%s" % count
        r = requests.get(url=url,
                         verify=self.session.ssl_verify,
                         cookies=self.session.cookies)
        if r.status_code != 200:
            raise Exception( "[error] get operations: %s - %s" % (r.status_code, r.text) )
           
        # success, save list operations
        rsp = json.loads(r.text)
        self.list = rsp["listeOperations"]
