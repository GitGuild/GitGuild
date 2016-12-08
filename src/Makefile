PYTHON_VERSION=2.7  # not used...
SHELL = /bin/bash  # for pushd, but would probably be better to avoid this
PREREQDIR=.

installledger = if [ !  -d $(1)/ledger ]; \
	then \
		git clone git://github.com/ledger/ledger.git $(1)/ledger; \
		pushd $(1)/ledger; \
		if [ $(VIRTUAL_ENV) ]; \
			then \
				./acprep --prefix=$(VIRTUAL_ENV) --python update; \
			else \
				./acprep  --python update; \
		fi; \
		make; \
		make install; \
		popd; \
	fi

makeclean = rm -rf .cache build dist *.egg-info test/__pycache__ \
	rm -rf test/*.pyc ggtest *.egg *~ *pyc test/*~ .eggs \
	rm -f .coverage*

dependencies:
	$(call installledger, $(PREREQDIR))

install:
	$(call makelog, "")
	$(call makerun, "")
	python setup.py -v install

clean:
	$(call makeclean, "")

purge:
	$(call makeclean, "")
	rm -rf $(PREREQDIR)/ledger
