Summary:	ezmlm - high-speed mailing list manager for qmail.
Summary(pl):	ezmlm - szybki mened¿er list dyskysyjnych dla qmail'a.
Name:		ezmlm-idx
Version:	0.53.322
Release:	1
Copyright:	Check with djb@koobera.math.uic.edu
Group:		Utilities/System
Group(pl):	Narzêdzia/System
Source0:	ftp://koobera.math.uic.edu/pub/software/ezmlm-0.53.tar.gz
Source1:	ftp://ftp.id.wustl.edu/pub/patches/%{name}-0.322.tar.gz
Source2:	ezman-0.32.html.tar.gz
Patch0:		%{name}-opt.patch
URL:		http://www.qmail.org/
Requires:	qmail
Conflicts:	ezmlm
Buildroot:	/tmp/%{name}-%{version}-root

%description
Qmail Mailing List Manager + Indexing, (Remote) Moderation, digest, make
patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl
Qmailowy Mened¿er List Dyskusyjnych + Indeksowanie, (Zdalne) Moderowanie,
obs³uga wielu jêzyków, MIME, globalny-interfejs, prosta obs³uga.

%prep
%setup -q -T -b 0 -n ezmlm-0.53
%setup -q -D -T -a 1 -n ezmlm-0.53
%patch0 -p1

mv -f ezmlm-idx-0.322/* .
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

%changelog
* Mon Jun 07 1999 Arkadiusz Mi¶kiewicz <misiek@pld.org.pl>
- updated to x.313
- added few macros
- %config _must be_ 644 (if not - ezmlm-web won't work)
- added ezmlm-idx.ezmlmrc.pl-fix.patch

* Sat Oct 17 1998 Bartek Rozkrut <madey@dione.ids.pl>
  [0.53.312-1d]
- First relase as a PLD package,
- added opt.patch prepared by Marcin Korzonek <mkorz@SHADOW.EU.ORG>.
