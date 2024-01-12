import fire

class Ids(object):
  

    def build(self):
        f = open("/var/ids/db.json", "x")
        
        print('Le Build a été effectué avec succès !')

    def check(self):
        print('Checking IDS...')

    def help(self):
        print('Helping IDS...')


if __name__ == '__main__':
  fire.Fire(Ids)