# TODO
#  - version 0.43 is out
%define	ezmlm_ver	0.53
%define	idx_ver		0.40
Summary:	ezmlm - high-speed mailing list manager for qmail
Summary(pl.UTF-8):	ezmlm - szybki zarządca list dyskysyjnych dla qmaila
Name:		ezmlm-idx
Version:	%{ezmlm_ver}_%{idx_ver}
Release:	2.2
Epoch:		1
License:	DJB (base ezmlm), GPL (ezmlm-idx additions) - non distributable as a whole?
Group:		Applications/System
Source0:	http://cr.yp.to/software/ezmlm-%{ezmlm_ver}.tar.gz
# Source0-md5:	108c632caaa8cdbfd3041e6c449191b2
Source1:	http://gd.tuwien.ac.at/infosys/mail/qmail/ezmlm-patches/%{name}-%{idx_ver}.tar.gz
# Source1-md5:	c6137114060cff19301a956e73d46fc0
Source2:	http://gd.tuwien.ac.at/infosys/mail/qmail/ezmlm-patches/ezman.html.tar.gz
# Source2-md5:	3ebdd5289f302063d21be43aaeef0585
Patch0:		%{name}-opt.patch
Patch1:		ezmlm-glibc.patch
Patch2:		%{name}-DESTDIR.patch
URL:		http://www.ezmlm.org/
BuildRequires:	groff
Obsoletes:	ezmlm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qmail mailing list manager + indexing, (remote) moderation, digest,
make patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl.UTF-8
Qmailowy zarządca list dyskusyjnych + indeksowanie, (zdalne)
moderowanie, obsługa wielu języków, MIME, globalny-interfejs, prosta
obsługa.

%prep
%setup -q -n ezmlm-%{ezmlm_ver} -a1
%patch -P0 -p1
%patch -P1
%patch -P2 -p1

mv -f ezmlm-idx-%{idx_ver}/* .
cat idx.patch | sed 's/conf-bin`/conf-bin2`/g' > idx2.patch
patch -s < idx2.patch
echo "%{_bindir}" > conf-bin2
cat Makefile | sed 's/auto_bin `head -n 1 conf-bin`/auto_bin `head -n 1 conf-bin2`/g' > Makefile.pld
mv -f Makefile.pld Makefile

mv -f ezmlmrc.pl ezmlmrc.pl.org
echo "%{idx_ver} - This must be on 1 and start in pos 1" > ezmlmrc.pl
cat ezmlmrc.pl.org >> ezmlmrc.pl

%build
%{__make}
%{__make} man
tar zxf %{SOURCE2}

%install
rm -rf $RPM_BUILD_ROOT
echo "%{_bindir}" > conf-bin
echo "%{_mandir}" > conf-man

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}

install ezmlmrc $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm

%{__make} setup \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%doc BLURB CHANGES CHANGES.idx FAQ.idx  README README.idx
%doc SYSDEPS TARGETS UPGRADE.idx  DOWNGRADE.idx ezmlmrc
%doc ezmlmrc.*[a-zA-Z] ezman

%attr(755,root,root) %dir %{_sysconfdir}/ezmlm
%attr(755,root,root) %{_bindir}/ezmlm-*
%{_mandir}/man[15]/*
%config %verify(not md5 mtime size) %{_sysconfdir}/ezmlm/*
