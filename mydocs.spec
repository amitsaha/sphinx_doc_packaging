# example of packaging a Sphinx project as an
# RPM
Name:           mydocs
Version:        1
Release:        0%{?dist}
Summary:        Documentation and Samples for a project
License:        LGPLv2+
URL:            http://www.mydocs.org
Source0:        http://downloads.mydocs.org/%{name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Group:          Documentation
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python-docutils >= 0.6
BuildRequires:  python-sphinx >= 1.0
BuildRequires:  python-sphinxcontrib-httpdomain


%description
My docs packaged as an RPM

%prep
%setup -q -n %{name}-%{version}

%build
make html

%install
mkdir -p %{buildroot}/%{_defaultdocdir}
cp -r %{_builddir}/%{name}-%{version}/_build/html %{buildroot}/%{_defaultdocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_defaultdocdir}/%{name}
