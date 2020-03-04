library(tm)
library(RCurl)
library(wordcloud)
library(XML)est

def termdocumentmatrix_example():
    # Create some very short sample documents

	text1="A l'abri derrière les premiers, est passé à l'offensive en entrant dans la ligne droite puis a résisté jusqu'au bout à l'attaque de Dark Orbit (4)."
	text2="Animateur, a bien accéléré dans le dernier tournant, prenant ses distances, avant de contrer courageusement l'effort de Valdelino (1) en fin de parcours."
	text3="Vite aux avant-postes, a été débordée au bout de la  ligne opposée, avant de revenir vite dans le dernier tournant et d''afficher une nette supériorité sur le plat."
	# Initialize class to create term-document matrix
	tdm = textmining.TermDocumentMatrix()
    # Add the documents
	tdm.add_doc(text1)
	tdm.add_doc(text2)
	tdm.add_doc(text3)
    # Write out the matrix to a csv file. Note that setting cutoff=1 means
    # that words which appear in 1 or more documents will be included in
    # the output (i.e. every word will appear in the output). The default
    # for cutoff is 2, since we usually aren't interested in words which
    # appear in a single document. For this example we want to see all
    # words however, hence cutoff=1.
    #tdm.write_csv('matrix.csv', cutoff=1)
    # Instead of writing out the matrix you can also access its rows directly.
    # Let's print them to the screen.
	for row in tdm.rows(cutoff=1):
		print (row)


termdocumentmatrix_example()