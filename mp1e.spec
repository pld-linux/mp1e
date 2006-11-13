#
# Conditional build:
%bcond_without	alsa	# without ALSA support
#
Summary:	MP1E - Real Time Software MPEG-1 Encoder
Summary(pl):	MP1E - koder MPEG-1 Real Time Software
Name:		mp1e
Version:	1.9.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/zapping/%{name}-%{version}.tar.bz2
# Source0-md5:	4dad97af4db5d4ba61c3a2aec5ebd932
Patch0:		%{name}-common.patch
URL:		http://zapping.sourceforge.net/
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	audiofile-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
# x86 or only i586/i686/athlon?
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MP1E program records video and audio from a v4l or v4l2 video capture
device and an OSS or ALSA audio device, as MPEG-1 system stream. Only
x86 CPUs with MMX extension are supported.

%description -l pl
Program MP1E zapisuje jako strumieñ MPEG-1 obraz i d¼wiêk z urz±dzenia
przechwytywania obrazu zgodnego z v4l lub v4l2 oraz urz±dzenia d¼wiêku
OSS lub ALSA. Obs³ugiwane s± tylko procesory x86 z rozszerzeniem MMX.

%package libs
Summary:	MP1E - Real Time Software MPEG-1 Encoder library
Summary(pl):	Biblioteka MP1E - kodera MPEG-1 Real Time Software
Group:		Libraries

%description libs
MP1E - Real Time Software MPEG-1 Encoder library, used by mp1e program
and mp1e backend in rte.

%description libs -l pl
Biblioteka MP1E - kodera MPEG-1 Real Time Software, u¿ywana przez
program mp1e oraz backend mp1e w rte.

%package devel
Summary:	Development files for MP1E library
Summary(pl):	Pliki programistyczne biblioteki MP1E
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for MP1E library.

%description devel -l pl
Pliki programistyczne biblioteki MP1E.

%package static
Summary:	Static MP1E library
Summary(pl):	Statyczna biblioteka MP1E
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MP1E library.

%description static -l pl
Statyczna biblioteka MP1E.

%prep
%setup -q
%patch0 -p1

rm -f macros/{alsa,as}.m4
%if !%{with alsa}
echo 'AC_DEFUN([AM_PATH_ALSA], [$3])' > macros/alsa.m4
%endif

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
