#import webscraper_ltm as latam
import webscraper_gol as gol

def main():
    lista = ['RBR', 'MCZ', 'MAO', 'SSA', 'FOR', 'BSB', 'VIX', 'GYN', 'SLZ', 'CGB', 'CGR', 'CNF', 'BEL', 'JPA', 'CWB', 'REC', 'THE', 'SDU', 'NAT', 'POA','FLN', 'AJU', 'PMW']
    #latam.main(lista)
    print('Raspagem de Dados da LATAM finalizada')
    gol.main(lista)
    print('Raspagem de Dados da GOL finalizada')

main()