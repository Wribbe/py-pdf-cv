DEPS_BUILD := \
	pandoc \
  mutool \

M := 0
STATICS := $(wildcard static/*)

all: builddeps cv.pdf md5hash.txt

cv.html : cv_base.html assemble.py ${STATICS}
	python -c "from assemble import html; print(html())" > $@

cv_raw.pdf : cv.html cv.css Makefile
	pandoc \
		$(filter %.html,$^) \
		-t html5 \
		-V margin-top=$M -V margin-left=$M -V margin-right=$M -V margin-bottom=$M \
		-c $(filter %.css,$^) -o $@

cv_uncompressed.pdf : cv_raw.pdf
	mutool clean -d -a $^ $@

cv.pdf : cv_uncompressed.pdf python.py assemble.py cv.js Makefile
	echo "'''" > $@
	cat cv_uncompressed.pdf >> $@
	echo "'''">> $@
	./assemble.py >> $@

md5hash.txt : cv.pdf
	cat $^ | md5sum | cut -d' ' -f1 > $@

.PHONY: builddeps

str_err := "ERROR: missing build-dependencies, please install:"

define check_deps
	deps_missing=""; \
	for d in ${DEPS_BUILD}; do \
		$$d -v > /dev/null 2>&1; \
		[ $$? -eq 0 ] || deps_missing="$${deps_missing} $$d"; \
	done; \
	if [ -n "$${deps_missing}" ]; then  \
		echo ${str_err}; \
		printf "  %s\n" $${deps_missing}; \
		exit 1; \
	fi;
endef

builddeps:
	@$(call check_deps)
