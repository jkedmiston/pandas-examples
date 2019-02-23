all:
	$(MAKE) -f Makefile_plotting -C pandas_examples all

update_repo:
	$(MAKE) -f Makefile_plotting -C pandas_examples update_repo
