Summary:	ezmlm - high-speed mailing list manager for qmail.
Summary(pl):	ezmlm - szybki mened¿er list dyskysyjnych dla qmail'a.
Name:		ezmlm-idx
%define  IDX  0.322
%define  EZMLM  0.53
Version:	%{EZMLM}_%{IDX}
Release:	2
Copyright:	Check with djb@koobera.math.uic.edu
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	ftp://koobera.math.uic.edu/software/ezmlm-%{EZMLM}.tar.gz
Source1:	ftp://ftp.id.wustl.edu/pub/patches/%{name}-%{IDX}.tar.gz
Source2:	ftp://ftp.id.wustl.edu/pub/patches/ezman/ezman-0.32.html.tar.gz
Patch0:		%{name}-opt.patch
Patch1:		%{name}-config.patch
URL:		http://www.qmail.org/
Requires:	qmail
Conflicts:	ezmlm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qmail Mailing List Manager + Indexing, (Remote) Moderation, digest,
make patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl
Qmailowy Mened¿er List Dyskusyjnych + Indeksowanie, (Zdalne)
Moderowanie, obs³uga wielu jêzyków, MIME, globalny-interfejs, prosta
obs³uga.

%prep
%setup -q -T -b 0 -n ezmlm-%{EZMLM}
%setup -q -D -T -a 1 -n ezmlm-%{EZMLM}
%patch0 -p1

mv -f ezmlm-idx-%{IDX}/* .
cat idx.patch | sed 's/conf-bin`/conf-bin2`/g' > idx2.patch
patch -s < idx2.patch
echo "%{_bindir}" > conf-bin2
cat Makefile | sed 's/auto_bin `head -1 conf-bin`/auto_bin `head -1 conf-bin2`/g' > Makefile.pld
mv -f Makefile.pld Makefile

%build
%{__make}
%{__make} man
if [ -z "$LANG" ]; then
patch -s -p1 < %{PATCH1}
%{__make} pl
else
%{__make} $LANG
fi
tar zxf %{SOURCE2}

%install
rm -rf $RPM_BUILD_ROOT
echo "$RPM_BUILD_ROOT%{_bindir}" > conf-bin
echo "$RPM_BUILD_ROOT%{_mandir}" > conf-man

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}

install ezmlmrc $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm

%{__make} setup

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,5}/*

strip $RPM_BUILD_ROOT%{_bindir}/ezmlm-* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%doc BLURB CHANGES CHANGES.idx FAQ.idx  README README.idx 
%doc SYSDEPS TARGETS UPGRADE.idx  DOWNGRADE.idx ezmlmrc 
%doc ezmlmrc.*[a-zA-Z] ezman 

%attr(755,root,root) %dir %{_sysconfdir}/ezmlm
%attr(755,root,root) %{_bindir}/ezmlm-*
%attr(644,root,root) %{_mandir}/man[15]/*
%attr(644,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/ezmlm/*
