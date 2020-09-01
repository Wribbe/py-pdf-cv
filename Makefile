all: cv.pdf

cv_raw.pdf : cv.md
	pandoc $^ -o $@

cv_uncompressed.pdf : cv_raw.pdf
	mutool clean -d -a $^ $@

cv.pdf : cv_uncompressed.pdf python.py Makefile
	echo "'''" >> $@
	cat cv_uncompressed.pdf >> $@
	echo "'''">> $@
	cat python.py >> $@
