%define	ezmlm_ver	0.53
%define	idx_ver		0.40
Summary:	ezmlm - high-speed mailing list manager for qmail.
Summary(pl):	ezmlm - szybki mened�er list dyskysyjnych dla qmail'a.
Name:		ezmlm-idx
Version:	%{ezmlm_ver}_%{idx_ver}
Release:	1
Epoch:		1
License:	Check with djb@cr.yp.to
Group:		Applications/System
Source0:	http://cr.yp.to/software/ezmlm-%{ezmlm_ver}.tar.gz
Source1:	http://gd.tuwien.ac.at/infosys/mail/qmail/ezmlm-patches/%{name}-%{idx_ver}.tar.gz
Source2:	http://gd.tuwien.ac.at/infosys/mail/qmail/ezmlm-patches/ezman.html.tar.gz
Patch0:		%{name}-opt.patch
URL:		http://www.ezmlm.org/
Obsoletes:	ezmlm
BuildRequires:	groff
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qmail Mailing List Manager + Indexing, (Remote) Moderation, digest,
make patches, multi-language, MIME, global-interface, easy-to-use.

%description -l pl
Qmailowy Mened�er List Dyskusyjnych + Indeksowanie, (Zdalne)
Moderowanie, obs�uga wielu j�zyk�w, MIME, globalny-interfejs, prosta
obs�uga.

%prep
%setup -q -T -b 0 -n ezmlm-%{ezmlm_ver}
%setup -q -D -T -a 1 -n ezmlm-%{ezmlm_ver}
%patch0 -p1

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
