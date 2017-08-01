# Holden
Asistente inteligente para jugar al Holdem Texas Poker con soporte para cualquier página web.

Para el calculo de probabilidades se utiliza el siguiente repositorio: https://github.com/ktseng/holdem_calc

----------------------------------------------------------------------------------------------------------

Enlaces interesantes:
 - Comparación de dos imágenes: http://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
 - OCR: https://pypi.python.org/pypi/pytesseract
 - Reconocimiento de figuras en una imagen: http://www.pyimagesearch.com/2014/08/04/opencv-python-color-detection/ y http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/
 - Git: https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

----------------------------------------------------------------------------------------------------------

COMANDOS BASICOS DE GIT:
- Actualizar carpeta local (basicamente descarga los ficheros de la nube): git pull origin [jose/manu/master] (dependiendo de cual quieras pillar)
- Actualizar carpeta remota (basicamente sube los ficheros a la nube): git push origin [jose/manu] (dependiendo de cual quieras actualizar). NO HACER GIT PUSH MASTER, master lo actualizaremos de otra forma.
- Saber en que rama estas y el estado: git status
- Cambiar de rama: git checkout [jose/manu/master] (dependiendo de a cual te quieres cambiar)
- Para saber que ramas existen: git branch

PASOS PARA AGREGAR CAMBIOS DE BRANCH A MASTER:
- git checkout master
- git pull origin master
- git merge test
- git push origin master

----------------------------------------------------------------------------------------------------------

Pytesseract - librería externa para reconocimiento de caracteres.
En windows, te descargas esto: https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download.
Y ademas en el prompt de anaconda haces "pip install pytesseract".
