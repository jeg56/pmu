import xlsxwriter

# ecrire dans un fichier
def writeFile(texte,path):
        fichier = open(path,"wb")
        fichier.write(texte.encode('utf-8'))
        fichier.close()

def writeFileAppend(texte,path):
        fichier = open(path,"a+b")
        fichier.write(texte.encode('utf-8'))
        fichier.close()
 
# lire un fichier
def readFile(path):
        fichier = open(path,"r")
        file = fichier.read()
        #return ligne
        fichier.close()

def reTraiteInfos(mot):
        if isinstance(mot, str):
            text = mot
            decoded = False
        else:
            text = mot.decode(encoding)
            decoded = True

        return text.strip().replace("\\",'').replace("\'",'_').replace('Ø','O').replace('Å','A').replace('ë','e').replace('ä','a').replace('å','a').replace('ø','o').replace(')','_').replace('È','E').replace('Ë','E').replace('É','E').replace('Ê','E').replace("'",'_').replace('.','_').replace('´','_').replace('Ô','O').replace('Ö','O').replace('(','_').replace('û','u').replace('Ü','U').replace('ó','o').replace('è','e').replace('é','e').replace('©','o').replace('ñ','n').replace(' ','_').replace(')','_').replace("'", '_').replace("-", '_').replace("&amp;", '_').replace('&quot;','_').replace('ö','o')


#print(reTraiteInfos("Egee De Mahey"))


def productXlsFile(table):
    workbook = xlsxwriter.Workbook('../05 - Documents/STATS/PRONOS.xlsx')
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, cost in (table):
        worksheet.write(row, col,     item)
        worksheet.write(row, col + 1, cost)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
