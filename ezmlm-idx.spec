%define	ezmlm_ver	0.53
%define	idx_ver		0.40
Summary:	ezmlm - high-speed mailing list manager for qmail
Summary(pl):	ezmlm - szybki zarz±dca list dyskysyjnych dla qmaila
Name:		ezmlm-idx
Version:	%{ezmlm_ver}_%{idx_ver}
Release:	2	
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
URL:		http://www.ezmlm.org/
BuildRequires:	groff
Obsoletes:	ezmlm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qmail mailing list manager + indexing, (remote) moderation, digest,
make patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl
Qmailowy zarz±dca list dyskusyjnych + indeksowanie, (zdalne)
moderowanie, obs³uga wielu jêzyków, MIME, globalny-interfejs, prosta
obs³uga.

%prep
%setup -q -n ezmlm-%{ezmlm_ver} -a1
%patch0 -p1
%patch1

mv -f ezmlm-idx-%{idx_ver}/* .
cat idx.patch | sed 's/conf-bin`/conf-bin2`/g' > idx2.patch
patch -s < idx2.patch
echo "%{_bindir}" > conf-bin2
cat Makefile | sed 's/auto_bin `head -1 conf-bin`/auto_bin `head -1 conf-bin2`/g' > Makefile.pld
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
echo "$RPM_BUILD_ROOT%{_bindir}" > conf-bin
echo "$RPM_BUILD_ROOT%{_mandir}" > conf-man

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}

install ezmlmrc $RPM_BUILD_ROOT%{_sysconfdir}/ezmlm

%{__make} setup

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
