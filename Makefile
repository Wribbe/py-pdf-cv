DEPS_BUILD := \
	pandoc \
  mutool \

DIR_VENV := venv

all: build_dependencies ${DIR_VENV} cv.pdf

cv_raw.pdf : cv.md
	pandoc $^ -o $@

cv_uncompressed.pdf : cv_raw.pdf
	mutool clean -d -a $^ $@

cv.pdf : cv_uncompressed.pdf python.py Makefile
	echo "'''" >> $@
	cat cv_uncompressed.pdf >> $@
	echo "'''">> $@
	cat python.py >> $@

${DIR_VENV} :
	python -m venv $@
	$@/bin/python -m pip install pip --upgrade
	$@/bin/python -m pip install -r requirements.txt -t .

.PHONY: build_dependencies

str_err := "ERROR: missing build-dependencies, please install:"

define check_dependencies
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

build_dependencies:
	@$(call check_dependencies)
