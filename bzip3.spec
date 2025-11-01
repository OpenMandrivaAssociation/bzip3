%define major 1

%define libname %mklibname bzip3
%define devname %mklibname -d bzip3

Name:           bzip3
Version:        1.5.3
Release:        1
Summary:        Tools for compressing and decompressing bzip3 files
License:        LGPL-3.0-or-later AND BSD-2-Clause
URL:            https://github.com/kspalaiologos/bzip3
Source0:        https://github.com/kspalaiologos/bzip3/releases/download/%{version}/%{name}-%{version}.tar.xz

# Import Fedora patch
# Do not use /usr/bin/env in shell bangs, not suitable for upstream,
# <https://github.com/kspalaiologos/bzip3/pull/75>.
#Patch0:         bzip3-1.2.2-Do-not-use-usr-bin-env-in-shell-bangs.patch

BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gawk
# We do not have it right now.
# For git-version-gen script executed from autoconf.ac
#BuildRequires:  gnulib-devel
BuildRequires:  libtool
BuildRequires:  make
# PKG_PROG_PKG_CONFIG in configure.ac
BuildRequires:  pkgconfig
# sed in build-aux/git-version-gen
BuildRequires:  sed

Requires:	%{libname} = %{EVRD}

# Executed by bz3grep
Requires:       grep
# Executed by bz3less
Requires:       less
# Executed by bz3more
Requires:       util-linux-core
# Executed by bz3most
Requires:       most


%description
These are tools for compressing, decompressing, printing, and searching bzip3
files. bzip3 features higher compression ratios and better performance than
bzip2 thanks to an order-0 context mixing entropy coder, a fast
Burrows-Wheeler transform code making use of suffix arrays and a run-length
encoding with Lempel-Ziv prediction pass based on LZ77-style string matching
and PPM-style context modeling.
 
%package -n %{libname}
Summary:        Shared libraries for bzip3 compression and decompresion
License:        LGPL-3.0-or-later AND Apache-2.0 

# Forked, fixed, and pruned libasais <https://github.com/IlyaGrebnov/libsais>
# because of rejected fix <https://github.com/IlyaGrebnov/libsais/issues/10>.
Provides:       bundled(libsais) = 2.7.0
 
%description -n %{libname}
This is a library for compressing and decompressing bzip3 compression format.
bzip3 features higher compression ratios and better performance than bzip2
thanks to an order-0 context mixing entropy coder, a fast Burrows-Wheeler
transform code making use of suffix arrays and a run-length encoding with
Lempel-Ziv prediction pass based on LZ77-style string matching and PPM-style
context modeling.
 
%package -n %{devname}
Summary:        Files for developing with bzip3 library
License:        LGPL-3.0-or-later
Requires:	%{libname} = %{EVRD}
 
%description -n %{devname}
Header files, a pkg-config module and link objects for building applications
which use a bzip3 library.
 
%prep
%autosetup -p1
# Remove generated autoconf files
#rm aclocal.m4 configure Makefile.in
# Remove generated manual pages
#for F in *.1.in; do
#    rm "${F%%.in}"
#done
# Unbundle autoconf macros and scripts, except those not yet packaged in
# autoconf-archive
#find build-aux -type f \! \( \
#    -name ax_progvar.m4 -o \
#    -name ax_subst_man_date.m4 -o \
#    -name ax_subst_transformed_package_name.m4 \
#    \) -delete
# Execute git-version-gen from a system location
#ln -s %{_datadir}/gnulib/build-aux/git-version-gen build-aux/git-version-gen
# Remove unused code
#echo > include/getopt-shim.h
 
%build
autoreconf -vfi
%configure \
    --disable-arch-native \
    --with-pic \
    --with-pthread \
    --enable-shared \
    --disable-static \
    --disable-static-exe
%{make_build}
 
%check
make check roundtrip %{?_smp_mflags}
 
%install
%{make_install}
find %{buildroot} -name '*.la' -delete
# Deduplicate identical files
if cmp %{buildroot}%{_mandir}/man1/{bz3cat,bunzip3}.1; then
    rm %{buildroot}%{_mandir}/man1/bunzip3.1
    ln -s bz3cat.1 %{buildroot}%{_mandir}/man1/bunzip3.1
fi
 
%files
%define programs \{bunzip3,bz3cat,bz3grep,bz3less,bz3more,bz3most,bzip3\}
%{_bindir}/%{programs}
%{_mandir}/man1/%{programs}.1*
 
%files -n %{libname}
%license LICENSE
%doc NEWS README.md
%{_libdir}/libbzip3.so.%{major}{,.*}
 
%files -n %{devname}
%{_includedir}/libbz3.h
%{_libdir}/libbzip3.so
%{_libdir}/pkgconfig/bzip3.pc
