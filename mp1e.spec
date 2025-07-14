#
# Conditional build:
%bcond_without	alsa		# ALSA support
#
Summary:	MP1E - Real Time Software MPEG-1 Encoder
Summary(pl.UTF-8):	MP1E - koder MPEG-1 Real Time Software
Name:		mp1e
Version:	1.9.4
Release:	2
License:	GPL v2
Group:		X11/Applications/Multimedia
#Source0Download: https://sourceforge.net/projects/zapping/files/OldFiles/
Source0:	https://downloads.sourceforge.net/zapping/%{name}-%{version}.tar.bz2
# Source0-md5:	4dad97af4db5d4ba61c3a2aec5ebd932
Patch0:		%{name}-gcc.patch
URL:		https://zapping.sourceforge.net/Zapping/index.html
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	audiofile-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	mp1e-libs < 1.9.4-2
Obsoletes:	mp1e-devel < 1.9.4-2
Obsoletes:	mp1e-static < 1.9.4-2
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

%prep
%setup -q
%patch -P0 -p1

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
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog README
%attr(755,root,root) %{_bindir}/mp1e
%{_mandir}/man1/mp1e.1*
