Summary:     ezmlm - high-speed mailing list manager for qmail.
Name:        ezmlm-idx
Version:     0.53.313
Release:     1
Group:       Utilities/System
Source:      ftp://koobera.math.uic.edu/pub/software/ezmlm-0.53.tar.gz
Source1:     ftp://ftp.id.wustl.edu/pub/patches/%{name}-0.313.tar.gz
Patch0:      %{name}-opt.patch
Patch1:	     %{name}.ezmlmrc.pl-fix.patch
URL:         http://www.qmail.org/
Copyright:   Check with djb@koobera.math.uic.edu
Requires:    qmail
Conflicts:   ezmlm
Buildroot:   /tmp/%{name}-%{version}-root
Summary(pl): ezmlm - szybki mened¿er list dyskysyjnych dla qmail'a.

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
%patch1 -p1

mv -f ezmlm-idx-0.313/* .
patch -s < idx.patch

%build
make
make man

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/{man1,man5}

install -s ezmlm-{clean,cron,gate,get,idx,issubn,list,make,\
manage,moderate,reject,request,return,send,store,sub,tstdig,\
unsub,warn,weed} $RPM_BUILD_ROOT%{_bindir}

install ezmlm-{accept,both,check,glconf,glmake} $RPM_BUILD_ROOT%{_bindir}

install *.1 $RPM_BUILD_ROOT%{_mandir}/man1
install *.5 $RPM_BUILD_ROOT%{_mandir}/man5

install ezmlmrc $RPM_BUILD_ROOT/etc

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man5/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%doc BLURB CHANGES CHANGES.idx FAQ.idx  README README.idx 
%doc SYSDEPS TARGETS UPGRADE.idx  DOWNGRADE.idx ezmlmrc.sv 
%doc ezmlmrc.da ezmlmrc.pl ezmlmrc.fr ezmlmrc.de ezmlmrc.jp 
%doc ezmlmrc.pt_BR ezdomo.tar.gz ezdomo.pl.tar.gz

%attr(755,root,root) /usr/bin/*
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
