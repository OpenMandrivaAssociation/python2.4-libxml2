%define name	python2.4-libxml2
%define version	2.6.29
%define release	%mkrel 1

Summary:    Python 2.4 bindings for the libxml2 library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group: Development/Python
URL:		http://www.xmlsoft.org/
Source0:	ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
# (fc) 2.4.23-3mdk remove references to -L/usr/lib
Patch1:		libxml2-2.4.23-libdir.patch
BuildRequires:  gtk-doc
BuildRequires:	python2.4-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf
Requires:       python2.4
BuildRoot:      %_tmppath/%name-%version

%description
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows you to manipulate XML files. It includes support 
for reading, modifying and writing XML and HTML files. There is DTDs 
support: this includes parsing and validation even with complex DtDs, 
either at parse time or later once the document has been modified.

%prep
%setup -q -n libxml2-%{version}
%patch1 -p1 -b .libdir

#fix build & needed by patch 1 
autoreconf

%build

#
# try to use compiler profiling, based on Arjan van de Ven <arjanv@redhat.com>
# initial test spec. This really doesn't work okay for most tests done.
#
GCC_VERSION=`gcc --version | grep "^gcc" | awk '{ print $3 }' | sed 's+\([0-9]\)\.\([0-9]\)\..*+\1\2+'`
if [ $GCC_VERSION -ge 34 -a $GCC_VERSION -lt 40]
then
    PROF_GEN='-fprofile-generate'
    PROF_USE='-fprofile-use'
fi

if [ "$PROF_GEN" != "" ]
then
    # First generate a profiling version
    CFLAGS="${RPM_OPT_FLAGS} ${PROF_GEN}" CC="" %configure2_5x
    %make
    # Run a few sampling
    make dba100000.xml
    ./xmllint --noout  dba100000.xml
    ./xmllint --stream  dba100000.xml
    ./xmllint --noout --valid test/valid/REC-xml-19980210.xml
    ./xmllint --stream --valid test/valid/REC-xml-19980210.xml
    # Then generate code based on profile
    export CFLAGS="${RPM_OPT_FLAGS} ${PROF_USE}"
fi

%configure2_5x --with-python=%{_bindir}/python2.4

%make

%install
rm -rf %{buildroot}

%makeinstall_std
# clean before packaging documentation
(cd doc/examples ; make clean ; rm -rf .deps)
gzip -9 doc/libxml2-api.xml


# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/xml2-config

# remove unpackaged files
rm -rf	%{buildroot}%{_prefix}/doc \
 	%{buildroot}%{_datadir}/doc \
	%{buildroot}%{_libdir}/python2.4/site-packages/*.{la,a} \
	%{buildroot}%{_libdir}/libxml2* \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_libdir}/xml2Conf.sh \
	%{buildroot}%{_datadir}/gtk-doc \
	%{buildroot}%{_datadir}/aclocal \
	%{buildroot}%{_mandir} \
	%{buildroot}%{_includedir}/libxml2 \
	%{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS README Copyright TODO 
%doc doc/*.py doc/python.html
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%{_libdir}/python2.4/site-packages/*.so
%{_libdir}/python2.4/site-packages/*.py

