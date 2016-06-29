%define _upstream 5db96c0

# Don't require plasma - this would pull in KDE
%global __requires_exclude ^plasma4

Name:		everpad
Version:	2.5.4_1.248_gf664f58
Release:	2
Summary:	Evernote client for the Linux desktop
License:	MIT and BSD and ASL 2.0
URL:		https://github.com/nvbn/everpad
# wget -o everpad-%{_upstream.tar.gz} \
#      https://api.github.com/repos/nvbn/everpad/tarball/%{upstream}
Source0:	everpad-%{_upstream}.tar.gz

# Patches from mwilck/everpad
Patch1:		0001-requirements-replace-py-oauth2-by-oauth2.patch
Patch2:		0002-everpad-provider-Fix-Attribute-errors-in-SyncThread.patch
Patch3:		0003-Use-resources-for-tray-icon.patch
Patch4:		0004-Create-resource-definition-file-during-build-process.patch

Requires:	python2
Requires:	qtwebkit
Requires:	dbus-python
Requires:	python-keyring
Requires:	python-magic
Requires:	python-sqlalchemy
Requires:	python-oauth2
Requires:	python-SecretStorage
Requires:	python-BeautifulSoup
Requires:	python-html2text
Requires:	python-httplib2
Requires:	python-regex
# Get the following two from https://copr-be.cloud.fedoraproject.org/results/mwilck/python
Requires:	python-pysqlite
Requires:	python-pyside >= 1.2.2-3mw

BuildRequires:	python-setuptools
BuildRequires:	python2-devel
# This is required for pyside-rcc (Patch4)
BuildRequires:	pyside-tools

%description
everpad is an Evernote client (well integrated into the Linux desktop.
Under KDE, it shows up as a system tray icon. Under GNOME, the icon will be shown in the
notifications area.

The evernote connection is created with everpad-provider, a daemon that caches evernote
notes locally in a SQLite data base, provides access to them via dbus, and synchronizes
to Evernote in regular intervals.

%prep
%setup -n nvbn-everpad-%{_upstream}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
cat >LICENSES.txt <<EOF
Main sources from https://github.com/nvbn/everpad: MIT license
Included evernote API sources: BSD 2-clause license
Included Thrift API sources: Apache 2.0 license
EOF

%build
%{__python2} setup.py build

%install
# setup.py install creates an egg file
# we need the data files (icons, scripts etc) separate to be found
# install_data and install_scripts don't support --root
%{__python2} setup.py install_data -d $RPM_BUILD_ROOT%{_prefix}
%{__python2} setup.py install_scripts -d $RPM_BUILD_ROOT%{_bindir}
%{__python2} setup.py bdist_egg --skip-build -d $RPM_BUILD_ROOT%{python_sitearch}
# Unity is Ubuntu-only
rm -rf $RPM_BUILD_ROOT%{_datadir}/unity
rm -f $RPM_BUILD_ROOT%{_datadir}/dbus-1/services/unity-lens-everpad.service

%files
%{python_sitearch}/everpad-*.egg
%{_bindir}/*
%{_datadir}/*
%doc README.rst
%doc LICENSES.txt

%changelog
* Mon Jun 27 2016 Martin Wilck 2.5.4_1.248_gf664f58
- First build
