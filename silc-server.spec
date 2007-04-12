%define name silc-server
%define version 0.9.20
%define release %mkrel 1

Summary:	Server for the secure Internet Live Conferencing (SILC) protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		ftp://ftp.silcnet.org/silc/server/sources/%{name}-%{version}.tar.bz2
License:	GPL
Group:		Networking/Chat
URL:		http://www.silcnet.org/
Requires:	silc-client
BuildRequires:  ncurses-devel >= 5.2
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

chmod 644 CHANGES COPYING CREDITS README TODO doc/FAQ
chmod 644 doc/example_silcd.conf doc/silcalgs.conf doc/*.txt

%build
%configure --cache-file=`pwd`/config.cache --with-etcdir=%{_silcetcdir} \
--with-helpdir=%{_silcdatadir}/help --with-logsdir=%{_var}/log/silc \
--mandir=%{_mandir} --with-simdir=%{_silclibdir}/modules \
--libdir=%{_silclibdir} \
--enable-ipv6 --disable-debug \
--with-silcd-pid-file=%{_var}/run/silcd.pid \
--with-perl=module \
--with-perl-lib=vendor 

# Set the built-in default perl module dir
# We don't care even if it doesn't exist yet
CC=$RPM_OPT_FLAGS make 

%install
rm -rf "$RPM_BUILD_ROOT"

make install DESTDIR="$RPM_BUILD_ROOT" PREFIX="$RPM_BUILD_ROOT/usr" 

install -m 644 doc/example_silcd.conf $RPM_BUILD_ROOT/%{_sysconfdir}/silc/silcd.conf

# creat log files
touch $RPM_BUILD_ROOT/var/log/silc/silcd_fatals.log
touch $RPM_BUILD_ROOT/var/log/silc/silcd_errors.log
touch $RPM_BUILD_ROOT/var/log/silc/silcd_warnings.log
touch $RPM_BUILD_ROOT/var/log/silc/silcd.log

# delete unwanted files since rpmbuild failed if unpackaged
rm -fr $RPM_BUILD_ROOT%{_prefix}/doc
rm -rf $RPM_BUILD_ROOT%_prefix/libsilc*
# delete libraries and modules (same as libsilclient)
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/silc/silcalgs.conf
rm -rf $RPM_BUILD_ROOT%_libdir/
# remove private keys files (generate it with silcd -C)
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/silc/silcd.prv
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/silc/silcd.pub

## Need to do a silc-common package for client & server

%post
echo "Post-install : generate keys"

/usr/sbin/silcd -C /etc/silc
chmod 600 /etc/silc/silcd.prv

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%doc CHANGES COPYING CREDITS README TODO doc/FAQ
%_sbindir/*
%config(noreplace) %_sysconfdir/silc/silcd.conf
%_mandir/man5/*
%_mandir/man8/*
/var/log/silc/*

