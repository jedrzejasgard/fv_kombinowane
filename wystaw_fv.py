from vendoasg.vendoasg import Vendo
import configparser
from datetime import datetime, timedelta
config = configparser.ConfigParser()
config.read('vendo.ini')

# połączenie z bazą vendo
vendoApi = Vendo(config.get('vendo','vendo_API_port'))
vendoApi.logInApi(config.get('vendo','logInApi_user'),config.get('vendo','logInApi_pass'))
vendoApi.loginUser(config.get('vendo','loginUser_user'),config.get('vendo','loginUser_pass'))

data = datetime.today()
td = timedelta(1)
dataStart = data - td
dataStart = dataStart.strftime("%Y-%m-%d")
print(dataStart)

def parse_date(datestring):
    '''
    Zmienia date w starym formacie Vendo w czytelną
    '''
    timepart = datestring.split('(')[1].split(')')[0]
    milliseconds = int(timepart[:-5])
    hours = int(timepart[-5:]) / 100
    time = milliseconds / 1000
    dt = datetime.fromtimestamp(time + hours * 3600)
    return dt.strftime("%Y-%m-%d")


#pobiera liste WZtek
def pobierz_lista_wz():
    lista_wz=vendoApi.getJson(
        '/json/reply/Dokumenty_Dokumenty_Lista',
        {"Token":vendoApi.USER_TOKEN,"Model":{
        "Rodzaj": {
            "Kod": "WZ",
            'Seria':'   A'},
        "Zamkniete": True, "SortowanieRosnaco":False,"DataOd":dataStart,
        }
    })
    #print(lista_wz)
    lista_wz = lista_wz['Wynik']['Rekordy']
    print(len(lista_wz))
    return lista_wz


def kombinowane(wd_wz):
    czy_kombinowane = False
    for wd in wd_wz:
        if wd['NazwaWewnetrzna'] == 'kombinowane' and wd['Wartosc']== True:
            print(wd['Wartosc'])
            czy_kombinowane = True
    return czy_kombinowane


def powiazane_dok(dok_id):
    dok_skojarzone=vendoApi.getJson(
        '/json/reply/Dokumenty_Dokumenty_Skojarzone',
        {"Token":vendoApi.USER_TOKEN,"Model":{"DokumentID":dok_id,"Magazynowe":False}})
    #print(dok_zrodlo['Wynik'])
    for element_powiazany in dok_skojarzone['Wynik']:
        id_dokumentow_skojarzonych = []
        if element_powiazany['DataType'] == 'Dokument':
            id_dokumentow_skojarzonych.append(element_powiazany['ID'])
        dok_zrodlowy=vendoApi.getJson(
            '/json/reply/Dokumenty_Dokumenty_Lista',
            {"Token":vendoApi.USER_TOKEN,"Model":{"DokumentyID":[id_dokumentow_skojarzonych]}})
        print(dok_zrodlowy)


if __name__ == '__main__':
    cala_lista_wz = pobierz_lista_wz()
    #print(cala_lista_wz)
    for dok_wz in cala_lista_wz:
        #print(dok_wz['PolaUzytkownika'])
        id_dok_wz = dok_wz['ID']
        print(dok_wz['NumerPelny'])
        powiazane_dok(id_dok_wz)
        if kombinowane(dok_wz['PolaUzytkownika']):
            id_dok_wz = dok_wz['ID']
        print('**')