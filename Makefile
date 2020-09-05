DEPS_BUILD := \
	pandoc \
  mutool \

all: builddeps cv.pdf

cv_raw.pdf : cv.html cv.css Makefile
	pandoc -t html $(filter %.html,$^) -c $(filter %.css,$^) -o $@

cv_uncompressed.pdf : cv_raw.pdf
	mutool clean -d -a $^ $@

cv.pdf : cv_uncompressed.pdf python.py assemble.py cv.js Makefile
	echo "'''" > $@
	cat cv_uncompressed.pdf >> $@
	echo "'''">> $@
	./assemble.py >> $@

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
