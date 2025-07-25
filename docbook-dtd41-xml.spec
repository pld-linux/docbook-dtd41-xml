Summary:	XML/SGML DocBook DTD 4.1
Summary(pl.UTF-8):	XML/SGML DocBook DTD 4.1
%define ver	4.1
%define sver	41
Name:		docbook-dtd%{sver}-xml
Version:	1.0
Release:	14
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbkx%{sver}.zip
# Source0-md5:	90afec959a2a8c8636b121c198a30de8
Patch0:		%{name}-dbcentx.patch
URL:		http://www.oasis-open.org/docbook/
BuildRequires:	unzip
BuildRequires:	rpm-build >= 4.0.2-94
Requires(post,preun):	/usr/bin/install-catalog
Requires:	sgml-common >= 0.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch

%define		dtd_path	%{_datadir}/sgml/docbook/xml-dtd-%{ver}
%define		xmlcat_file	%{dtd_path}/catalog.xml
%define		sgmlcat_file	%{dtd_path}/catalog

%description
DocBook is an XML/SGML vocabulary particularly well suited to books and papers
about computer hardware and software (though it is by no means limited to only
these applications).

%description -l pl.UTF-8
DocBook DTD jest zestawem definicji dokumentów XML/SGML przeznaczonych do
tworzenia dokumentacji technicznej. Stosowany jest do pisania podręczników
systemowych, instrukcji jak i wielu innych ciekawych rzeczy.

%prep
%setup -q -c
chmod -R a+rX *
%patch -P0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dtd_path}

install *.dtd *.mod $RPM_BUILD_ROOT%{dtd_path}
install *.ent $RPM_BUILD_ROOT%{dtd_path} || :
cp -a ent $RPM_BUILD_ROOT%{dtd_path}

%docbook_sgmlcat_fix $RPM_BUILD_ROOT%{sgmlcat_file} %{ver}

# install catalog (but filter out ISO entities)
#grep -v 'ISO ' docbook.cat >> $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog
cat docbook.cat >> $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Update the centralized catalog corresponding to this version of the DTD
/usr/bin/install-catalog --add /etc/sgml/xml-docbook-%{ver}.cat /usr/share/sgml/docbook/xml-dtd-%{ver}/catalog > /dev/null

%preun
/usr/bin/install-catalog --remove /etc/sgml/xml-docbook-%{ver}.cat /usr/share/sgml/docbook/xml-dtd-%{ver}/catalog > /dev/null

%files
%defattr(644,root,root,755)
%doc *.txt ChangeLog
%{_datadir}/sgml/docbook/*
