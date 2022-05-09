#------------------------------------------------------------------------------
# PACKAGES
#------------------------------------------------------------------------------
# Classic Packs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Word Cloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from stop_words import get_stop_words
import stylecloud
from PIL import Image
import PyPDF4

#import nltk
#from nltk.corpus import stopwords
#nltk.download("stopwords")
#stopwords = set(stopwords.words('spanish', 'english'))
#stopwords.update([ "y", "el", "lo", "en", "que", "de", "la", "con", "al",
#               "por", "para", "se", "esta", "del", "un", "este", "solo",
#               "o", "ello", "ella", "le", "el", "u"])

# Path, create folder
import os, re
from pathlib import Path

#------------------------------------------------------------------------------
# PARTE 1: DEFINIR UN WORK PATH
#------------------------------------------------------------------------------

# 1.1 Main path
os.chdir(r'D:\Github\Word-Cloud-Python')

# 1.2 Object path
main_directory = os.getcwd()

# 1.3 Create fodlers and paths
names_folder = ['A_Rawdata', 'B_Figures']

for i in np.arange(0,2,1):
    Path(str(names_folder[i])).mkdir(exist_ok=True)
    names_folder[i] = os.path.join(main_directory, str(names_folder[i]))

#------------------------------------------------------------------------------
# PARTE 2: Example 1 (txt y WordCloud)
#------------------------------------------------------------------------------

# 2.1 Read text file
text_1 = open(names_folder[0]+'\ejemplo_01.txt', mode='r', encoding='utf-8').read()

# 2.2 Exclude redundat words (but en English)
stopwords = STOPWORDS

print(stopwords)
print(len(stopwords))

# 2.3 Word Cloud to imagen
wc_1 = WordCloud(
        background_color='white',
        stopwords=stopwords,
        height=600,
        width=400
    )

wc_1.generate(text_1)

wc_1.to_file(names_folder[1]+'\ejemplo_01.png')

#------------------------------------------------------------------------------
# PARTE 3: Example 2 (txt, stylecloud y un ícono como base)
#------------------------------------------------------------------------------

### 3.0 Recursos
# Iconos para usar en stylecloud: https://fontawesome.com/icons?d=gallery&p=1&m=free
# Paleta de colores de stylecloud: https://jiffyclub.github.io/palettable/
# Código de colores HTML: https://htmlcolorcodes.com/

### 3.1 Word Cloud - Apple shape (Con palabras irrelevantes 'Stopwords')
stylecloud.gen_stylecloud(file_path=names_folder[0]+'\ejemplo_02.txt',
                          icon_name='fab fa-apple',
                          colors = 'white',
                          background_color='black',
                          collocations=False,
                          #size=1024,
                          output_name= names_folder[1]+'\ejemplo_02_Con_Stopwords.png'
                          )

### 3.2 Previo a un Word Cloud y Stopwords (En español)
palabras_irrelevantes = get_stop_words('spanish') # get_stop_word ya tiene unas palabras predeterminadas

## 3.2.1 En caso deseas agregar palabras
palabras_irrelevantes = set(get_stop_words('es'))
new_stop = {"zero1", "zero2"}
palabras_irrelevantes = palabras_irrelevantes.union(new_stop)

# 3.2.2 En caso deseas borrar palabras
delete_word = ['zero1', 'zero2']
for i in np.arange(0,2,1):
    palabras_irrelevantes.remove(str(delete_word[i]))    

### 3.3 Word Cloud - Apple shape (Sin palabras irrelevantes 'Stopwords')
stylecloud.gen_stylecloud(file_path=names_folder[0]+'\ejemplo_02.txt',
                          icon_name='fab fa-apple',
                          colors = 'white',
                          background_color='black',
                          collocations=False,
                          size=1024,
                          output_name= names_folder[1]+'\ejemplo_02_Sin_Stopwords.png',
                          custom_stopwords=palabras_irrelevantes)

# 3.3.1 Con una paleta de colores
stylecloud.gen_stylecloud(file_path=names_folder[0]+'\ejemplo_02.txt',
                          icon_name='fab fa-apple',
                          #colors = 'white',
                          background_color='black',
                          collocations=False,
                          size=1024,
                          output_name= names_folder[1]+'\ejemplo_02_Sin_Stopwords_Paleta.png',
                          custom_stopwords=palabras_irrelevantes,
                          palette = 'cartocolors.qualitative.Pastel_3')

#------------------------------------------------------------------------------
# PARTE 4: Example 3 (txt, WordCloud, y una imagen como base)
#------------------------------------------------------------------------------

### 4.1 Cargar imagen
my_mask = np.array(Image.open(names_folder[0]+'\imagen.jpg'))

### 4.2 Formato del WordCloud sin Palabras Irrelevantes
wc_3 = WordCloud(background_color='white',
                 mask=my_mask,
                 collocations=False,
                 width = 600,
                 height = 300,
                 stopwords=palabras_irrelevantes
                 )

### 4.3 Lectura de txt file
text_3 = open(names_folder[0]+'\ejemplo_03.txt', mode='r', encoding='utf-8').read()

### 4.4 Incluir txt al wc
wc_3.generate(text_3)

### 4.5 Si quierew usar el color de la propia imagen
image_colors = ImageColorGenerator(my_mask)
wc_3.recolor(color_func=image_colors)

# 4.6 Formato de la imagen considerando Matplotlib
plt.figure(figsize=(100,50))
plt.imshow(wc_3, interpolation='bilinear')
plt.axis('off')
plt.show()
wc_3.to_file(names_folder[1]+'\ejemplo_03.jpg') # guardar la imagen

#------------------------------------------------------------------------------
# PARTE 5: Example 4 (WORD, WordCloud y una imagen como base)
#------------------------------------------------------------------------------

#------------------------------------------------
# 1 HOJA
#------------------------------------------------
### 5.1 Lectura del PDF
pdfFileObj = open(names_folder[0]+'\ejemplo_04.pdf', 'rb')
pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)

# Selección de la hoja y extracción de palabras
pageObj = pdfReader.getPage(1)
print(pageObj.extractText())
pdfFileObj.close()

### 5.2 Cargar la imagen para la base
ourMask = np.array(Image.open(names_folder[0]+'\imagen.jpg'))

### 5.3 Más palabras irrelevantes
new_stop = {"si", "página"}
palabras_irrelevantes = palabras_irrelevantes.union(new_stop)

### 5.3 Formato del WordCloud
wc_41 = WordCloud(background_color='white',
                  mask=ourMask,
                  stopwords=palabras_irrelevantes
                  ).generate(pageObj.extractText())

### 5.4 Formato de la imagen considerando Matplotlib
plt.figure(figsize=(100,50))
plt.imshow(wc_41, interpolation='bilinear')
plt.imshow(wc_41)
plt.axis('off')
plt.show()
wc_41.to_file(names_folder[1]+'\ejemplo_04_1-hoja.jpg')

#------------------------------------------------
# N HOJAS
#------------------------------------------------
### 5.5 Lectura del PDF
pdfFileObj = open(names_folder[0]+'\ejemplo_04.pdf', 'rb')
pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)

# Selección de laS hojaS y extracción de palabras
pageData = ''
for page in pdfReader.pages:
    pageData += page.extractText()
    print(pageData)

### 5.6 Cargar la imagen para la base
ourMask = np.array(Image.open(names_folder[0]+'\imagen.jpg'))

### 5.7 Formato del WordCloud
wc_42 = WordCloud(background_color='white',
                  mask=ourMask,
                  stopwords=palabras_irrelevantes
                  ).generate(pageData)

### 5.8 Formato de la imagen considerando Matplotlib
plt.figure(figsize=(100,50))
plt.imshow(wc_42, interpolation='bilinear')
plt.imshow(wc_42)
plt.axis('off')
plt.show()
wc_42.to_file(names_folder[1]+'\ejemplo_04_n-hojas.jpg')




























