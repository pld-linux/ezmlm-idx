Summary:	ezmlm - high-speed mailing list manager for qmail.
Summary(pl):	ezmlm - szybki mened�er list dyskysyjnych dla qmail'a.
Name:		ezmlm-idx
%define  IDX  0.40
%define  EZMLM  0.53
Version:	%{EZMLM}_%{IDX}
Release:	1
Copyright:	Check with djb@koobera.math.uic.edu
Group:		Utilities/System
Group(pl):	Narz�dzia/System
Source0:	ftp://koobera.math.uic.edu/pub/software/ezmlm-%{EZMLM}.tar.gz
Source1:	ftp://ftp.id.wustl.edu/pub/patches/%{name}-%{IDX}.tar.gz
Source2:	ftp://ftp.id.wustl.edu/pub/patches/ezman/ezman-0.32.html.tar.gz
Patch0:		%{name}-opt.patch
URL:		http://www.qmail.org/
Requires:	qmail
Conflicts:	ezmlm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qmail Mailing List Manager + Indexing, (Remote) Moderation, digest, make
patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl
Qmailowy Mened�er List Dyskusyjnych + Indeksowanie, (Zdalne) Moderowanie,
obs�uga wielu j�zyk�w, MIME, globalny-interfejs, prosta obs�uga.

%prep
%setup -q -T -b 0 -n ezmlm-%{EZMLM}
%setup -q -D -T -a 1 -n ezmlm-%{EZMLM}
%patch0 -p1

mv -f ezmlm-idx-%{IDX}/* .
patch -s < idx.patch

%build
make
make man
if [ -z "$LANG" ]; then
make pl
else
make $LANG
fi
tar zxf %{SOURCE2}

%install
rm -rf $RPM_BUILD_ROOT
echo "$RPM_BUILD_ROOT%{_bindir}" > conf-bin
echo "$RPM_BUILD_ROOT%{_mandir}" > conf-man

install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}

install ezmlmrc $RPM_BUILD_ROOT/etc

make setup

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,5}/*

strip $RPM_BUILD_ROOT%{_bindir}/ezmlm-* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%doc BLURB CHANGES CHANGES.idx FAQ.idx  README README.idx 
%doc SYSDEPS TARGETS UPGRADE.idx  DOWNGRADE.idx ezmlmrc 
%doc ezmlmrc.*[a-zA-Z] ezman utils 

%attr(755,root,root) /usr/bin/ezmlm-*
%attr(644,root,root) %{_mandir}/man[15]/*
%attr(644,root,root) %config %verify(not size mtime md5) /etc/*
