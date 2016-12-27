DESTDIR ?= /usr/bin
USE_GITHUB ?= true
USE_GITOLITE ?= true

GG_DIR = $(HOME)/gitguild
GIT_HOME = $(shell echo ~git)
USER_NAME := $(shell git config user.name)
USER_EMAIL := $(shell git config user.email)
IDENT_REMOTE = ""

gpg := $(shell which gpg)
check_or_install_gpg = if [ "$(gpg)" = "" ]; then \
	sudo apt-get install gnupg2; \
fi

# TODO other distros and OSes
check_or_install_ledger = if [ "$(shell which ledger))" = "" ]; then \
	releasestr:=$(shell cat /etc/*-release); \
	if [ "$(shell echo "$(releasestr)" | grep 'Ubuntu' )" != "" ]; then \
		echo "install ledger from PPA?"; \
		read ledgerppa; \
		echo; \
		if [ "$( echo "$(ledgerppa)" | grep '[yY].*' )" != "" ]; then \
			sudo add-apt-repository ppa:mbudde/ledger; \
			sudo apt-get update; \
			sudo apt-get install ledger; \
		fi \
	fi \
fi

ssh := $(shell which ssh )
check_or_install_ssh = if [ "$(ssh)" = "" ]; then \
	sudo apt-get install ssh; \
fi

# create and/or arrange ssh keys
setup_ssh = if [ -e "$(HOME)/.ssh/$(USER_NAME).pub" ]; then \
	echo "found ssh key to use $(HOME)/.ssh/$(USER_NAME).pub"; \
elif [ -f "$(HOME)/.ssh/id_rsa.pub" ]; then \
	echo "found default id_rsa.pub ssh key to use, making a symbolic link with \
username"; \
	ln -sf $(HOME)/.ssh/id_rsa $(HOME)/.ssh/$(USER_NAME); \
	ln -sf $(HOME)/.ssh/id_rsa.pub $(HOME)/.ssh/$(USER_NAME).pub; \
else \
	ssh-keygen -t rsa -b 4096 -C $(USER_EMAIL) -f $(HOME)/.ssh/$(USER_NAME); \
fi

setup_github = if [ "$(USE_GITHUB)" = "true" ] && [ ! -d $(GG_DIR)/ok.sh ]; then \
	git clone https://github.com/whiteinge/ok.sh.git $(GG_DIR)/ok.sh; \
	sudo ln -sf $(GG_DIR)/ok.sh/ok.sh $(DESTDIR)/ok.sh; \
	_=$( ok.sh create_repo $(USER_NAME) "$(USER_NAME)'s personal guild" ); \
fi

# Optional for now, but gitolite is the server of choice for gitguild.
# Gitguild will build toward a p2p architecture where all users
# will run gitolite on their primary devices.
# renames gitolite-admin repo to USER_NAME
setup_gitolite = [ "$(USE_GITOLITE)" = "true" ]; then \
	if [ ! -d /usr/lib/gitolite ]; then \
		cd /tmp; \
		if [ ! -d gitolite ]; then \
			git clone https://github.com/isysd/gitolite.git; \
		fi; \
		cd gitolite; \
		sudo mkdir -p /usr/lib/gitolite; \
		sed -z -i.bak "s/\# GL_ADMIN_REPO                   =>  \"gitolite-admin\"/ GL_ADMIN_REPO                   =>  \"$(USER_NAME)\"/g" src/lib/Gitolite/Rc.pm; \
		sudo ./install -to /usr/lib/gitolite; \
		sudo ln -sf /usr/lib/gitolite/gitolite /usr/bin/gitolite; \
		cp "$(HOME)/.ssh/$(USER_NAME).pub" "/tmp/$(USER_NAME).pub"; \
		sudo -H -u git sh -c 'gitolite setup -pk /tmp/$(USER_NAME).pub -m "guild seeded w gitolite-admin template"'; \
		sudo rm -fR $(GIT_HOME)/repositories $(GIT_HOME)/.gitolite; \
		sudo -H -u git sh -c 'gitolite setup -pk /tmp/$(USER_NAME).pub -m "guild seeded w gitolite-admin template"'; \
		sudo chmod -R g+rwx $(GIT_HOME)/repositories; \
		sudo chmod -R g+rwx $(GIT_HOME)/.gitolite*; \
		sudo ln -sf $(GIT_HOME)/repositories $(HOME)/repositories; \
		sudo ln -sf $(GIT_HOME)/.gitolite $(HOME)/.gitolite; \
		sudo ln -sf $(GIT_HOME)/.gitolite.rc $(HOME)/.gitolite.rc; \
	fi; \
fi

uninstall_gitolite = if [ "$(USE_GITOLITE)" = "true" ]; then \
	sudo rm -fR $(GIT_HOME)/repositories $(HOME)/repositories $(GIT_HOME)/.gitolite $(HOME)/.gitolite $(HOME)/.gitolite.rc $(GIT_HOME)/.gitolite.rc /usr/lib/gitolite /usr/bin/gitolite; \
fi

uninstall_github = if [ "$(USE_GITHUB)" = "true" ]; then \
	rm -fR $(GG_DIR)/ok.sh; \
	sudo rm -fR $(DESTDIR)/ok.sh; \
fi

clone_ident = if [ "$(USE_GITOLITE)" = "true" ]; then \
	gitguild clone $(USER_NAME) file://$(GIT_HOME)/repositories/$(USER_NAME).git; \
else \
	gitguild clone $(USER_NAME); \
fi; \
cd $(GG_DIR)/$(USER_NAME); \
gitguild template build gitguild/template/clean_gitolite_admin.patch; \
gitguild template build gitguild/template/add_member_authors.patch; \
gitguild template build gitguild/template/add_general_project_files.patch; \
gitguild template build gitguild/template/ledger_basics.patch; \
gitguild template build gitguild/template/personal_ledger_init.patch; \
gitguild template build gitguild/template/add_GUILD.patch; \
export LAST_TRANSACTION=init_personal; \
gitguild tx finish; \
cat ledger/equity.*; \
git add .gitignore; \
git add -A; \
git commit -q -m "initialize identity guild"; \
gitguild push

clone_gitguild = if [ ! -d "$(GG_DIR)/gitguild" ]; then \
	./gitguild clone "gitguild" git@mirror.gitguild.com:gitguild; \
fi

fork_gitguild = if [ ! -d "$(GIT_HOME)/repositories/gitguild.git" ]; then \
	gitguild fork "gitguild" git@mirror.gitguild.com:gitguild; \
fi

rm_user_dir = if [ "$(USER_NAME)" != "" ]; then \
	rm -fR $(GG_DIR)/$(USER_NAME); \
fi

install:
	$(call check_or_install_gpg)
	$(call check_or_install_ledger)
	$(call check_or_install_ssh)
	$(call setup_ssh)
	$(call setup_gitolite)
	$(call setup_github)
	$(call clone_gitguild)
	sudo ln -sf $(GG_DIR)/gitguild/gitguild $(DESTDIR)/gitguild

personal:
	$(call clone_ident)
	$(call fork_gitguild)

test:
	cd "./t"; \
	./run_tests.sh all

testinstall:
	cd "./t"; \
	./run_tests.sh install

uninstall:
	$(call rm_user_dir)
	sudo rm -f $(DESTDIR)/gitguild
	$(call uninstall_gitolite)
	$(call uninstall_github)

