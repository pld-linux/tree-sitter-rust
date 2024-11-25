Summary:	Rust grammar for tree-sitter
Name:		tree-sitter-rust
Version:	0.23.2
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/tree-sitter/tree-sitter-rust/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	631772eed9a23eb5936e1f921adb44f6
URL:		https://github.com/tree-sitter/tree-sitter-rust
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_rust_soname	libtree-sitter-rust.so.14.0

%description
Rust grammar for tree-sitter.

%package devel
Summary:	Header files for tree-sitter-rust
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	tree-sitter-devel

%description devel
Header files for tree-sitter-rust.

%package static
Summary:	Static tree-sitter-rust library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-rust library.

%package -n neovim-parser-rust
Summary:	Rust parser for Neovim
Group:		Applications/Editors
Requires:	%{name} = %{version}-%{release}

%description -n neovim-parser-rust
Rust parser for Neovim.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CPPFLAGS="%{rpmcppflags}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} %{_libdir}/%{ts_rust_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/rust.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/%{ts_rust_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-rust.so
%{_includedir}/tree_sitter/tree-sitter-rust.h
%{_pkgconfigdir}/tree-sitter-rust.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-rust.a

%files -n neovim-parser-rust
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/rust.so
