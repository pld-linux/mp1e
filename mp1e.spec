#
# Conditional build:
%bcond_without	alsa		# ALSA support
%bcond_without	static_libs	# static library
#
Summary:	MP1E - Real Time Software MPEG-1 Encoder
Summary(pl.UTF-8):	MP1E - koder MPEG-1 Real Time Software
Name:		mp1e
Version:	1.9.4
Release:	1
License:	GPL v2
Group:		X11/Applications/Multimedia
#Source0Download: https://sourceforge.net/projects/zapping/files/OldFiles/
Source0:	https://downloads.sourceforge.net/zapping/%{name}-%{version}.tar.bz2
# Source0-md5:	4dad97af4db5d4ba61c3a2aec5ebd932
Patch0:		%{name}-common.patch
Patch1:		%{name}-gcc.patch
URL:		https://zapping.sourceforge.net/Zapping/index.html
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

%description -l pl.UTF-8
Program MP1E zapisuje jako strumień MPEG-1 obraz i dźwięk z urządzenia
przechwytywania obrazu zgodnego z v4l lub v4l2 oraz urządzenia dźwięku
OSS lub ALSA. Obsługiwane są tylko procesory x86 z rozszerzeniem MMX.

%package libs
Summary:	MP1E - Real Time Software MPEG-1 Encoder library
Summary(pl.UTF-8):	Biblioteka MP1E - kodera MPEG-1 Real Time Software
Group:		Libraries

%description libs
MP1E - Real Time Software MPEG-1 Encoder library, used by mp1e program
and mp1e backend in rte.

%description libs -l pl.UTF-8
Biblioteka MP1E - kodera MPEG-1 Real Time Software, używana przez
program mp1e oraz backend mp1e w rte.

%package devel
Summary:	Development files for MP1E library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki MP1E
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for MP1E library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki MP1E.

%package static
Summary:	Static MP1E library
Summary(pl.UTF-8):	Statyczna biblioteka MP1E
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MP1E library.

%description static -l pl.UTF-8
Statyczna biblioteka MP1E.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__rm} macros/{alsa,as}.m4
%if %{without alsa}
echo 'AC_DEFUN([AM_PATH_ALSA], [$3])' > macros/alsa.m4
%endif

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
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
%attr(755,root,root) %{_bindir}/mp1e
%{_mandir}/man1/mp1e.1*

%files libs
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README
%attr(755,root,root) %{_libdir}/libmp1e_common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmp1e_common.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmp1e_common.so
%{_libdir}/libmp1e_common.la

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmp1e_common.a
%endif
