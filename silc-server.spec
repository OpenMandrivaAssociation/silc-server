Summary:	Server for the secure Internet Live Conferencing (SILC) protocol
Name:		silc-server
Version:	1.1.8
Release:	%mkrel 1
License:	GPLv2
Group:		Networking/Chat
URL:		http://www.silcnet.org/
Source:		ftp://ftp.silcnet.org/silc/server/sources/%{name}-%{version}.tar.bz2
Requires:	silc-client
BuildRequires:  ncurses-devel >= 5.2
BuildRequires:	nasm
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

%define _silcdatadir %{_datadir}/silc
%define _silclibdir %{_libdir}/silc
%define _silcetcdir %{_sysconfdir}/silc

%prep

%setup -q -n %{name}-%{version}

#chmod 644 CHANGES COPYING CREDITS README TODO doc/FAQ
#chmod 644 doc/example_silcd.conf doc/silcalgs.conf doc/*.txt

%build
%configure2_5x \
	--with-etcdir=%{_silcetcdir} \
	--with-helpdir=%{_silcdatadir}/help \
	--with-logsdir=%{_var}/log/silc \
	--mandir=%{_mandir} \
	--with-simdir=%{_silclibdir}/modules \
	--libdir=%{_silclibdir} \
	--enable-ipv6 \
	--disable-debug \
	--with-silcd-pid-file=%{_var}/run/silcd.pid \
	--with-perl=module \
	--with-perl-lib=vendor 

# Set the built-in default perl module dir
# We don't care even if it doesn't exist yet
#CC=$RPM_OPT_FLAGS make 
%make

%install
rm -rf %{buildroot}

#make install DESTDIR="$RPM_BUILD_ROOT" PREFIX="$RPM_BUILD_ROOT/usr" 
%makeinstall_std
#install -m 644 -D doc/example_silcd.conf $RPM_BUILD_ROOT/%{_sysconfdir}/silc/silcd.conf

# creat log files
touch %{buildroot}/var/log/silc/silcd_fatals.log
touch %{buildroot}/var/log/silc/silcd_errors.log
touch %{buildroot}/var/log/silc/silcd_warnings.log
touch %{buildroot}/var/log/silc/silcd.log

# delete unwanted files since rpmbuild failed if unpackaged
rm -fr %{buildroot}%{_prefix}/doc
rm -rf %{buildroot}%{_prefix}/libsilc*
# delete libraries and modules (same as libsilclient)
rm -rf %{buildroot}/%{_sysconfdir}/silcalgs.conf
rm -rf %{buildroot}%{_libdir}/
# remove private keys files (generate it with silcd -C)
rm -rf %{buildroot}/%{_sysconfdir}/silc/silcd.prv
rm -rf %{buildroot}/%{_sysconfdir}/silc/silcd.pub

## Need to do a silc-common package for client & server

%post
echo "Post-install : generate keys"

/usr/sbin/silcd -C /etc
chmod 600 /etc/silc/silcd.prv

%clean
rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc CREDITS README TODO doc/FAQ
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/*.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_logdir}/silc/*
